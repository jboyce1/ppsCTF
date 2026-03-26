#!/usr/bin/env python3
import os
import re
import sys
import pwd
import random
import shutil
import subprocess
import string

"""
Run with:

curl -sSL https://raw.githubusercontent.com/jboyce1/ppsCTF/main/challenges/KingOfTheHill/koth_box3.py -o cyberus3_setup.py && sudo python3 cyberus3_setup.py
"""

UBUNTU_PASS_LEN = 5
FLAG_PREFIX = "pps{koth3_"


def run(cmd, *, check=True, capture=False):
    if isinstance(cmd, str):
        raise ValueError("run() expects a list like ['sudo', 'ufw', 'status']")
    kwargs = {}
    if capture:
        kwargs.update({
            "stdout": subprocess.PIPE,
            "stderr": subprocess.PIPE,
            "text": True
        })
    p = subprocess.run(cmd, **kwargs)
    if check and p.returncode != 0:
        err = ""
        if capture and p.stderr:
            err = "\n" + p.stderr.strip()
        raise RuntimeError(f"Command failed ({p.returncode}): {' '.join(cmd)}{err}")
    return p


def generate_password(length):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


def generate_flag():
    salt_len = random.randint(5, 8)
    salt_alphabet = "abcdefghijklmnopqrstuvwxyz0123456789-+"
    salt = "".join(random.choice(salt_alphabet) for _ in range(salt_len))
    return f"{FLAG_PREFIX}{salt}}}"


def ensure_command_exists(cmd):
    if shutil.which(cmd) is None:
        raise RuntimeError(f"Missing required command: {cmd}")


def user_exists(username):
    try:
        pwd.getpwnam(username)
        return True
    except KeyError:
        return False


def set_sshd_password_auth():
    run([
        "sudo", "sed", "-i",
        r"s/^#\?PasswordAuthentication .*/PasswordAuthentication yes/",
        "/etc/ssh/sshd_config"
    ])

    if shutil.which("sshd"):
        run(["sudo", "sshd", "-t"], check=True)

    run(["sudo", "systemctl", "restart", "ssh"], check=False)
    run(["sudo", "systemctl", "restart", "sshd"], check=False)


def configure_ufw_for_telnet():
    ensure_command_exists("ufw")
    run(["sudo", "ufw", "deny", "22"], check=False)
    run(["sudo", "ufw", "allow", "23"], check=False)
    run(["sudo", "ufw", "--force", "enable"], check=True)


def install_telnet_services():
    ensure_command_exists("apt-get")
    run(["sudo", "apt-get", "update"], check=True)
    run(["sudo", "apt-get", "install", "-y", "telnetd", "openbsd-inetd"], check=True)
    run(["sudo", "systemctl", "enable", "--now", "openbsd-inetd"], check=False)
    run(["sudo", "systemctl", "restart", "openbsd-inetd"], check=False)


def create_restricted_shell_script():
    path = "/usr/local/bin/telnet_shell.sh"
    contents = """#!/bin/bash
echo "Limited access environment."
echo "You may only use a small set of commands."
export PATH=/usr/bin:/bin
exec /bin/bash --restricted
"""
    run(["sudo", "bash", "-c", f"cat > {path} <<'EOF'\n{contents}\nEOF"])
    run(["sudo", "chmod", "755", path])
    return path


def create_user_noninteractive(username, password, shell_path):
    if user_exists(username):
        run(["sudo", "usermod", "-s", shell_path, username], check=False)
    else:
        run(["sudo", "useradd", "-m", "-s", shell_path, username], check=True)

    run(["sudo", "bash", "-c", f"echo '{username}:{password}' | chpasswd"], check=True)


def setup_ubuntu_password_for_koth():
    ubuntu_pass = generate_password(UBUNTU_PASS_LEN)

    run(["sudo", "bash", "-c", f"echo 'ubuntu:{ubuntu_pass}' | chpasswd"])

    file_path = "/home/cyberus3/ubuntu_pass.txt"
    contents = f"the new ubuntu password is: {ubuntu_pass}\n"

    run(["sudo", "bash", "-c", f"echo '{contents}' > {file_path}"])
    run(["sudo", "chown", "cyberus3:cyberus3", file_path])
    run(["sudo", "chmod", "600", file_path])

    print(f"[OK] ubuntu password randomized and stored at {file_path}")


def write_flag_to_cyberus3(flag):
    flag_path = "/home/ubuntu/Desktop/ssh_flag.txt"
    run(["sudo", "bash", "-c", f"echo '{flag}' > {flag_path}"])
    run(["sudo", "chown", "ubuntu:ubuntu", flag_path])
    run(["sudo", "chmod", "600", flag_path])
    return flag_path


def main():
    try:
        username = "cyberus3"
        password = "password"

        install_telnet_services()
        configure_ufw_for_telnet()
        set_sshd_password_auth()

        shell_path = create_restricted_shell_script()
        create_user_noninteractive(username, password, shell_path)

        setup_ubuntu_password_for_koth()

        flag = generate_flag()
        flag_path = write_flag_to_cyberus3(flag)
        print(f"Flag written to: {flag_path}")

        print(f"{username} user created successfully with password: {password}")

    except Exception as e:
        print(f"\nERROR: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
