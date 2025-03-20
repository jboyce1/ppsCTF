#!/usr/bin/env python3
import os
import subprocess
import tarfile

# === CONFIGURATION ===
TAR_FILE = "/home/ubuntu/Desktop/Bully1.tar.gz"
EXTRACT_PATH = "/home"
SSH_CONFIG_PATH = "/etc/ssh/sshd_config"
USER_CREDENTIALS = {
    "Brady1": "123123123",
    "Brandon2": "br@nd0nrulz!",
    "Brian3": "Yer-muh-b0y_b1u3!"
}

# === FUNCTION: Change Password of the Initial Ubuntu User ===
def change_initial_password():
    print("[+] Changing initial Ubuntu user password...")
    subprocess.run(["echo", "ubuntu:123123123", "|", "sudo", "chpasswd"], shell=True)

# === FUNCTION: Extract Tar File ===
def extract_tar():
    print(f"[+] Extracting {TAR_FILE}...")
    if os.path.exists(TAR_FILE):
        with tarfile.open(TAR_FILE, "r:gz") as tar:
            tar.extractall(EXTRACT_PATH)
        print("[+] Extraction complete!")
    else:
        print(f"[!] ERROR: {TAR_FILE} not found!")
        exit(1)

# === FUNCTION: Create Users & Set Passwords ===
def create_users():
    for user, password in USER_CREDENTIALS.items():
        print(f"[+] Creating user: {user}")
        subprocess.run(["sudo", "useradd", "-m", "-s", "/bin/bash", user], check=True)
        subprocess.run(["sudo", "chpasswd"], input=f"{user}:{password}", text=True)

# === FUNCTION: Setup SSH Access ===
def setup_ssh():
    print("[+] Configuring SSH access for all users...")
    for user in USER_CREDENTIALS.keys():
        subprocess.run(["sudo", "mkdir", "-p", f"/home/{user}/.ssh"], check=True)
        subprocess.run(["sudo", "chmod", "700", f"/home/{user}/.ssh"], check=True)
        subprocess.run(["sudo", "touch", f"/home/{user}/.ssh/authorized_keys"], check=True)
        subprocess.run(["sudo", "chmod", "600", f"/home/{user}/.ssh/authorized_keys"], check=True)
        subprocess.run(["sudo", "chown", "-R", f"{user}:{user}", f"/home/{user}/.ssh"], check=True)
    subprocess.run(["sudo", "sed", "-i", 's/^#PasswordAuthentication no/PasswordAuthentication yes/', SSH_CONFIG_PATH], shell=True)
    subprocess.run(["sudo", "systemctl", "restart", "ssh"], check=True)

# === FUNCTION: Main ===
def main():
    change_initial_password()
    extract_tar()
    create_users()
    setup_ssh()
    print("[✅] Bully1 setup complete! Ready for CTF deployment.")

if __name__ == "__main__":
    main()
