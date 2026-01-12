#!/usr/bin/env python3

import os
import pwd
import shutil
import subprocess
import sys

JAKE_USER = "jake"
JAKE_PASS = "stagecrew"
PROFILE_DIR = "jake_profile"

def run(cmd):
    subprocess.run(cmd, shell=True, check=True)

def user_exists(username):
    try:
        pwd.getpwnam(username)
        return True
    except KeyError:
        return False

def create_user():
    print("[*] Creating user 'jake'")
    run(f"useradd -m -s /bin/bash {JAKE_USER}")
    run(f"echo '{JAKE_USER}:{JAKE_PASS}' | chpasswd")

def ensure_ssh_access():
    print("[*] Ensuring SSH password auth is enabled")
    run("sed -i 's/^#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config")
    run("sed -i 's/^PasswordAuthentication no/PasswordAuthentication yes/' /etc/ssh/sshd_config")
    run("systemctl restart ssh")

def deploy_files():
    src = os.path.abspath(PROFILE_DIR)
    dest = f"/home/{JAKE_USER}/Desktop/jake_profile"

    print("[*] Deploying target profile to Desktop")

    if os.path.exists(dest):
        shutil.rmtree(dest)

    shutil.copytree(src, dest)
    run(f"chown -R {JAKE_USER}:{JAKE_USER} {dest}")

def main():
    if os.geteuid() != 0:
        print("ERROR: Run this script with sudo")
        sys.exit(1)

    if not user_exists(JAKE_USER):
        create_user()
    else:
        print("[*] User already exists")

    ensure_ssh_access()
    deploy_files()

    print("\n[+] deployment complete")

if __name__ == "__main__":
    main()
