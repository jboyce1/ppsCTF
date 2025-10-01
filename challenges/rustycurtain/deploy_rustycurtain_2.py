#!/usr/bin/env python3
import os
import random
import subprocess
import sys
import zipfile
import shutil
import logging

# -----------------------------------------------------------------------------
# Logging Setup
# -----------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# -----------------------------------------------------------------------------
# Git Repo Constants
# -----------------------------------------------------------------------------
GITHUB_REPO_URL = "https://github.com/jboyce1/ppsCTF.git"

# We assume you're 'ubuntu', but use getlogin() to be dynamic
CURRENT_USER = os.getlogin()
LOCAL_REPO_PATH = f"/home/{CURRENT_USER}/ppsCTF"

# Challenges folder containing the ZIP files
CHALLENGES_DIR = os.path.join(LOCAL_REPO_PATH, "challenges", "rustycurtain")

NIKOLI_ZIP = os.path.join(CHALLENGES_DIR, "nikoli.zip")   # has ftp/ (somewhere)
YURI_ZIP   = os.path.join(CHALLENGES_DIR, "yuri.zip")     # has Desktop/ & firefox/ (somewhere)

# -----------------------------------------------------------------------------
# User/Password Constants
# -----------------------------------------------------------------------------
NIKOLI_USER = "nikoli"
NIKOLI_PASS = "t3sL@"

YURI_USER   = "yuri"
YURI_PASS   = "Vostok1"

# -----------------------------------------------------------------------------
# High-port range for random FTP & SSH
# -----------------------------------------------------------------------------
PORT_LOW  = 21000
PORT_HIGH = 24000

# -----------------------------------------------------------------------------
# Subprocess Helper
# -----------------------------------------------------------------------------
def run_command(cmd, exit_on_fail=True):
    """
    Runs a shell command. If 'exit_on_fail' is True and the command fails,
    we log an error and exit. Otherwise, we log a warning and continue.
    Returns stdout on success, or '' on fail if exit_on_fail=False.
    """
    logging.debug(f"Running command: {cmd}")
    proc = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if proc.returncode != 0:
        stderr_str = proc.stderr.strip()
        logging.debug(f"STDERR: {stderr_str}")
        if exit_on_fail:
            logging.error(f"Command failed: {cmd}")
            sys.exit(1)
        else:
            logging.warning(f"Command failed (continuing anyway): {cmd}")
            return ""
    return proc.stdout

# -----------------------------------------------------------------------------
# Git Clone/Update
# -----------------------------------------------------------------------------
def clone_or_update_repo():
    """
    Clone the GitHub repo if not present. Otherwise, pull the latest changes.
    """
    if not os.path.isdir(LOCAL_REPO_PATH):
        logging.info(f"Cloning repository from {GITHUB_REPO_URL} to {LOCAL_REPO_PATH}...")
        run_command(f"git clone {GITHUB_REPO_URL} {LOCAL_REPO_PATH}")
    else:
        logging.info(f"Repository already at {LOCAL_REPO_PATH}. Pulling latest changes...")
        run_command(f"git -C {LOCAL_REPO_PATH} pull")

# -----------------------------------------------------------------------------
# User Management
# -----------------------------------------------------------------------------
def user_exists(username):
    """
    Return True if 'username' exists, False otherwise.
    """
    proc = subprocess.run(["id", username], capture_output=True, text=True)
    return (proc.returncode == 0)

def create_user(username, password):
    """
    Create user if needed, set password, remove from sudo group if present.
    """
    logging.info(f"Ensuring user '{username}' exists...")

    if not user_exists(username):
        logging.info(f"Creating user '{username}'...")
        run_command(f"sudo useradd -m -s /bin/bash {username}", exit_on_fail=False)
    else:
        logging.info(f"User '{username}' already exists. Skipping creation.")

    logging.info(f"Setting password for user '{username}'...")
    run_command(f"echo '{username}:{password}' | sudo chpasswd", exit_on_fail=False)

    # Ensure user isn't in sudo
    logging.info(f"Removing '{username}' from any 'sudo' group membership...")
    run_command(f"sudo deluser {username} sudo", exit_on_fail=False)

# -----------------------------------------------------------------------------
# Directory-Finder (case-insensitive)
# -----------------------------------------------------------------------------
def find_subdir_case_insensitive(base_dir, target):
    """
    Searches 'base_dir' recursively for a folder whose name matches 'target'
    (case-insensitive). Returns the path to that folder if found, else None.
    """
    for root, dirs, files in os.walk(base_dir):
        for d in dirs:
            if d.lower() == target.lower():
                return os.path.join(root, d)
    return None

# -----------------------------------------------------------------------------
# Extraction for nikoli.zip (FTP)
# -----------------------------------------------------------------------------
def extract_nikoli_zip(zip_file, dest_path):
    """
    Extracts nikoli.zip to a temp folder, searches for 'ftp' dir anywhere,
    and moves its contents into /srv (dest_path).
    """
    if not os.path.isfile(zip_file):
        logging.warning(f"ZIP file '{zip_file}' not found. Skipping extraction.")
        return

    logging.info(f"Extracting {zip_file} -> temp folder, looking for 'ftp' dir...")

    tmp_dir = "/tmp/nikoli_extract"
    if os.path.exists(tmp_dir):
        shutil.rmtree(tmp_dir)
    os.makedirs(tmp_dir)

    with zipfile.ZipFile(zip_file, 'r') as zf:
        zf.extractall(tmp_dir)

    # Find 'ftp' (case-insensitive)
    ftp_dir = find_subdir_case_insensitive(tmp_dir, "ftp")
    if ftp_dir and os.path.isdir(ftp_dir):
        logging.info(f"Found ftp folder: {ftp_dir} -- moving contents to {dest_path}")
        # Make sure /srv exists
        run_command(f"sudo mkdir -p {dest_path}", exit_on_fail=False)
        for item in os.listdir(ftp_dir):
            src = os.path.join(ftp_dir, item)
            dst = os.path.join(dest_path, item)
            shutil.move(src, dst)
    else:
        logging.warning(f"No 'ftp' folder found anywhere in {zip_file}.")

    shutil.rmtree(tmp_dir)

# -----------------------------------------------------------------------------
# Extraction for yuri.zip (Desktop & firefox)
# -----------------------------------------------------------------------------
def extract_yuri_zip(zip_file, yuri_home):
    """
    Extracts yuri.zip, searches for 'Desktop' and 'firefox' dirs anywhere,
    and moves their contents to:
      Desktop => /home/yuri/Desktop
      firefox => /home/yuri/.mozilla/firefox
    """
    if not os.path.isfile(zip_file):
        logging.warning(f"ZIP file '{zip_file}' not found. Skipping extraction.")
        return

    logging.info(f"Extracting {zip_file} -> temp folder, looking for Desktop & firefox...")

    tmp_dir = "/tmp/yuri_extract"
    if os.path.exists(tmp_dir):
        shutil.rmtree(tmp_dir)
    os.makedirs(tmp_dir)

    with zipfile.ZipFile(zip_file, 'r') as zf:
        zf.extractall(tmp_dir)

    # Ensure Desktop & firefox paths exist
    desktop_path = os.path.join("/home", yuri_home, "Desktop")
    firefox_path = os.path.join("/home", yuri_home, ".mozilla", "firefox")
    run_command(f"sudo mkdir -p {desktop_path}", exit_on_fail=False)
    run_command(f"sudo mkdir -p {firefox_path}", exit_on_fail=False)

    # 1) Find 'Desktop' folder
    desktop_dir = find_subdir_case_insensitive(tmp_dir, "desktop")
    if desktop_dir and os.path.isdir(desktop_dir):
        logging.info(f"Found Desktop folder: {desktop_dir} -- moving contents into {desktop_path}")
        for item in os.listdir(desktop_dir):
            src = os.path.join(desktop_dir, item)
            dst = os.path.join(desktop_path, item)
            shutil.move(src, dst)
    else:
        logging.warning(f"No 'Desktop' folder found anywhere in {zip_file}.")

    # 2) Find 'firefox' folder
    firefox_dir = find_subdir_case_insensitive(tmp_dir, "firefox")
    if firefox_dir and os.path.isdir(firefox_dir):
        logging.info(f"Found firefox folder: {firefox_dir} -- moving contents into {firefox_path}")
        for item in os.listdir(firefox_dir):
            src = os.path.join(firefox_dir, item)
            dst = os.path.join(firefox_path, item)
            shutil.move(src, dst)
    else:
        logging.warning(f"No 'firefox' folder found anywhere in {zip_file}.")

    shutil.rmtree(tmp_dir)

    # Fix ownership
    run_command(f"sudo chown -R {yuri_home}:{yuri_home} {desktop_path}", exit_on_fail=False)
    run_command(f"sudo chown -R {yuri_home}:{yuri_home} /home/{yuri_home}/.mozilla", exit_on_fail=False)

# -----------------------------------------------------------------------------
# FTP Setup (Random High Port)
# -----------------------------------------------------------------------------
def setup_ftp_on_random_port():
    random_port = random.randint(PORT_LOW, PORT_HIGH)
    logging.info("[FTP] Installing vsftpd + net-tools...")
    run_command("sudo apt-get update -y")
    run_command("sudo apt-get install -y vsftpd net-tools")

    logging.info("[FTP] Stopping vsftpd if running...")
    run_command("sudo systemctl stop vsftpd", exit_on_fail=False)

    vsftpd_conf = "/etc/vsftpd.conf"
    # Remove old references
    patterns = ["listen_port", "^listen=", "^listen_ipv6=", "^anonymous_enable"]
    for pat in patterns:
        run_command(f"sudo sed -i '/{pat}/d' {vsftpd_conf}", exit_on_fail=False)
        run_command(f"sudo sed -i '/#{pat}/d' {vsftpd_conf}", exit_on_fail=False)

    # Append new lines
    logging.info(f"[FTP] Configuring vsftpd on port {random_port} (anonymous).")
    conf_lines = [
        "listen=YES",
        "listen_ipv6=NO",
        f"listen_port={random_port}",
        "anonymous_enable=YES"
    ]
    for line in conf_lines:
        run_command(f"echo '{line}' | sudo tee -a {vsftpd_conf}", exit_on_fail=False)

    run_command("sudo systemctl enable vsftpd")
    run_command("sudo systemctl restart vsftpd")

    logging.info(f"[FTP] Verifying vsftpd on port {random_port}...")
    net_check = run_command("sudo netstat -tulnp || sudo ss -tulnp", exit_on_fail=False)
    if f":{random_port}" not in net_check:
        logging.warning("[FTP] vsftpd not detected on that port (could be IPv6 or config).")

    return random_port

# -----------------------------------------------------------------------------
# SSH Setup (Random High Port)
# -----------------------------------------------------------------------------
def setup_ssh_on_random_port():
    random_port = random.randint(PORT_LOW, PORT_HIGH)
    logging.info("[SSH] Installing OpenSSH server + net-tools...")
    run_command("sudo apt-get update -y")
    run_command("sudo apt-get install -y openssh-server net-tools")

    sshd_conf = "/etc/ssh/sshd_config"
    logging.info("[SSH] Removing old 'Port' lines...")
    run_command(f"sudo sed -i '/^Port /d' {sshd_conf}", exit_on_fail=False)
    run_command(f"sudo sed -i '/^#Port /d' {sshd_conf}", exit_on_fail=False)

    logging.info(f"[SSH] Setting random SSH port: {random_port}")
    run_command(f"echo 'Port {random_port}' | sudo tee -a {sshd_conf}", exit_on_fail=False)

    logging.info("[SSH] Enabling password authentication...")
    run_command(f"sudo sed -i 's/^#PasswordAuthentication no/PasswordAuthentication yes/' {sshd_conf}", exit_on_fail=False)
    run_command(f"sudo sed -i 's/^PasswordAuthentication no/PasswordAuthentication yes/' {sshd_conf}", exit_on_fail=False)

    run_command("sudo systemctl enable ssh")
    run_command("sudo systemctl restart ssh")

    logging.info(f"[SSH] Verifying SSH on port {random_port}...")
    net_check = run_command("sudo netstat -tulnp || sudo ss -tulnp", exit_on_fail=False)
    if f":{random_port}" not in net_check:
        logging.warning(f"[SSH] Not detected on port {random_port}. Check logs if needed.")

    return random_port

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------
def main():
    # 1) Clone (or update) the repo so we have nikoli.zip & yuri.zip
    clone_or_update_repo()

    # 2) Create users (nikoli & yuri) with no sudo privileges
    create_user(NIKOLI_USER, NIKOLI_PASS)
    create_user(YURI_USER, YURI_PASS)

    # 3) Set up FTP on random port, then extract nikoli.zip => /srv
    ftp_port = setup_ftp_on_random_port()
    extract_nikoli_zip(NIKOLI_ZIP, "/srv")

    # 4) Set up SSH on random port, then extract yuri.zip => Desktop & firefox
    ssh_port = setup_ssh_on_random_port()
    extract_yuri_zip(YURI_ZIP, YURI_USER)

    # 5) Final info
    logging.info("---------------------------------------------------")
    logging.info("CTF2 Setup Complete! Sudo for 'ubuntu' is preserved.")
    logging.info(f"FTP (anonymous) on high port {ftp_port}")
    logging.info(f"SSH for user '{YURI_USER}' on high port {ssh_port} (pass: {YURI_PASS})")
    logging.info("Users 'nikoli' and 'yuri' have no sudo privileges.")
    logging.info("---------------------------------------------------")

if __name__ == "__main__":
    main()
