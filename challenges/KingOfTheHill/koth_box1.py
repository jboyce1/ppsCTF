#!/usr/bin/env python3
import os
import shutil
import subprocess
import sys
"""
Box1 turns on password authentication for ssh and telnet
"""
def run(cmd, check=True):
    print("[+] " + " ".join(cmd))
    r = subprocess.run(cmd)
    if check and r.returncode != 0:
        raise RuntimeError("Command failed: " + " ".join(cmd))

def command_exists(cmd):
    return shutil.which(cmd) is not None

def apt_install(pkgs):
    run(["apt-get", "update"])
    run(["apt-get", "install", "-y"] + pkgs)

def set_password(user, password):
    run(["bash", "-c", f"echo '{user}:{password}' | chpasswd"])

def ensure_ssh_password_auth():
    run([
        "sed", "-i",
        r"s/^#\?PasswordAuthentication .*/PasswordAuthentication yes/",
        "/etc/ssh/sshd_config"
    ])
    run(["systemctl", "restart", "ssh"], check=False)
    run(["systemctl", "restart", "sshd"], check=False)

def install_telnet():
    apt_install(["telnetd", "openbsd-inetd"])
    run(["systemctl", "enable", "--now", "openbsd-inetd"], check=False)
    run(["systemctl", "restart", "openbsd-inetd"], check=False)

def ensure_ufw():
    if not command_exists("ufw"):
        apt_install(["ufw"])

def main():
    if os.geteuid() != 0:
        print("Run with sudo.")
        sys.exit(1)

    set_password("ubuntu", "password")
    ensure_ssh_password_auth()
    install_telnet()

    ensure_ufw()
    run(["ufw", "--force", "reset"])
    run(["ufw", "default", "allow", "incoming"])
    run(["ufw", "default", "allow", "outgoing"])
    run(["ufw", "allow", "22"])
    run(["ufw", "allow", "23"])
    run(["ufw", "--force", "enable"])

    print("\n[OK] Box 1 ready.")

if __name__ == "__main__":
    main()
