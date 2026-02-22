#!/usr/bin/env python3
"""
deploy-victim2.py  (boys: virgil1 + vinny2)

Run from:
  git clone https://github.com/jboyce1/ppsCTF.git && cd ppsCTF/challenges/cyberbully/ && sudo python3 deploy-victim2.py

Assumptions:
- You are currently in ppsCTF/challenges/cyberbully/
- The folder Victim2/ exists beside this script (tracked in git), with:
    Victim2/
      virgil1/
        icmp_broadcast_flag_victim.py
        tcp_broadcast_flag_pass_victim.py
        (copy 1).py backups (ignored)
      vinny2/
        Desktop/flag.txt

What this does:
- Installs required packages (scapy, nmap, netcat-openbsd, tcpdump, wireshark, etc.)
- Creates/updates users: virgil1, vinny2
- Locks down default 'ubuntu' user BEFORE enabling SSH password auth (prevents ubuntu:password)
- Enables SSH password auth (optional toggle)
- Copies Victim2/<user>/* into /home/<user>/
- Starts BOTH broadcasters (the *non-copy* scripts) in the background (no terminal hog)
  logging to:
    /home/virgil1/icmp_broadcast.log
    /home/virgil1/tcp_broadcast.log
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

# =========================
# CONFIG
# =========================
USER_CREDENTIALS = {
    "virgil1": "123213123",   # change if you want
    "vinny2": "vin4theWIN!",  # change if you want
}

# Run broadcasters automatically
RUN_ICMP_BROADCASTER = True
RUN_TCP_BROADCASTER  = True

# Enable password auth for SSH (we still deny ubuntu + allowlist only our users)
ENABLE_SSH_PASSWORD_AUTH = True

# Packages (netcat-openbsd + nmap are needed for your banner-verified host discovery)
APT_PACKAGES = [
    "python3-scapy",
    "tcpdump",
    "wireshark",
    "nmap",
    "netcat-openbsd",
    "openssh-server",
]

# Paths (relative to this deploy script location)
SCRIPT_DIR = Path(__file__).resolve().parent
VICTIM_DIR = SCRIPT_DIR / "Victim2"

# The scripts to run (NOT the copy backups)
ICMP_SCRIPT_DEST = "/home/virgil1/icmp_broadcast_flag_victim.py"
TCP_SCRIPT_DEST  = "/home/virgil1/tcp_broadcast_flag_pass_victim.py"

ICMP_LOG_PATH = "/home/virgil1/icmp_broadcast.log"
TCP_LOG_PATH  = "/home/virgil1/tcp_broadcast.log"


# =========================
# Helpers
# =========================
def run(cmd, check=True, capture=False, shell=False, env=None):
    if capture:
        return subprocess.run(cmd, check=check, text=True, capture_output=True, shell=shell, env=env)
    return subprocess.run(cmd, check=check, shell=shell, env=env)

def ensure_root():
    if os.geteuid() != 0:
        print("[!] Please run with sudo: sudo python3 deploy-victim2.py")
        sys.exit(1)

def user_exists(user: str) -> bool:
    r = run(["bash", "-lc", f"id -u {user} >/dev/null 2>&1"], check=False)
    return r.returncode == 0

def install_dependencies():
    print("[+] Installing required packages...")
    env = os.environ.copy()
    env["DEBIAN_FRONTEND"] = "noninteractive"
    run(["apt-get", "update"], env=env)
    run(["apt-get", "install", "-y", "--allow-change-held-packages", *APT_PACKAGES], env=env)
    print("[+] Dependencies installed successfully!")

def create_or_update_users():
    for user, password in USER_CREDENTIALS.items():
        if user_exists(user):
            print(f"[+] User exists: {user} (updating password + sudoers rule)")
        else:
            print(f"[+] Creating user: {user}")
            run(["useradd", "-m", "-s", "/bin/bash", user])

        run(["bash", "-lc", f"echo '{user}:{password}' | chpasswd"])

        # tcpdump sudo NOPASSWD (kept consistent with your earlier approach)
        sudoers_path = Path(f"/etc/sudoers.d/{user}")
        sudoers_path.write_text(f"{user} ALL=(ALL) NOPASSWD: /usr/sbin/tcpdump\n")
        run(["chmod", "440", str(sudoers_path)])

def setup_ssh_dirs():
    print("[+] Ensuring .ssh directories exist...")
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
    Prevent ubuntu default password logins before enabling PasswordAuthentication.
    """
    if user_exists("ubuntu"):
        print("[+] Locking default 'ubuntu' account password...")
        run(["passwd", "-l", "ubuntu"], check=False)

    allow_users = " ".join(USER_CREDENTIALS.keys())
    sshd_config = "/etc/ssh/sshd_config"

    print("[+] Updating sshd_config: DenyUsers ubuntu + AllowUsers our users...")

    run(["bash", "-lc",
         r"grep -qE '^\s*DenyUsers\s+.*\bubuntu\b' /etc/ssh/sshd_config || "
         r"echo 'DenyUsers ubuntu' >> /etc/ssh/sshd_config"
    ], check=False)

    run(["bash", "-lc",
         rf"if grep -qE '^\s*AllowUsers\s+' {sshd_config}; then "
         rf"  sed -i 's/^\s*AllowUsers\s\+.*/AllowUsers {allow_users}/' {sshd_config}; "
         rf"else "
         rf"  echo 'AllowUsers {allow_users}' >> {sshd_config}; "
         rf"fi"
    ], check=False)

def configure_ssh_password_authentication():
    if not ENABLE_SSH_PASSWORD_AUTH:
        print("[=] ENABLE_SSH_PASSWORD_AUTH=False, leaving PasswordAuthentication unchanged.")
        return

    print("[+] Enabling SSH password authentication (PasswordAuthentication yes)...")
    run(["bash", "-lc",
         r"if grep -qE '^\s*#?\s*PasswordAuthentication\s+' /etc/ssh/sshd_config; then "
         r"  sed -i 's/^\s*#\?\s*PasswordAuthentication\s\+.*/PasswordAuthentication yes/' /etc/ssh/sshd_config; "
         r"else "
         r"  echo 'PasswordAuthentication yes' >> /etc/ssh/sshd_config; "
         r"fi"
    ], check=False)

    run(["systemctl", "restart", "ssh"])
    print("[+] SSH restarted.")

def distribute_files():
    """
    Copy Victim2/<user>/* -> /home/<user>/
    Ignores your "(copy 1)" scripts automatically because we only run the non-copy names.
    """
    if not VICTIM_DIR.exists():
        raise RuntimeError(f"Victim2 directory not found: {VICTIM_DIR}")

    for user in USER_CREDENTIALS.keys():
        src = VICTIM_DIR / user
        dst = Path(f"/home/{user}")

        if not src.exists():
            print(f"[!] Missing source directory for {user}: {src}")
            continue
        if not dst.exists():
            print(f"[!] Missing destination directory for {user}: {dst}")
            continue

        print(f"[+] Copying files for {user}: {src} -> {dst}")
        for item in src.iterdir():
            target = dst / item.name
            if item.is_dir():
                shutil.copytree(item, target, dirs_exist_ok=True)
            else:
                shutil.copy2(item, target)

        run(["chown", "-R", f"{user}:{user}", str(dst)])

def start_background(script_path: str, log_path: str):
    sp = Path(script_path)
    if not sp.exists():
        raise RuntimeError(f"Broadcaster script not found: {script_path}")

    print(f"[+] Starting broadcaster in background: {script_path}")
    Path(log_path).parent.mkdir(parents=True, exist_ok=True)

    logf = open(log_path, "a", buffering=1)
    subprocess.Popen(
        ["python3", script_path],
        stdout=logf,
        stderr=logf,
        start_new_session=True,
        cwd=str(sp.parent)
    )
    print(f"[+] Logging to: {log_path}")

def main():
    ensure_root()

    install_dependencies()
    create_or_update_users()

    # SECURITY ORDER MATTERS
    lock_down_ubuntu_before_password_auth()
    configure_ssh_password_authentication()

    setup_ssh_dirs()
    distribute_files()

    # Start broadcasters (non-copy scripts only)
    if RUN_ICMP_BROADCASTER:
        start_background(ICMP_SCRIPT_DEST, ICMP_LOG_PATH)
    else:
        print("[=] RUN_ICMP_BROADCASTER=False (not starting ICMP)")

    if RUN_TCP_BROADCASTER:
        start_background(TCP_SCRIPT_DEST, TCP_LOG_PATH)
    else:
        print("[=] RUN_TCP_BROADCASTER=False (not starting TCP)")

    print("[✅] Victim2 setup complete!")
    print(f"    - Users: {', '.join(USER_CREDENTIALS.keys())}")
    print(f"    - ICMP log: {ICMP_LOG_PATH}")
    print(f"    - TCP  log: {TCP_LOG_PATH}")
    print("    - Backup scripts '(copy 1)' are present but NOT used.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[!] ERROR: {e}")
        sys.exit(1)
