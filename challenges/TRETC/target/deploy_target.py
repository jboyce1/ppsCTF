#!/usr/bin/env python3
import os
import pwd
import shutil
import subprocess
import sys
from pathlib import Path

# ---- TARGET CONFIG (keep stable; change for new targets if needed) ----
TARGET_USER = "jake"
TARGET_PASS = "stagecrew"

PROFILE_DIR = ".target_profile"
PROFILE_DESKTOP_SUBDIR = "Desktop"
PROFILE_FTP_SUBDIR = "BuriedTreasure"

FTP_ROOT = Path("/srv/ftp")
VSFTPD_CONF = Path("/etc/vsftpd.conf")
# ----------------------------------------------------------------------


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def run_shell(cmd: str) -> None:
    subprocess.run(cmd, shell=True, check=True)


def user_exists(username: str) -> bool:
    try:
        pwd.getpwnam(username)
        return True
    except KeyError:
        return False


def ensure_target_user() -> None:
    if not user_exists(TARGET_USER):
        print("[*] Creating target user")
        run(["useradd", "-m", "-s", "/bin/bash", TARGET_USER])
    else:
        print("[*] Target user already exists")

    # Set/Reset password (quietly)
    p = subprocess.run(["chpasswd"], input=f"{TARGET_USER}:{TARGET_PASS}\n".encode(), check=True)
    _ = p

    # Make the target user sudo-capable (your “root-like” requirement)
    run(["usermod", "-aG", "sudo", TARGET_USER])


def ensure_desktop_deploy(profile_root: Path) -> None:
    src_desktop = profile_root / PROFILE_DESKTOP_SUBDIR
    if not src_desktop.exists() or not src_desktop.is_dir():
        raise SystemExit(f"ERROR: Missing required folder: {src_desktop}")

    dest_desktop = Path(f"/home/{TARGET_USER}/Desktop")
    dest_desktop.mkdir(parents=True, exist_ok=True)

    print("[*] Deploying target Desktop content")

    # Copy contents of src Desktop into target Desktop (not nested)
    for item in src_desktop.iterdir():
        dest = dest_desktop / item.name
        if dest.exists():
            if dest.is_dir():
                shutil.rmtree(dest)
            else:
                dest.unlink()
        if item.is_dir():
            shutil.copytree(item, dest)
        else:
            shutil.copy2(item, dest)

    # Ownership: user owns their desktop
    run(["chown", "-R", f"{TARGET_USER}:{TARGET_USER}", str(dest_desktop)])


def install_vsftpd() -> None:
    print("[*] Installing vsftpd (if needed)")
    run(["apt-get", "update"])
    run(["apt-get", "install", "-y", "vsftpd"])


def configure_vsftpd_anonymous() -> None:
    if not VSFTPD_CONF.exists():
        raise SystemExit("ERROR: /etc/vsftpd.conf not found (vsftpd install failed?)")

    # Read-only anonymous FTP rooted at /srv/ftp
    conf = f"""\
listen=YES
listen_ipv6=NO

anonymous_enable=YES
local_enable=NO
write_enable=NO

anon_root={FTP_ROOT}

# Safety / stability
dirmessage_enable=YES
use_localtime=YES
xferlog_enable=YES
connect_from_port_20=YES
secure_chroot_dir=/var/run/vsftpd/empty
pam_service_name=vsftpd
rsa_cert_file=/etc/ssl/certs/ssl-cert-snakeoil.pem
rsa_private_key_file=/etc/ssl/private/ssl-cert-snakeoil.key

# Reduce “who owns this file” noise
hide_ids=YES
"""

    print("[*] Configuring vsftpd for anonymous FTP")
    VSFTPD_CONF.write_text(conf)


def deploy_ftp_treasure(profile_root: Path) -> None:
    src_treasure = profile_root / PROFILE_FTP_SUBDIR
    if not src_treasure.exists() or not src_treasure.is_dir():
        raise SystemExit(f"ERROR: Missing required folder: {src_treasure}")

    print("[*] Deploying FTP")

    FTP_ROOT.mkdir(parents=True, exist_ok=True)

    # Clear existing FTP root contents (only within /srv/ftp)
    for item in FTP_ROOT.iterdir():
        if item.is_dir():
            shutil.rmtree(item)
        else:
            item.unlink()

    # Copy treasure contents into /srv/ftp (not nested)
    for item in src_treasure.iterdir():
        dest = FTP_ROOT / item.name
        if item.is_dir():
            shutil.copytree(item, dest)
        else:
            shutil.copy2(item, dest)

    # Permissions: anonymous must be able to read directories/files
    run(["chown", "-R", "root:root", str(FTP_ROOT)])
    run_shell(f"chmod -R a+rX '{FTP_ROOT}'")


def restart_vsftpd() -> None:
    print("[*] Restarting vsftpd")
    run(["systemctl", "enable", "--now", "vsftpd"])
    run(["systemctl", "restart", "vsftpd"])


def ensure_ssh_access() -> None:
    # Keep this minimal but deterministic.
    print("[*] Ensuring SSH password authentication is enabled")
    run_shell("sed -i 's/^#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config")
    run_shell("sed -i 's/^PasswordAuthentication no/PasswordAuthentication yes/' /etc/ssh/sshd_config")
    run_shell("systemctl restart ssh || service ssh restart")


def main() -> None:
    if os.geteuid() != 0:
        print("ERROR: Run this script with sudo (sudo python3 deploy_target.py)")
        sys.exit(1)

    profile_root = Path.cwd() / PROFILE_DIR
    if not profile_root.exists() or not profile_root.is_dir():
        print(f"ERROR: Expected ./{PROFILE_DIR} next to deploy_target.py")
        sys.exit(1)

    ensure_target_user()
    ensure_ssh_access()
    ensure_desktop_deploy(profile_root)

    install_vsftpd()
    configure_vsftpd_anonymous()
    deploy_ftp_treasure(profile_root)
    restart_vsftpd()

    print("[+] target deployment complete")


if __name__ == "__main__":
    main()
