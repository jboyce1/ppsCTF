#!/usr/bin/env python3
import os
import subprocess
import logging
import zipfile
import shutil

# -----------------------------------------------------------------------------
# Configure Logging
# -----------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# -----------------------------------------------------------------------------
# Global Variables
# -----------------------------------------------------------------------------
CURRENT_USER = os.getlogin()
GITHUB_REPO_URL = "https://github.com/jboyce1/ppsCTF.git"
LOCAL_REPO_PATH = f"/home/{CURRENT_USER}/ppsCTF"

# Challenge sub-directory containing the ZIP files
CHALLENGES_PATH = os.path.join(LOCAL_REPO_PATH, "challenges", "rustycurtain")

# Define user accounts, passwords, and ZIP files
USERS = [
    {
        "username": "ivan",
        "password": "TheT3rrible",
        "zip_file": "ivan.zip",
        "extract_to": "/srv/ftp",        # for FTP (anonymous)
    },
    {
        "username": "tanya",
        "password": "L3tsG0",
        "zip_file": "tanya.zip",
        "extract_to": "/home/tanya/Desktop",  # for Telnet
    },
    {
        "username": "boris",
        "password": "Pieinth3sky",
        "zip_file": "boris.zip",
        "extract_to": "/home/boris/Desktop",  # for SSH
    }
]

# -----------------------------------------------------------------------------
# Helper Functions
# -----------------------------------------------------------------------------
def run_command(command_list, check=True, capture_output=False, input_data=None):
    """
    Safely run a shell command via subprocess.
    :param command_list: list of command + arguments
    :param check: raise an error if command fails
    :param capture_output: capture stdout/stderr if True
    :param input_data: optional data passed to subprocess stdin
    :return: CompletedProcess instance
    """
    logging.debug(f"Running command: {' '.join(command_list)}")
    return subprocess.run(
        command_list,
        check=check,
        capture_output=capture_output,
        input=input_data
    )

def clone_repo_if_needed():
    """
    Clone the GitHub repo if it doesn't exist, otherwise pull the latest.
    """
    if not os.path.isdir(LOCAL_REPO_PATH):
        logging.info(f"Cloning {GITHUB_REPO_URL} -> {LOCAL_REPO_PATH} ...")
        run_command(["git", "clone", GITHUB_REPO_URL, LOCAL_REPO_PATH])
    else:
        logging.info(f"Repository already at {LOCAL_REPO_PATH}. Pulling latest changes...")
        run_command(["git", "-C", LOCAL_REPO_PATH, "pull"])

def create_user(username, password):
    """
    Create a Linux user if not exists and set the password.
    """
    try:
        subprocess.run(["id", username], check=True, capture_output=True)
        user_exists = True
    except subprocess.CalledProcessError:
        user_exists = False

    if not user_exists:
        logging.info(f"Creating user '{username}'...")
        run_command(["useradd", "-m", "-s", "/bin/bash", username])
    else:
        logging.info(f"User '{username}' already exists. Skipping creation...")

    # Set or update password
    logging.info(f"Setting password for user '{username}'...")
    run_command(["chpasswd"], input_data=f"{username}:{password}".encode("utf-8"))

def ensure_directory(path, owner=None, mode=None):
    """
    Ensure a directory exists, optionally set owner and mode.
    """
    if not os.path.isdir(path):
        os.makedirs(path, exist_ok=True)
    if owner:
        run_command(["chown", owner, path])
    if mode:
        run_command(["chmod", mode, path])

def extract_zip_no_nesting(zip_path, dest_path):
    """
    Extract the contents of a ZIP file into dest_path, avoiding nested directories.
    """
    if not os.path.isfile(zip_path):
        logging.error(f"ZIP file not found: {zip_path}")
        return

    logging.info(f"Extracting {zip_path} -> {dest_path}")
    ensure_directory(dest_path)

    # Temporary extraction folder
    temp_extract_path = "/tmp/ctf_extract_temp"
    if os.path.exists(temp_extract_path):
        shutil.rmtree(temp_extract_path)
    os.makedirs(temp_extract_path)

    # Extract to temp
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(temp_extract_path)

    # Move items from temp's top-level into dest_path
    for root, dirs, files in os.walk(temp_extract_path, topdown=True):
        # Move directories
        for d in dirs:
            src_dir = os.path.join(root, d)
            for item in os.listdir(src_dir):
                src_item = os.path.join(src_dir, item)
                dst_item = os.path.join(dest_path, item)
                shutil.move(src_item, dst_item)
            break  # Only handle top-level
        # Move files
        for f in files:
            src_file = os.path.join(root, f)
            dst_file = os.path.join(dest_path, f)
            shutil.move(src_file, dst_file)
        break  # top-level only

    shutil.rmtree(temp_extract_path)

def configure_ftp():
    """
    Install and configure vsftpd for anonymous (read-only) access.
    """
    logging.info("Installing and configuring vsftpd (FTP)...")
    run_command(["apt-get", "update"])
    run_command(["apt-get", "-y", "install", "vsftpd"])

    vsftpd_config = "/etc/vsftpd.conf"
    backup_config = "/etc/vsftpd.conf.bak"
    if not os.path.isfile(backup_config):
        shutil.copyfile(vsftpd_config, backup_config)

    # Force 'anonymous_enable=YES' in config
    new_config_lines = []
    with open(backup_config, 'r') as f:
        for line in f:
            if line.strip().startswith("anonymous_enable"):
                new_config_lines.append("anonymous_enable=YES\n")
            else:
                new_config_lines.append(line)

    # If missing, append
    if not any("anonymous_enable" in line for line in new_config_lines):
        new_config_lines.append("anonymous_enable=YES\n")

    # Write updated config
    with open(vsftpd_config, 'w') as f:
        f.writelines(new_config_lines)

    # Ensure /srv/ftp exists
    ensure_directory("/srv/ftp")
    # Make /srv/ftp owned by root:root and not writable by others (755)
    run_command(["chown", "root:root", "/srv/ftp"])
    run_command(["chmod", "755", "/srv/ftp"])

    # Enable and restart vsftpd
    run_command(["systemctl", "enable", "vsftpd"])
    run_command(["systemctl", "restart", "vsftpd"])

def configure_telnet():
    """
    Install & enable Telnet via xinetd for Tanya.
    """
    logging.info("Installing and configuring Telnet (xinetd)...")
    run_command(["apt-get", "update"])
    run_command(["apt-get", "-y", "install", "xinetd", "telnetd"])

    telnet_config = "/etc/xinetd.d/telnet"
    if not os.path.isfile(telnet_config):
        config_text = """# Telnet service via xinetd
service telnet
{
    disable         = no
    socket_type     = stream
    wait            = no
    user            = root
    log_on_failure  += USERID
    log_on_success  += USERID
    server          = /usr/sbin/in.telnetd
    bind            = 0.0.0.0
    port            = 23
}
"""
        with open(telnet_config, 'w') as f:
            f.write(config_text)

    run_command(["systemctl", "enable", "xinetd"])
    run_command(["systemctl", "restart", "xinetd"])

def configure_ssh():
    """
    Install and configure SSH with password authentication for Boris.
    """
    logging.info("Installing and configuring OpenSSH (SSH)...")
    run_command(["apt-get", "update"])
    run_command(["apt-get", "-y", "install", "openssh-server"])

    ssh_config_file = "/etc/ssh/sshd_config"
    backup_config = "/etc/ssh/sshd_config.bak"
    if not os.path.isfile(backup_config):
        shutil.copyfile(ssh_config_file, backup_config)

    # Ensure PasswordAuthentication is yes
    new_config_lines = []
    with open(backup_config, 'r') as f:
        for line in f:
            if line.strip().startswith("PasswordAuthentication"):
                new_config_lines.append("PasswordAuthentication yes\n")
            else:
                new_config_lines.append(line)

    if not any("PasswordAuthentication" in line for line in new_config_lines):
        new_config_lines.append("PasswordAuthentication yes\n")

    with open(ssh_config_file, 'w') as f:
        f.writelines(new_config_lines)

    run_command(["systemctl", "enable", "ssh"])
    run_command(["systemctl", "restart", "ssh"])

def verify_service(service_name):
    """
    Verify that a given service (systemd) is active.
    """
    try:
        result = run_command(["systemctl", "is-active", service_name], capture_output=True)
        status = result.stdout.decode().strip()
        if status == "active":
            logging.info(f"Service '{service_name}' is active.")
        else:
            logging.warning(f"Service '{service_name}' is NOT active (status={status}).")
    except subprocess.CalledProcessError:
        logging.error(f"Failed to verify service '{service_name}'.")

# -----------------------------------------------------------------------------
# Main Function
# -----------------------------------------------------------------------------
def main():
    # 1) Clone or update the GitHub repo
    clone_repo_if_needed()

    # 2) Create/Update user accounts
    for user in USERS:
        create_user(user["username"], user["password"])

    # 3) Extract each user's ZIP file to the correct location
    for user in USERS:
        zip_file_path = os.path.join(CHALLENGES_PATH, user["zip_file"])
        extract_zip_no_nesting(zip_file_path, user["extract_to"])

        # Ownership rules
        if user["username"] == "ivan":
            # For anonymous FTP, we keep /srv/ftp owned by root:root + chmod 755
            # so do NOT set ftp:ftp ownership (which triggers chroot error).
            pass
        else:
            # For tanya, boris => own their Desktop files
            run_command(["chown", "-R", f"{user['username']}:{user['username']}", user["extract_to"]])

    # 4) Configure vsftpd, Telnet, and SSH
    configure_ftp()
    configure_telnet()
    configure_ssh()

    # 5) Verify services are running
    verify_service("vsftpd")  # FTP
    verify_service("xinetd")  # Telnet
    verify_service("ssh")     # SSH

    logging.info("CTF environment setup complete!")
    logging.info("Use ftp/telnet/ssh to test. Anonymous FTP will be read-only without the OOPS error.")

if __name__ == "__main__":
    main()
