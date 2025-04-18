#!/usr/bin/env python3
import os
import subprocess
import tarfile
import shutil

# Configuration
TAR_FILE = "Bully1.tar.gz"  # Assumed to be in the same directory as the script
EXTRACT_PATH = os.getcwd()  # Extract in the current directory
USER_CREDENTIALS = {
    "Brady1": "123123123",
    "Brandon2": "br@nd0nrulz!",
    "Brian3": "Yer-muh-b0y_b1u3!"
}

# Function to install required dependencies
def install_dependencies():
    print("[+] Installing required packages...")
    packages = ["python3-scapy", "tcpdump", "iftop", "nmap", "python3-pip"]
    subprocess.run(["sudo", "apt-get", "update"], check=True)
    subprocess.run(["sudo", "apt-get", "install", "-y", "--allow-change-held-packages"] + packages, check=True)
    print("[+] All dependencies installed successfully!")

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
        subprocess.run(["sudo", "useradd", "-m", "-s", "/bin/bash", user], check=True)
        subprocess.run(f"echo '{user}:{password}' | sudo chpasswd", shell=True)
        if user.endswith('1'):  # Granting sudo privileges to users whose names end with '1'
            with open(f'/etc/sudoers.d/{user}', 'w') as sudoers_file:
                sudoers_file.write(f"{user} ALL=(ALL) NOPASSWD: ALL\n")

# Function to setup SSH access
def setup_ssh():
    print("[+] Configuring SSH access for all users...")
    for user in USER_CREDENTIALS.keys():
        ssh_dir = f"/home/{user}/.ssh"
        os.makedirs(ssh_dir, exist_ok=True)
        subprocess.run(["sudo", "chmod", "700", ssh_dir])
        subprocess.run(["sudo", "touch", f"{ssh_dir}/authorized_keys"])
        subprocess.run(["sudo", "chmod", "600", f"{ssh_dir}/authorized_keys"])

# Function to copy extracted files to user directories
def distribute_files():
    base_extracted_path = os.path.join(EXTRACT_PATH, "Bully1")
    for user in USER_CREDENTIALS.keys():
        user_path = os.path.join(base_extracted_path, user)
        if os.path.exists(user_path):
            dest_path = f"/home/{user}"
            if os.path.exists(dest_path):
                print(f"[+] Copying files for {user}...")
                for item in os.listdir(user_path):
                    item_path = os.path.join(user_path, item)
                    if os.path.isdir(item_path):
                        shutil.copytree(item_path, os.path.join(dest_path, item), dirs_exist_ok=True)
                    else:
                        shutil.copy(item_path, os.path.join(dest_path, item))
                print(f"[+] Files copied for {user}")

# Main function
def main():
    install_dependencies()
    extract_tar()
    create_users()
    setup_ssh()
    distribute_files()
    print("[✅] Bully1 setup complete! Ready for CTF deployment.")

if __name__ == "__main__":
    main()
