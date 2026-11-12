#!/usr/bin/env python3
"""Interactive classroom target setup. Run with sudo on a disposable range VM.

Reuses the existing SSH/FTP installers and FTP configuration helper. Companion
scripts are loaded from beside this file, or downloaded from the same repository.
"""
import ftplib
import os
from pathlib import Path
import random
import re
import runpy
import shutil
import socket
import subprocess
import sys
import tempfile
import time
from urllib.request import urlopen

BASE = 'https://raw.githubusercontent.com/jboyce1/ppsCTF/main/workrole/cybercartographer/challenges/flagscripts/'
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


def run(*args, check=True):
    return subprocess.run(args, check=check, text=True, capture_output=True)


def parse_choices(text):
    digits = re.sub(r'[\s,]', '', text)
    if not digits or any(c not in OPTIONS for c in digits):
        raise ValueError('Enter option digits, for example 136 or 2,5,9.')
    choices = list(dict.fromkeys(digits))
    for group, label in [('345', 'FTP'), ('68', 'standard Telnet'), ('79', 'high-port Telnet')]:
        if sum(c in group for c in choices) > 1:
            raise ValueError(f'Choose only one {label} option per run.')
    return choices


def load_helper(name):
    local = Path(__file__).resolve().parent / name
    if local.is_file():
        return runpy.run_path(str(local))
    print(f'Downloading existing helper: {name}', flush=True)
    with urlopen(BASE + name, timeout=45) as response:
        source = response.read().decode('utf-8')
    namespace = {'__name__': 'classroom_helper'}
    exec(compile(source, name, 'exec'), namespace)
    return namespace


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
    helper['install_openssh']()
    path = Path('/etc/ssh/sshd_config')
    backup(path, backups)
    # Put these first: OpenSSH uses the first obtained authentication value.
    lines = path.read_text().splitlines()
    lines = [line for line in lines if not re.match(r'^\s*#?\s*Port\s+', line, re.I)]
    path.write_text('\n'.join([*(f'Port {p}' for p in ports),
                              'PasswordAuthentication yes',
                              'KbdInteractiveAuthentication yes', *lines]) + '\n')
    run('/usr/sbin/sshd', '-t')
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
    helper['install_vsftpd']()
    backup('/etc/vsftpd.conf', backups)
    helper['stop_vsftpd']()
    helper['configure_vsftpd'](port)
    root = Path('/srv/ftp')
    root.mkdir(parents=True, exist_ok=True)
    root.chmod(0o755)
    set_config('/etc/vsftpd.conf', {
        'anonymous_enable': 'NO' if mode == 'user' else 'YES',
        'local_enable': 'NO' if mode == 'anonymous' else 'YES',
        'write_enable': 'NO', 'anon_upload_enable': 'NO',
        'anon_mkdir_write_enable': 'NO', 'anon_other_write_enable': 'NO',
        'no_anon_password': 'YES',
    })
    flag_path = None
    if flag:
        flag_path = root / (flag + '.txt')
        flag_path.write_text(flag + '\n')
        flag_path.chmod(0o644)
    helper['restart_vsftpd']()
    wait_listener(port)
    summary = [f'FTP TCP {port}: LISTENING; mode={mode}; read-only.']
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
    run('apt-get', 'update')
    run('apt-get', 'install', '-y', 'inetutils-telnetd', 'xinetd')
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


def main():
    print('CyberCartographer target setup — Ubuntu / Kali, systemd required')
    for number, description in OPTIONS.items():
        print(f'  {number}. {description}')
    print('Combine digits: 136 = SSH 22 + FTP 21 + Telnet 23. High ports: 21000–24000.')
    print('Rerunning reconfigures selected services; other existing services/flags may remain.')
    selection = input('Options (Enter to cancel): ')
    if not selection.strip():
        print('Cancelled; no changes made.')
        return 0
    try:
        choices = parse_choices(selection)
    except ValueError as error:
        print(error)
        return 1
    if os.geteuid() != 0:
        print('Run with: sudo python3 deploy-target.py')
        return 1
    mode = 'anonymous'
    if any(c in choices for c in '345'):
        mode = input('FTP login: anonymous / user / both [anonymous]: ').strip().lower() or 'anonymous'
        if mode not in ('anonymous', 'user', 'both'):
            print('Unknown FTP login mode; no changes made.')
            return 1
    ftp_flag = '4' in choices or ('5' in choices and input('Add an FTP flag? [y/N]: ').strip().lower() == 'y')
    if ftp_flag and mode == 'user':
        print('FTP flags use anonymous download: choose anonymous or both. No changes made.')
        return 1
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
    print('Planned: ' + ', '.join(OPTIONS[c] for c in choices))
    print('This configures password/plaintext services. Use the range VM console when changing SSH ports.')
    if input('Apply to this VM? [y/N]: ').strip().lower() != 'y':
        print('Cancelled; no changes made.')
        return 0
    # Fetch helpers before changing this machine. Do not call their repo-removal functions.
    ssh_helper = load_helper('6_ssh-highport-generator.py') if ssh_ports else None
    ftp_helper = load_helper('3_ftp-anon-highport.py') if any(c in choices for c in '345') else None
    backups = Path(tempfile.mkdtemp(prefix='cybercartographer-backup-', dir='/root'))
    print(f'Configuration backups: {backups}', flush=True)
    summary = []
    failed = False
    jobs = []
    if ssh_ports:
        jobs.append(('SSH', lambda: configure_ssh(ssh_ports, ssh_helper, backups)))
    if ftp_helper:
        jobs.append(('FTP', lambda: configure_ftp(ftp_port, flag, mode, ftp_helper, backups)))
    if telnet_specs:
        jobs.append(('Telnet', lambda: configure_telnet(telnet_specs, backups)))
    for name, job in jobs:
        print(f'\nSetting up {name}...', flush=True)
        try:
            summary.extend(job())
        except (Exception, SystemExit) as error:
            failed = True
            summary.append(f'{name}: FAILED / INCOMPLETE — {error}')
            if isinstance(error, subprocess.CalledProcessError):
                print(error.stdout or '')
                print(error.stderr or '')
    report = '\n'.join(['CyberCartographer verification summary', run('hostname', '-I').stdout.strip(),
                        *summary, f'Backups: {backups}',
                        'Local checks only: validate from Kali; network/firewall access is not tested.']) + '\n'
    print('\n' + report)
    report_path = backups / 'target-summary.txt'
    report_path.write_text(report)
    print(f'Summary saved: {report_path}')
    return int(failed)


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print('\nStopped; changes already applied may remain.')
        raise SystemExit(130)
    except Exception as error:
        print(f'Setup stopped: {error}', file=sys.stderr)
        raise SystemExit(1)
