"""No packages installed and no host services changed by these tests."""
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch

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

    def test_cancel_does_not_install(self):
        with patch('builtins.input', side_effect=['136', '', 'n']), patch.object(deploy.os, 'geteuid', return_value=0), patch.object(deploy, 'ensure_packages') as packages:
            self.assertEqual(deploy.main([]), 0)
            packages.assert_not_called()

    def test_installed_packages_skip_apt(self):
        result = subprocess.CompletedProcess([], 0, 'install ok installed', '')
        with patch.object(deploy, 'run', return_value=result) as command:
            deploy.ensure_packages(['openssh-server', 'vsftpd'])
            self.assertTrue(all(call.args[0] == 'dpkg-query' for call in command.call_args_list))

    def test_missing_packages_update_once(self):
        def response(*args, **kwargs):
            return subprocess.CompletedProcess(args, 1 if args[0] == 'dpkg-query' else 0, '', '')
        with patch.object(deploy, 'APT_UPDATED', False), patch.object(deploy, 'run', side_effect=response) as command:
            deploy.ensure_packages(['vsftpd'])
            deploy.ensure_packages(['xinetd'])
            updates = [c for c in command.call_args_list if 'update' in c.args]
            self.assertEqual(len(updates), 1)
            for call in command.call_args_list:
                if call.args[0] == 'apt-get':
                    self.assertIn('timeout', call.kwargs)

    def test_failed_update_does_not_install(self):
        def response(*args, **kwargs):
            if args[0] == 'dpkg-query':
                return subprocess.CompletedProcess(args, 1, '', '')
            raise subprocess.CalledProcessError(100, args, output='repository unavailable')
        with patch.object(deploy, 'APT_UPDATED', False), patch.object(deploy, 'run', side_effect=response) as command:
            with self.assertRaises(subprocess.CalledProcessError):
                deploy.ensure_packages(['openssh-server'])
            self.assertFalse(any('install' in c.args for c in command.call_args_list))

    def test_real_command_output_and_failure(self):
        result = deploy.run(sys.executable, '-c', "print('progress evidence')")
        self.assertIn('progress evidence', result.stdout)
        with self.assertRaises(subprocess.CalledProcessError) as error:
            deploy.run(sys.executable, '-c', "print('failure evidence'); raise SystemExit(4)")
        self.assertIn('failure evidence', error.exception.stdout)

    def test_real_command_timeout(self):
        with self.assertRaises(subprocess.TimeoutExpired):
            deploy.run(sys.executable, '-c', 'import time; time.sleep(20)', timeout=0.2)

    def test_job_failure_still_saves_diagnostics_and_other_services(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            with patch('builtins.input', side_effect=['136', '', 'y']), patch.object(deploy.os, 'geteuid', return_value=0), patch.object(deploy, 'acquire_lock', return_value=Mock()), patch.object(deploy, 'report_folder', return_value=root), patch.object(deploy, 'preflight'), patch.object(deploy, 'configure_ssh', return_value=['SSH checked']), patch.object(deploy, 'configure_ftp', side_effect=RuntimeError('FTP login refused')), patch.object(deploy, 'configure_telnet', return_value=['Telnet checked']), patch.object(deploy, 'check_local', return_value=[]), patch.object(deploy, 'diagnostics') as diag, patch.object(deploy, 'hand_back'):
                self.assertEqual(deploy.main([]), 1)
            report = json.loads((root / 'results.json').read_text())
            self.assertTrue(report['failed'])
            self.assertIn('telnet: setup completed', report['setup'])
            self.assertIn('FTP login refused', (root / 'target-summary.txt').read_text())
            diag.assert_called_once_with(root)
            self.assertEqual(len(json.loads((root / 'expectations.json').read_text())['services']), 3)

    def test_preflight_failure_still_writes_report(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            with patch('builtins.input', side_effect=['1', 'y']), patch.object(deploy.os, 'geteuid', return_value=0), patch.object(deploy, 'acquire_lock', return_value=Mock()), patch.object(deploy, 'report_folder', return_value=root), patch.object(deploy, 'preflight', side_effect=RuntimeError('unfinished dpkg work')), patch.object(deploy, 'configure_ssh') as ssh, patch.object(deploy, 'diagnostics'), patch.object(deploy, 'hand_back'):
                self.assertEqual(deploy.main([]), 1)
                ssh.assert_not_called()
            self.assertIn('unfinished dpkg work', (root / 'target-summary.txt').read_text())

    def test_failed_ssh_attempts_config_and_service_restore(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / 'etc_ssh_sshd_config').write_text('old config')
            with patch.object(deploy, 'run', return_value=subprocess.CompletedProcess([], 0, 'active', '')) as command, patch.object(deploy, 'apply_ssh', side_effect=RuntimeError('restart failed')), patch.object(deploy.shutil, 'copy2') as copy:
                with self.assertRaisesRegex(RuntimeError, 'restart failed'):
                    deploy.configure_ssh([22], None, root)
                copy.assert_called_once_with(root / 'etc_ssh_sshd_config', '/etc/ssh/sshd_config')
                self.assertTrue(any(c.args == ('systemctl', 'start', 'ssh') for c in command.call_args_list))

    def test_recheck_does_not_configure_services(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            plan = root / 'plan.json'
            plan.write_text(json.dumps({'services': [{'service': 'ssh', 'port': 22}]}))
            with patch.object(deploy.os, 'geteuid', return_value=0), patch.object(deploy, 'acquire_lock', return_value=Mock()), patch.object(deploy, 'report_folder', return_value=root), patch.object(deploy, 'preflight'), patch.object(deploy, 'configure_ssh') as ssh, patch.object(deploy, 'check_local', return_value=[]), patch.object(deploy, 'diagnostics'), patch.object(deploy, 'hand_back'):
                self.assertEqual(deploy.main(['--check', str(plan)]), 0)
                ssh.assert_not_called()


if __name__ == '__main__':
    unittest.main()
