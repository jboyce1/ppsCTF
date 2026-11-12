#!/usr/bin/env python3
"""Interactive classroom target setup. Run with sudo on a disposable range VM.

Keeps the existing service configuration approach, with bounded commands,
package reuse, diagnostics, and a machine-readable validation plan. No helpers downloaded.
"""
import argparse
from datetime import datetime, timezone
import ftplib
import fcntl
import json
import platform
import selectors
import shlex
import signal
import traceback
import os
from pathlib import Path
import random
import re
import shutil
import socket
import subprocess
import sys
import time

VERSION = '2.0'
LOG = None
APT_UPDATED = False
OPTIONS = {
    '1': 'SSH — port 22 (existing user/password)',
    '2': 'SSH — random high port (existing user/password)',
    '3': 'FTP — port 21',
    '4': 'FTP + flag — port 21',
    '5': 'FTP — random high port (optional flag)',
    '6': 'Telnet — port 23',
    '7': 'Telnet — random high port',
    '8': 'Telnet + banner flag — port 23',
    '9': 'Telnet + banner flag — random high port',
}


def emit(message):
    print(message, flush=True)
    if LOG:
        LOG.write(message + '\n')
        LOG.flush()


def run(*args, check=True, timeout=45, live=False):
    """Bound every command, retain output, and kill its process group on timeout."""
    command = list(args)
    label = shlex.join(command)
    emit(f'[command, timeout={timeout}s] {label}')
    started = time.monotonic()
    chunks = []
    env = dict(os.environ, LC_ALL='C', DEBIAN_FRONTEND='noninteractive')
    with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                          env=env, start_new_session=True) as process:
        selector = selectors.DefaultSelector()
        selector.register(process.stdout, selectors.EVENT_READ)
        last_heartbeat = started
        try:
            while selector.get_map():
                now = time.monotonic()
                if now - started > timeout:
                    raise subprocess.TimeoutExpired(command, timeout)
                for key, _ in selector.select(timeout=0.5):
                    data = os.read(key.fileobj.fileno(), 65536)
                    if not data:
                        selector.unregister(key.fileobj)
                        continue
                    text = data.decode('utf-8', errors='replace')
                    chunks.append(text)
                    if LOG:
                        LOG.write(text)
                        LOG.flush()
                    if live:
                        print(text, end='', flush=True)
                if now - last_heartbeat >= 15:
                    emit(f'  Still running: {args[0]} ({int(now - started)}s)')
                    last_heartbeat = now
            process.wait(timeout=max(1, timeout - (time.monotonic() - started)))
        except BaseException:
            if process.poll() is None:
                os.killpg(process.pid, signal.SIGTERM)
                try:
                    process.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    os.killpg(process.pid, signal.SIGKILL)
                    process.wait()
            raise
        finally:
            selector.close()
    output = ''.join(chunks)
    emit(f'[exit {process.returncode}; {time.monotonic() - started:.1f}s] {args[0]}')
    if check and process.returncode:
        raise subprocess.CalledProcessError(process.returncode, command, output=output)
    return subprocess.CompletedProcess(command, process.returncode, output, '')


def ensure_packages(packages):
    """Skip installed packages; update the index at most once per run."""
    global APT_UPDATED
    missing = []
    for package in packages:
        result = run('dpkg-query', '-W', '-f=${Status}', package, check=False)
        if result.returncode == 0 and result.stdout.strip() == 'install ok installed':
            emit(f'[package] {package}: already installed; leaving version unchanged.')
        else:
            missing.append(package)
    if not missing:
        return
    if not APT_UPDATED:
        run('apt-get', '-o', 'DPkg::Lock::Timeout=60', '-o', 'Acquire::Retries=1', '-o', 'APT::Update::Error-Mode=any',
            '-o', 'Acquire::http::Timeout=20', '-o', 'Acquire::https::Timeout=20',
            'update', timeout=240, live=True)
        APT_UPDATED = True
    run('apt-get', '-o', 'DPkg::Lock::Timeout=60', '-o', 'Acquire::Retries=1', '-o', 'APT::Update::Error-Mode=any',
        '-o', 'Acquire::http::Timeout=20', '-o', 'Acquire::https::Timeout=20',
        'install', '-y', '--no-install-recommends', *missing, timeout=360, live=True)


def safe_run(*args, timeout=30):
    try:
        result = run(*args, check=False, timeout=timeout)
        return f'$ {shlex.join(args)}\n{result.stdout}\nexit={result.returncode}\n'
    except Exception as error:
        return f'$ {shlex.join(args)}\nERROR: {error}\n'


def diagnostics(folder):
    """Collect evidence even when setup failed. Never collect passwords."""
    commands = [
        ('uname', '-a'), ('cat', '/etc/os-release'), ('hostname', '-I'),
        ('ip', '-brief', 'address'), ('ip', 'route'), ('ss', '-ltnp'),
        ('dpkg-query', '-W', 'openssh-server', 'vsftpd', 'xinetd', 'inetutils-telnetd'),
        ('systemctl', '--no-pager', '--full', 'status', 'ssh', 'ssh.socket', 'vsftpd', 'xinetd'),
        ('journalctl', '--no-pager', '-n', '60', '-u', 'ssh', '-u', 'vsftpd', '-u', 'xinetd'),
        ('ufw', 'status', 'verbose'), ('nft', 'list', 'ruleset'),
    ]
    text = f'CyberCartographer {VERSION}; {platform.platform()}\n'
    for command in commands:
        text += safe_run(*command)
    if Path('/usr/sbin/sshd').exists():
        text += safe_run('/usr/sbin/sshd', '-t')
        text += safe_run('/usr/sbin/sshd', '-T')
    for path in [Path('/etc/vsftpd.conf'), *Path('/etc/xinetd.d').glob('cybercartographer-*')]:
        try:
            text += f'\n# {path}\n{path.read_text()}\n'
        except OSError as error:
            text += str(error) + '\n'
    (folder / 'diagnostics.txt').write_text(text)


def preflight():
    if not Path('/run/systemd/system').is_dir():
        raise RuntimeError('This launcher requires a running systemd VM (not a normal container).')
    for name in ('systemctl', 'apt-get', 'dpkg-query', 'ss'):
        if not shutil.which(name):
            raise RuntimeError(f'Required tool missing: {name}. No service changes made.')
    state = run('dpkg', '--audit')
    if state.stdout.strip():
        raise RuntimeError('dpkg reports unfinished package work; see run.log and resolve it before setup.')


def parse_choices(text):
    digits = re.sub(r'[\s,]', '', text)
    if not digits or any(c not in OPTIONS for c in digits):
        raise ValueError('Enter option digits, for example 136 or 2,5,9.')
    choices = list(dict.fromkeys(digits))
    for group, label in [('345', 'FTP'), ('68', 'standard Telnet'), ('79', 'high-port Telnet')]:
        if sum(c in group for c in choices) > 1:
            raise ValueError(f'Choose only one {label} option per run.')
    return choices



def high_port(used):
    for _ in range(3000):
        port = random.randint(21000, 24000)
        if port in used:
            continue
        with socket.socket() as probe:
            try:
                probe.bind(('0.0.0.0', port))
            except OSError:
                continue
        used.add(port)
        return port
    raise RuntimeError('No available high port in 21000–24000.')


def backup(path, folder):
    path = Path(path)
    if path.exists():
        shutil.copy2(path, folder / str(path).lstrip('/').replace('/', '_'))


def set_config(path, settings):
    path = Path(path)
    lines = path.read_text().splitlines() if path.exists() else []
    keys = set(settings)
    lines = [line for line in lines if line.split('=', 1)[0].strip() not in keys]
    lines.extend(f'{key}={value}' for key, value in settings.items())
    path.write_text('\n'.join(lines) + '\n')


def listening(port):
    result = run('ss', '-H', '-ltn')
    return any(line.split()[3].rsplit(':', 1)[-1] == str(port)
               and not line.split()[3].startswith(('127.', '[::1]:'))
               for line in result.stdout.splitlines() if len(line.split()) >= 4)


def wait_listener(port):
    for _ in range(10):
        if listening(port):
            return
        time.sleep(0.5)
    raise RuntimeError(f'Port {port} is not listening on a non-loopback interface.')


def configure_ssh(ports, helper, backups):
    previous = {}
    for unit in ('ssh', 'ssh.socket'):
        previous[unit] = {
            'active': run('systemctl', 'is-active', unit, check=False).stdout.strip() == 'active',
            'enabled': run('systemctl', 'is-enabled', unit, check=False).stdout.strip(),
        }
    try:
        return apply_ssh(ports, backups)
    except Exception:
        emit('[SSH] Setup failed; attempting to restore the previous configuration and unit state.')
        saved = backups / 'etc_ssh_sshd_config'
        if saved.exists():
            try:
                shutil.copy2(saved, '/etc/ssh/sshd_config')
                run('/usr/sbin/sshd', '-t')
                run('systemctl', 'stop', 'ssh', 'ssh.socket', check=False)
                run('systemctl', 'daemon-reload')
                for unit, state in previous.items():
                    if state['enabled'] in ('enabled', 'disabled'):
                        run('systemctl', 'enable' if state['enabled'] == 'enabled' else 'disable', unit, check=False)
                    if state['active']:
                        run('systemctl', 'start', unit)
                emit('[SSH] Previous configuration restored; inspect diagnostics before retrying.')
            except Exception as rollback_error:
                emit(f'[SSH] RESTORE FAILED: {rollback_error}; use the VM console and backup.')
        raise


def apply_ssh(ports, backups):
    ensure_packages(['openssh-server'])
    Path('/run/sshd').mkdir(parents=True, exist_ok=True)
    run('ssh-keygen', '-A')
    path = Path('/etc/ssh/sshd_config')
    backup(path, backups)
    # Put these first: OpenSSH uses the first obtained authentication value.
    original = re.sub(r'(?ms)^# BEGIN CYBERCARTOGRAPHER\n.*?^# END CYBERCARTOGRAPHER\n', '', path.read_text())
    lines = original.splitlines()
    lines = [line for line in lines if not re.match(r'^\s*#?\s*Port\s+', line, re.I)]
    path.write_text('\n'.join(['# BEGIN CYBERCARTOGRAPHER', *(f'Port {p}' for p in ports),
                              'PasswordAuthentication yes',
                              'KbdInteractiveAuthentication yes', '# END CYBERCARTOGRAPHER', *lines]) + '\n')
    try:
        run('/usr/sbin/sshd', '-t')
    except Exception:
        saved = backups / 'etc_ssh_sshd_config'
        if saved.exists():
            shutil.copy2(saved, path)
        raise
    # Socket activation can otherwise keep Ubuntu listening on the old port.
    run('systemctl', 'disable', '--now', 'ssh.socket', check=False)
    run('systemctl', 'enable', 'ssh')
    run('systemctl', 'restart', 'ssh')
    for port in ports:
        wait_listener(port)
    effective = run('/usr/sbin/sshd', '-T').stdout
    if 'passwordauthentication yes' not in effective:
        raise RuntimeError('SSH password authentication was not enabled.')
    return [f'SSH TCP {p}: LISTENING; password authentication enabled; use an existing VM account (login not tested).'
            for p in ports]


def configure_ftp(port, flag, mode, helper, backups):
    ensure_packages(['vsftpd'])
    backup('/etc/vsftpd.conf', backups)
    # Same vsftpd settings as 3_ftp-anon-highport.py, without shell helpers.
    run('systemctl', 'stop', 'vsftpd')
    set_config('/etc/vsftpd.conf', {
        'listen': 'YES', 'listen_ipv6': 'NO', 'listen_port': str(port),
        'anonymous_enable': 'YES', 'anon_root': '/srv/ftp',
    })
    root = Path('/srv/ftp')
    root.mkdir(parents=True, exist_ok=True)
    root.chmod(0o755)
    set_config('/etc/vsftpd.conf', {
        'anonymous_enable': 'NO' if mode == 'user' else 'YES',
        'local_enable': 'NO' if mode == 'anonymous' else 'YES',
        'write_enable': 'NO', 'anon_upload_enable': 'NO',
        'anon_mkdir_write_enable': 'NO', 'anon_other_write_enable': 'NO',
        'no_anon_password': 'YES', 'pasv_enable': 'YES',
        'pasv_min_port': '30000', 'pasv_max_port': '30020',
    })
    flag_path = None
    if flag:
        flag_path = root / (flag + '.txt')
        flag_path.write_text(flag + '\n')
        flag_path.chmod(0o644)
    run('systemctl', 'enable', 'vsftpd')
    run('systemctl', 'restart', 'vsftpd')
    wait_listener(port)
    summary = [f'FTP TCP {port}: LISTENING; mode={mode}; read-only; passive data TCP 30000–30020 (firewall unchanged).']
    if mode != 'user':
        with ftplib.FTP() as ftp:
            ftp.connect('127.0.0.1', port, timeout=10)
            ftp.login('anonymous', 'teacher@example.test')
            names = ftp.nlst()
            if flag_path:
                received = []
                ftp.retrlines('RETR ' + flag_path.name, received.append)
                if received != [flag]:
                    raise RuntimeError('FTP flag download did not match.')
            summary.append(f'FTP TCP {port}: anonymous login and directory listing VERIFIED ({len(names)} entries).')
    if mode != 'anonymous':
        summary.append('FTP local-user login enabled; use an existing non-root VM account (login not tested).')
    if flag_path:
        summary.append(f'FTP flag: {flag}; file={flag_path}')
    return summary


def configure_telnet(specs, backups):
    ensure_packages(['inetutils-telnetd', 'xinetd'])
    candidates = ['/usr/sbin/in.telnetd', '/usr/sbin/telnetd']
    server = next((p for p in candidates if Path(p).is_file()), None)
    if not server:
        raise RuntimeError('Installed telnet daemon was not found.')
    run('systemctl', 'disable', '--now', 'telnet.socket', check=False)
    # Disable the legacy script configuration to avoid a duplicate port 23.
    legacy = Path('/etc/xinetd.d/telnet')
    if legacy.exists():
        backup(legacy, backups)
        legacy.write_text('service telnet\n{\n    disable = yes\n}\n')
    summary = []
    for port, flag in specs:
        path = Path(f'/etc/xinetd.d/cybercartographer-telnet-{port}')
        backup(path, backups)
        banner_line = ''
        if flag:
            banner = Path(f'/etc/cybercartographer-telnet-{port}.banner')
            backup(banner, backups)
            banner.write_text(flag + '\r\n')
            banner_line = f'    banner = {banner}\n'
        path.write_text(f'''service cybercartographer_telnet_{port}
{{
    type = UNLISTED
    disable = no
    socket_type = stream
    protocol = tcp
    wait = no
    user = root
    server = {server}
    bind = 0.0.0.0
    port = {port}
{banner_line}}}
''')
    run('systemctl', 'enable', 'xinetd')
    run('systemctl', 'restart', 'xinetd')
    for port, flag in specs:
        wait_listener(port)
        with socket.create_connection(('127.0.0.1', port), timeout=10) as connection:
            connection.settimeout(5)
            data = b''
            try:
                while len(data) < 8192:
                    chunk = connection.recv(1024)
                    if not chunk:
                        break
                    data += chunk
                    if flag and flag.encode() in data:
                        break
                    if not flag and data:
                        break
            except socket.timeout:
                pass
        if not data or (flag and flag.encode() not in data):
            raise RuntimeError(f'Telnet {port}: no expected greeting/flag received.')
        summary.append(f'Telnet TCP {port}: LISTENING; greeting VERIFIED; existing VM login (not tested).')
        if flag:
            summary.append(f'Telnet banner flag VERIFIED: {flag}')
    return summary


def report_folder(output):
    folder = Path(output or f'cybercartographer-target-{datetime.now().strftime("%Y%m%d-%H%M%S")}').resolve()
    folder.mkdir(mode=0o700, parents=True, exist_ok=False)
    return folder


def hand_back(folder):
    """Let the invoking desktop user read/copy reports made with sudo."""
    if os.environ.get('SUDO_UID') and os.environ.get('SUDO_GID'):
        uid, gid = int(os.environ['SUDO_UID']), int(os.environ['SUDO_GID'])
        for path in [*folder.rglob('*'), folder]:
            os.chown(path, uid, gid)


def expected_services(choices, ssh_ports, ftp_port, ftp_flag, mode, telnet_specs):
    entries = [{'service': 'ssh', 'port': p, 'user_login': True} for p in ssh_ports]
    if any(c in choices for c in '345'):
        entries.append({'service': 'ftp', 'port': ftp_port, 'anonymous': mode != 'user',
                        'user_login': mode != 'anonymous', 'flag': ftp_flag,
                        'flag_file': ftp_flag + '.txt' if ftp_flag else None})
    entries.extend({'service': 'telnet', 'port': port, 'user_login': True, 'flag': flag}
                   for port, flag in telnet_specs)
    return entries


class TelnetStream:
    """Small bounded Telnet reader; handles negotiation across packet boundaries."""
    def __init__(self, connection):
        self.connection = connection
        self.state = 'data'
        self.verb = None

    def decode(self, raw):
        output = bytearray()
        for byte in raw:
            if self.state == 'data':
                if byte == 255:
                    self.state = 'iac'
                else:
                    output.append(byte)
            elif self.state == 'iac':
                if byte == 255:
                    output.append(byte)
                    self.state = 'data'
                elif byte in (251, 252, 253, 254):
                    self.verb, self.state = byte, 'option'
                elif byte == 250:
                    self.state = 'sub'
                else:
                    self.state = 'data'
            elif self.state == 'option':
                if self.verb == 251:  # WILL: accept echo/suppress-go-ahead only
                    self.connection.sendall(bytes([255, 253 if byte in (1, 3) else 254, byte]))
                elif self.verb == 253:  # DO: decline local options
                    self.connection.sendall(bytes([255, 252, byte]))
                self.state = 'data'
            elif self.state == 'sub':
                if byte == 255:
                    self.state = 'sub_iac'
            elif self.state == 'sub_iac':
                self.state = 'data' if byte == 240 else 'sub'
        return output.decode('utf-8', errors='replace')

    def read_until(self, pattern, timeout=10):
        deadline = time.monotonic() + timeout
        text = ''
        while time.monotonic() < deadline and len(text) < 32768:
            self.connection.settimeout(min(1, max(0.01, deadline - time.monotonic())))
            try:
                raw = self.connection.recv(4096)
            except socket.timeout:
                continue
            if not raw:
                break
            text += self.decode(raw)
            if re.search(pattern, text, re.I | re.M):
                break
        return text



def check_local(entries):
    results = []
    for entry in entries:
        port, service = entry['port'], entry['service']
        try:
            wait_listener(port)
            with socket.create_connection(('127.0.0.1', port), timeout=5) as connection:
                connection.settimeout(5)
                if service == 'telnet':
                    greeting = TelnetStream(connection).read_until(r'(?:login|username):\s*$', 8)
                    if not re.search(r'(?:login|username):\s*$', greeting, re.I):
                        raise RuntimeError('Telnet did not reach a login prompt after negotiation.')
                    if entry.get('flag') and entry['flag'] not in greeting:
                        raise RuntimeError('Expected Telnet banner flag is missing.')
                    data = greeting.encode()
                else:
                    data = b''
                    while len(data) < 4096 and b'\n' not in data:
                        chunk = connection.recv(4096 - len(data))
                        if not chunk:
                            break
                        data += chunk
            if service == 'ssh' and not data.startswith(b'SSH-'):
                raise RuntimeError('Expected an SSH greeting but received another protocol.')
            if service == 'ftp':
                if not data.startswith(b'220'):
                    raise RuntimeError('Expected FTP 220 greeting.')
                with ftplib.FTP() as ftp:
                    ftp.connect('127.0.0.1', port, timeout=6)
                    if entry.get('anonymous'):
                        ftp.login('anonymous', 'teacher@example.test')
                        ftp.nlst()
                        if entry.get('flag_file'):
                            lines = []
                            ftp.retrlines('RETR ' + entry['flag_file'], lines.append)
                            if lines != [entry['flag']]:
                                raise RuntimeError('FTP flag download differs from expected content.')
                    else:
                        try:
                            ftp.login('anonymous', 'teacher@example.test')
                        except ftplib.error_perm as error:
                            if not str(error).startswith('530'):
                                raise
                        else:
                            raise RuntimeError('Anonymous FTP succeeded although it should be disabled.')
            if service == 'telnet' and not data:
                raise RuntimeError('Telnet accepted the connection but sent no greeting.')
            results.append({'service': service, 'port': port, 'status': 'PASS',
                            'detail': 'Local listener and protocol check passed; user login not tested.'})
        except Exception as error:
            results.append({'service': service, 'port': port, 'status': 'FAIL', 'detail': str(error)})
    return results


def acquire_lock():
    lock = Path('/run/lock/cybercartographer-target.lock').open('a')
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        lock.close()
        raise RuntimeError('Another CyberCartographer setup/check is running; wait for it to finish.')
    return lock


def main(argv=None):
    global LOG
    parser = argparse.ArgumentParser(description='Set up and diagnose classroom services; no upgrades of installed packages.')
    parser.add_argument('--check', metavar='EXPECTATIONS_JSON', help='Read-only local recheck using a previous expectations.json')
    parser.add_argument('--output', help='New report directory (must not already exist)')
    args = parser.parse_args(argv)
    if os.geteuid() != 0:
        print('Run with sudo python3 deploy-target.py')
        return 1
    entries, jobs = [], []
    if args.check:
        manifest = json.loads(Path(args.check).read_text())
        entries = manifest['services']
        if not isinstance(entries, list) or not 1 <= len(entries) <= 100:
            raise ValueError('Expected 1–100 services in the check file.')
        for entry in entries:
            if entry.get('service') not in ('ssh', 'ftp', 'telnet') or type(entry.get('port')) is not int or not 1 <= entry['port'] <= 65535:
                raise ValueError('Invalid service or port in the check file.')
            if entry.get('flag_file') and '/' in entry['flag_file']:
                raise ValueError('Expected FTP filename must be a simple filename.')
            for key in ('flag', 'flag_file'):
                value = entry.get(key)
                if value is not None and (not isinstance(value, str) or len(value) > 500 or '\r' in value or '\n' in value):
                    raise ValueError('Invalid flag in the check file.')
    else:
        print(f'CyberCartographer target setup v{VERSION} — Ubuntu / Kali')
        for number, description in OPTIONS.items():
            print(f'  {number}. {description}')
        print('Combine digits: 136 = SSH 22 + FTP 21 + Telnet 23. High ports: 21000–24000.')
        selection = input('Options (Enter to cancel): ')
        if not selection.strip():
            return 0
        choices = parse_choices(selection)
        mode = 'anonymous'
        if any(c in choices for c in '345'):
            mode = input('FTP login: anonymous / user / both [anonymous]: ').strip().lower() or 'anonymous'
            if mode not in ('anonymous', 'user', 'both'):
                raise ValueError('Unknown FTP mode; no changes made.')
        ftp_flag = '4' in choices or ('5' in choices and input('Add an FTP flag? [y/N]: ').strip().lower() == 'y')
        if ftp_flag and mode == 'user':
            raise ValueError('FTP flags require anonymous or both. No changes made.')
        used = {21, 22, 23}
        ssh_ports = ([22] if '1' in choices else []) + ([high_port(used)] if '2' in choices else [])
        ftp_port = high_port(used) if '5' in choices else 21
        telnet_specs = []
        for choice in choices:
            if choice in '6789':
                port = high_port(used) if choice in '79' else 23
                flag = f'pps{{1x{choice}_telnetp0rt#{port}}}' if choice in '89' else None
                telnet_specs.append((port, flag))
        flag = f'pps{{1x3_ftp0rt#{ftp_port}}}' if ftp_flag else None
        entries = expected_services(choices, ssh_ports, ftp_port, flag, mode, telnet_specs)
        print('Planned: ' + ', '.join(f"{e['service']}:{e['port']}" for e in entries))
        print('Installed packages are reused. Password/plaintext services; keep the VM console open.')
        print('Other old listeners/flags may remain; the student scan reports unexpected services.')
        if input('Apply to this VM? [y/N]: ').strip().lower() != 'y':
            return 0
        if ssh_ports:
            jobs.append(('ssh', lambda backups: configure_ssh(ssh_ports, None, backups)))
        if any(c in choices for c in '345'):
            jobs.append(('ftp', lambda backups: configure_ftp(ftp_port, flag, mode, None, backups)))
        if telnet_specs:
            jobs.append(('telnet', lambda backups: configure_telnet(telnet_specs, backups)))
    lock = acquire_lock()
    folder = report_folder(args.output)
    LOG = (folder / 'run.log').open('w', buffering=1)
    summary, failed = [], False
    started = datetime.now(timezone.utc).isoformat()
    backups = folder / 'backups'
    backups.mkdir()
    emit(f'CyberCartographer {VERSION}; report directory: {folder}')
    manifest = {'version': VERSION, 'created_utc': started, 'services': entries}
    (folder / 'expectations.json').write_text(json.dumps(manifest, indent=2) + '\n')
    try:
        preflight()
        for name, job in jobs:
            emit(f'\n[SETUP] {name}')
            try:
                for line in job(backups):
                    emit(line)
                summary.append(f'{name}: setup completed')
            except (Exception, SystemExit) as error:
                failed = True
                detail = str(error)
                if isinstance(error, subprocess.CalledProcessError):
                    detail += '\n' + (error.stdout or '')[-6000:]
                summary.append(f'{name}: FAILED / INCOMPLETE — {detail}')
                emit(summary[-1])
                LOG.write(traceback.format_exc())
        checks = check_local(entries)
        failed = failed or any(c['status'] == 'FAIL' for c in checks)
    except (Exception, KeyboardInterrupt) as error:
        failed = True
        summary.append(f'RUN FAILED / INTERRUPTED: {error}')
        LOG.write(traceback.format_exc())
        checks = []
    finally:
        emit('\nCollecting service status, journal, listeners, and firewall diagnostics...')
        try:
            diagnostics(folder)
        except Exception as error:
            summary.append(f'Diagnostics incomplete: {error}')
            failed = True
        report = {'version': VERSION, 'created_utc': started, 'failed': failed,
                  'setup': summary, 'checks': checks, 'services': entries}
        (folder / 'results.json').write_text(json.dumps(report, indent=2) + '\n')
        lines = [f'CyberCartographer {VERSION} target report', *summary]
        lines.extend(f"{c['status']} {c['service']} TCP {c['port']}: {c['detail']}" for c in checks)
        lines.extend(['User credentials have not been tested locally. Run validate-target.py from Kali.',
                      'Local success does not prove network/firewall access.',
                      f'Report directory: {folder}',
                      'Share target-summary.txt, results.json, diagnostics.txt, and run.log for troubleshooting.',
                      'expectations.json can be copied to the instructor validation machine for comparison.'])
        text = '\n'.join(lines) + '\n'
        (folder / 'target-summary.txt').write_text(text)
        emit('\n' + text)
        LOG.close()
        LOG = None
        hand_back(folder)
        lock.close()
    return int(failed)


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (KeyboardInterrupt, EOFError):
        print('\nStopped; changes already applied may remain.')
        raise SystemExit(130)
    except Exception as error:
        print(f'Setup stopped: {error}', file=sys.stderr)
        raise SystemExit(1)
