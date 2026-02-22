#!/usr/bin/env python3
"""
deploy-victim1.py

Goal: From a fresh VM, you run:
  git clone https://github.com/jboyce1/ppsCTF.git && cd ppsCTF/challenges/cyberbully/ && sudo python3 deploy-victim1.py
Notes:
- This assumes Victim1.tar.gz contains:
    Victim1/
      vera1/icmp_broadcast_flag_victim.py
      vera1/tcp_broadcast_flag_pass_victim.py
      victoria2/...
- Broadcaster scripts should already include your port-22 SSH banner live-host discovery + 5-minute rescan logic.
"""
import os
import subprocess
import tarfile
import shutil
from pathlib import Path

# Configuration
TAR_FILE = "Victim1.tar.gz"          # Assumed to be in the same directory as the script
EXTRACT_PATH = os.getcwd()           # Extract in the current directory
EXTRACT_ROOT_DIRNAME = "Victim1"

USER_CREDENTIALS = {
    "vera1": "123213123",
    "victoria2": "V1ct0ry!"
}

UBUNTU_USER = "ubuntu"
DEFAULT_REPO_PATH = f"/home/{UBUNTU_USER}/ppsCTF"


def run(cmd, check=True, shell=False):
    return subprocess.run(cmd, check=check, shell=shell)


# ----------------------------
# Step 0: Secure ubuntu account (before SSH changes)
# ----------------------------
def secure_ubuntu_account():
    print("\n[!] Step 1: Set a NEW password for the 'ubuntu' account.")
    print("[!] Students should NOT know this password.\n")
    run(["sudo", "passwd", UBUNTU_USER], check=True)

    # If ubuntu has passwordless sudo entries in /etc/sudoers.d, convert NOPASSWD -> PASSWD (best effort)
    print("[+] Checking for passwordless sudo entries for ubuntu...")
    grep = subprocess.run(
        ["sudo", "grep", "-R", "-n", r"\bubuntu\b.*NOPASSWD", "/etc/sudoers.d"],
        capture_output=True,
        text=True
    )
    if grep.returncode == 0 and grep.stdout.strip():
        print("[!] Found NOPASSWD entries for ubuntu. Converting to PASSWD (with backups)...")
        for line in grep.stdout.strip().splitlines():
            file_path = line.split(":", 1)[0]
            run(["sudo", "cp", "-a", file_path, f"{file_path}.bak"], check=False)
            run(["sudo", "sed", "-i", "s/NOPASSWD:/PASSWD:/g", file_path], check=False)
        print("[+] Converted ubuntu NOPASSWD entries.")
    else:
        print("[+] No ubuntu NOPASSWD sudo entries found (good).")


# ----------------------------
# Install dependencies
# ----------------------------
def install_dependencies():
    print("[+] Installing required packages...")
    packages = ["python3-scapy", "tcpdump", "wireshark", "openssh-server"]
    run(["sudo", "apt-get", "update"], check=True)
    run(["sudo", "apt-get", "install", "-y"] + packages, check=True)
    print("[+] Dependencies installed successfully!")


# ----------------------------
# Extract tar
# ----------------------------
def extract_tar():
    print(f"[+] Extracting {TAR_FILE}...")
    if os.path.exists(TAR_FILE):
        with tarfile.open(TAR_FILE, "r:gz") as tar:
            tar.extractall(EXTRACT_PATH)
        print("[+] Extraction complete!")
    else:
        print(f"[!] ERROR: {TAR_FILE} not found!")
        raise SystemExit(1)


# ----------------------------
# Create users and set passwords
# ----------------------------
def create_users():
    for user, password in USER_CREDENTIALS.items():
        print(f"[+] Creating user: {user}")
        # useradd will fail if user exists; we allow that by check=False then ensure passwd is set
        run(["sudo", "useradd", "-m", "-s", "/bin/bash", user], check=False)
        run(f"echo '{user}:{password}' | sudo chpasswd", shell=True, check=True)

        # Allow tcpdump only (no full sudo). NOTE: tcpdump path is typically /usr/sbin/tcpdump on Ubuntu.
        sudoers_path = f"/etc/sudoers.d/{user}"
        sudoers_line = f"{user} ALL=(ALL) NOPASSWD: /usr/sbin/tcpdump\n"
        tmp = "/tmp/tcpdump_sudoers.tmp"
        with open(tmp, "w") as f:
            f.write(sudoers_line)
        run(["sudo", "mv", tmp, sudoers_path], check=True)
        run(["sudo", "chmod", "440", sudoers_path], check=True)


# ----------------------------
# Enable password authentication for SSH
# ----------------------------
def configure_ssh_password_authentication():
    print("[+] Enabling SSH password authentication...")
    run([
        "sudo", "sed", "-i",
        r's/^\s*#\?\s*PasswordAuthentication\s\+.*/PasswordAuthentication yes/',
        "/etc/ssh/sshd_config"
    ], check=True)

    # Ensure SSH is enabled and restarted
    run(["sudo", "systemctl", "enable", "--now", "ssh"], check=False)
    run(["sudo", "systemctl", "restart", "ssh"], check=True)

    print("[+] SSH password authentication enabled and SSH restarted.")


# ----------------------------
# Setup SSH dirs (optional, but keeps your structure consistent)
# ----------------------------
def setup_ssh():
    print("[+] Configuring SSH directories for all users...")
    for user in USER_CREDENTIALS.keys():
        ssh_dir = f"/home/{user}/.ssh"
        run(["sudo", "mkdir", "-p", ssh_dir], check=True)
        run(["sudo", "chmod", "700", ssh_dir], check=True)
        run(["sudo", "touch", f"{ssh_dir}/authorized_keys"], check=True)
        run(["sudo", "chmod", "600", f"{ssh_dir}/authorized_keys"], check=True)
        run(["sudo", "chown", "-R", f"{user}:{user}", ssh_dir], check=True)


# ----------------------------
# Distribute extracted files
# ----------------------------
def distribute_files():
    base_extracted_path = os.path.join(EXTRACT_PATH, EXTRACT_ROOT_DIRNAME)
    for user in USER_CREDENTIALS.keys():
        user_path = os.path.join(base_extracted_path, user)
        if os.path.exists(user_path):
            dest_path = f"/home/{user}"
            if os.path.exists(dest_path):
                print(f"[+] Copying files for {user}...")
                for item in os.listdir(user_path):
                    item_path = os.path.join(user_path, item)
                    if os.path.isdir(item_path):
                        shutil.copytree(item_path, os.path.join(dest_path, item), dirs_exist_ok=True)
                    else:
                        shutil.copy(item_path, os.path.join(dest_path, item))
                run(["sudo", "chown", "-R", f"{user}:{user}", dest_path], check=False)
                print(f"[+] Files copied for {user}")


# ----------------------------
# Permanently delete ppsCTF from ubuntu user's home
# ----------------------------
def delete_repo_from_ubuntu_home():
    """
    Deletes /home/ubuntu/ppsCTF (default). If that doesn't exist,
    attempts to infer repo root based on this script path.
    """
    candidates = []

    # Most common path when using your one-liner from /home/ubuntu
    candidates.append(Path(DEFAULT_REPO_PATH))

    # Fallback: infer repo root from script location: .../ppsCTF/challenges/.../deploy.py
    script_path = Path(__file__).resolve()
    for parent in script_path.parents:
        if parent.name == "ppsCTF":
            candidates.append(parent)
            break

    for p in candidates:
        try:
            if p.exists() and p.is_dir():
                print(f"[+] Deleting repo directory permanently: {p}")
                os.chdir("/")  # avoid deleting current working dir
                run(["sudo", "rm", "-rf", str(p)], check=False)
                print("[+] Repo deleted.")
                return
        except Exception:
            continue

    print("[!] Repo directory not found to delete (skipping).")


# ----------------------------
# Main
# ----------------------------
def main():
    # 1) Password change first (before SSH changes)
    secure_ubuntu_account()

    # 2) Now do installs + deploy
    install_dependencies()
    extract_tar()
    create_users()
    configure_ssh_password_authentication()
    setup_ssh()
    distribute_files()

    # 3) Remove repo (answer hygiene)
    delete_repo_from_ubuntu_home()

    print("[✅] Victim1 setup complete! Ready for CTF deployment.")


if __name__ == "__main__":
    main()
