#!/usr/bin/env python3

import os
import subprocess
import random
import sys

USER_CHOICES = [
    "stjones8",
    "stmiller4",
    "stbrown8",
]

PASSWORD_CHOICES = [
    "Y0uf0undm3B@!",
    "P@ssw0rd!",
    "Secur1ty!",
    "Cha1nL0ck!",
    "H@ckM3N0w!",
    "Saf3Guard!",
    "K33p0ut!",
    "Pr0t3ct!",
    "F0rtR3ss!",
    "Gu@rd1@n!",
    "LockD0wn!",
]

ZIP_URL = "https://raw.githubusercontent.com/jboyce1/ppsCTF/main/challenges/CornerPocket/cp2.zip"
ZIP_NAME = "cp2.zip"

UBUNTU_NEW_PASSWORD = "123123"


def run(cmd, **kwargs):
    subprocess.run(cmd, check=True, text=True, **kwargs)


def require_root():
    if os.geteuid() != 0:
        print("Run with sudo")
        sys.exit(1)


def create_user(username, password):

    print(f"\n[+] Selected username : {username}")
    print(f"[+] Selected password : {password}\n")

    subprocess.run(["adduser", "--disabled-password", "--gecos", "", username])

    subprocess.run(
        ["chpasswd"],
        input=f"{username}:{password}\n",
        text=True
    )


def setup_files(username):

    home = f"/home/{username}"
    desktop = f"{home}/Desktop"

    os.makedirs(desktop, exist_ok=True)

    os.chdir(desktop)

    run(["wget", ZIP_URL])
    run(["unzip", ZIP_NAME])

    os.remove(ZIP_NAME)

    run(["chown", "-R", f"{username}:{username}", home])


def change_ubuntu_password():

    subprocess.run(
        ["chpasswd"],
        input=f"ubuntu:{UBUNTU_NEW_PASSWORD}\n",
        text=True
    )

    print("[+] Ubuntu password changed")


def enable_ssh_password():

    run([
        "sed",
        "-i",
        "s/^#\\?PasswordAuthentication .*/PasswordAuthentication yes/",
        "/etc/ssh/sshd_config"
    ])

    try:
        run(["systemctl", "restart", "ssh"])
    except:
        run(["systemctl", "restart", "sshd"])

    print("[+] SSH password authentication enabled")


def start_ping():

    target = input("\nEnter IP to start pinging (Box 1): ")

    print(f"\n[+] Starting ping to {target}\n")

    subprocess.run(["ping", target])


def main():

    require_root()

    username = random.choice(USER_CHOICES)
    password = random.choice(PASSWORD_CHOICES)

    create_user(username, password)

    setup_files(username)

    change_ubuntu_password()

    enable_ssh_password()

    start_ping()


if __name__ == "__main__":
    main()
