#!/usr/bin/env python3
import os
import sys
import tarfile
import shutil
import subprocess
import tempfile
import time
from pathlib import Path

TAR_FILE = "Bully2.tar.gz"
EXTRACT_ROOT_DIRNAME = "Bully2"

USER_CREDENTIALS = {
    "becky1": "b3ki-b33n-b@@@d",
    "betty2": "123123123"
}

BULLY_USER = "becky1"
BULLY_SCRIPT = f"/home/{BULLY_USER}/tcp_udp_icmp_cyberbully.py"
CONF_PATH = f"/home/{BULLY_USER}/.cyberbully.conf"
LOG_PATH = f"/home/{BULLY_USER}/.cyberbully.log"
PID_PATH = f"/home/{BULLY_USER}/.cyberbully.pid"

APT_LOCKS = [
    "/var/lib/dpkg/lock-frontend",
    "/var/lib/dpkg/lock",
    "/var/cache/apt/archives/lock",
    "/var/lib/apt/lists/lock",
]

# ----------------------------
# Helpers
# ----------------------------
def run(cmd, check=True, shell=False, env=None):
    return subprocess.run(cmd, check=check, shell=shell, env=env)

def user_exists(username: str) -> bool:
    r = subprocess.run(["id", "-u", username], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return r.returncode == 0

def is_locked() -> bool:
    for lf in APT_LOCKS:
        r = subprocess.run(["sudo", "fuser", lf], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if r.returncode == 0:
            return True
    return False

def wait_for_apt(timeout_sec=600):
    """
    Wait for apt/dpkg locks. On Kali, unattended upgrades / apt timers often hold locks.
    We wait, and if still locked, we stop the common services/timers once.
    """
    start = time.time()
    attempted_stop = False

    while is_locked():
        if time.time() - start > timeout_sec:
            raise RuntimeError("Timed out waiting for apt/dpkg locks.")

        if not attempted_stop:
            attempted_stop = True
            # Stop common background apt jobs on Kali/Debian.
            run(["sudo", "systemctl", "stop", "unattended-upgrades"], check=False)
            run(["sudo", "systemctl", "stop", "apt-daily.service", "apt-daily-upgrade.service"], check=False)
            run(["sudo", "systemctl", "stop", "packagekit.service"], check=False)
            # Stop timers so they don't restart immediately
            run(["sudo", "systemctl", "stop", "apt-daily.timer", "apt-daily-upgrade.timer"], check=False)

        print("[*] Waiting for apt/dpkg lock to clear...")
        time.sleep(2)

    # If a background apt run was interrupted, make sure dpkg isn't half-configured.
    run(["sudo", "dpkg", "--configure", "-a"], check=False)
    run(["sudo", "apt-get", "-f", "install", "-y"], check=False)

def apt_install(packages: list[str]):
    """
    Non-interactive install:
    - Keeps existing config files if prompted
    - Avoids curses prompt hangs
    """
    env = os.environ.copy()
    env["DEBIAN_FRONTEND"] = "noninteractive"

    # Update
    wait_for_apt()
    run(["sudo", "apt-get", "update"], check=True, env=env)

    # Install with dpkg options to prevent interactive prompts
    wait_for_apt()
    cmd = [
        "sudo", "apt-get", "install", "-y",
        "-o", "Dpkg::Options::=--force-confold",
        "-o", "Dpkg::Options::=--force-confdef",
    ] + packages
    run(cmd, check=True, env=env)

# ----------------------------
# Steps
# ----------------------------
def install_dependencies_and_enable_ssh():
    print("[+] Installing required packages and enabling SSH...")
    packages = ["python3-scapy", "tcpdump", "iftop", "nmap", "openssh-server"]
    apt_install(packages)

    # Enable/start SSH (Kali service usually "ssh")
    run(["sudo", "systemctl", "enable", "--now", "ssh"], check=False)
    run(["sudo", "systemctl", "restart", "ssh"], check=False)

    print("[+] Dependencies installed; SSH enabled.")

def secure_kali_account():
    print("\n[!] Step 1: Set a NEW password for the 'kali' account.")
    print("[!] Students should NOT know this password.\n")

    # Interactive prompt (intended)
    run(["sudo", "passwd", "kali"])

    # Convert any NOPASSWD for kali in /etc/sudoers.d (best effort)
    print("[+] Checking for passwordless sudo entries for kali...")
    try:
        grep = subprocess.run(
            ["sudo", "grep", "-R", "-n", r"\bkali\b.*NOPASSWD", "/etc/sudoers.d"],
            capture_output=True,
            text=True,
            check=False
        )
        if grep.returncode == 0 and grep.stdout.strip():
            print("[!] Found NOPASSWD entries for kali. Converting to PASSWD...")
            for line in grep.stdout.strip().splitlines():
                file_path = line.split(":", 1)[0]
                run(["sudo", "cp", "-a", file_path, f"{file_path}.bak"], check=False)
                run(["sudo", "sed", "-i", "s/NOPASSWD:/PASSWD:/g", file_path], check=False)
            print("[+] Converted kali NOPASSWD entries (backups saved as *.bak).")
        else:
            print("[+] No kali NOPASSWD sudo entries found (good).")
    except Exception:
        print("[!] Could not scan /etc/sudoers.d for NOPASSWD entries (continuing).")

def extract_tar_to_temp(script_dir: Path) -> Path:
    tar_path = script_dir / TAR_FILE
    if not tar_path.exists():
        print(f"[!] ERROR: {TAR_FILE} not found in {script_dir}")
        sys.exit(1)

    tmpdir = Path(tempfile.mkdtemp(prefix="bully2_extract_"))
    print(f"[+] Extracting {tar_path} to {tmpdir} ...")

    with tarfile.open(tar_path, "r:gz") as tar:
        tar.extractall(tmpdir)

    extracted_root = tmpdir / EXTRACT_ROOT_DIRNAME
    if not extracted_root.is_dir():
        print(f"[!] ERROR: Expected '{EXTRACT_ROOT_DIRNAME}/' inside tar, but not found.")
        print("[!] Ensure tar contains Bully2/becky1/... and Bully2/betty2/...")
        sys.exit(1)

    print("[+] Extraction complete.")
    return extracted_root

def create_users_no_sudo():
    print("[+] Creating users (NO sudo for students)...")
    for user, password in USER_CREDENTIALS.items():
        if not user_exists(user):
            run(["sudo", "useradd", "-m", "-s", "/bin/bash", user], check=True)

        run(f"echo '{user}:{password}' | sudo chpasswd", shell=True, check=True)

        # Ensure they are not sudoers; also remove any leftover sudoers file.
        run(["sudo", "deluser", user, "sudo"], check=False)
        run(["sudo", "rm", "-f", f"/etc/sudoers.d/{user}"], check=False)

    print("[+] Users ready.")

def setup_ssh_dirs():
    print("[+] Setting up SSH directories...")
    for user in USER_CREDENTIALS.keys():
        ssh_dir = Path(f"/home/{user}/.ssh")
        run(["sudo", "mkdir", "-p", str(ssh_dir)], check=True)
        run(["sudo", "chmod", "700", str(ssh_dir)], check=True)
        run(["sudo", "touch", str(ssh_dir / "authorized_keys")], check=True)
        run(["sudo", "chmod", "600", str(ssh_dir / "authorized_keys")], check=True)
        run(["sudo", "chown", "-R", f"{user}:{user}", str(ssh_dir)], check=True)
    print("[+] SSH dirs set.")

def distribute_files(extracted_root: Path):
    print("[+] Distributing extracted files into home directories...")
    for user in USER_CREDENTIALS.keys():
        src = extracted_root / user
        dst = Path(f"/home/{user}")

        if not src.exists():
            print(f"[!] WARNING: Missing content for {user} at {src}")
            continue

        for item in src.iterdir():
            dst_item = dst / item.name
            if item.is_dir():
                shutil.copytree(item, dst_item, dirs_exist_ok=True)
            else:
                shutil.copy2(item, dst_item)

        run(["sudo", "chown", "-R", f"{user}:{user}", str(dst)], check=True)

    print("[+] Files copied.")

def prompt_for_victim_ip() -> str:
    ip = input("\n[?] Step 2: Enter the VICTIM IP address for the cyberbully broadcaster: ").strip()
    if not ip:
        print("[!] ERROR: victim IP cannot be blank.")
        sys.exit(1)
    return ip

def write_config(victim_ip: str):
    print(f"[+] Writing config to {CONF_PATH} ...")
    conf_text = f"""# Cyberbully traffic generator config
victim_ip={victim_ip}
tcp_port=31337
udp_port=31337
interval=2
behavior=1
# message=uncomment to override rotation
"""
    tmp = Path(tempfile.mkstemp(prefix="cyberbully_conf_", text=True)[1])
    tmp.write_text(conf_text, encoding="utf-8")

    run(["sudo", "mv", str(tmp), CONF_PATH], check=True)
    run(["sudo", "chown", f"{BULLY_USER}:{BULLY_USER}", CONF_PATH], check=True)
    run(["sudo", "chmod", "600", CONF_PATH], check=True)

def start_broadcaster_background():
    print("[+] Starting broadcaster in background (NOT systemd)...")

    # Stop previous instance if PID file exists
    stop_cmd = f"""
set -e
if [ -f "{PID_PATH}" ]; then
  pid="$(cat "{PID_PATH}" 2>/dev/null || true)"
  if [ -n "$pid" ] && kill -0 "$pid" 2>/dev/null; then
    kill "$pid" 2>/dev/null || true
    sleep 1
  fi
  rm -f "{PID_PATH}"
fi
"""
    run(["sudo", "bash", "-lc", stop_cmd], check=False)

    # Sanity: ensure bully script exists
    exists_cmd = f'test -f "{BULLY_SCRIPT}"'
    r = subprocess.run(["sudo", "bash", "-lc", exists_cmd])
    if r.returncode != 0:
        print(f"[!] ERROR: bully script not found at {BULLY_SCRIPT}")
        sys.exit(1)

    # Start new instance as becky1; log + pid file
    start_cmd = f"""
set -e
nohup /usr/bin/python3 "{BULLY_SCRIPT}" --config "{CONF_PATH}" >> "{LOG_PATH}" 2>&1 &
echo $! > "{PID_PATH}"
"""
    run(["sudo", "-u", BULLY_USER, "bash", "-lc", start_cmd], check=True)

    # Lock down permissions
    run(["sudo", "chown", f"{BULLY_USER}:{BULLY_USER}", LOG_PATH, PID_PATH], check=False)
    run(["sudo", "chmod", "600", PID_PATH], check=False)
    run(["sudo", "chmod", "644", LOG_PATH], check=False)

    print(f"[+] Broadcaster running. PID file: {PID_PATH}")
    print(f"[+] Log file: {LOG_PATH}")

def remove_repo_self_destruct():
    script_path = Path(__file__).resolve()
    repo_root = script_path.parents[2]  # cyberbully -> challenges -> ppsCTF
    print(f"[+] Removing repo directory to prevent answer leakage: {repo_root}")

    os.chdir("/")
    run(["sudo", "rm", "-rf", str(repo_root)], check=False)

def main():
    script_dir = Path(__file__).resolve().parent

    install_dependencies_and_enable_ssh()
    secure_kali_account()

    extracted_root = extract_tar_to_temp(script_dir)
    create_users_no_sudo()
    setup_ssh_dirs()
    distribute_files(extracted_root)

    victim_ip = prompt_for_victim_ip()
    write_config(victim_ip)
    start_broadcaster_background()

    # Clean temp extraction dir
    try:
        shutil.rmtree(extracted_root.parent, ignore_errors=True)
    except Exception:
        pass

    remove_repo_self_destruct()

    print("\n[✅] Bully2 deployed.\n")
    print("Useful commands:")
    print(f"  Tail bully log:   sudo tail -f {LOG_PATH}")
    print(f"  Check PID:        sudo cat {PID_PATH}")
    print(f"  Stop bully:       sudo kill $(cat {PID_PATH})")
    print(f"  Change IP live:   sudo nano {CONF_PATH}   (script reloads automatically)")
    print(f"  Restart bully:    sudo kill $(cat {PID_PATH}) && sudo -u {BULLY_USER} nohup python3 {BULLY_SCRIPT} --config {CONF_PATH} >> {LOG_PATH} 2>&1 &")

if __name__ == "__main__":
    main()
