#!/usr/bin/env python3
"""Offline asset checks and Ubuntu target deployment for Hamhunt v2.

Run with sudo on the assigned Ubuntu target; downloads and deployment are automatic.
Use --check without sudo to validate adjacent local ZIPs only.
Add --reset to end challenge-user sessions and restore a previous test run.
"""
import argparse
import grp
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import pwd
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import zipfile
import urllib.request

SCRIPT_DIR = Path(__file__).resolve().parent
ASSETS = SCRIPT_DIR
DOWNLOAD_URL = 'https://raw.githubusercontent.com/jboyce1/ppsCTF/main/challenges/hamhunt_v2'
STATE = Path('/var/lib/hamhunt_v2')
SSH_CONFIG = Path('/etc/ssh/sshd_config')
BEGIN = '# BEGIN HAMHUNT V2'
END = '# END HAMHUNT V2'
USERS = {'leroy': 'leroythehunt3r', 'mums_the_word': '0ink0INK!',
         'callsign_hambone': 'Her3piggyp1ggy'}
ADMIN = 'ubuntu'
ADMIN_PASSWORD = 'hamhunt'
SHA256 = {
    'leroy': '6e645fe21ebaa380a80f3cecf4d4b838e8e733b3ae36c89f12c0e247ba4335f2',
    'mums_the_word': 'af14ca11bf909a76c637d4acc86ca5e4819763f67b336b159fcd2c2c01e0e584',
    'callsign_hambone': '9bb44f9ecd7f0e748010351975a2ec45a17fe74cc2a2e3f724c6c9b9ae8f03f2',
}


def run(args, *, input=None, check=True):
    return subprocess.run(args, input=input, text=True, capture_output=True, check=check)


def prepare_assets():
    """Stage validated adjacent files or download missing files into a private cache."""
    global ASSETS
    STATE.mkdir(mode=0o700, parents=True, exist_ok=True)
    os.chmod(STATE, 0o700)
    ASSETS = STATE / 'downloads'
    ASSETS.mkdir(mode=0o700, exist_ok=True)
    os.chmod(ASSETS, 0o700)
    expected = {user + '.zip': digest for user, digest in SHA256.items()}
    expected['hamhunt_setup_guide.txt'] = None
    for name, digest in expected.items():
        destination = ASSETS / name
        local = SCRIPT_DIR / name
        if local.is_file() and (digest is None or hashlib.sha256(local.read_bytes()).hexdigest() == digest):
            if local.resolve() != destination.resolve():
                shutil.copyfile(local, destination)
            os.chmod(destination, 0o600)
            continue
        if destination.is_file() and (digest is None or hashlib.sha256(destination.read_bytes()).hexdigest() == digest):
            continue
        print('Downloading ' + name + ' ...', flush=True)
        temporary = None
        try:
            with tempfile.NamedTemporaryFile(prefix='download-', dir=ASSETS, delete=False) as output:
                temporary = Path(output.name)
                with urllib.request.urlopen(DOWNLOAD_URL + '/' + name, timeout=60) as response:
                    total = 0
                    while True:
                        chunk = response.read(1024 * 1024)
                        if not chunk:
                            break
                        total += len(chunk)
                        if total > 64 * 1024 * 1024:
                            raise ValueError(name + ': download is unexpectedly large')
                        output.write(chunk)
            if digest and hashlib.sha256(temporary.read_bytes()).hexdigest() != digest:
                raise ValueError(name + ': downloaded checksum does not match this installer')
            temporary.replace(destination)
        except OSError as error:
            raise RuntimeError(f'Could not download {name}: {error}. Publish the v2 files together first, '
                               'or copy the whole local v2 folder to the target for an unpublished test.') from error
        finally:
            if temporary and temporary.exists():
                temporary.unlink()
    print('Deployment files: ' + str(ASSETS), flush=True)


def checked_archives():
    """Verify provenance, safe paths, CRCs, all nine selection puzzles and the finale."""
    summary = {}
    for user in USERS:
        path = ASSETS / (user + '.zip')
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != SHA256[user]:
            raise ValueError(f'{path.name}: missing or different from the validated v2 asset')
        with zipfile.ZipFile(path) as z:
            if sum(i.file_size for i in z.infolist()) > 256 * 1024 * 1024:
                raise ValueError(f'{user}: archive expands beyond the expected size')
            for entry in z.infolist():
                parts = PurePosixPath(entry.filename).parts
                mode = entry.external_attr >> 16
                if ('\\' in entry.filename or not parts or parts[0] != user
                        or '..' in parts or stat.S_ISLNK(mode)
                        or (len(parts) > 1 and parts[1] != 'Desktop')
                        or (len(parts) == 1 and not entry.is_dir())):
                    raise ValueError(f'Unsafe archive entry: {entry.filename}')
            files = {i.filename: z.read(i) for i in z.infolist() if not i.is_dir()}
        if f'{user}/Desktop/flag.txt' not in files:
            raise ValueError(f'{user}: Desktop flag missing')
        for stage in (3, 4):
            readme = next(n for n in files if n.endswith(f'/mdx{stage}/0mdx{stage}_readme.txt'))
            target = re.search(r'[0-9a-f]{15,32}', files[readme].decode())[0]
            folder = readme.rsplit('/', 1)[0] + '/'
            matches = []
            for name, data in files.items():
                if name.startswith(folder) and name != readme:
                    digest = hashlib.md5(data).hexdigest()
                    if (digest == target if stage == 3 else target in digest):
                        matches.append(name)
            if len(matches) != 1:
                raise ValueError(f'{user}/mdx{stage}: expected one match, found {len(matches)}')
        known = next(n for n in files if n.endswith('/known_good_hashes.txt'))
        hashes = set(re.findall(rb'\b[0-9a-f]{32}\b', files[known]))
        folder = known.rsplit('/', 1)[0] + '/'
        unmatched = [n for n, data in files.items() if n.startswith(folder)
                     and n.rsplit('/', 1)[-1] not in {'known_good_hashes.txt', '0mdx5_readme.txt'}
                     and hashlib.md5(data).hexdigest().encode() not in hashes]
        if len(unmatched) != 1:
            raise ValueError(f'{user}/mdx5: expected one unmatched file, found {len(unmatched)}')
        if user == 'callsign_hambone':
            number = unmatched[0].rsplit('_', 1)[1]
            password = f'pps{{3x5_md5_{number}}}'.encode()
            nested = next(data for n, data in files.items() if n.endswith('/messages.yaml.zip'))
            with zipfile.ZipFile(io.BytesIO(nested)) as final:
                if not final.read('messages.yaml', pwd=password):
                    raise ValueError('Final message is empty')
        summary[user] = len(files)
    return summary


def existing_user(user):
    try:
        return pwd.getpwnam(user)
    except KeyError:
        return None


def preflight(reset):
    if os.geteuid() != 0:
        raise ValueError('Deploy with sudo from the ubuntu administrator account.')
    if os.environ.get('SUDO_USER') in USERS:
        raise ValueError('Use the ubuntu administrator, not a challenge account, for deployment.')
    admin = existing_user(ADMIN)
    if not admin or admin.pw_uid == 0:
        raise ValueError('Expected an existing non-root ubuntu administrator account.')
    if grp.getgrnam('sudo').gr_gid not in os.getgrouplist(ADMIN, admin.pw_gid):
        raise ValueError('ubuntu must already belong to sudo; its administrator access is preserved.')
    for user in USERS:
        entry = existing_user(user)
        home = Path('/home') / user
        if home.is_symlink() or (home.exists() and home.resolve() != home):
            raise ValueError(f'Refusing an unexpected home path: {home}')
        if entry:
            if entry.pw_uid < 1000 or entry.pw_uid == admin.pw_uid or entry.pw_dir != str(home):
                raise ValueError(f'Refusing to modify unexpected system/account identity: {user}')
            if not reset:
                raise ValueError(f'{user} already exists. Use --deploy --reset to restore this lab.')
        elif home.exists():
            raise ValueError(f'{home} exists without its account; inspect it before deployment.')
    missing = [cmd for cmd in ('sshd', 'sudo', 'useradd', 'usermod', 'chpasswd') if not shutil.which(cmd)]
    if missing:
        print('Installing missing target dependencies: ' + ', '.join(missing), flush=True)
        run(['apt-get', 'update'])
        run(['apt-get', 'install', '-y', 'openssh-server', 'sudo', 'passwd'])
    if not SSH_CONFIG.is_file():
        raise ValueError('The Ubuntu OpenSSH server configuration is missing.')
    for command in ('systemctl', 'ssh-keygen', 'sudo', 'visudo', 'sshd', 'useradd', 'usermod', 'chpasswd', 'pkill'):
        if not shutil.which(command):
            raise ValueError(f'Required target command is missing: {command}')
    run(['visudo', '-c'])
    if run(['sudo', '-l', '-U', ADMIN], check=False).returncode != 0:
        raise ValueError('ubuntu has no effective sudo grant; repair administrator access first.')
    STATE.mkdir(parents=True, exist_ok=True)
    os.chmod(STATE, 0o700)
    # Keep installer, passwords and all-account ZIPs outside students' reach.
    os.chmod(ASSETS, 0o700)


def remove_owned_path(path):
    if path.is_symlink() or path.is_file():
        path.unlink()
    elif path.exists():
        shutil.rmtree(path)


def install_accounts(stage, backup, reset):
    for user in USERS:
        entry = existing_user(user)
        if entry and reset:
            result = run(['pkill', '-KILL', '-u', str(entry.pw_uid)], check=False)
            if result.returncode not in (0, 1):
                raise ValueError(f'Could not end existing sessions for {user}')
        if not entry:
            run(['useradd', '-m', '-U', '-s', '/bin/bash', user])
        # Remove every supplementary group, including sudo/admin/docker/lxd.
        run(['usermod', '-G', '', '-s', '/bin/bash', user])
        entry = pwd.getpwnam(user)
        if set(os.getgrouplist(user, entry.pw_gid)) != {entry.pw_gid}:
            raise ValueError(f'{user}: supplementary groups remain')
        # Direct sudoers rules may exist from an older/custom deployment.
        if run(['sudo', '-l', '-U', user], check=False).returncode == 0:
            raise ValueError(f'{user} still has a direct sudoers grant. Remove it before continuing.')
        home = Path(entry.pw_dir)
        home.mkdir(mode=0o700, parents=True, exist_ok=True)
        os.chown(home, entry.pw_uid, entry.pw_gid)
        os.chmod(home, 0o700)
        desktop = home / 'Desktop'
        if desktop.exists() or desktop.is_symlink():
            if desktop.is_symlink():
                raise ValueError(f'Refusing a symlink Desktop for {user}')
            shutil.move(str(desktop), str(backup / (user + '-Desktop')))
        for name in ('.ssh', '.bash_history'):
            if reset:
                remove_owned_path(home / name)
        shutil.copytree(stage / user / 'Desktop', desktop)
        for parent, dirs, files in os.walk(desktop):
            os.chown(parent, entry.pw_uid, entry.pw_gid)
            os.chmod(parent, 0o755)
            for name in files:
                path = Path(parent) / name
                os.chown(path, entry.pw_uid, entry.pw_gid)
                os.chmod(path, 0o644)
    # chpasswd sets lab passwords as root; adduser's password flags are not used.
    run(['chpasswd'], input=''.join(f'{user}:{password}\n' for user, password in USERS.items()))
    os.chmod('/home', 0o755)


def ssh_text(original):
    if original.count(BEGIN) != original.count(END) or original.count(BEGIN) > 1:
        raise ValueError('Malformed existing Hamhunt SSH block; inspect sshd_config.')
    text = re.sub(re.escape(BEGIN) + r'.*?' + re.escape(END) + r'\n?', '', original, flags=re.S)
    return (text.rstrip() + '\n\n' + BEGIN + '\nMatch User ' + ','.join([*USERS, ADMIN])
            + '\n    PasswordAuthentication yes\n    PubkeyAuthentication yes'
            + '\n    AuthenticationMethods any\n' + END + '\n')


def configure_ssh(backup):
    original = SSH_CONFIG.read_bytes()
    shutil.copy2(SSH_CONFIG, backup / 'sshd_config')
    run(['ssh-keygen', '-A'])
    Path('/run/sshd').mkdir(mode=0o755, parents=True, exist_ok=True)
    try:
        SSH_CONFIG.write_text(ssh_text(original.decode()))
        run(['sshd', '-t', '-f', str(SSH_CONFIG)])
        for user in [*USERS, ADMIN]:
            result = run(['sshd', '-T', '-f', str(SSH_CONFIG), '-C',
                          f'user={user},host=localhost,addr=127.0.0.1'])
            values = dict(line.split(' ', 1) for line in result.stdout.splitlines() if ' ' in line)
            if (values.get('passwordauthentication') != 'yes'
                    or values.get('pubkeyauthentication') != 'yes'
                    or values.get('authenticationmethods') != 'any'):
                raise ValueError(f'{user}: an earlier SSH Match block conflicts with lab login settings')
        run(['systemctl', 'enable', 'ssh'])
        run(['systemctl', 'restart', 'ssh'])
        run(['systemctl', 'is-active', '--quiet', 'ssh'])
    except Exception:
        SSH_CONFIG.write_bytes(original)
        run(['systemctl', 'restart', 'ssh'], check=False)
        raise


def deploy(reset):
    preflight(reset)
    backup = Path(tempfile.mkdtemp(prefix='backup-', dir=STATE))
    with tempfile.TemporaryDirectory(prefix='stage-', dir=STATE) as temp:
        stage = Path(temp)
        for user in USERS:
            with zipfile.ZipFile(ASSETS / (user + '.zip')) as z:
                z.extractall(stage)  # Paths and symlinks were rejected by checked_archives.
        install_accounts(stage, backup, reset)
        configure_ssh(backup)
        run(['chpasswd'], input=f'{ADMIN}:{ADMIN_PASSWORD}\n')
    (STATE / 'last-deployment.json').write_text(json.dumps({'users': list(USERS), 'backup': str(backup)}, indent=2))
    print('\nDeployment complete. Student accounts have no sudo access.')
    print('Start students with: ssh leroy@ASSIGNED_TARGET_IP')
    print('Student starting password: ' + USERS['leroy'])
    print('Ubuntu administrator login: ubuntu')
    print('Ubuntu administrator password: ' + ADMIN_PASSWORD)
    print('Private backup directory: ' + str(backup))
    print('Verify remote SSH/SCP from Kali before handing out the target.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument('--check', action='store_true', help='validate local ZIPs and puzzles only; no target changes')
    modes.add_argument('--deploy', action='store_true', help='configure this Ubuntu target (default; requires sudo)')
    parser.add_argument('--reset', action='store_true', help='end lab-user sessions, restore Desktops/passwords and remove their SSH keys')
    args = parser.parse_args()
    if args.reset and args.check:
        parser.error('--reset cannot be combined with --check')
    args.deploy = not args.check
    os.environ['PATH'] = '/usr/sbin:/usr/bin:/sbin:/bin:' + os.environ.get('PATH', '')
    try:
        if args.deploy:
            if os.geteuid() != 0 or os.environ.get('SUDO_USER') in USERS:
                raise ValueError('Run this installer with sudo from the ubuntu administrator account.')
            prepare_assets()
        summary = checked_archives()
        print('ZIP integrity, all nine hash-selection puzzles, and final-message decryption: PASS', flush=True)
        print('Files per account: ' + ', '.join(f'{u}={count}' for u, count in summary.items()), flush=True)
        if args.deploy:
            deploy(args.reset)
        else:
            print('Check only: no accounts, passwords, filesystems, packages or SSH settings changed.')
        return 0
    except subprocess.CalledProcessError as error:
        # Never echo the chpasswd input containing passwords in error output.
        print(f'ERROR: {error.cmd[0]} failed (exit {error.returncode}).', file=sys.stderr)
        if error.stderr:
            print(error.stderr.strip(), file=sys.stderr)
    except (OSError, ValueError, KeyError, zipfile.BadZipFile, RuntimeError) as error:
        print('ERROR: ' + str(error), file=sys.stderr)
    if args.deploy:
        print('Deployment is incomplete. Inspect the error; after correcting it, rerun with --reset.', file=sys.stderr)
        print('Requested Ubuntu administrator password: ' + ADMIN_PASSWORD, file=sys.stderr)
    return 1


if __name__ == '__main__':
    sys.exit(main())
