#!/usr/bin/env python3
import os
import sys
import tarfile
import shutil
import subprocess
import tempfile
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

def run(cmd, check=True, shell=False):
    return subprocess.run(cmd, check=check, shell=shell)

def user_exists(username: str) -> bool:
    r = subprocess.run(["id", "-u", username], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return r.returncode == 0

def install_dependencies_and_enable_ssh():
    print("[+] Installing required packages and enabling SSH...")
    packages = ["python3-scapy", "tcpdump", "iftop", "nmap", "openssh-server"]
    run(["sudo", "apt-get", "update"])
    run(["sudo", "apt-get", "install", "-y"] + packages)

    # Enable/start SSH (service name on kali is typically "ssh")
    run(["sudo", "systemctl", "enable", "--now", "ssh"], check=False)
    run(["sudo", "systemctl", "restart", "ssh"], check=False)

    print("[+] Dependencies installed; SSH enabled.")

def secure_kali_account():
    print("\n[!] Step 1: Set a NEW password for the 'kaliu' account.")
    print("[!] Students should NOT know this password.\n")

    # Interactive prompt
    run(["sudo", "passwd", "kali"])

    # If this box came from a cloud image, kali might have NOPASSWD in /etc/sudoers.d
    # We'll try to convert any kali NOPASSWD entries to PASSWD safely.
    print("[+] Checking for passwordless sudo entries for kali...")
    try:
        grep = subprocess.run(
            ["sudo", "grep", "-R", "-n", r"kali.*NOPASSWD", "/etc/sudoers.d"],
            capture_output=True,
            text=True,
            check=False
        )
        if grep.returncode == 0 and grep.stdout.strip():
            print("[!] Found potential NOPASSWD sudo entries for kali. Converting to PASSWD...")
            # For each hit, replace NOPASSWD: with PASSWD:
            for line in grep.stdout.strip().splitlines():
                file_path = line.split(":", 1)[0]
                # backup once per file
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
            run(["sudo", "useradd", "-m", "-s", "/bin/bash", user])
        # set password
        run(f"echo '{user}:{password}' | sudo chpasswd", shell=True)

        # ensure they are not sudoers
        run(["sudo", "deluser", user, "sudo"], check=False)
        run(["sudo", "rm", "-f", f"/etc/sudoers.d/{user}"], check=False)

    print("[+] Users ready.")

def setup_ssh_dirs():
    print("[+] Setting up SSH directories...")
    for user in USER_CREDENTIALS.keys():
        ssh_dir = Path(f"/home/{user}/.ssh")
        run(["sudo", "mkdir", "-p", str(ssh_dir)])
        run(["sudo", "chmod", "700", str(ssh_dir)])
        run(["sudo", "touch", str(ssh_dir / "authorized_keys")])
        run(["sudo", "chmod", "600", str(ssh_dir / "authorized_keys")])
        run(["sudo", "chown", "-R", f"{user}:{user}", str(ssh_dir)])
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

        run(["sudo", "chown", "-R", f"{user}:{user}", str(dst)])

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
message=you dont belong here
"""
    tmp = Path(tempfile.mkstemp(prefix="cyberbully_conf_", text=True)[1])
    tmp.write_text(conf_text, encoding="utf-8")

    run(["sudo", "mv", str(tmp), CONF_PATH])
    run(["sudo", "chown", f"{BULLY_USER}:{BULLY_USER}", CONF_PATH])
    run(["sudo", "chmod", "600", CONF_PATH])

def start_broadcaster_background():
    print("[+] Starting broadcaster in background (NOT systemd)...")
    # Stop previous instance if PID file exists and process is alive
    stop_cmd = f"""
if [ -f "{PID_PATH}" ]; then
  pid=$(cat "{PID_PATH}" 2>/dev/null || true)
  if [ -n "$pid" ] && kill -0 "$pid" 2>/dev/null; then
    kill "$pid" 2>/dev/null || true
    sleep 1
  fi
  rm -f "{PID_PATH}"
fi
"""
    run(["sudo", "bash", "-lc", stop_cmd], check=False)

    # Start new instance as becky1; log + pidfile owned by becky1
    start_cmd = f"""
nohup /usr/bin/python3 "{BULLY_SCRIPT}" --config "{CONF_PATH}" >> "{LOG_PATH}" 2>&1 &
echo $! > "{PID_PATH}"
"""
    run(["sudo", "-u", BULLY_USER, "bash", "-lc", start_cmd], check=True)

    # lock down log/pid permissions
    run(["sudo", "chown", f"{BULLY_USER}:{BULLY_USER}", LOG_PATH, PID_PATH], check=False)
    run(["sudo", "chmod", "600", PID_PATH], check=False)
    run(["sudo", "chmod", "644", LOG_PATH], check=False)

    print(f"[+] Broadcaster running. PID file: {PID_PATH}")
    print(f"[+] Log file: {LOG_PATH}")

def remove_repo_self_destruct():
    # Determine repo root: .../ppsCTF/challenges/cyberbully/deploy-bully2.py -> parents[2] == ppsCTF
    script_path = Path(__file__).resolve()
    repo_root = script_path.parents[2]  # cyberbully -> challenges -> ppsCTF
    print(f"[+] Removing repo directory to prevent answer leakage: {repo_root}")

    # Move out of repo before deleting
    os.chdir("/")

    # Use sudo rm -rf (safer than shutil when permissions vary)
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

    print("\n[✅] Bully2 deployed.")
    print("\nUseful commands:")
    print(f"  Tail bully log:   sudo tail -f {LOG_PATH}")
    print(f"  Check PID:        sudo cat {PID_PATH}")
    print(f"  Stop bully:       sudo kill $(cat {PID_PATH})")
    print(f"  Change IP live:   sudo nano {CONF_PATH}   (script reloads automatically)")
    print(f"  Restart bully:    sudo kill $(cat {PID_PATH}) && sudo -u {BULLY_USER} nohup python3 {BULLY_SCRIPT} --config {CONF_PATH} >> {LOG_PATH} 2>&1 &")

if __name__ == "__main__":
    main()
