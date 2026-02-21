#!/usr/bin/env python3
"""
deploy-victim1.py

Goal: From a fresh VM, you run:
  git clone https://github.com/jboyce1/ppsCTF.git && cd ppsCTF/challenges/cyberbully/ && sudo python3 deploy-victim1.py

…and it will:
  1) install required dependencies (including netcat-openbsd + nmap for banner-verified scanning)
  2) extract Victim1.tar.gz (assumed to be in this same directory)
  3) create users + set passwords (idempotent)
  4) lock down default 'ubuntu' account BEFORE enabling SSH password auth
  5) enable SSH password auth (if desired)
  6) distribute files into /home/<user>/
  7) optionally start BOTH broadcaster scripts in the background (no terminal hog)
     - logs to /home/vera1/icmp_broadcast.log and /home/vera1/tcp_broadcast.log

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
import sys
from pathlib import Path

# =========================
# CONFIG
# =========================
TAR_FILE = "Victim1.tar.gz"                      # must be in same dir as this script
SCRIPT_DIR = Path(__file__).resolve().parent
EXTRACT_PATH = SCRIPT_DIR                        # extract into the challenge dir (so Victim1/ appears here)

USER_CREDENTIALS = {
    "vera1": "123213123",
    "victoria2": "V1ct0ry!"
}

# Toggle running broadcasters automatically
RUN_ICMP_BROADCASTER = True
RUN_TCP_BROADCASTER = True

# Where the broadcaster scripts should end up after distribute_files()
ICMP_SCRIPT_PATH = "/home/vera1/icmp_broadcast_flag_victim.py"
TCP_SCRIPT_PATH  = "/home/vera1/tcp_broadcast_flag_pass_victim.py"

ICMP_LOG_PATH = "/home/vera1/icmp_broadcast.log"
TCP_LOG_PATH  = "/home/vera1/tcp_broadcast.log"

# Packages: include netcat-openbsd + nmap so the broadcaster scripts' banner verification always works.
APT_PACKAGES = [
    "python3-scapy",
    "tcpdump",
    "wireshark",
    "nmap",
    "netcat-openbsd",
    "openssh-server",
]

# If you want password auth enabled, leave True.
# If you only want password auth for your created users (and not ubuntu), we allowlist users and deny ubuntu below.
ENABLE_SSH_PASSWORD_AUTH = True

# =========================
# Helpers
# =========================
def run(cmd, check=True, capture=False, shell=False, env=None):
    if capture:
        return subprocess.run(cmd, check=check, text=True, capture_output=True, shell=shell, env=env)
    return subprocess.run(cmd, check=check, shell=shell, env=env)

def ensure_root():
    if os.geteuid() != 0:
        print("[!] Please run with sudo: sudo python3 deploy-victim1.py")
        sys.exit(1)

def install_dependencies():
    print("[+] Installing required packages...")
    env = os.environ.copy()
    env["DEBIAN_FRONTEND"] = "noninteractive"
    run(["apt-get", "update"], env=env)
    run(["apt-get", "install", "-y", "--allow-change-held-packages", *APT_PACKAGES], env=env)
    print("[+] Dependencies installed successfully!")

def extract_tar():
    tar_path = SCRIPT_DIR / TAR_FILE
    print(f"[+] Extracting {tar_path} -> {EXTRACT_PATH} ...")
    if tar_path.exists():
        with tarfile.open(tar_path, "r:gz") as tar:
            tar.extractall(str(EXTRACT_PATH))
        print("[+] Extraction complete!")
    else:
        print(f"[!] ERROR: {tar_path} not found!")
        sys.exit(1)

def user_exists(user: str) -> bool:
    r = run(["bash", "-lc", f"id -u {user} >/dev/null 2>&1"], check=False)
    return r.returncode == 0

def create_or_update_users():
    for user, password in USER_CREDENTIALS.items():
        if user_exists(user):
            print(f"[+] User exists: {user} (updating password + sudoers rule)")
        else:
            print(f"[+] Creating user: {user}")
            run(["useradd", "-m", "-s", "/bin/bash", user])

        # set password
        run(["bash", "-lc", f"echo '{user}:{password}' | chpasswd"])

        # Grant sudo privileges for tcpdump to both users (idempotent)
        sudoers_path = Path(f"/etc/sudoers.d/{user}")
        sudoers_content = f"{user} ALL=(ALL) NOPASSWD: /usr/sbin/tcpdump\n"
        sudoers_path.write_text(sudoers_content)
        run(["chmod", "440", str(sudoers_path)])

def setup_ssh_dirs():
    print("[+] Ensuring .ssh directories exist (safe scaffolding)...")
    for user in USER_CREDENTIALS.keys():
        ssh_dir = Path(f"/home/{user}/.ssh")
        ssh_dir.mkdir(parents=True, exist_ok=True)
        run(["chmod", "700", str(ssh_dir)])
        ak = ssh_dir / "authorized_keys"
        ak.touch(exist_ok=True)
        run(["chmod", "600", str(ak)])
        run(["chown", "-R", f"{user}:{user}", str(ssh_dir)])

def lock_down_ubuntu_before_password_auth():
    """
    Critical: prevent "ubuntu:password" (or any default ubuntu password) from being usable.
    Do this BEFORE enabling PasswordAuthentication and restarting ssh.
    """
    if user_exists("ubuntu"):
        print("[+] Locking default 'ubuntu' account password...")
        run(["passwd", "-l", "ubuntu"], check=False)

    # Hard deny ubuntu over SSH, and allow only our users.
    allow_users = " ".join(USER_CREDENTIALS.keys())
    sshd_config = "/etc/ssh/sshd_config"

    print("[+] Updating sshd_config: DenyUsers ubuntu + AllowUsers <our users> ...")

    # Ensure DenyUsers ubuntu exists
    run(["bash", "-lc",
         r"grep -qE '^\s*DenyUsers\s+.*\bubuntu\b' /etc/ssh/sshd_config || "
         r"echo 'DenyUsers ubuntu' >> /etc/ssh/sshd_config"
    ], check=False)

    # Set/replace AllowUsers line
    run(["bash", "-lc",
         rf"if grep -qE '^\s*AllowUsers\s+' {sshd_config}; then "
         rf"  sed -i 's/^\s*AllowUsers\s\+.*/AllowUsers {allow_users}/' {sshd_config}; "
         rf"else "
         rf"  echo 'AllowUsers {allow_users}' >> {sshd_config}; "
         rf"fi"
    ], check=False)

def configure_ssh_password_authentication():
    if not ENABLE_SSH_PASSWORD_AUTH:
        print("[=] ENABLE_SSH_PASSWORD_AUTH=False, leaving sshd_config unchanged for PasswordAuthentication.")
        return

    print("[+] Enabling SSH password authentication (PasswordAuthentication yes)...")
    # Replace existing line or add if missing (idempotent)
    run(["bash", "-lc",
         r"if grep -qE '^\s*#?\s*PasswordAuthentication\s+' /etc/ssh/sshd_config; then "
         r"  sed -i 's/^\s*#\?\s*PasswordAuthentication\s\+.*/PasswordAuthentication yes/' /etc/ssh/sshd_config; "
         r"else "
         r"  echo 'PasswordAuthentication yes' >> /etc/ssh/sshd_config; "
         r"fi"
    ], check=False)

    run(["systemctl", "restart", "ssh"])
    print("[+] SSH password authentication enabled and SSH service restarted.")

def distribute_files():
    """
    Copy extracted Victim1/<user>/* into /home/<user>/
    """
    base_extracted_path = EXTRACT_PATH / "Victim1"
    if not base_extracted_path.exists():
        raise RuntimeError(f"Expected extracted folder not found: {base_extracted_path}")

    for user in USER_CREDENTIALS.keys():
        user_path = base_extracted_path / user
        dest_path = Path(f"/home/{user}")

        if user_path.exists() and dest_path.exists():
            print(f"[+] Copying files for {user}...")
            for item in user_path.iterdir():
                target = dest_path / item.name
                if item.is_dir():
                    shutil.copytree(item, target, dirs_exist_ok=True)
                else:
                    shutil.copy2(item, target)
            run(["chown", "-R", f"{user}:{user}", str(dest_path)])
            print(f"[+] Files copied for {user}")
        else:
            print(f"[!] Skipping {user}: source or destination missing ({user_path} -> {dest_path})")

def start_background(script_path: str, log_path: str):
    """
    Run a script detached so it doesn't hog a terminal.
    Uses start_new_session=True so it survives terminal logout.
    """
    sp = Path(script_path)
    if not sp.exists():
        raise RuntimeError(f"Broadcaster script not found: {script_path}")

    print(f"[+] Starting broadcaster: {script_path}")
    os.makedirs(str(Path(log_path).parent), exist_ok=True)

    logf = open(log_path, "a", buffering=1)
    subprocess.Popen(
        ["python3", script_path],
        stdout=logf,
        stderr=logf,
        start_new_session=True,
        cwd=str(Path(script_path).parent)
    )
    print(f"[+] Logging to: {log_path}")

def main():
    ensure_root()

    install_dependencies()
    extract_tar()
    create_or_update_users()

    # SECURITY ORDER MATTERS:
    # lock down ubuntu BEFORE enabling password auth
    lock_down_ubuntu_before_password_auth()

    configure_ssh_password_authentication()
    setup_ssh_dirs()
    distribute_files()

    # Start broadcasters (optional toggles)
    if RUN_ICMP_BROADCASTER:
        start_background(ICMP_SCRIPT_PATH, ICMP_LOG_PATH)
    else:
        print("[=] RUN_ICMP_BROADCASTER=False (not starting ICMP)")

    if RUN_TCP_BROADCASTER:
        start_background(TCP_SCRIPT_PATH, TCP_LOG_PATH)
    else:
        print("[=] RUN_TCP_BROADCASTER=False (not starting TCP)")

    print("[✅] Victim1 setup complete!")
    print(f"    - Users: {', '.join(USER_CREDENTIALS.keys())}")
    print(f"    - ICMP log: {ICMP_LOG_PATH}")
    print(f"    - TCP  log: {TCP_LOG_PATH}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[!] ERROR: {e}")
        sys.exit(1)
