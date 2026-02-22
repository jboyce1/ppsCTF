#!/usr/bin/env python3
import os
import sys
import tarfile
import shutil
import subprocess
import tempfile
import time
from pathlib import Path

# ----------------------------
# Configuration
# ----------------------------
TAR_FILE = "Bully3.tar.gz"
EXTRACT_ROOT_DIRNAME = "Bully3"

USER_CREDENTIALS = {
    "bekah1": "the-BIG-b@b00n!",
    "brenda2": "123123123",
}

KALI_USER = "kali"

BRENDA_HOME = "/home/brenda2"
BEKAH_HOME = "/home/bekah1"

BULLY_SCRIPT = f"{BRENDA_HOME}/tcp_udp_icmp_cyberbully.py"
TCP_MONITOR  = f"{BRENDA_HOME}/tcp_monitor.py"
MEM_MONITOR  = f"{BRENDA_HOME}/memory_monitor.py"

# Victim2 IP config file (one line with IP)
# IMPORTANT: bully runs as root now, but we still keep config in brenda2's home
VICTIM_CONF_BRENDA = f"{BRENDA_HOME}/.victim2.conf"

# Background run state
STATE_DIR = f"{BRENDA_HOME}/.bully3"
LOG_BULLY = f"{STATE_DIR}/cyberbully.log"
LOG_TCP   = f"{STATE_DIR}/tcp_monitor.log"
LOG_MEM   = f"{STATE_DIR}/memory_monitor.log"
PID_BULLY = f"{STATE_DIR}/cyberbully.pid"
PID_TCP   = f"{STATE_DIR}/tcp_monitor.pid"
PID_MEM   = f"{STATE_DIR}/memory_monitor.pid"

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
    start = time.time()
    attempted_stop = False
    while is_locked():
        if time.time() - start > timeout_sec:
            raise RuntimeError("Timed out waiting for apt/dpkg locks.")
        if not attempted_stop:
            attempted_stop = True
            # stop common culprits (Kali)
            run(["sudo", "systemctl", "stop", "unattended-upgrades"], check=False)
            run(["sudo", "systemctl", "stop", "apt-daily.service", "apt-daily-upgrade.service"], check=False)
            run(["sudo", "systemctl", "stop", "packagekit.service"], check=False)
            run(["sudo", "systemctl", "stop", "apt-daily.timer", "apt-daily-upgrade.timer"], check=False)
        print("[*] Waiting for apt/dpkg lock to clear...")
        time.sleep(2)

    # repair partial dpkg state if any
    run(["sudo", "dpkg", "--configure", "-a"], check=False)
    run(["sudo", "apt-get", "-f", "install", "-y"], check=False)

def apt_install(packages):
    env = os.environ.copy()
    env["DEBIAN_FRONTEND"] = "noninteractive"

    wait_for_apt()
    run(["sudo", "apt-get", "update"], check=True, env=env)

    wait_for_apt()
    cmd = [
        "sudo", "apt-get", "install", "-y",
        "-o", "Dpkg::Options::=--force-confold",
        "-o", "Dpkg::Options::=--force-confdef",
    ] + packages
    run(cmd, check=True, env=env)

def secure_kali_password_first():
    print("\n[!] Step 1: Set a NEW password for the 'kali' account (students should NOT know it).")
    run(["sudo", "passwd", KALI_USER], check=True)

    print("[+] Checking for passwordless sudo entries for kali...")
    grep = subprocess.run(
        ["sudo", "grep", "-R", "-n", r"\bkali\b.*NOPASSWD", "/etc/sudoers.d"],
        capture_output=True, text=True, check=False
    )
    if grep.returncode == 0 and grep.stdout.strip():
        print("[!] Found NOPASSWD entries for kali. Converting to PASSWD (with backups)...")
        for line in grep.stdout.strip().splitlines():
            file_path = line.split(":", 1)[0]
            run(["sudo", "cp", "-a", file_path, f"{file_path}.bak"], check=False)
            run(["sudo", "sed", "-i", "s/NOPASSWD:/PASSWD:/g", file_path], check=False)
        print("[+] Converted kali NOPASSWD entries.")
    else:
        print("[+] No kali NOPASSWD sudo entries found (good).")

def install_deps_enable_ssh_restrict_users():
    print("[+] Installing required packages and enabling SSH...")
    packages = [
        "openssh-server",
        "python3-scapy",
        "python3-psutil",
        "tcpdump",
        "iftop",
        "nmap",
    ]
    apt_install(packages)

    run(["sudo", "systemctl", "enable", "--now", "ssh"], check=False)

    # Restrict SSH to ONLY bekah1
    sshd = "/etc/ssh/sshd_config"
    run(["sudo", "cp", "-a", sshd, f"{sshd}.bak"], check=False)
    run(["sudo", "sed", "-i", r"/^\s*AllowUsers\s\+/d", sshd], check=False)
    run(["sudo", "bash", "-lc", f"echo 'AllowUsers bekah1' | sudo tee -a {sshd} >/dev/null"], check=False)
    run(["sudo", "sed", "-i", r"s/^\s*#\?\s*PasswordAuthentication\s\+.*/PasswordAuthentication yes/", sshd], check=False)

    # Recommended: disable root SSH just in case
    run(["sudo", "sed", "-i", r"s/^\s*#\?\s*PermitRootLogin\s\+.*/PermitRootLogin no/", sshd], check=False)

    run(["sudo", "systemctl", "restart", "ssh"], check=True)
    print("[+] SSH enabled and restricted to: bekah1")

def extract_tar_to_temp(script_dir: Path) -> Path:
    tar_path = script_dir / TAR_FILE
    if not tar_path.exists():
        print(f"[!] ERROR: {TAR_FILE} not found in {script_dir}")
        sys.exit(1)

    tmpdir = Path(tempfile.mkdtemp(prefix="bully3_extract_"))
    print(f"[+] Extracting {tar_path} to {tmpdir} ...")
    with tarfile.open(tar_path, "r:gz") as tar:
        tar.extractall(tmpdir)

    extracted_root = tmpdir / EXTRACT_ROOT_DIRNAME
    if not extracted_root.is_dir():
        print(f"[!] ERROR: Expected '{EXTRACT_ROOT_DIRNAME}/' inside tar, but not found.")
        sys.exit(1)

    print("[+] Extraction complete.")
    return extracted_root

def create_users():
    print("[+] Creating users...")
    for user, password in USER_CREDENTIALS.items():
        if not user_exists(user):
            run(["sudo", "useradd", "-m", "-s", "/bin/bash", user], check=True)
        run(f"echo '{user}:{password}' | sudo chpasswd", shell=True, check=True)

    # Remove sudo privileges if any
    for user in USER_CREDENTIALS.keys():
        run(["sudo", "deluser", user, "sudo"], check=False)
        run(["sudo", "rm", "-f", f"/etc/sudoers.d/{user}"], check=False)

    # Prevent brenda2 interactive logins
    run(["sudo", "usermod", "-s", "/usr/sbin/nologin", "brenda2"], check=False)
    run(["sudo", "passwd", "-l", "brenda2"], check=False)

    print("[+] Users ready. brenda2 login disabled.")

def setup_ssh_dirs():
    print("[+] Creating SSH dirs for bekah1...")
    user = "bekah1"
    ssh_dir = Path(f"/home/{user}/.ssh")
    run(["sudo", "mkdir", "-p", str(ssh_dir)], check=True)
    run(["sudo", "chmod", "700", str(ssh_dir)], check=True)
    run(["sudo", "touch", str(ssh_dir / "authorized_keys")], check=True)
    run(["sudo", "chmod", "600", str(ssh_dir / "authorized_keys")], check=True)
    run(["sudo", "chown", "-R", f"{user}:{user}", str(ssh_dir)], check=True)

def distribute_files(extracted_root: Path):
    print("[+] Distributing files to /home/<user> ...")
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

        run(["sudo", "chown", "-R", f"{user}:{user}", str(dst)], check=False)

    # OPTIONAL: remove bekah Desktop .storage if present (you can remove this if you still want it)
    storage = Path(f"{BEKAH_HOME}/Desktop/.storage")
    if storage.exists():
        run(["sudo", "rm", "-rf", str(storage)], check=False)

    print("[+] File distribution complete.")

def prompt_for_victim2_ip() -> str:
    ip = input("\n[?] Enter victim2 IP address (Vinny/Virgil target): ").strip()
    if not ip:
        print("[!] ERROR: victim2 IP cannot be blank.")
        sys.exit(1)
    return ip

def write_victim_conf(victim_ip: str):
    tmp = Path(tempfile.mkstemp(prefix="victim2_", text=True)[1])
    tmp.write_text(victim_ip + "\n", encoding="utf-8")

    run(["sudo", "mv", str(tmp), VICTIM_CONF_BRENDA], check=True)
    run(["sudo", "chown", "brenda2:brenda2", VICTIM_CONF_BRENDA], check=False)
    # readable by root (for bully) and brenda2 (for monitors). no need for bekah1.
    run(["sudo", "chmod", "600", VICTIM_CONF_BRENDA], check=False)

def ensure_state_dir():
    run(["sudo", "mkdir", "-p", STATE_DIR], check=True)
    run(["sudo", "chown", "-R", "brenda2:brenda2", STATE_DIR], check=False)
    run(["sudo", "chmod", "700", STATE_DIR], check=False)

def stop_if_running(pid_path: str):
    stop_cmd = f"""
if [ -f "{pid_path}" ]; then
  pid="$(cat "{pid_path}" 2>/dev/null || true)"
  if [ -n "$pid" ] && kill -0 "$pid" 2>/dev/null; then
    kill "$pid" 2>/dev/null || true
    sleep 1
  fi
  rm -f "{pid_path}"
fi
"""
    run(["sudo", "bash", "-lc", stop_cmd], check=False)

def start_bg_as_user(username: str, script_path: str, pid_path: str, log_path: str):
    stop_if_running(pid_path)
    start_cmd = f"""
set -e
nohup /usr/bin/python3 "{script_path}" >> "{log_path}" 2>&1 &
echo $! > "{pid_path}"
"""
    run(["sudo", "-u", username, "bash", "-lc", start_cmd], check=True)
    run(["sudo", "chown", f"{username}:{username}", pid_path, log_path], check=False)
    run(["sudo", "chmod", "600", pid_path], check=False)
    run(["sudo", "chmod", "644", log_path], check=False)

def start_bg_as_root(script_path: str, pid_path: str, log_path: str):
    stop_if_running(pid_path)
    start_cmd = f"""
set -e
nohup /usr/bin/python3 "{script_path}" >> "{log_path}" 2>&1 &
echo $! > "{pid_path}"
"""
    run(["sudo", "bash", "-lc", start_cmd], check=True)
    # keep state owned by brenda2 so you can manage it easily
    run(["sudo", "chown", "brenda2:brenda2", pid_path, log_path], check=False)
    run(["sudo", "chmod", "600", pid_path], check=False)
    run(["sudo", "chmod", "644", log_path], check=False)

def start_all():
    print("[+] Starting bully + monitors (background, not systemd)...")
    ensure_state_dir()

    # Sanity checks
    for p in [BULLY_SCRIPT, TCP_MONITOR, MEM_MONITOR]:
        if not Path(p).exists():
            print(f"[!] ERROR: missing expected script: {p}")
            sys.exit(1)

    # IMPORTANT:
    # - bully runs as root (Scapy/raw sockets)
    # - monitors run as brenda2 (no SSH access)
    start_bg_as_root(BULLY_SCRIPT, PID_BULLY, LOG_BULLY)
    start_bg_as_user("brenda2", TCP_MONITOR, PID_TCP, LOG_TCP)
    start_bg_as_user("brenda2", MEM_MONITOR, PID_MEM, LOG_MEM)

    print("[+] Running:")
    print(f"    cyberbully (root): {PID_BULLY} -> {LOG_BULLY}")
    print(f"    tcp_monitor:       {PID_TCP} -> {LOG_TCP}")
    print(f"    mem_monitor:       {PID_MEM} -> {LOG_MEM}")

def remove_repo_self_destruct():
    # deploy-bully3.py is in: .../ppsCTF/challenges/cyberbully/
    script_path = Path(__file__).resolve()
    repo_root = script_path.parents[2]  # cyberbully -> challenges -> ppsCTF
    print(f"[+] Removing repo directory permanently: {repo_root}")
    os.chdir("/")
    run(["sudo", "rm", "-rf", str(repo_root)], check=False)

def main():
    script_dir = Path(__file__).resolve().parent

    secure_kali_password_first()
    install_deps_enable_ssh_restrict_users()

    extracted_root = extract_tar_to_temp(script_dir)
    create_users()
    setup_ssh_dirs()
    distribute_files(extracted_root)

    victim_ip = prompt_for_victim2_ip()
    write_victim_conf(victim_ip)

    start_all()

    # cleanup extraction tempdir
    try:
        shutil.rmtree(extracted_root.parent, ignore_errors=True)
    except Exception:
        pass

    remove_repo_self_destruct()

    print("\n[✅] Bully3 deployed.\n")
    print("Student access:")
    print("  SSH allowed ONLY for: bekah1")
    print("\nQuick checks:")
    print(f"  Bully log:  sudo tail -n 50 {LOG_BULLY}")
    print(f"  PIDs:       sudo ls -l {STATE_DIR}/*.pid")
    print("\nStop all:")
    print(f"  sudo kill $(cat {PID_BULLY}) $(cat {PID_TCP}) $(cat {PID_MEM})")

if __name__ == "__main__":
    main()
