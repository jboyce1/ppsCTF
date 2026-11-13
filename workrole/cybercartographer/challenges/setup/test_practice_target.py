"""Practice copy tests: no host packages or services are changed."""
import ast
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch

SCRIPT = Path(__file__).resolve().parents[1] / 'practice/deploy-practice.py'
spec = importlib.util.spec_from_file_location('practice', SCRIPT)
practice = importlib.util.module_from_spec(spec)
spec.loader.exec_module(practice)


class PracticeTests(unittest.TestCase):
    def test_copy_contains_no_challenge_generation_or_fields(self):
        source = SCRIPT.read_text()
        self.assertNotIn('pps{', source)
        self.assertFalse(any(isinstance(n, ast.Name) and 'flag' in n.id for n in ast.walk(ast.parse(source))))
        entries = practice.expected_services([22], 21, 'both', [23])
        self.assertTrue(all(set(e) <= {'service', 'port', 'anonymous', 'user_login'} for e in entries))

    def test_menu_and_conflicts(self):
        self.assertEqual(set(practice.OPTIONS), set('123456'))
        self.assertEqual(practice.parse_choices('135'), ['1', '3', '5'])
        self.assertEqual(practice.parse_choices('2,4,6'), ['2', '4', '6'])
        for value in ['7', '8', '9', '34', '1345']:
            with self.assertRaises(ValueError):
                practice.parse_choices(value)

    def test_standard_and_high_port_recipes(self):
        for answers, ssh_ports, ftp_port, telnet_ports in [(['135', '', 'y'], [22], 21, [23]), (['246', 'both', 'y'], [23344], 23345, [23346])]:
            with self.subTest(answers=answers), tempfile.TemporaryDirectory() as folder:
                root = Path(folder)
                with patch('builtins.input', side_effect=answers), patch.object(practice.os, 'geteuid', return_value=0), patch.object(practice, 'acquire_lock', return_value=Mock()), patch.object(practice, 'report_folder', return_value=root), patch.object(practice, 'preflight'), patch.object(practice, 'high_port', side_effect=[23344, 23345, 23346]), patch.object(practice, 'configure_ssh', return_value=[]) as ssh, patch.object(practice, 'configure_ftp', return_value=[]) as ftp, patch.object(practice, 'configure_telnet', return_value=[]) as telnet, patch.object(practice, 'check_local', side_effect=lambda entries: [dict(service=e['service'], port=e['port'], status='PASS', detail='test') for e in entries]), patch.object(practice, 'diagnostics'), patch.object(practice, 'machine_addresses', return_value=['10.15.1.144']), patch.object(practice, 'hand_back'):
                    self.assertEqual(practice.main([]), 0)
                self.assertEqual(ssh.call_args.args[0], ssh_ports)
                self.assertEqual(ftp.call_args.args[0], ftp_port)
                self.assertEqual(telnet.call_args.args[0], telnet_ports)
                plan = json.loads((root / 'expectations.json').read_text())
                self.assertTrue(all('flag' not in e and 'flag_file' not in e for e in plan['services']))
                self.assertNotIn('FLAG', (root / 'inventory.txt').read_text())

    def test_ftp_creates_no_challenge_files(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder) / 'ftp'
            with patch.object(practice, 'Path', return_value=root), patch.object(practice, 'ensure_packages'), patch.object(practice, 'backup'), patch.object(practice, 'set_config') as settings, patch.object(practice, 'run'), patch.object(practice, 'wait_listener'):
                practice.configure_ftp(21, 'anonymous', Path(folder))
            self.assertEqual(list(root.iterdir()), [])
            self.assertEqual(settings.call_args.args[1]['listen_port'], '21')

    def test_telnet_config_has_no_banner(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            daemon = root / 'usr/sbin/in.telnetd'
            daemon.parent.mkdir(parents=True)
            daemon.touch()
            (root / 'etc/xinetd.d').mkdir(parents=True)
            def local_path(value):
                return root / str(value).lstrip('/')
            with patch.object(practice, 'Path', side_effect=local_path), patch.object(practice, 'ensure_packages'), patch.object(practice, 'backup'), patch.object(practice, 'run'), patch.object(practice, 'wait_listener'):
                practice.configure_telnet([23, 23345], root)
            for port in [23, 23345]:
                config = (root / f'etc/xinetd.d/cybercartographer-telnet-{port}').read_text()
                self.assertNotIn('banner', config)
                self.assertNotIn('pps{', config)


if __name__ == '__main__':
    unittest.main()
