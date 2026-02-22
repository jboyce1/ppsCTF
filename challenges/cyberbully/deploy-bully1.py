#!/usr/bin/env python3
import os
import subprocess
import tarfile
import shutil
import sys

# Configuration
TAR_FILE = "Bully1.tar.gz"
EXTRACT_PATH = os.getcwd()

USER_CREDENTIALS = {
    "Brady1": "123123123",
    "Brandon2": "br@nd0nrulz!",
    "Brian3": "Yer-muh-b0y_b1u3!"
}

# ----------------------------
# Install Dependencies
# ----------------------------
def install_dependencies():
    print("[+] Installing required packages...")
    packages = ["python3-scapy", "tcpdump", "iftop", "nmap"]
    subprocess.run(["sudo", "apt-get", "update"], check=True)
    subprocess.run(["sudo", "apt-get", "install", "-y"] + packages, check=True)
    print("[+] Dependencies installed.")


# ----------------------------
# Force Ubuntu Password Reset
# ----------------------------
def secure_ubuntu_account():
    print("\n[!] You MUST set a secure password for the ubuntu account.")
    print("[!] Students should NOT know this password.\n")

    subprocess.run(["sudo", "passwd", "ubuntu"], check=True)

    # Ensure ubuntu does not have passwordless sudo
    subprocess.run(["sudo", "deluser", "ubuntu", "sudo"], check=False)

    print("[+] Ubuntu account secured.\n")


# ----------------------------
# Extract Tar
# ----------------------------
def extract_tar():
    print(f"[+] Extracting {TAR_FILE}...")
    if not os.path.exists(TAR_FILE):
        print(f"[!] ERROR: {TAR_FILE} not found!")
        sys.exit(1)

    with tarfile.open(TAR_FILE, "r:gz") as tar:
        tar.extractall(EXTRACT_PATH)

    print("[+] Extraction complete.")


# ----------------------------
# Create Users (NO SUDO)
# ----------------------------
def create_users():
    for user, password in USER_CREDENTIALS.items():
        print(f"[+] Creating user: {user}")

        subprocess.run(["sudo", "useradd", "-m", "-s", "/bin/bash", user], check=False)
        subprocess.run(f"echo '{user}:{password}' | sudo chpasswd", shell=True)

        # Ensure user has NO sudo
        subprocess.run(["sudo", "deluser", user, "sudo"], check=False)


# ----------------------------
# Setup SSH
# ----------------------------
def setup_ssh():
    print("[+] Configuring SSH directories...")
    for user in USER_CREDENTIALS.keys():
        ssh_dir = f"/home/{user}/.ssh"
        subprocess.run(["sudo", "mkdir", "-p", ssh_dir])
        subprocess.run(["sudo", "chmod", "700", ssh_dir])
        subprocess.run(["sudo", "touch", f"{ssh_dir}/authorized_keys"])
        subprocess.run(["sudo", "chmod", "600", f"{ssh_dir}/authorized_keys"])
        subprocess.run(["sudo", "chown", "-R", f"{user}:{user}", f"/home/{user}/.ssh"])


# ----------------------------
# Distribute Files
# ----------------------------
def distribute_files():
    base_extracted_path = os.path.join(EXTRACT_PATH, "Bully1")

    for user in USER_CREDENTIALS.keys():
        user_path = os.path.join(base_extracted_path, user)

        if os.path.exists(user_path):
            dest_path = f"/home/{user}"

            print(f"[+] Copying files for {user}...")

            for item in os.listdir(user_path):
                item_path = os.path.join(user_path, item)
                dest_item = os.path.join(dest_path, item)

                if os.path.isdir(item_path):
                    shutil.copytree(item_path, dest_item, dirs_exist_ok=True)
                else:
                    shutil.copy(item_path, dest_item)

            subprocess.run(["sudo", "chown", "-R", f"{user}:{user}", dest_path])

    print("[+] Files distributed.")


# ----------------------------
# Create Systemd Services
# ----------------------------
def create_services():
    print("[+] Creating systemd services for Brady1 scripts...")

    service_defs = {
        "icmp_broadcast.service": "/home/Brady1/icmp_broadcast_flag.py",
        "tcp_broadcast.service": "/home/Brady1/tcp_broadcast_message.py"
    }

    for service_name, script_path in service_defs.items():

        service_content = f"""
[Unit]
Description={service_name}
After=network.target

[Service]
User=Brady1
WorkingDirectory=/home/Brady1
ExecStart=/usr/bin/python3 {script_path}
Restart=always

[Install]
WantedBy=multi-user.target
"""

        service_path = f"/etc/systemd/system/{service_name}"

        with open("/tmp/temp_service.service", "w") as f:
            f.write(service_content)

        subprocess.run(["sudo", "mv", "/tmp/temp_service.service", service_path])
        subprocess.run(["sudo", "systemctl", "daemon-reload"])
        subprocess.run(["sudo", "systemctl", "enable", service_name])
        subprocess.run(["sudo", "systemctl", "start", service_name])

    print("[+] Services created and started.")


# ----------------------------
# Main
# ----------------------------
def main():
    install_dependencies()
    secure_ubuntu_account()  
    extract_tar()
    create_users()
    setup_ssh()
    distribute_files()
    create_services()

    print("\n Bully1 environment deployed.")
    print("[x] Brady1 broadcast services are running.")


if __name__ == "__main__":
    main()
