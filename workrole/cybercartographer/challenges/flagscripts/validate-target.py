#!/usr/bin/env python3
"""Instructor's student-side discovery and access validation for one range VM.

Python standard library for scan/FTP/Telnet; optional python3-paramiko for SSH
password login. No sudo required, no password in arguments or report files.
"""
import argparse
import base64
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import ftplib
import getpass
import hashlib
import importlib.util
import ipaddress
import json
from pathlib import Path
import re
import secrets
import socket
import sys
import time

VERSION = '2.1'
DEFAULT_PORTS = '21,22,23,21000-24000'


def ports_from_text(text):
    ports = set()
    for item in text.split(','):
        parts = item.strip().split('-')
        if len(parts) not in (1, 2) or not all(p.isdigit() for p in parts):
            raise ValueError('Ports must look like 21,22,23,21000-24000.')
        low, high = int(parts[0]), int(parts[-1])
        if not 1 <= low <= high <= 65535:
            raise ValueError('Port ranges must be within 1–65535.')
        ports.update(range(low, high + 1))
    return sorted(ports)


def load_plan(path):
    data = json.loads(Path(path).read_text())
    entries = data['services']
    if not isinstance(entries, list) or not 1 <= len(entries) <= 100:
        raise ValueError('Expectations must contain 1–100 service entries.')
    seen = set()
    for entry in entries:
        if entry.get('service') not in ('ssh', 'ftp', 'telnet'):
            raise ValueError('Unsupported service in expectations.')
        port = entry.get('port')
        if type(port) is not int or not 1 <= port <= 65535 or port in seen:
            raise ValueError('Invalid or duplicate port in expectations.')
        seen.add(port)
        for key in ('flag', 'flag_file'):
            value = entry.get(key)
            if value is not None and (not isinstance(value, str) or len(value) > 500 or '\r' in value or '\n' in value):
                raise ValueError('Invalid flag in expectations.')
        if entry.get('flag_file') and '/' in entry['flag_file']:
            raise ValueError('Expected FTP filename must be a simple filename.')
    return entries


def scan_port(host, port, timeout):
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return port, 'open'
    except ConnectionRefusedError:
        return port, 'closed'
    except (socket.timeout, TimeoutError):
        return port, 'timeout'
    except OSError:
        return port, 'unreachable'


def scan(host, ports, timeout):
    opened, counts = [], {'open': 0, 'closed': 0, 'timeout': 0, 'unreachable': 0}
    started = time.monotonic()
    with ThreadPoolExecutor(max_workers=64) as pool:
        futures = [pool.submit(scan_port, host, port, timeout) for port in ports]
        try:
            for index, future in enumerate(as_completed(futures), 1):
                port, state = future.result()
                counts[state] += 1
                if state == 'open':
                    opened.append(port)
                    print(f'  OPEN TCP {port}', flush=True)
                if index % 500 == 0:
                    print(f'  Scanned {index}/{len(ports)} ports ({time.monotonic() - started:.1f}s)', flush=True)
        except BaseException:
            for future in futures:
                future.cancel()
            raise
    return sorted(opened), counts


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


def detect(host, port, timeout):
    with socket.create_connection((host, port), timeout=timeout) as connection:
        connection.settimeout(timeout)
        greeting = b''
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline and len(greeting) < 4096:
            connection.settimeout(max(0.01, deadline - time.monotonic()))
            try:
                chunk = connection.recv(4096 - len(greeting))
            except socket.timeout:
                break
            if not chunk:
                break
            greeting += chunk
            if ((greeting.startswith((b'SSH-', b'220')) and b'\n' in greeting)
                    or b'\xff' in greeting or re.search(rb'(login:|username:|telnet)', greeting, re.I)):
                break
        if not greeting:
            return 'unknown', 'No unsolicited greeting'
    if greeting.startswith(b'SSH-'):
        return 'ssh', repr(greeting[:300])
    if greeting.startswith(b'220'):
        # Distinguish FTP from SMTP and other services with 220 greetings.
        with ftplib.FTP() as ftp:
            ftp.connect(host, port, timeout=timeout)
            reply = ftp.sendcmd('FEAT')
            if not reply.startswith('211'):
                raise RuntimeError('Service did not answer FTP FEAT as expected.')
        return 'ftp', repr(greeting[:300])
    if b'\xff' in greeting or re.search(rb'(login:|username:|telnet)', greeting, re.I):
        return 'telnet', repr(greeting[:300])
    return 'unknown', repr(greeting[:300])


def check_ssh(host, port, username, password, timeout):
    if not username:
        return [('SKIP', 'SSH password login: no account supplied.')]
    if importlib.util.find_spec('paramiko') is None:
        return [('SKIP', 'SSH login needs python3-paramiko; install it on this validation machine.')]
    import paramiko
    client = paramiko.SSHClient()
    # Temporary classroom connection: do not change the student's known_hosts.
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(host, port=port, username=username, password=password,
                       look_for_keys=False, allow_agent=False, timeout=timeout,
                       banner_timeout=timeout, auth_timeout=timeout)
        key = client.get_transport().get_remote_server_key()
        fingerprint = base64.b64encode(hashlib.sha256(key.asbytes()).digest()).decode().rstrip('=')
        marker = 'CC_CHECK_' + secrets.token_hex(12)
        _, stdout, stderr = client.exec_command("printf '%s\\n' " + marker, timeout=timeout)
        stdout.channel.settimeout(timeout)
        received = stdout.read(4096).decode('utf-8', errors='replace').strip()
        if received != marker or stdout.channel.recv_exit_status() != 0:
            raise RuntimeError('SSH authenticated but the validation command did not succeed.')
        return [('PASS', f'SSH password login and command execution verified; host key SHA256:{fingerprint} (un-pinned classroom connection).')]
    finally:
        client.close()


def ftp_login(host, port, username, password, entry, timeout):
    with ftplib.FTP() as ftp:
        ftp.connect(host, port, timeout=timeout)
        ftp.login(username, password)
        names = ftp.nlst()
        details = [f'FTP {username}: login and directory listing verified ({len(names)} entries).']
        candidates = [entry['flag_file']] if entry.get('flag_file') else [name for name in names if name.startswith('pps{') and name.endswith('.txt')][:10]
        for name in candidates:
            if '\r' in name or '\n' in name or '/' in name:
                continue
            content = bytearray()
            def collect(chunk):
                if len(content) + len(chunk) > 65536:
                    raise RuntimeError('Flag file exceeds the 64 KiB validation limit.')
                content.extend(chunk)
            ftp.retrbinary('RETR ' + name, collect)
            text = content.decode('utf-8', errors='replace').strip()
            if entry.get('flag') and text != entry['flag']:
                raise RuntimeError('Downloaded FTP flag does not match expectations.')
            details.append(f'FTP flag download verified: {name!r}; content={text!r}')
        return details


def check_ftp(host, port, username, password, entry, timeout):
    results = []
    if entry.get('anonymous') is False:
        try:
            with ftplib.FTP() as ftp:
                ftp.connect(host, port, timeout=timeout)
                ftp.login('anonymous', 'classroom@example.test')
        except ftplib.error_perm as error:
            results.append(('PASS' if str(error).startswith('530') else 'FAIL',
                            f'Anonymous login denied: {error}'))
        except Exception as error:
            results.append(('FAIL', f'Could not verify anonymous login denial: {error}'))
        else:
            results.append(('FAIL', 'Anonymous FTP succeeded but expectations require it disabled.'))
    else:
        try:
            details = ftp_login(host, port, 'anonymous', 'classroom@example.test', entry, timeout)
        except ftplib.error_perm as error:
            results.append(('FAIL' if entry.get('anonymous') else 'INFO', f'Anonymous FTP access denied: {error}'))
        except Exception as error:
            results.append(('FAIL', f'Anonymous FTP access failed: {error}'))
        else:
            results.extend(('PASS', detail) for detail in details)
    if entry.get('user_login') or (username and 'user_login' not in entry):
        if not username:
            results.append(('SKIP', 'FTP user login: no account supplied.'))
        else:
            try:
                # A local account starts in its home, not /srv/ftp; do not expect the anonymous flag here.
                details = ftp_login(host, port, username, password, {}, timeout)
                results.extend(('PASS', detail) for detail in details)
            except ftplib.error_perm as error:
                if entry.get('user_login') is True:
                    results.append(('FAIL', f'Expected FTP user access failed: {error}'))
                else:
                    results.append(('INFO', f'FTP user access denied: {error}; user login was not explicitly expected. Supply expectations.json to verify the intended login mode.'))
            except Exception as error:
                results.append(('FAIL', f'FTP user access failed: {error}'))
    return results


def check_telnet(host, port, username, password, entry, timeout):
    results = []
    with socket.create_connection((host, port), timeout=timeout) as connection:
        stream = TelnetStream(connection)
        greeting = stream.read_until(r'(?:login|username):\s*$', timeout)
        if not re.search(r'(?:login|username):\s*$', greeting, re.I):
            raise RuntimeError('Telnet did not reach a login prompt (not just an open socket).')
        results.append(('PASS', 'Telnet negotiation and login prompt verified.'))
        if entry.get('flag'):
            if entry['flag'] not in greeting:
                raise RuntimeError('Expected Telnet flag is missing from the banner.')
            results.append(('PASS', 'Telnet banner flag verified: ' + entry['flag']))
        else:
            flags = re.findall(r'pps\{[^\r\n}]+\}', greeting)
            results.extend(('PASS', 'Telnet banner flag observed: ' + flag) for flag in flags)
        if not username:
            results.append(('SKIP', 'Telnet login: no account supplied.'))
            return results
        connection.sendall(username.encode() + b'\r\n')
        prompt = stream.read_until(r'password:\s*$|login incorrect|authentication fail', timeout)
        if not re.search(r'password:\s*$', prompt, re.I):
            raise RuntimeError('Telnet did not request a password for the supplied account.')
        connection.sendall(password.encode() + b'\r\n')
        prompt = stream.read_until(r'[$#>]\s*$|login incorrect|authentication fail|login:\s*$', timeout)
        if re.search(r'login incorrect|authentication fail|login:\s*$', prompt, re.I):
            raise RuntimeError('Telnet credentials were rejected.')
        # The command's echo cannot contain the expected output marker.
        marker = 'CC_CHECK_' + secrets.token_hex(12)
        encoded = ''.join(f'\\{ord(c):03o}' for c in marker)
        connection.sendall(f"printf '{encoded}\\n'\r\n".encode())
        response = stream.read_until(re.escape(marker), timeout)
        if marker not in response:
            raise RuntimeError('Telnet login/command execution could not be verified.')
        connection.sendall(b'exit\r\n')
        results.append(('PASS', 'Telnet password login and command execution verified.'))
    return results


def validate(host, entries, opened, username, password, timeout):
    expected = {entry['port']: entry for entry in entries}
    results = []
    def record(service, port, status, detail):
        if password:
            detail = detail.replace(password, '[REDACTED]')
        results.append({'service': service, 'port': port, 'status': status, 'detail': detail})
        print(f'{status} {service} TCP {port}: {detail}', flush=True)
    for port in sorted(set(opened) | set(expected)):
        entry = expected.get(port, {})
        service = entry.get('service', 'unknown')
        if port not in opened and port in expected:
            print(f'  Retrying expected TCP {port} with {timeout}s timeout...', flush=True)
            if scan_port(host, port, timeout)[1] == 'open':
                opened.append(port)
        if port not in opened:
            record(service, port, 'FAIL', 'Expected port is not reachable/open from this machine.')
            continue
        try:
            detected, greeting = detect(host, port, timeout)
            if service != 'unknown' and detected != service:
                raise RuntimeError(f'Expected {service}, detected {detected}; greeting={greeting}')
            service = detected
            record(service, port, 'PASS' if service != 'unknown' else 'INFO', 'Protocol probe: ' + greeting)
            if entries and port not in expected:
                record(service, port, 'WARN', 'Unexpected open port within the scan scope; may be an old listener.')
            if service == 'ssh':
                checks = check_ssh(host, port, username, password, timeout)
            elif service == 'ftp':
                checks = check_ftp(host, port, username, password, entry, timeout)
            elif service == 'telnet':
                checks = check_telnet(host, port, username, password, entry, timeout)
            else:
                checks = [('SKIP', 'Unknown protocol; access not validated.')]
            for status, detail in checks:
                record(service, port, status, detail)
        except Exception as error:
            record(service, port, 'FAIL', f'{type(error).__name__}: {error}')
    return results


def main(argv=None):
    parser = argparse.ArgumentParser(description='Discover and validate a single classroom target from the student side.')
    parser.add_argument('target', nargs='?', help='Single target IPv4/IPv6 address (no subnets)')
    parser.add_argument('--expect', help='Optional expectations.json copied from the target report')
    parser.add_argument('--ports', default=DEFAULT_PORTS, help='Scan scope, default: ' + DEFAULT_PORTS)
    parser.add_argument('--timeout', type=float, default=8, help='Protocol/login timeout seconds (default 8)')
    parser.add_argument('--connect-timeout', type=float, default=0.7, help='Per-port discovery timeout (default 0.7)')
    parser.add_argument('--no-login', action='store_true', help='Skip account/password prompt; report user checks as SKIP')
    parser.add_argument('--output', help='New report directory')
    args = parser.parse_args(argv)
    host = str(ipaddress.ip_address(args.target or input('Target VM IP: ').strip()))
    if not 0.1 <= args.timeout <= 60 or not 0.1 <= args.connect_timeout <= 10:
        raise ValueError('Timeouts must be 0.1–60 seconds (connect timeout at most 10).')
    entries = load_plan(args.expect) if args.expect else []
    ports = sorted(set(ports_from_text(args.ports)) | {entry['port'] for entry in entries})
    folder = Path(args.output or f'cybercartographer-student-{datetime.now().strftime("%Y%m%d-%H%M%S")}').resolve()
    folder.mkdir(parents=True, mode=0o700, exist_ok=False)
    username, password = '', ''
    if not args.no_login:
        print('Optional: enter one existing non-root VM account for SSH/FTP-user/Telnet access checks.')
        username = input('VM username (Enter to skip user logins): ').strip()
        if username:
            if '\r' in username or '\n' in username:
                raise ValueError('Username must be one line.')
            password = getpass.getpass('VM password (not saved): ')
            if '\r' in password or '\n' in password:
                raise ValueError('Telnet validation requires a one-line password.')
    print(f'CyberCartographer validator {VERSION}; target={host}; scanning {len(ports)} TCP ports.', flush=True)
    print('Scope: ' + args.ports + '; expected ports added automatically. No UDP checks.', flush=True)
    results, opened, counts = [], [], {}
    interrupted = False
    try:
        opened, counts = scan(host, ports, args.connect_timeout)
        if not opened:
            results.append({'status': 'FAIL', 'service': 'discovery', 'port': None,
                            'detail': 'No open ports found. Check VM IP, state, firewall, range routing, or increase --connect-timeout.'})
        results.extend(validate(host, entries, opened, username, password, args.timeout))
    except KeyboardInterrupt:
        interrupted = True
        results.append({'status': 'FAIL', 'service': 'run', 'port': None, 'detail': 'Validation interrupted; results incomplete.'})
    except Exception as error:
        results.append({'status': 'FAIL', 'service': 'run', 'port': None, 'detail': f'{type(error).__name__}: {error}'})
    finally:
        if not entries:
            results.append({'status': 'INFO', 'service': 'expectations', 'port': None,
                            'detail': 'No expectations file: only discovered services were checked; missing intended services cannot be identified.'})
        report = {'version': VERSION, 'created_utc': datetime.now(timezone.utc).isoformat(),
                  'target': host, 'scanned_ports': ports, 'discovery_counts': counts, 'open_ports': opened,
                  'expectations_supplied': bool(entries), 'results': results}
        # No password is intentionally logged; also scrub error strings from remote servers.
        encoded = json.dumps(report, indent=2)
        if password:
            encoded = encoded.replace(json.dumps(password)[1:-1], '[REDACTED]')
        (folder / 'student-results.json').write_text(encoded + '\n')
        lines = [f'CyberCartographer {VERSION} student-side report: {host}',
                 f'TCP ports scanned: {len(ports)}; open: {opened}; states: {counts}']
        lines.extend(f"{r['status']} {r['service']} TCP {r['port']}: {r['detail']}" for r in results)
        failed = any(r['status'] == 'FAIL' for r in results)
        incomplete = any(r['status'] in ('SKIP', 'WARN') for r in results) or not entries
        lines.append('OVERALL: ' + ('FAIL' if failed else 'INCOMPLETE' if incomplete else 'PASS'))
        text = '\n'.join(lines) + '\n'
        if password:
            text = text.replace(password, '[REDACTED]')
        (folder / 'student-summary.txt').write_text(text)
        print('\n' + text)
        print(f'Reports saved: {folder}')
    return 130 if interrupted else 1 if failed else 2 if incomplete else 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (KeyboardInterrupt, EOFError):
        print('\nCancelled.')
        raise SystemExit(130)
    except Exception as error:
        print(f'Validation stopped: {error}', file=sys.stderr)
        raise SystemExit(1)
