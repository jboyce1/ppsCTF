#!/usr/bin/env python3
"""Set up the fixed-password SSHerlock targets on a class Ubuntu VM.

sudo python3 ssherlock_fixed_targets.py
sudo python3 ssherlock_fixed_targets.py --target 1

Without --target, all three accounts are created on this VM.
Running it again resets the selected accounts to their challenge passwords.
"""

import argparse
import os
import pwd
import shutil
import subprocess
from pathlib import Path


TARGETS = {
    "1": ("HackproofHoudini", "pps{M3ta5pl01tL0ve$$#}"),
    "2": ("MetaMischiefMaker", "pps{M3tasploitL0v3s5$H}"),
    "3": ("CipherSensei", "pps{M3t4sploitL0ve5S$#}"),
}


def run(command, **kwargs):
    return subprocess.run(command, check=True, text=True, **kwargs)


def setup_ssh():
    sshd = shutil.which("sshd") or "/usr/sbin/sshd"
    if not Path(sshd).exists():
        run(["apt-get", "update"])
        run(["apt-get", "install", "-y", "openssh-server"])

    config = Path("/etc/ssh/sshd_config")
    dropin = Path("/etc/ssh/sshd_config.d/00-ssherlock.conf")
    original = config.read_text()
    previous_dropin = dropin.read_bytes() if dropin.exists() else None
    backup = config.with_name("sshd_config.before-ssherlock")
    if not backup.exists():
        shutil.copy2(config, backup)

    dropin.parent.mkdir(parents=True, exist_ok=True)
    dropin.write_text("PasswordAuthentication yes\nPubkeyAuthentication yes\n")
    # Put this first so an earlier cloud-image setting does not override it.
    include = "Include /etc/ssh/sshd_config.d/00-ssherlock.conf\n"
    config.write_text(include + original.replace(include, ""))
    Path("/run/sshd").mkdir(parents=True, exist_ok=True)
    try:
        run([sshd, "-t"])
    except subprocess.CalledProcessError:
        config.write_text(original)
        if previous_dropin is None:
            dropin.unlink()
        else:
            dropin.write_bytes(previous_dropin)
        raise

    run(["systemctl", "enable", "--now", "ssh"])
    run(["systemctl", "restart", "ssh"])


def setup_user(username, password):
    try:
        account = pwd.getpwnam(username)
    except KeyError:
        # useradd accepts the mixed-case names used in this challenge.
        run(["useradd", "-m", "-s", "/bin/bash", username])
    else:
        if account.pw_uid < 1000 or account.pw_uid == 65534:
            raise RuntimeError("Refusing to change a system account: " + username)
    # Pass passwords through stdin so $, # and braces stay literal.
    run(["chpasswd"], input=username + ":" + password + "\n")
    print("Ready: " + username)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", choices=sorted(TARGETS),
                        help="Create just target 1, 2, or 3 on this VM")
    args = parser.parse_args()
    if os.geteuid() != 0:
        parser.exit(1, "Run with sudo on the class Ubuntu target.\n")

    setup_ssh()
    selected = [TARGETS[args.target]] if args.target else list(TARGETS.values())
    for username, password in selected:
        setup_user(username, password)

    print("SSH password authentication is on. Passwords do not rotate.")
    print("Target IP:")
    run(["hostname", "-I"])


if __name__ == "__main__":
    try:
        main()
    except (subprocess.CalledProcessError, OSError, RuntimeError) as error:
        raise SystemExit("Setup stopped: " + str(error))
