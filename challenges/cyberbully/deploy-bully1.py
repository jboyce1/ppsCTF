#!/usr/bin/env python3
import os
import subprocess
import tarfile
import shutil

# Configuration
TAR_FILE = "Bully1.tar.gz"  # The tar.gz file in the current working directory
EXTRACT_PATH = os.getcwd()  # Extract in the current directory

USER_CREDENTIALS = {
    "Brady1": "123123123",
    "Brandon2": "br@nd0nrulz!",
    "Brian3": "Yer-muh-b0y_b1u3!"
}

# Function to extract tar file
def extract_tar():
    print(f"[+] Extracting {TAR_FILE}...")
    if os.path.exists(TAR_FILE):
        with tarfile.open(TAR_FILE, "r:gz") as tar:
            tar.extractall(EXTRACT_PATH)
        print("[+] Extraction complete!")
    else:
        print(f"[!] ERROR: {TAR_FILE} not found!")
        exit(1)

# Function to create users and set passwords
def create_users():
    for user, password in USER_CREDENTIALS.items():
        print(f"[+] Creating user: {user}")
        subprocess.run(["sudo", "useradd", "-m", "-s", "/bin/bash", "-p", password, user], check=True)
        subprocess.run(f"echo '{user}:{password}' | sudo chpasswd", shell=True)

# Function to setup SSH access
def setup_ssh():
    print("[+] Configuring SSH access for all users...")
    for user in USER_CREDENTIALS.keys():
        subprocess.run(f"sudo mkdir -p /home/{user}/.ssh", shell=True)
        subprocess.run(f"sudo chmod 700 /home/{user}/.ssh", shell=True)
        subprocess.run(f"sudo touch /home/{user}/.ssh/authorized_keys", shell=True)
        subprocess.run(f"sudo chmod 600 /home/{user}/.ssh/authorized_keys", shell=True)

# Function to move extracted files to user directories
def distribute_files():
    for user in USER_CREDENTIALS.keys():
        user_path = os.path.join(EXTRACT_PATH, user)
        if os.path.exists(user_path):
            dest_path = f"/home/{user}"
            if os.path.exists(dest_path):
                print(f"[+] Distributing files for {user}...")
                for item in os.listdir(user_path):
                    shutil.move(os.path.join(user_path, item), os.path.join(dest_path, item))
                print(f"[+] Files moved for {user}")
            else:
                print(f"[!] Destination path {dest_path} does not exist for {user}")

# Main function
def main():
    extract_tar()
    create_users()
    setup_ssh()
    distribute_files()
    print("[✅] Bully1 setup complete! Ready for CTF deployment.")

if __name__ == "__main__":
    main()
