#!/usr/bin/env python3
import os
import re
import sys
import pwd
import random
import shutil
import subprocess
from getpass import getpass

FLAG_PREFIX = "pps{1x?_H1ghb@ll_"  # keep theme


def run(cmd, *, check=True, capture=False):
    """
    Run a command and raise a clean error if it fails.
    """
    if isinstance(cmd, str):
        raise ValueError("run() expects a list like ['sudo','ufw','status']")
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


def generate_flag() -> str:
    salt_len = random.randint(5, 8)
    salt_alphabet = "abcdefghijklmnopqrstuvwxyz0123456789-+"
    salt = "".join(random.choice(salt_alphabet) for _ in range(salt_len))
    return f"{FLAG_PREFIX}{salt}}}"


def safe_username(u: str) -> str:
    u = u.strip()
    if not re.fullmatch(r"[a-z_][a-z0-9_-]{0,30}", u):
        raise ValueError("Username must match: [a-z_][a-z0-9_-]{0,30}")
    return u


def ensure_command_exists(cmd):
    if shutil.which(cmd) is None:
        raise RuntimeError(f"Missing required command: {cmd}")


def desktop_path_for_current_user() -> str:
    # Put flag on Desktop of the user running the script (not root)
    home = os.path.expanduser("~")
    desktop = os.path.join(home, "Desktop")
    os.makedirs(desktop, exist_ok=True)
    return desktop


def write_flag_to_desktop(flag: str) -> str:
    desktop = desktop_path_for_current_user()
    flag_path = os.path.join(desktop, "ssh_flag.txt")
    with open(flag_path, "w", encoding="utf-8") as f:
        f.write(flag + "\n")
    # Lock down permissions: owner read/write only
    os.chmod(flag_path, 0o600)
    return flag_path


def set_sshd_password_auth():
    # Turn on PasswordAuthentication yes (even if SSH port is blocked)
    run([
        "sudo", "sed", "-i",
        r"s/^#\?\s*PasswordAuthentication\s+.*/PasswordAuthentication yes/",
        "/etc/ssh/sshd_config"
    ])
    # Validate config if sshd exists, then restart ssh/sshd whichever is present
    if shutil.which("sshd"):
        run(["sudo", "sshd", "-t"], check=True)
    # restart service (ubuntu often uses "ssh")
    # don't crash if one name doesn't exist
    run(["sudo", "systemctl", "restart", "ssh"], check=False)
    run(["sudo", "systemctl", "restart", "sshd"], check=False)


def configure_ufw_for_telnet():
    ensure_command_exists("ufw")
    # Deny SSH and allow telnet
    run(["sudo", "ufw", "deny", "22"], check=False)    # check=False in case rule already exists
    run(["sudo", "ufw", "allow", "23"], check=False)
    # Force-enable without interactive prompt
    run(["sudo", "ufw", "--force", "enable"], check=True)


def install_telnet_services():
    ensure_command_exists("apt-get")
    run(["sudo", "apt-get", "update"], check=True)
    run(["sudo", "apt-get", "install", "-y", "telnetd", "openbsd-inetd"], check=True)
    # Ensure inetd is enabled and running
    run(["sudo", "systemctl", "enable", "--now", "openbsd-inetd"], check=False)
    run(["sudo", "systemctl", "restart", "openbsd-inetd"], check=False)


def create_restricted_shell_script() -> str:
    """
    Creates a simple restricted bash wrapper.
    """
    path = "/usr/local/bin/telnet_shell.sh"
    contents = """#!/bin/bash
echo "Limited access environment."
echo "You may only use a small set of commands."
export PATH=/usr/bin:/bin
exec /bin/bash --restricted
"""
    # Write as root
    run(["sudo", "bash", "-c", f"cat > {path} <<'EOF'\n{contents}\nEOF"])
    run(["sudo", "chmod", "755", path])
    return path


def user_exists(username: str) -> bool:
    try:
        pwd.getpwnam(username)
        return True
    except KeyError:
        return False


def create_user_noninteractive(username: str, password: str, shell_path: str):
    if user_exists(username):
        # Update password + shell
        run(["sudo", "usermod", "-s", shell_path, username], check=False)
    else:
        # Create user with home dir and set shell
        run(["sudo", "useradd", "-m", "-s", shell_path, username], check=True)

    # Set password via chpasswd (non-interactive)
    run(["sudo", "bash", "-c", f"echo '{username}:{password}' | chpasswd"], check=True)


def main():
    try:
        username = safe_username(input("New username to create for teluser: "))
        password = getpass("Password: ")
        password2 = getpass("Confirm password: ")
        if password != password2:
            print("ERROR: passwords do not match.")
            sys.exit(1)
        if not password:
            print("ERROR: password cannot be empty.")
            sys.exit(1)
        flag = generate_flag()
        flag_path = write_flag_to_desktop(flag)
        print(f"Flag written to: {flag_path}")
        configure_ufw_for_telnet()
        set_sshd_password_auth()
        install_telnet_services()
        shell_path = create_restricted_shell_script()
        create_user_noninteractive(username, password, shell_path)

        print(f"{username} user created successfully with {password}.")

    except Exception as e:
        print(f"\nERROR: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
