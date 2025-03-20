#!/usr/bin/env python3
import os
import subprocess
import tarfile
import shutil

# === CONFIGURATION ===
TAR_FILE = "Bully1.tar.gz"
EXTRACT_PATH = "/home"
SSH_CONFIG_PATH = "/etc/ssh/sshd_config"
USER_CREDENTIALS = {
    "Brady1": "123123123",
    "Brandon2": "br@nd0nrulz!",
    "Brian3": "Yer-muh-b0y_b1u3!"
}

# === STEP 1: EXTRACT TAR FILE ===
def extract_tar():
    print(f"[+] Extracting {TAR_FILE}...")
    with tarfile.open(TAR_FILE, "r:gz") as tar:
        tar.extractall(EXTRACT_PATH)
    print("[+] Extraction complete!")

# === STEP 2: CREATE USERS & SET PASSWORDS ===
def create_users():
    for user, password in USER_CREDENTIALS.items():
        print(f"[+] Creating user: {user}")

        # Check if user already exists
        if subprocess.run(["id", user], capture_output=True, text=True).returncode == 0:
            print(f"[!] User {user} already exists, skipping...")
            continue

        # Create the user
        subprocess.run(["sudo", "useradd", "-m", "-s", "/bin/bash", user])
        
        # Set user password
        subprocess.run(["sudo", "chpasswd"], input=f"{user}:{password}", text=True)

        # Ensure proper ownership of home directory
        subprocess.run(["sudo", "chown", "-R", f"{user}:{user}", f"/home/{user}"])

# === STEP 3: SETUP SSH ACCESS ===
def configure_ssh():
    print("[+] Configuring SSH access for all users...")

    # Ensure each user has a proper .ssh directory
    for user in USER_CREDENTIALS.keys():
        ssh_dir = f"/home/{user}/.ssh"
        auth_keys = f"{ssh_dir}/authorized_keys"

        subprocess.run(["sudo", "mkdir", "-p", ssh_dir])
        subprocess.run(["sudo", "chmod", "700", ssh_dir])
        subprocess.run(["sudo", "touch", auth_keys])
        subprocess.run(["sudo", "chmod", "600", auth_keys"])
        subprocess.run(["sudo", "chown", "-R", f"{user}:{user}", ssh_dir])

    # Ensure SSH allows password authentication
    subprocess.run(["sudo", "sed", "-i", 's/^PasswordAuthentication no/PasswordAuthentication yes/', SSH_CONFIG_PATH])
    subprocess.run(["sudo", "systemctl", "restart", "ssh"])

# === STEP 4: MOVE DESKTOP FILES ===
def setup_desktops():
    for user in USER_CREDENTIALS.keys():
        user_home = f"/home/{user}"
        desktop_path = f"{user_home}/Desktop"

        if os.path.exists(desktop_path):
            print(f"[+] Setting up Desktop for {user}...")
            subprocess.run(["sudo", "chmod", "-R", "755", desktop_path])
            subprocess.run(["sudo", "chown", "-R", f"{user}:{user}", desktop_path])

# === STEP 5: INSTALL REQUIRED DEPENDENCIES ===
def install_dependencies():
    print("[+] Installing required dependencies (Scapy, Python3, etc.)...")
    subprocess.run(["sudo", "apt", "update", "-y"])
    subprocess.run(["sudo", "apt", "install", "-y", "python3", "python3-pip", "python3-scapy", "tcpdump"])
    print("[+] Dependencies installed!")

# === MAIN FUNCTION ===
def main():
    extract_tar()
    create_users()
    configure_ssh()
    setup_desktops()
    install_dependencies()
    print("[✅] Bully1 setup complete! Ready for CTF deployment.")

if __name__ == "__main__":
    main()
