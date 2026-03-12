#!/usr/bin/env python3

import os
import subprocess
import sys
import pwd

USERNAME = "rogerdodger"
USER_PASSWORD = "J@ney8aby"
UBUNTU_PASSWORD = "123123"

ZIP_URL = "https://raw.githubusercontent.com/jboyce1/ppsCTF/main/challenges/CornerPocket/CornerPocket3.zip"
ZIP_NAME = "CornerPocket3.zip"


def run(cmd, check=True, **kwargs):
    print(f"[+] Running: {' '.join(cmd)}")
    return subprocess.run(cmd, check=check, text=True, **kwargs)


def require_root():
    if os.geteuid() != 0:
        print("[-] Run this script with sudo.")
        sys.exit(1)


def user_exists(username):
    try:
        pwd.getpwnam(username)
        return True
    except KeyError:
        return False


def create_user():
    if user_exists(USERNAME):
        print(f"[!] User {USERNAME} already exists. Skipping adduser.")
    else:
        run(["adduser", "--disabled-password", "--gecos", "", USERNAME])

    run(["chpasswd"], input=f"{USERNAME}:{USER_PASSWORD}\n")
    print(f"[+] Set password for {USERNAME}")


def put_files_on_desktop():
    home = f"/home/{USERNAME}"
    desktop = os.path.join(home, "Desktop")
    zip_path = os.path.join(desktop, ZIP_NAME)

    os.makedirs(desktop, exist_ok=True)

    run(["wget", "-O", zip_path, ZIP_URL])
    run(["unzip", "-o", zip_path, "-d", desktop])

    if os.path.exists(zip_path):
        os.remove(zip_path)
        print(f"[+] Deleted {ZIP_NAME}")

    run(["chown", "-R", f"{USERNAME}:{USERNAME}", home])


def change_ubuntu_password():
    if user_exists("ubuntu"):
        run(["chpasswd"], input=f"ubuntu:{UBUNTU_PASSWORD}\n")
        print("[+] Changed ubuntu password")
    else:
        print("[!] ubuntu user does not exist. Skipping password change.")


def enable_ssh_password_auth():
    run([
        "sed",
        "-i",
        r"s/^#\?PasswordAuthentication .*/PasswordAuthentication yes/",
        "/etc/ssh/sshd_config"
    ])

    try:
        run(["systemctl", "restart", "ssh"])
    except subprocess.CalledProcessError:
        run(["systemctl", "restart", "sshd"])

    print("[+] SSH password authentication enabled")


def prompt_and_ping():
    ip = input("Enter IP address to ping from this new box: ").strip()

    if not ip:
        print("[-] No IP entered. Skipping ping.")
        return

    print(f"[+] Starting ping to {ip}. Press Ctrl+C to stop.")
    try:
        subprocess.run(["ping", ip])
    except KeyboardInterrupt:
        print("\n[+] Ping stopped.")


def main():
    require_root()
    create_user()
    put_files_on_desktop()
    change_ubuntu_password()
    enable_ssh_password_auth()
    prompt_and_ping()
    print("[+] Done.")


if __name__ == "__main__":
    main()
