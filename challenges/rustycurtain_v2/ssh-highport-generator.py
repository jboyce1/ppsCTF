import os
import random
import subprocess
import sys

# === CONFIGURATION (EDIT THESE) ===
BOX_LEVEL = "1"          # e.g. "1"
CHALLENGE_VALUE = "3"    # e.g. "3"
PORT_LOW = 21000          # minimum random port
PORT_HIGH = 24000        # maximum random port

def run_cmd(cmd, exit_on_fail=True):
    """Utility to run shell commands."""
    proc = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if proc.returncode != 0 and exit_on_fail:
        print(f"[!] Error running: {cmd}")
        print(proc.stderr)
        sys.exit(1)
    return proc.stdout

def install_openssh():
    """Install (or update) OpenSSH server if needed."""
    print("[+] Installing/updating OpenSSH server...")
    run_cmd("sudo apt update -y")
    run_cmd("sudo apt install -y openssh-server")

def remove_old_port_lines():
    """Remove any existing 'Port' directives from sshd_config."""
    print("[+] Removing old 'Port' lines in /etc/ssh/sshd_config...")
    run_cmd("sudo sed -i '/^Port /d' /etc/ssh/sshd_config", exit_on_fail=False)
    run_cmd("sudo sed -i '/^#Port /d' /etc/ssh/sshd_config", exit_on_fail=False)

def set_random_port(random_port):
    """Add the new Port directive."""
    print(f"[+] Setting SSH to random port {random_port}...")
    cmd = f"echo 'Port {random_port}' | sudo tee -a /etc/ssh/sshd_config"
    run_cmd(cmd)

def enable_password_auth():
    """Ensure PasswordAuthentication is set to yes."""
    print("[+] Enabling password authentication...")
    # Uncomment or replace the 'PasswordAuthentication no' line, or if it's commented, remove it.
    run_cmd("sudo sed -i 's/^#PasswordAuthentication no/PasswordAuthentication yes/' /etc/ssh/sshd_config", exit_on_fail=False)
    run_cmd("sudo sed -i 's/^PasswordAuthentication no/PasswordAuthentication yes/' /etc/ssh/sshd_config", exit_on_fail=False)

def restart_ssh():
    """Restart the SSH service."""
    print("[+] Restarting SSH service...")
    run_cmd("sudo systemctl restart ssh")

def verify_ssh_port(random_port):
    """Check if SSH is listening on the chosen random port."""
    print(f"[+] Verifying SSH is listening on port {random_port}...")
    out = run_cmd("sudo netstat -tulnp || sudo ss -tulnp", exit_on_fail=False)
    if f":{random_port}" not in out:
        print(f"[-] SSH not showing up on port {random_port}!")
        print("    Possibly it's binding to IPv6, or the environment disallows this port.")
        sys.exit(1)
    print(f"[+] SSH is running on port {random_port}!\n")

def main():
    # 1) Install/Update OpenSSH
    install_openssh()

    # 2) Generate random port in [PORT_LOW, PORT_HIGH]
    random_port = random.randint(PORT_LOW, PORT_HIGH)

    # 3) Remove old Port lines & set new random port
    remove_old_port_lines()
    set_random_port(random_port)

    # 4) Enable password auth
    enable_password_auth()

    # 5) Restart SSH
    restart_ssh()

    # 6) Verify new SSH port
    verify_ssh_port(random_port)

    # 7) Print final flag
    flag = f"pps{{{BOX_LEVEL}x{CHALLENGE_VALUE}_sshp0rt#{random_port}}}"
    print(f"🎯 FLAG: {flag}\n")

if __name__ == "__main__":
    main()
