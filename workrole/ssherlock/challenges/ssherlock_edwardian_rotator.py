#!/usr/bin/env python3
"""
ssherlock_edwardian_rotator.py

Creates 3 Edwardian-themed sudo users, writes a themed password list,
and rotates those users' passwords every 5 minutes via systemd timer.

Optionally kills active sessions for those users and restarts ssh service.

USAGE (recommended):
  sudo python3 ssherlock_edwardian_rotator.py --install
  sudo systemctl status ssherlock-rotate.timer
  sudo journalctl -u ssherlock-rotate.service -n 50 --no-pager

Run one rotation now:
  sudo python3 ssherlock_edwardian_rotator.py --run-once

Stop/disable:
  sudo systemctl disable --now ssherlock-rotate.timer
"""

from __future__ import annotations

import argparse
import os
import random
import shutil
import subprocess
from pathlib import Path
from typing import List, Tuple

BASE_DIR = Path("/opt/ssherlock_edwardian")
PASSFILE = BASE_DIR / "passwords.txt"
STATEFILE = BASE_DIR / "last_passwords.tsv"

# 3 Edwardian-ish user names (easy to recognize, not real people)
USERS = ["inspector_lestrade", "lady_bexley", "mr_pemberton"]

# 15 Edwardian-inspired passwords (intentionally "guessable" for training)
PASSWORDS = [
    "TeaAtFour",
    "GaslampLane",
    "VelvetParlour",
    "BrassMonocle",
    "SteamCarriage",
    "FoggyThames",
    "DoverStreet",
    "SilkGloves",
    "Candlewick9",
    "PearlLocket",
    "Clockwork7",
    "TopHatGent",
    "WinterCoat5",
    "MannersMatter",
    "Detective1899",
]

SSH_SERVICE_CANDIDATES = ["ssh", "sshd"]  # ubuntu is usually "ssh"


def run(cmd: List[str], check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, check=check, text=True, capture_output=True)


def require_root() -> None:
    if os.geteuid() != 0:
        raise SystemExit("Run as root: sudo python3 ssherlock_edwardian_rotator.py --install")


def ensure_dirs() -> None:
    BASE_DIR.mkdir(parents=True, exist_ok=True)
    os.chmod(BASE_DIR, 0o700)


def write_password_file() -> None:
    PASSFILE.write_text("\n".join(PASSWORDS) + "\n", encoding="utf-8")
    os.chmod(PASSFILE, 0o600)


def user_exists(username: str) -> bool:
    return run(["id", username], check=False).returncode == 0


def create_user(username: str) -> None:
    # Create with home dir + bash shell
    run(["useradd", "-m", "-s", "/bin/bash", username], check=True)
    # Add to sudo group (Ubuntu)
    run(["usermod", "-aG", "sudo", username], check=True)


def ensure_users() -> None:
    for u in USERS:
        if not user_exists(u):
            create_user(u)
        else:
            # Ensure sudo membership even if user already existed
            run(["usermod", "-aG", "sudo", u], check=True)


def read_last_passwords() -> dict:
    last = {}
    if STATEFILE.exists():
        for line in STATEFILE.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            user, pw = line.split("\t", 1)
            last[user] = pw
    return last


def write_last_passwords(last: dict) -> None:
    lines = [f"{u}\t{last.get(u,'')}" for u in USERS]
    STATEFILE.write_text("\n".join(lines) + "\n", encoding="utf-8")
    os.chmod(STATEFILE, 0o600)


def choose_new_password(old: str | None) -> str:
    choices = PASSWORDS[:]
    if old in choices and len(choices) > 1:
        choices.remove(old)
    return random.choice(choices)


def set_password(username: str, password: str) -> None:
    # Use chpasswd safely
    proc = subprocess.run(
        ["chpasswd"],
        input=f"{username}:{password}\n",
        text=True,
        capture_output=True,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"chpasswd failed for {username}: {proc.stderr.strip()}")


def detect_ssh_service_name() -> str | None:
    for name in SSH_SERVICE_CANDIDATES:
        r = run(["systemctl", "status", f"{name}.service"], check=False)
        if r.returncode == 0:
            return name
    return None


def restart_ssh() -> None:
    svc = detect_ssh_service_name()
    if not svc:
        # If neither is found, don't crash; just report.
        return
    run(["systemctl", "restart", f"{svc}.service"], check=False)


def kick_user_sessions(usernames: List[str]) -> None:
    # Kills all processes owned by each user (will drop their SSH sessions).
    # Does not affect root or other accounts.
    for u in usernames:
        run(["pkill", "-KILL", "-u", u], check=False)


def rotate_passwords(kick: bool) -> Tuple[dict, List[Tuple[str, str]]]:
    last = read_last_passwords()
    changed = []

    for u in USERS:
        old = last.get(u)
        newpw = choose_new_password(old)
        set_password(u, newpw)
        last[u] = newpw
        changed.append((u, newpw))

    write_last_passwords(last)

    if kick:
        kick_user_sessions(USERS)

    restart_ssh()
    return last, changed


SYSTEMD_SERVICE = """\
[Unit]
Description=SSHerlock Edwardian password rotator

[Service]
Type=oneshot
ExecStart=/usr/bin/python3 /opt/ssherlock_edwardian/ssherlock_edwardian_rotator.py --run-once --kick
"""

SYSTEMD_TIMER = """\
[Unit]
Description=Run SSHerlock Edwardian password rotation every 5 minutes

[Timer]
OnBootSec=60
OnUnitActiveSec=300
AccuracySec=5
Persistent=true

[Install]
WantedBy=timers.target
"""


def install_systemd_units() -> None:
    service_path = Path("/etc/systemd/system/ssherlock-rotate.service")
    timer_path = Path("/etc/systemd/system/ssherlock-rotate.timer")

    service_path.write_text(SYSTEMD_SERVICE, encoding="utf-8")
    timer_path.write_text(SYSTEMD_TIMER, encoding="utf-8")

    run(["systemctl", "daemon-reload"], check=True)
    run(["systemctl", "enable", "--now", "ssherlock-rotate.timer"], check=True)


def copy_self_to_opt() -> None:
    # Ensure the script lives in /opt/ssherlock_edwardian for systemd ExecStart path
    dest = BASE_DIR / "ssherlock_edwardian_rotator.py"
    src = Path(__file__).resolve()
    if src != dest:
        shutil.copy2(src, dest)
        os.chmod(dest, 0o700)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--install", action="store_true", help="Create users, write password list, install systemd timer")
    parser.add_argument("--run-once", action="store_true", help="Rotate passwords once now")
    parser.add_argument("--kick", action="store_true", help="Kill the 3 users' processes (drops their SSH sessions)")
    args = parser.parse_args()

    if args.install:
        require_root()
        ensure_dirs()
        copy_self_to_opt()
        write_password_file()
        ensure_users()
        # Initialize state so first rotation doesn't fail
        if not STATEFILE.exists():
            write_last_passwords({u: "" for u in USERS})
        install_systemd_units()
        print("Installed. Timer running: ssherlock-rotate.timer")
        print("Users:", ", ".join(USERS))
        print("Passwords file:", str(PASSFILE))
        return

    if args.run_once:
        require_root()
        ensure_dirs()
        # Ensure passfile exists even if someone runs --run-once first
        if not PASSFILE.exists():
            write_password_file()
        last, changed = rotate_passwords(kick=args.kick)
        # Do NOT print the passwords (students shouldn't see them in teacher output).
        print("Rotated passwords for:", ", ".join([u for (u, _) in changed]))
        print("SSH service restarted (if present).")
        if args.kick:
            print("Killed sessions for those users.")
        return

    parser.print_help()


if __name__ == "__main__":
    main()
