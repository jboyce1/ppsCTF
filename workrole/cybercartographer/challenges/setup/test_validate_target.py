"""Real loopback protocol tests plus failure/report tests. No system services used."""
from contextlib import contextmanager
import importlib.util
import json
from pathlib import Path
import re
import socket
import socketserver
import tempfile
import threading
import time
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('validator', Path(__file__).resolve().parents[1] / 'flagscripts/validate-target.py')
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


@contextmanager
def server(handler):
    class Service(socketserver.ThreadingTCPServer):
        allow_reuse_address = True
        daemon_threads = True
        def handle_error(self, request, client_address):
            pass  # Probes deliberately disconnect before completing login.
    instance = Service(('127.0.0.1', 0), handler)
    thread = threading.Thread(target=instance.serve_forever, daemon=True)
    thread.start()
    try:
        yield instance.server_address[1]
    finally:
        instance.shutdown()
        instance.server_close()
        thread.join(2)


class FTPHandler(socketserver.StreamRequestHandler):
    flag = 'pps{test_ftp}'
    def handle(self):
        passive = None
        self.wfile.write(b'220 Test FTP\r\n')
        while True:
            line = self.rfile.readline().decode().strip()
            if not line:
                break
            command, _, argument = line.partition(' ')
            if command == 'QUIT':
                self.wfile.write(b'221 Bye\r\n')
                break
            if command == 'FEAT':
                self.wfile.write(b'211 End\r\n')
            elif command == 'USER':
                self.wfile.write(b'331 Password\r\n')
            elif command == 'PASS':
                self.wfile.write(b'230 Welcome\r\n' if argument in ('classroom@example.test', 'teacher@example.test', 'secret') else b'530 Login incorrect\r\n')
            elif command == 'TYPE':
                self.wfile.write(b'200 Type set\r\n')
            elif command == 'PASV':
                passive = socket.socket()
                passive.bind(('127.0.0.1', 0))
                passive.listen()
                passive.settimeout(2)
                port = passive.getsockname()[1]
                self.wfile.write(f'227 Passive (127,0,0,1,{port // 256},{port % 256})\r\n'.encode())
            elif command in ('NLST', 'RETR'):
                self.wfile.write(b'150 Opening data\r\n')
                connection, _ = passive.accept()
                content = self.flag + ('.txt' if command == 'NLST' else '') + '\r\n'
                connection.sendall(content.encode())
                connection.close()
                passive.close()
                self.wfile.write(b'226 Complete\r\n')
            else:
                self.wfile.write(b'500 Unknown command\r\n')
        if passive:
            passive.close()


class TelnetHandler(socketserver.StreamRequestHandler):
    def handle(self):
        self.wfile.write(b'pps{test_telnet}\r\nlogin: ')
        if self.rfile.readline().strip() != b'student':
            return
        self.wfile.write(b'Password: ')
        if self.rfile.readline().strip() != b'secret':
            self.wfile.write(b'Login incorrect\r\n')
            return
        self.wfile.write(b'Welcome\r\nstudent@vm:~$ ')
        command = self.rfile.readline().decode()
        self.wfile.write(command.encode())  # Echo the command: must not count as execution.
        match = re.search(r"printf '((?:\\[0-7]{3})+)", command)
        if match:
            output = ''.join(chr(int(octal, 8)) for octal in re.findall(r'\\([0-7]{3})', match.group(1)))
            self.wfile.write(output.encode() + b'\r\nstudent@vm:~$ ')


class EchoOnlyTelnet(TelnetHandler):
    def handle(self):
        self.wfile.write(b'login: ')
        self.rfile.readline()
        self.wfile.write(b'Password: ')
        self.rfile.readline()
        self.wfile.write(b'$ ')
        self.wfile.write(self.rfile.readline())


class ValidatorTests(unittest.TestCase):
    def test_port_ranges(self):
        self.assertEqual(validator.ports_from_text('21,22,22,21000-21002'), [21, 22, 21000, 21001, 21002])
        for text in ('0', '65536', '30-21', '22;echo', ''):
            with self.assertRaises(ValueError):
                validator.ports_from_text(text)

    def test_real_scan_open_and_closed(self):
        with server(TelnetHandler) as port:
            opened, counts = validator.scan('127.0.0.1', [port], 1)
            self.assertEqual(opened, [port])
            self.assertEqual(counts['open'], 1)
        self.assertEqual(validator.scan_port('127.0.0.1', port, 1)[1], 'closed')

    def test_real_ftp_discovery_listing_and_flag_download(self):
        with server(FTPHandler) as port:
            self.assertEqual(validator.detect('127.0.0.1', port, 2)[0], 'ftp')
            entry = {'anonymous': True, 'flag': FTPHandler.flag, 'flag_file': FTPHandler.flag + '.txt'}
            result = validator.check_ftp('127.0.0.1', port, '', '', entry, 2)
            self.assertTrue(all(status == 'PASS' for status, _ in result), result)
            self.assertTrue(any('download verified' in text for _, text in result))
            entry['flag'] = 'pps{wrong}'
            result = validator.check_ftp('127.0.0.1', port, '', '', entry, 2)
            self.assertTrue(any(status == 'FAIL' for status, _ in result))

    def test_anonymous_access_is_a_failure_when_disabled_in_plan(self):
        with server(FTPHandler) as port:
            result = validator.check_ftp('127.0.0.1', port, '', '', {'anonymous': False}, 2)
            self.assertTrue(any(status == 'FAIL' for status, _ in result))

    def test_target_local_ftp_and_telnet_rechecks(self):
        target_spec = importlib.util.spec_from_file_location('target_check', Path(__file__).resolve().parents[1] / 'flagscripts/deploy-target.py')
        target = importlib.util.module_from_spec(target_spec)
        target_spec.loader.exec_module(target)
        with server(FTPHandler) as ftp_port, server(TelnetHandler) as telnet_port, patch.object(target, 'wait_listener'):
            entries = [
                {'service': 'ftp', 'port': ftp_port, 'anonymous': True, 'flag': FTPHandler.flag, 'flag_file': FTPHandler.flag + '.txt'},
                {'service': 'telnet', 'port': telnet_port, 'flag': 'pps{test_telnet}'},
            ]
            result = target.check_local(entries)
            self.assertEqual([r['status'] for r in result], ['PASS', 'PASS'])
            entries[1]['flag'] = 'pps{missing}'
            self.assertEqual(target.check_local(entries)[1]['status'], 'FAIL')

    def test_real_ftp_wrong_user_password_fails(self):
        with server(FTPHandler) as port:
            result = validator.check_ftp('127.0.0.1', port, 'student', 'wrong', {'anonymous': True, 'user_login': True}, 2)
            self.assertTrue(any(status == 'FAIL' and 'user access' in detail for status, detail in result))

    def test_telnet_packet_boundary_negotiation(self):
        class Connection:
            def __init__(self):
                self.sent = []
            def sendall(self, data):
                self.sent.append(data)
        connection = Connection()
        stream = validator.TelnetStream(connection)
        self.assertEqual(stream.decode(b'log\xff\xfb'), 'log')
        self.assertEqual(stream.decode(b'\x01in: '), 'in: ')
        self.assertEqual(connection.sent, [b'\xff\xfd\x01'])
        self.assertEqual(stream.decode(b'\xff\xfa\x18abc\xff'), '')
        self.assertEqual(stream.decode(b'\xf0ready'), 'ready')

    def test_real_telnet_login_and_flag(self):
        with server(TelnetHandler) as port:
            result = validator.check_telnet('127.0.0.1', port, 'student', 'secret', {'flag': 'pps{test_telnet}'}, 2)
            self.assertTrue(all(status == 'PASS' for status, _ in result))
            self.assertTrue(any('command execution' in text for _, text in result))
            with self.assertRaisesRegex(RuntimeError, 'rejected'):
                validator.check_telnet('127.0.0.1', port, 'student', 'wrong', {}, 2)
            with self.assertRaisesRegex(RuntimeError, 'flag is missing'):
                validator.check_telnet('127.0.0.1', port, '', '', {'flag': 'missing'}, 2)

    def test_echo_does_not_falsely_verify_telnet_login(self):
        with server(EchoOnlyTelnet) as port:
            with self.assertRaisesRegex(RuntimeError, 'could not be verified'):
                validator.check_telnet('127.0.0.1', port, 'student', 'secret', {}, 1)

    def test_missing_expected_service_fails(self):
        with patch.object(validator, 'scan_port', return_value=(22, 'closed')):
            result = validator.validate('127.0.0.1', [{'service': 'ssh', 'port': 22}], [], '', '', 1)
        self.assertEqual(result[0]['status'], 'FAIL')

    def test_wrong_protocol_fails_and_other_checks_continue(self):
        with patch.object(validator, 'detect', return_value=('ftp', '220 FTP')):
            result = validator.validate('127.0.0.1', [{'service': 'ssh', 'port': 22}], [22], '', '', 1)
        self.assertEqual(result[-1]['status'], 'FAIL')

    def test_expected_filename_rejects_command_injection(self):
        with tempfile.TemporaryDirectory() as folder:
            plan = Path(folder) / 'plan.json'
            plan.write_text(json.dumps({'services': [{'service': 'ftp', 'port': 21, 'flag_file': 'foo\r\nDELE bar'}]}))
            with self.assertRaises(ValueError):
                validator.load_plan(plan)

    def test_report_redacts_password_and_marks_skipped_incomplete(self):
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / 'output'
            with patch('builtins.input', return_value='student'), patch.object(validator.getpass, 'getpass', return_value='topsecret'), patch.object(validator, 'scan', return_value=([22], {'open': 1})), patch.object(validator, 'validate', return_value=[{'status': 'SKIP', 'service': 'ssh', 'port': 22, 'detail': 'remote error topsecret'}]):
                self.assertEqual(validator.main(['127.0.0.1', '--ports', '22', '--output', str(output)]), 2)
            for path in output.iterdir():
                self.assertNotIn('topsecret', path.read_text())

    @unittest.skipUnless(importlib.util.find_spec('paramiko'), 'optional paramiko not installed')
    def test_real_ssh_password_login_and_exec(self):
        import paramiko
        key = paramiko.RSAKey.generate(2048)
        class Auth(paramiko.ServerInterface):
            def check_auth_password(self, username, password):
                return paramiko.AUTH_SUCCESSFUL if (username, password) == ('student', 'secret') else paramiko.AUTH_FAILED
            def get_allowed_auths(self, username):
                return 'password'
            def check_channel_request(self, kind, chanid):
                return paramiko.OPEN_SUCCEEDED if kind == 'session' else paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED
            def check_channel_exec_request(self, channel, command):
                marker = command.decode().split()[-1]
                channel.sendall((marker + '\n').encode())
                channel.send_exit_status(0)
                channel.shutdown_write()
                return True
        class SSHHandler(socketserver.BaseRequestHandler):
            def handle(self):
                transport = paramiko.Transport(self.request)
                transport.add_server_key(key)
                try:
                    transport.start_server(server=Auth())
                    channel = transport.accept(3)
                    if channel:
                        deadline = time.monotonic() + 3
                        while transport.is_active() and time.monotonic() < deadline:
                            time.sleep(0.02)
                finally:
                    transport.close()
        with server(SSHHandler) as port:
            result = validator.check_ssh('127.0.0.1', port, 'student', 'secret', 3)
            self.assertEqual(result[0][0], 'PASS')
            with self.assertRaises(paramiko.AuthenticationException):
                validator.check_ssh('127.0.0.1', port, 'student', 'wrong', 3)


if __name__ == '__main__':
    unittest.main()
