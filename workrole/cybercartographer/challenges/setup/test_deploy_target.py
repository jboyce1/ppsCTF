"""No packages installed and no host services changed by these tests."""
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

spec = importlib.util.spec_from_file_location('deploy', Path(__file__).resolve().parents[1] / 'flagscripts/deploy-target.py')
deploy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(deploy)


class DeployTests(unittest.TestCase):
    def test_recipe_matrix_dispatches_correct_ports_modes_and_flags(self):
        cases = [
            (['148', '', 'y'], [22], (21, 'pps{1x3_ftp0rt#21}', 'anonymous'), [(23, 'pps{1x8_telnetp0rt#23}')]),
            (['248', '', 'y'], [23344], (21, 'pps{1x3_ftp0rt#21}', 'anonymous'), [(23, 'pps{1x8_telnetp0rt#23}')]),
            (['259', 'both', 'y', 'y'], [23344], (23345, 'pps{1x3_ftp0rt#23345}', 'both'), [(23346, 'pps{1x9_telnetp0rt#23346}')]),
            (['136', 'both', 'y'], [22], (21, None, 'both'), [(23, None)]),
            (['136', 'user', 'y'], [22], (21, None, 'user'), [(23, None)]),
            (['128', 'y'], [22, 23344], None, [(23, 'pps{1x8_telnetp0rt#23}')]),
        ]
        for answers, ssh_ports, ftp_args, telnet_specs in cases:
            with self.subTest(recipe=answers), tempfile.TemporaryDirectory() as folder:
                root = Path(folder)
                with patch('builtins.input', side_effect=answers), patch.object(deploy.os, 'geteuid', return_value=0), patch.object(deploy, 'acquire_lock', return_value=Mock()), patch.object(deploy, 'report_folder', return_value=root), patch.object(deploy, 'preflight'), patch.object(deploy, 'high_port', side_effect=[23344, 23345, 23346]), patch.object(deploy, 'configure_ssh', return_value=[]) as ssh, patch.object(deploy, 'configure_ftp', return_value=[]) as ftp, patch.object(deploy, 'configure_telnet', return_value=[]) as telnet, patch.object(deploy, 'check_local', side_effect=lambda entries: [dict(service=e['service'], port=e['port'], status='PASS', detail='test') for e in entries]), patch.object(deploy, 'diagnostics'), patch.object(deploy, 'machine_addresses', return_value=['10.15.1.144']), patch.object(deploy, 'hand_back'):
                    self.assertEqual(deploy.main([]), 0)
                self.assertEqual(ssh.call_args.args[0], ssh_ports)
                if ftp_args:
                    self.assertEqual(ftp.call_args.args[:3], ftp_args)
                else:
                    ftp.assert_not_called()
                self.assertEqual(telnet.call_args.args[0], telnet_specs)
                self.assertIn('10.15.1.144', (root / 'inventory.txt').read_text())
                self.assertTrue((root / 'validation-handoff.txt').exists())

    def test_handoff_fills_in_high_port_user_ip_and_path(self):
        entries = [{'service': 'ssh', 'port': 23344}]
        checks = [{'service': 'ssh', 'port': 23344, 'status': 'PASS'}]
        with patch.dict(deploy.os.environ, {'SUDO_USER': 'ubuntu'}), patch.object(deploy.pwd, 'getpwnam', return_value=SimpleNamespace(pw_uid=1000)):
            text = deploy.validation_handoff(entries, checks, ['10.15.1.144'], Path('/home/ubuntu/Desktop/report folder'))
        command = next(line for line in text.splitlines() if line.startswith('scp '))
        self.assertEqual(deploy.shlex.split(command), ['scp', '-P', '23344', 'ubuntu@10.15.1.144:/home/ubuntu/Desktop/report folder/expectations.json', './expectations.json'])
        self.assertIn('python3 validate-target.py --expect expectations.json', text)

    def test_handoff_prefers_standard_ssh_and_handles_ipv6(self):
        entries = [{'service': 'ssh', 'port': p} for p in (23344, 22)]
        checks = [dict(service='ssh', port=e['port'], status='PASS') for e in entries]
        with patch.dict(deploy.os.environ, {'SUDO_USER': 'kali'}), patch.object(deploy.pwd, 'getpwnam', return_value=SimpleNamespace(pw_uid=1000)):
            text = deploy.validation_handoff(entries, checks, ['2001:db8::1'], Path('/tmp/report'))
        command = next(line for line in text.splitlines() if line.startswith('scp '))
        self.assertEqual(deploy.shlex.split(command)[1:4], ['-P', '22', 'kali@[2001:db8::1]:/tmp/report/expectations.json'])

    def test_handoff_uses_fileshare_when_ssh_failed_or_user_is_root(self):
        entries = [{'service': 'ssh', 'port': 22}]
        checks = [{'service': 'ssh', 'port': 22, 'status': 'FAIL'}]
        self.assertIn('classroom fileshare', deploy.validation_handoff(entries, checks, ['10.15.1.144'], Path('/tmp/report')))
        checks[0]['status'] = 'PASS'
        with patch.dict(deploy.os.environ, {'SUDO_USER': 'root'}), patch.object(deploy.pwd, 'getpwnam', return_value=SimpleNamespace(pw_uid=0)):
            self.assertIn('No invoking non-root username', deploy.validation_handoff(entries, checks, ['10.15.1.144'], Path('/tmp/report')))

    def test_inventory_has_ip_ports_access_and_all_flags(self):
        entries = [
            {'service': 'ssh', 'port': 23344, 'user_login': True},
            {'service': 'ftp', 'port': 21, 'anonymous': True, 'user_login': False, 'flag': 'pps{ftp_flag}'},
            {'service': 'telnet', 'port': 23, 'flag': 'pps{telnet_flag}'},
        ]
        checks = [dict(service=e['service'], port=e['port'], status='PASS') for e in entries]
        text = deploy.inventory_summary(entries, checks, ['10.15.1.144'], [])
        for expected in ('10.15.1.144', '23344', '21', '23', 'anonymous', 'pps{ftp_flag}', 'pps{telnet_flag}'):
            self.assertIn(expected, text)
        rows = [line for line in text.splitlines() if line.startswith(('SSH ', 'FTP ', 'TELNET '))]
        self.assertEqual(len(rows), 3)
        self.assertTrue(all('PASS' in row for row in rows))

    def test_inventory_does_not_claim_failed_setup_passed(self):
        entries = [{'service': 'ssh', 'port': 22}]
        checks = [{'service': 'ssh', 'port': 22, 'status': 'PASS'}]
        text = deploy.inventory_summary(entries, checks, [], ['ssh: FAILED / INCOMPLETE — restart failed'])
        self.assertIn('SETUP FAILED', text)
        self.assertIn('UNKNOWN', text)
        self.assertIn('NOT CHECKED', deploy.inventory_summary(entries, [], [], []))

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
