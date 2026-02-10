#!/usr/bin/env python3
"""
CTF RustyCurtain Deployer (FTP/Telnet/SSH) — clean, predictable, and testable.

What it does:
- Requires running as root (sudo).
- Clones/pulls https://github.com/jboyce1/ppsCTF.git into /home/<invoking_user>/ppsCTF
- Creates users: ivan, tanya, boris and sets passwords.
- Extracts ivan.zip -> /srv/ftp (anonymous FTP drop)
         tanya.zip -> /home/tanya/Desktop
         boris.zip -> /home/boris/Desktop
  Extraction avoids one-level "nesting folder" inside ZIPs.
- Installs/configures:
    vsftpd (anonymous read-only)
    xinetd + telnetd (telnet on port 23)
    openssh-server (password auth enabled)
- Prompts operator to set a NEW root password (local account)
- Explicitly disables SSH root login (PermitRootLogin no) so students can't SSH root.
- Verifies services are active.
"""

import os
import sys
import subprocess
import logging
import zipfile
import shutil
import getpass
from pathlib import Path

# -----------------------------------------------------------------------------
# Logging
# -----------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# -----------------------------------------------------------------------------
# Config
# -----------------------------------------------------------------------------
GITHUB_REPO_URL = "https://github.com/jboyce1/ppsCTF.git"

USERS = [
    {
        "username": "ivan",
        "password": "TheT3rrible",
        "zip_file": "ivan.zip",
        "extract_to": "/srv/ftp",                 # anonymous FTP drop
        "chown_recursive": False,                 # keep root:root
    },
    {
        "username": "tanya",
        "password": "L3tsG0",
        "zip_file": "tanya.zip",
        "extract_to": "/home/tanya/Desktop",      # telnet user drop
        "chown_recursive": True,
    },
    {
        "username": "boris",
        "password": "Pieinth3sky",
        "zip_file": "boris.zip",
        "extract_to": "/home/boris/Desktop",      # ssh user drop
        "chown_recursive": True,
    }
]

# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------
def run_command(command_list, check=True, capture_output=False, input_data=None, text=False):
    logging.debug("Running: %s", " ".join(command_list))
    return subprocess.run(
        command_list,
        check=check,
        capture_output=capture_output,
        input=input_data,
        text=text
    )

def require_root():
    if os.geteuid() != 0:
        logging.error("Run this script with sudo/root.")
        sys.exit(1)

def get_invoking_user_home():
    """
    When running under sudo, os.getlogin() can be flaky.
    Prefer SUDO_USER if available, else fallback to current.
    """
    sudo_user = os.environ.get("SUDO_USER")
    user = sudo_user if sudo_user else os.environ.get("USER") or "root"
    home = str(Path("~" + user).expanduser())
    return user, home

def clone_or_pull_repo(local_repo_path: str):
    if not os.path.isdir(local_repo_path):
        logging.info("Cloning %s -> %s", GITHUB_REPO_URL, local_repo_path)
        run_command(["git", "clone", GITHUB_REPO_URL, local_repo_path])
    else:
        logging.info("Repo exists at %s. Pulling latest...", local_repo_path)
        run_command(["git", "-C", local_repo_path, "pull"])

def user_exists(username: str) -> bool:
    try:
        run_command(["id", username], check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError:
        return False

def create_or_update_user(username: str, password: str):
    if not user_exists(username):
        logging.info("Creating user '%s'...", username)
        run_command(["useradd", "-m", "-s", "/bin/bash", username])
    else:
        logging.info("User '%s' exists. Skipping creation.", username)

    logging.info("Setting password for '%s'...", username)
    run_command(["chpasswd"], input_data=f"{username}:{password}\n".encode("utf-8"))

def ensure_directory(path: str):
    os.makedirs(path, exist_ok=True)

def extract_zip_flat_one_level(zip_path: str, dest_path: str):
    """
    Extract zip to dest_path, flattening a single top-level folder if present.
    - If zip contains a single top-level directory, its contents are moved into dest_path.
    - If zip contains multiple top-level items, they are moved into dest_path as-is.
    """
    if not os.path.isfile(zip_path):
        logging.error("ZIP not found: %s", zip_path)
        return False

    logging.info("Extracting %s -> %s", zip_path, dest_path)
    ensure_directory(dest_path)

    temp_dir = "/tmp/ctf_extract_temp"
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)

    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(temp_dir)

    # Determine top-level items
    top_items = os.listdir(temp_dir)
    if len(top_items) == 1 and os.path.isdir(os.path.join(temp_dir, top_items[0])):
        # Single folder nesting; move its contents up
        nested = os.path.join(temp_dir, top_items[0])
        for item in os.listdir(nested):
            shutil.move(os.path.join(nested, item), os.path.join(dest_path, item))
    else:
        # Move all top-level items directly
        for item in top_items:
            shutil.move(os.path.join(temp_dir, item), os.path.join(dest_path, item))

    shutil.rmtree(temp_dir)
    return True

def chown_recursive(path: str, user: str):
    run_command(["chown", "-R", f"{user}:{user}", path])

def prompt_set_root_password():
    logging.info("Rotate/Set the LOCAL root password (students should not know it).")
    pw1 = getpass.getpass("Enter NEW root password: ")
    pw2 = getpass.getpass("Confirm NEW root password: ")

    if not pw1:
        logging.error("Root password cannot be empty.")
        sys.exit(1)
    if pw1 != pw2:
        logging.error("Passwords do not match.")
        sys.exit(1)

    run_command(["chpasswd"], input_data=f"root:{pw1}\n".encode("utf-8"))
    logging.info("Root password updated.")

def write_file_backup_once(path: str, backup_path: str):
    if not os.path.isfile(backup_path):
        shutil.copyfile(path, backup_path)

def set_or_append_config_line(lines, key, value):
    """
    Replace existing key line (even if commented) or append if missing.
    """
    out = []
    found = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith(key) or stripped.startswith(f"#{key}"):
            out.append(f"{key} {value}\n")
            found = True
        else:
            out.append(line)
    if not found:
        out.append(f"{key} {value}\n")
    return out

# -----------------------------------------------------------------------------
# Services
# -----------------------------------------------------------------------------
def configure_vsftpd_anonymous():
    logging.info("Installing/configuring vsftpd (anonymous read-only FTP)...")
    run_command(["apt-get", "update"])
    run_command(["apt-get", "-y", "install", "vsftpd"])

    conf = "/etc/vsftpd.conf"
    bak = "/etc/vsftpd.conf.bak"
    write_file_backup_once(conf, bak)

    with open(bak, "r") as f:
        lines = f.readlines()

    # Force anonymous on; keep it simple
    # NOTE: we intentionally do not enable write.
    new_lines = []
    saw_anon = False
    for line in lines:
        if line.strip().startswith("anonymous_enable"):
            new_lines.append("anonymous_enable=YES\n")
            saw_anon = True
        else:
            new_lines.append(line)
    if not saw_anon:
        new_lines.append("anonymous_enable=YES\n")

    with open(conf, "w") as f:
        f.writelines(new_lines)

    # Ensure ftp root
    ensure_directory("/srv/ftp")
    run_command(["chown", "root:root", "/srv/ftp"])
    run_command(["chmod", "755", "/srv/ftp"])

    run_command(["systemctl", "enable", "vsftpd"])
    run_command(["systemctl", "restart", "vsftpd"])

def configure_telnet_xinetd():
    logging.info("Installing/configuring telnet via xinetd...")
    run_command(["apt-get", "update"])
    run_command(["apt-get", "-y", "install", "xinetd", "telnetd"])

    telnet_conf = "/etc/xinetd.d/telnet"
    if not os.path.isfile(telnet_conf):
        config_text = """# Telnet service via xinetd
service telnet
{
    disable         = no
    socket_type     = stream
    wait            = no
    user            = root
    log_on_failure  += USERID
    log_on_success  += USERID
    server          = /usr/sbin/in.telnetd
    bind            = 0.0.0.0
    port            = 23
}
"""
        with open(telnet_conf, "w") as f:
            f.write(config_text)

    run_command(["systemctl", "enable", "xinetd"])
    run_command(["systemctl", "restart", "xinetd"])

def configure_ssh_password_auth_and_disable_root_login():
    logging.info("Installing/configuring OpenSSH (password auth on, root SSH disabled)...")
    run_command(["apt-get", "update"])
    run_command(["apt-get", "-y", "install", "openssh-server"])

    conf = "/etc/ssh/sshd_config"
    bak = "/etc/ssh/sshd_config.bak"
    write_file_backup_once(conf, bak)

    with open(bak, "r") as f:
        lines = f.readlines()

    # Ensure password auth yes, explicitly block root SSH login
    lines = set_or_append_config_line(lines, "PasswordAuthentication", "yes")
    lines = set_or_append_config_line(lines, "PermitRootLogin", "no")

    with open(conf, "w") as f:
        f.writelines(lines)

    run_command(["systemctl", "enable", "ssh"])
    run_command(["systemctl", "restart", "ssh"])

def verify_service(service_name: str):
    try:
        res = run_command(["systemctl", "is-active", service_name], capture_output=True)
        status = res.stdout.decode().strip()
        if status == "active":
            logging.info("Service '%s' is active.", service_name)
        else:
            logging.warning("Service '%s' is NOT active (status=%s).", service_name, status)
    except subprocess.CalledProcessError:
        logging.error("Failed to verify service '%s'.", service_name)

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------
def main():
    require_root()

    invoking_user, invoking_home = get_invoking_user_home()
    local_repo_path = os.path.join(invoking_home, "ppsCTF")
    challenges_path = os.path.join(local_repo_path, "challenges", "rustycurtain")

    logging.info("Invoking user: %s", invoking_user)
    logging.info("Repo path: %s", local_repo_path)
    logging.info("Challenge ZIP path: %s", challenges_path)

    # 0) Prompt to rotate root password (local) and block root SSH regardless
    prompt_set_root_password()

    # 1) Clone or update repo
    clone_or_pull_repo(local_repo_path)

    # 2) Create/update users
    for u in USERS:
        create_or_update_user(u["username"], u["password"])

    # 3) Extract zips
    for u in USERS:
        zip_path = os.path.join(challenges_path, u["zip_file"])
        ok = extract_zip_flat_one_level(zip_path, u["extract_to"])
        if not ok:
            logging.warning("Skipping ownership for %s because extraction failed.", u["username"])
            continue

        if u["chown_recursive"]:
            chown_recursive(u["extract_to"], u["username"])
        else:
            # Keep /srv/ftp root-owned for anonymous FTP.
            run_command(["chown", "root:root", u["extract_to"]])
            run_command(["chmod", "755", u["extract_to"]])

    # 4) Configure services
    configure_vsftpd_anonymous()
    configure_telnet_xinetd()
    configure_ssh_password_auth_and_disable_root_login()

    # 5) Verify services
    verify_service("vsftpd")
    verify_service("xinetd")
    verify_service("ssh")

    logging.info("CTF environment setup complete.")
    logging.info("FTP: anonymous -> /srv/ftp")
    logging.info("Telnet: enabled on port 23 (use tanya creds)")
    logging.info("SSH: password auth enabled (use boris creds); root SSH disabled.")

if __name__ == "__main__":
    main()
