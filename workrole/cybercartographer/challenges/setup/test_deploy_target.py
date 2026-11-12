"""Launcher tests: no packages installed and no host services changed."""
import importlib.util
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('deploy', Path(__file__).resolve().parents[1] / 'flagscripts/deploy-target.py')
deploy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(deploy)


class DeployTests(unittest.TestCase):
    def test_combined_choices_and_conflicts(self):
        self.assertEqual(deploy.parse_choices('136'), ['1', '3', '6'])
        self.assertEqual(deploy.parse_choices('2, 5, 9, 2'), ['2', '5', '9'])
        for text in ('', '0', '10', '3; reboot', '34', '35', '68', '79'):
            with self.subTest(text=text), self.assertRaises(ValueError):
                deploy.parse_choices(text)

    def test_listener_exact_port_and_interface(self):
        for endpoint, expected in [('0.0.0.0:21', True), ('[::]:21', True),
                                   ('0.0.0.0:21000', False), ('127.0.0.1:21', False),
                                   ('[::1]:21', False)]:
            result = subprocess.CompletedProcess([], 0, f'LISTEN 0 128 {endpoint} 0.0.0.0:*\n', '')
            with self.subTest(endpoint=endpoint), patch.object(deploy, 'run', return_value=result):
                self.assertEqual(deploy.listening(21), expected)

    def test_config_replaces_keys_without_duplicates(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'vsftpd.conf'
            path.write_text('# example\nlisten_port=21001\nlocal_enable=NO\nlisten_port=22\n')
            deploy.set_config(path, {'listen_port': '21', 'local_enable': 'YES'})
            self.assertEqual(path.read_text(), '# example\nlisten_port=21\nlocal_enable=YES\n')

    def test_cancel_does_not_load_or_install(self):
        with patch('builtins.input', side_effect=['136', '', 'n']), patch.object(deploy.os, 'geteuid', return_value=0), patch.object(deploy, 'load_helper') as helper:
            self.assertEqual(deploy.main(), 0)
            helper.assert_not_called()

    def test_combination_summary_and_failure(self):
        for fails in (False, True):
            with self.subTest(fails=fails), tempfile.TemporaryDirectory() as folder:
                with patch('builtins.input', side_effect=['136', '', 'y']), patch.object(deploy.os, 'geteuid', return_value=0), patch.object(deploy, 'load_helper', return_value={'helper': True}), patch.object(deploy.tempfile, 'mkdtemp', return_value=folder), patch.object(deploy, 'configure_ssh', return_value=['SSH checked']) as ssh, patch.object(deploy, 'configure_ftp', return_value=['FTP checked']) as ftp, patch.object(deploy, 'configure_telnet', return_value=['Telnet checked']) as telnet, patch.object(deploy, 'run', return_value=subprocess.CompletedProcess([], 0, '10.15.1.2', '')):
                    if fails:
                        ftp.side_effect = RuntimeError('login refused')
                    self.assertEqual(deploy.main(), int(fails))
                    self.assertEqual(ssh.call_args.args[0], [22])
                    self.assertEqual(ftp.call_args.args[:3], (21, None, 'anonymous'))
                    self.assertEqual(telnet.call_args.args[0], [(23, None)])
                    report = (Path(folder) / 'target-summary.txt').read_text()
                    self.assertIn('FAILED / INCOMPLETE' if fails else 'FTP checked', report)
                    self.assertIn('Telnet checked', report)


if __name__ == '__main__':
    unittest.main()
