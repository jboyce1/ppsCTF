import os
import random
import subprocess
import sys

# === CONFIGURATION (EDIT THESE) ===
BOX_VALUE = "1"          # e.g. "1"
CHALLENGE_VALUE = "3"    # e.g. "3"
PORT_LOW = 3000          # minimum random port
PORT_HIGH = 10000        # maximum random port

USER_NAME = "ubuntu"     # Which user's Desktop will hold the flag?
FLAG_FILENAME = ""        # If blank, defaults to pps{{{BOX_VALUE}x{CHALLENGE_VALUE}_sshp0rt#{PORT}}}.txt

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
    # Replace 'PasswordAuthentication no' with 'PasswordAuthentication yes'
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
        print("    Possibly it's binding to IPv6 or environment disallows that port.")
        sys.exit(1)
    print(f"[+] SSH is running on port {random_port}!\n")

def place_flag_on_desktop(box_val, chal_val, port):
    """
    Place a file on the user's Desktop containing the SSH flag.
    If FLAG_FILENAME is blank, default to pps{{{box_val}x{chal_val}_sshp0rt#{port}}}.txt
    """
    global FLAG_FILENAME
    final_flag = f"pps{{{box_val}x{chal_val}_sshp0rt#{port}}}"

    # Decide on a filename
    if not FLAG_FILENAME.strip():
        FLAG_FILENAME = f"{final_flag}.txt"

    # Prepare the Desktop path
    desktop_dir = f"/home/{USER_NAME}/Desktop"
    print(f"[+] Creating Desktop directory if needed: {desktop_dir}")
    run_cmd(f"sudo mkdir -p {desktop_dir}", exit_on_fail=False)

    # Place the file
    print(f"[+] Placing flag file '{FLAG_FILENAME}' on the Desktop...")
    run_cmd(f"echo '{final_flag}' | sudo tee {desktop_dir}/{FLAG_FILENAME}", exit_on_fail=False)

    # Make sure the user owns it and can read it
    run_cmd(f"sudo chown {USER_NAME}:{USER_NAME} {desktop_dir}/{FLAG_FILENAME}", exit_on_fail=False)
    run_cmd(f"sudo chmod 644 {desktop_dir}/{FLAG_FILENAME}", exit_on_fail=False)

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

    # 7) Place the flag file on the Desktop
    place_flag_on_desktop(BOX_VALUE, CHALLENGE_VALUE, random_port)

    # 8) Print final instructions
    final_flag = f"pps{{{BOX_VALUE}x{CHALLENGE_VALUE}_sshp0rt#{random_port}}}"
    print(f"🎯 FLAG: {final_flag}\n")
    print("[+] SSH is up on a random high port. The flag file is on the user's Desktop.")
    print(f"[+] Connect with: ssh -p {random_port} {USER_NAME}@<SERVER_IP>")
    print(f"[+] Then do: cd ~/Desktop && cat {FLAG_FILENAME}\n")

if __name__ == "__main__":
    main()
