#!/usr/bin/env python3
import os
import random
import re
import shutil
import subprocess
import sys
from pathlib import Path

UBU = "ubuntu"
UBU_HOME = Path("/home/ubuntu")
UBU_SSH = UBU_HOME / ".ssh"
UBU_DESKTOP = UBU_HOME / "Desktop"
FLAG_PATH = UBU_DESKTOP / "flag.txt"

SALT_ALPHABET = "abcdefghijklmnopqrstuvwxyz0123456789"
FLAG_PREFIX = "pps{Ladder_"


def run(cmd, check=True, capture=False):
    if isinstance(cmd, str):
        raise ValueError("run expects a list")
    kwargs = {}
    if capture:
        kwargs.update({"stdout": subprocess.PIPE, "stderr": subprocess.PIPE, "text": True})
    p = subprocess.run(cmd, **kwargs)
    if check and p.returncode != 0:
        err = ""
        if capture and p.stderr:
            err = "\n" + p.stderr.strip()
        raise RuntimeError(f"Command failed ({p.returncode}): {' '.join(cmd)}{err}")
    return p


def run_as_ubuntu(cmd, check=True):
    return run(["sudo", "-u", UBU] + cmd, check=check)


def is_ip(s: str) -> bool:
    s = s.strip()
    m = re.fullmatch(r"(?:\d{1,3}\.){3}\d{1,3}", s)
    if not m:
        return False
    parts = [int(x) for x in s.split(".")]
    return all(0 <= x <= 255 for x in parts)


def gen_flag() -> str:
    salt_len = random.randint(5, 8)
    salt = "".join(random.choice(SALT_ALPHABET) for _ in range(salt_len))
    return f"{FLAG_PREFIX}{salt}}}"


def set_password_auth(enable: bool):
    value = "yes" if enable else "no"
    # matches your working sed style; no \s
    run(["sudo", "sed", "-i",
         rf"s/^#\?PasswordAuthentication[[:space:]].*/PasswordAuthentication {value}/",
         "/etc/ssh/sshd_config"], check=False)

    if shutil.which("sshd"):
        run(["sudo", "sshd", "-t"], check=True)

    run(["sudo", "systemctl", "restart", "ssh"], check=False)
    run(["sudo", "systemctl", "restart", "sshd"], check=False)


def write_flag_for_ubuntu(flag: str):
    UBU_DESKTOP.mkdir(parents=True, exist_ok=True)
    FLAG_PATH.write_text(flag + "\n", encoding="utf-8")
    os.chmod(FLAG_PATH, 0o600)
    run(["sudo", "chown", f"{UBU}:{UBU}", str(FLAG_PATH)], check=False)


def start_slow_ping(target_ip: str):
    # ping every 5 seconds; systemd unit so it persists
    run([
        "sudo", "systemd-run",
        "--unit=keyladder-ping",
        "--property=Restart=always",
        "--property=RestartSec=5",
        "/bin/bash", "-lc", f"ping -i 5 {target_ip}"
    ], check=False)
    print("[*] Ping beacon unit running: keyladder-ping")
    print("    Stop with: sudo systemctl stop keyladder-ping")


def ensure_ubuntu_key_4096():
    if not UBU_HOME.exists():
        raise RuntimeError("/home/ubuntu not found (script assumes user 'ubuntu').")

    UBU_SSH.mkdir(mode=0o700, parents=True, exist_ok=True)
    run(["sudo", "chown", "-R", f"{UBU}:{UBU}", str(UBU_SSH)], check=False)

    key_path = UBU_SSH / "id_rsa"
    pub_path = UBU_SSH / "id_rsa.pub"

    if key_path.exists() or pub_path.exists():
        ans = input(f"[?] {pub_path} exists. Re-generate and overwrite? (y/n): ").strip().lower()
        if ans == "y":
            try:
                key_path.unlink(missing_ok=True)
                pub_path.unlink(missing_ok=True)
            except Exception:
                pass
        else:
            print("[*] Keeping existing ubuntu key.")
            return str(pub_path)

    run_as_ubuntu(["ssh-keygen", "-t", "rsa", "-b", "4096", "-f", str(key_path), "-N", ""], check=True)

    run(["sudo", "chmod", "700", str(UBU_SSH)], check=False)
    run(["sudo", "chmod", "600", str(key_path)], check=False)
    run(["sudo", "chmod", "644", str(pub_path)], check=False)
    run(["sudo", "chown", f"{UBU}:{UBU}", str(key_path), str(pub_path)], check=False)

    print(f"[*] Generated ubuntu keypair: {key_path} / {pub_path}")
    return str(pub_path)


def ubuntu_ssh_copy_id(next_ip: str, pubkey_path: str):
    # push THIS box's ubuntu pubkey INTO next node's ubuntu authorized_keys
    run_as_ubuntu(["ssh-copy-id", "-i", pubkey_path, f"{UBU}@{next_ip}"], check=True)
    print("[*] ssh-copy-id completed to NEXT node.")


def main():
    if os.geteuid() != 0:
        print("Run as root (sudo).")
        sys.exit(1)

    print("\n=== Forward Key Ladder Builder (current -> next) ===\n")

    prev_ip = input("Previous node IP (for ping/beacon back): ").strip()
    if not is_ip(prev_ip):
        print("ERROR: invalid previous IP.")
        sys.exit(1)

    next_ip = input("Next node IP (where to install THIS box's ssh key): ").strip()
    if not is_ip(next_ip):
        print("ERROR: invalid next IP.")
        sys.exit(1)

    print("[*] Enabling PasswordAuthentication on THIS box (so you can still log in while building chain)...")
    set_password_auth(True)

    flag = gen_flag()
    write_flag_for_ubuntu(flag)
    print(f"[*] Desktop flag written: {FLAG_PATH}")
    print(f"[*] Flag value: {flag}")

    print("[*] Starting slow ping (5s) to PREVIOUS node...")
    start_slow_ping(prev_ip)

    pubkey = ensure_ubuntu_key_4096()

    print("[*] Installing THIS box's ubuntu public key onto NEXT node (prompts for NEXT node ubuntu password)...")
    ubuntu_ssh_copy_id(next_ip, pubkey)

    ans = input("[?] Disable PasswordAuthentication on THIS box now? (y/n): ").strip().lower()
    if ans == "y":
        set_password_auth(False)
        print("[*] Disabled PasswordAuthentication on THIS box.")

    print("\n[*] Done. Move to the NEXT box and repeat.")
    print("    Desired chain: Box1 -> Box2 -> Box3 -> ... (each box pushes its key forward).")


if __name__ == "__main__":
    main()
