#!/usr/bin/env python3
import os
import re
import sys
import pwd
import time
import random
import shutil
import subprocess
from getpass import getpass
from pathlib import Path

# ===== Flag formats =====
DESKTOP_FLAG_PREFIX = "pps{Ladder_"
BEACON_FLAG_PREFIX  = "pps{Beacon_"
SALT_ALPHABET = "abcdefghijklmnopqrstuvwxyz0123456789"

FLAG_TXT_NAME = "flag.txt"
FLAG_IMG_NAME = "flag.png"

TARGET_DESKTOP_USER = "ubuntu"  # <-- forced per your request


def run(cmd, *, check=True, capture=False):
    if isinstance(cmd, str):
        raise ValueError("run() expects a list, not a string")
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


def is_ip(s: str) -> bool:
    s = s.strip()
    m = re.fullmatch(r"(?:\d{1,3}\.){3}\d{1,3}", s)
    if not m:
        return False
    parts = [int(x) for x in s.split(".")]
    return all(0 <= x <= 255 for x in parts)


def safe_username(u: str) -> str:
    u = u.strip()
    if not re.fullmatch(r"[a-z_][a-z0-9_-]{0,30}", u):
        raise ValueError("Username must match: [a-z_][a-z0-9_-]{0,30}")
    return u


def gen_flag(prefix: str) -> str:
    salt_len = random.randint(5, 8)
    salt = "".join(random.choice(SALT_ALPHABET) for _ in range(salt_len))
    return f"{prefix}{salt}}}"


def desktop_path_for_user(username: str) -> Path:
    d = Path(f"/home/{username}/Desktop")
    d.mkdir(parents=True, exist_ok=True)
    return d


def chown_to_user(path: Path, username: str):
    # Ensure ubuntu can see/read it without sudo
    run(["chown", f"{username}:{username}", str(path)], check=False)


def write_flag_text_to_ubuntu(flag: str) -> Path:
    p = desktop_path_for_user(TARGET_DESKTOP_USER) / FLAG_TXT_NAME
    p.write_text(flag + "\n", encoding="utf-8")
    os.chmod(p, 0o600)
    chown_to_user(p, TARGET_DESKTOP_USER)
    return p


def ensure_apt_pkg(pkg: str):
    run(["apt-get", "update"], check=True)
    run(["apt-get", "install", "-y", pkg], check=True)


def ensure_ufw():
    if shutil.which("ufw") is None:
        ensure_apt_pkg("ufw")


def ufw_reset_defaults():
    ensure_ufw()
    run(["ufw", "--force", "reset"], check=True)
    run(["ufw", "default", "deny", "incoming"], check=True)
    run(["ufw", "default", "allow", "outgoing"], check=True)


def ufw_enable():
    run(["ufw", "--force", "enable"], check=True)


def ufw_allow_ssh_any():
    run(["ufw", "allow", "22"], check=True)


def ufw_allow_ssh_from(ip: str):
    run(["ufw", "allow", "from", ip, "to", "any", "port", "22"], check=True)


def ufw_allow_telnet_from(ip: str):
    run(["ufw", "allow", "from", ip, "to", "any", "port", "23"], check=True)


def set_sshd_password_auth():
    # robust sed (no \s)
    run(["sed", "-i",
         r"s/^#\?PasswordAuthentication[[:space:]].*/PasswordAuthentication yes/",
         "/etc/ssh/sshd_config"], check=False)

    if shutil.which("sshd"):
        run(["sshd", "-t"], check=True)

    run(["systemctl", "restart", "ssh"], check=False)
    run(["systemctl", "restart", "sshd"], check=False)


def install_telnet_services():
    ensure_apt_pkg("telnetd")
    ensure_apt_pkg("openbsd-inetd")
    run(["systemctl", "enable", "--now", "openbsd-inetd"], check=False)
    run(["systemctl", "restart", "openbsd-inetd"], check=False)


def create_restricted_shell_script() -> str:
    path = "/usr/local/bin/telnet_shell.sh"
    contents = """#!/bin/bash
echo "Limited access."
echo "Allowed commands: ls, cat"
export PATH=/bin
exec /bin/bash --restricted
"""
    run(["bash", "-c", f"cat > {path} <<'EOF'\n{contents}\nEOF"], check=True)
    run(["chmod", "755", path], check=True)
    return path


def user_exists(username: str) -> bool:
    try:
        pwd.getpwnam(username)
        return True
    except KeyError:
        return False


def create_user_noninteractive(username: str, password: str, shell_path: str):
    if user_exists(username):
        run(["usermod", "-s", shell_path, username], check=False)
    else:
        run(["useradd", "-m", "-s", shell_path, username], check=True)
    run(["bash", "-c", f"echo '{username}:{password}' | chpasswd"], check=True)


def ensure_pillow():
    try:
        import PIL  # noqa
        return
    except Exception:
        pass
    print("[*] Installing Pillow (python3-pil)...")
    ensure_apt_pkg("python3-pil")


def write_flag_image_pixels_to_ubuntu(flag: str) -> Path:
    """
    Draws the flag into pixels so strings/exif won't reveal it.
    Always writes to /home/ubuntu/Desktop/flag.png and chowns it to ubuntu.
    """
    ensure_pillow()
    from PIL import Image, ImageDraw, ImageFont

    w, h = 900, 220
    img = Image.new("RGB", (w, h), (245, 245, 245))
    draw = ImageDraw.Draw(img)

    font = None
    for fp in [
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]:
        if os.path.exists(fp):
            try:
                font = ImageFont.truetype(fp, 28)
                break
            except Exception:
                pass
    if font is None:
        font = ImageFont.load_default()

    draw.text((30, 70), "FLAG:", fill=(20, 20, 20), font=font)
    draw.text((30, 120), flag, fill=(20, 20, 20), font=font)

    p = desktop_path_for_user(TARGET_DESKTOP_USER) / FLAG_IMG_NAME
    img.save(p, format="PNG", optimize=True)
    os.chmod(p, 0o644)
    chown_to_user(p, TARGET_DESKTOP_USER)

    # hard verify
    if not p.exists():
        raise RuntimeError(f"Expected image not found after save: {p}")

    return p


def start_icmp_beacon(prev_ip: str):
    run([
        "systemd-run",
        "--unit=portalord-icmp",
        "--property=Restart=always",
        "--property=RestartSec=2",
        "/bin/bash", "-lc", f"ping -i 2 {prev_ip}"
    ], check=False)
    print("[*] ICMP beacon running: portalord-icmp")


def start_udp_stream(prev_ip: str, port: int, payload: str):
    py = f"""python3 - <<'PY'
import socket, time
ip={prev_ip!r}
port={port}
msg={payload!r}.encode()
s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
while True:
    try:
        s.sendto(msg, (ip, port))
    except Exception:
        pass
    time.sleep(0.5)
PY
"""
    run([
        "systemd-run",
        "--unit=portalord-udp",
        "--property=Restart=always",
        "--property=RestartSec=1",
        "/bin/bash", "-lc", py
    ], check=False)
    print("[*] UDP stream running: portalord-udp")
    print("    Stop with: systemctl stop portalord-udp")


def main():
    if os.geteuid() != 0:
        print("Run with sudo/root.")
        sys.exit(1)

    print("\n=== Portalord: Versatile Node Setup (fixed) ===\n")
    print("Access type:")
    print("  1) open_to_all")
    print("  2) telnet_only (from previous node)")
    print("  3) ssh_with_image (from previous node)")
    access = input("Choose [1/2/3]: ").strip()

    prev_ip = None
    if access in {"2", "3"}:
        prev_ip = input("Previous node IP: ").strip()
        if not is_ip(prev_ip):
            print("ERROR: invalid previous IP.")
            sys.exit(1)

    print("\nBeacon type:")
    print("  1) icmp")
    print("  2) udp_stream (includes DIFFERENT beacon-flag)")
    print("  3) none")
    beacon = input("Choose [1/2/3]: ").strip()

    # Generate two distinct flags
    desktop_flag = gen_flag(DESKTOP_FLAG_PREFIX)
    beacon_flag  = gen_flag(BEACON_FLAG_PREFIX)

    print(f"[*] Desktop flag (Ladder): {desktop_flag}")
    print(f"[*] Beacon flag (Beacon): {beacon_flag}")

    # Baseline
    set_sshd_password_auth()
    ufw_reset_defaults()

    # Configure access
    if access == "1":
        ufw_allow_ssh_any()
        ufw_enable()
        p = write_flag_text_to_ubuntu(desktop_flag)
        print(f"[*] Desktop flag file (ubuntu): {p}")

    elif access == "2":
        install_telnet_services()
        ufw_allow_telnet_from(prev_ip)
        ufw_enable()

        username = safe_username(input("Telnet username to create: "))
        pw1 = getpass("Password: ")
        pw2 = getpass("Confirm: ")
        if not pw1 or pw1 != pw2:
            print("ERROR: password mismatch or empty.")
            sys.exit(1)

        shell_path = create_restricted_shell_script()
        create_user_noninteractive(username, pw1, shell_path)

        p = write_flag_text_to_ubuntu(desktop_flag)
        print(f"[*] Desktop flag file (ubuntu): {p}")
        print(f"[*] Telnet user created: {username}")

    elif access == "3":
        ufw_allow_ssh_from(prev_ip)
        ufw_enable()
        p = write_flag_image_pixels_to_ubuntu(desktop_flag)
        print(f"[*] Desktop flag image (ubuntu): {p}")
        print("    Students must SCP /home/ubuntu/Desktop/flag.png to read it visually.")

    else:
        print("ERROR: invalid access type.")
        sys.exit(1)

    # Configure beacon
    if beacon == "1":
        if not prev_ip:
            print("Beacon requires Previous node IP (choose access 2 or 3).")
            sys.exit(1)
        start_icmp_beacon(prev_ip)

    elif beacon == "2":
        if not prev_ip:
            print("Beacon requires Previous node IP (choose access 2 or 3).")
            sys.exit(1)
        port = int(input("UDP port to send to on previous node [5555]: ").strip() or "5555")
        payload = f"PORTALORD_UDP|{beacon_flag}|{time.time():.0f}"
        start_udp_stream(prev_ip, port, payload)

    # Status
    print("\n[*] UFW status:\n")
    print(run(["ufw", "status", "verbose"], capture=True).stdout)
    print("[*] Done.\n")


if __name__ == "__main__":
    main()
