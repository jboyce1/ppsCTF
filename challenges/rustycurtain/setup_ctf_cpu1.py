import os
import subprocess
import shutil

# Paths for repositories and extracted files
repo_url = "https://github.com/jboyce1/ppsCTF.git"
repo_dir = "/home/$(logname)/ppsCTF"
challenge_dir = f"{repo_dir}/challenges/rustycurtain"

# ZIP files and their contents
zip_files = {
    "ivan.zip": "ftp",
    "tanya.zip": "Desktop",
    "boris.zip": "Desktop"
}

# Users to create
users = {
    "ivan": {
        "password": "TheT3rrible",
        "zip": "ivan.zip",
        "script": "ftp-anon-login.py",
        "service": "ftp",
    },
    "tanya": {
        "password": "L3tsG0",
        "zip": "tanya.zip",
        "script": "deploy-telnet-23.py",
        "service": "telnet",
    },
    "boris": {
        "password": "Pieinth3sky",
        "zip": "boris.zip",
        "script": None,  # SSH handled separately
        "service": "ssh",
    }
}

def run_command(command):
    """Run a shell command and return the output."""
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {command}\n{e}")

def setup_repo():
    """Clone the repository if it doesn't exist."""
    if not os.path.exists(repo_dir):
        run_command(f"git clone {repo_url} {repo_dir}")

def extract_zip_files():
    """Extracts the required ZIP files into their respective directories."""
    for zip_file, target_dir in zip_files.items():
        zip_path = f"{challenge_dir}/{zip_file}"
        extract_path = f"/tmp/{target_dir}"
        if os.path.exists(zip_path):
            run_command(f"unzip -o {zip_path} -d {extract_path}")

def create_user(username, password):
    """Create a user and set their password."""
    run_command(f"sudo adduser --gecos '' --disabled-password {username}")
    run_command(f"echo '{username}:{password}' | sudo chpasswd")
    run_command(f"sudo usermod -L {username}")  # Locking password reset ability
    run_command(f"sudo deluser {username} sudo")  # Remove sudo privileges

def deploy_files(username, directory):
    """Move extracted files to the appropriate user's home directory."""
    source_path = f"/tmp/{directory}"
    target_path = f"/home/{username}/{directory}"
    if os.path.exists(source_path):
        shutil.move(source_path, target_path)
        run_command(f"sudo chown -R {username}:{username} {target_path}")

def enable_ftp_anonymous():
    """Enable anonymous FTP login for ivan."""
    script_path = f"{challenge_dir}/ftp-anon-login.py"
    if os.path.exists(script_path):
        run_command(f"sudo python3 {script_path}")

def enable_telnet():
    """Enable Telnet service for tanya."""
    script_path = f"{challenge_dir}/deploy-telnet-23.py"
    if os.path.exists(script_path):
        run_command(f"sudo python3 {script_path}")

def enable_ssh():
    """Enable SSH password authentication and restart SSH service."""
    ssh_config_cmd = "sudo sed -i 's/^#\\?PasswordAuthentication .*/PasswordAuthentication yes/' /etc/ssh/sshd_config"
    run_command(ssh_config_cmd)
    run_command("sudo systemctl restart ssh")

def setup_users():
    """Create users, configure services, and deploy files."""
    for user, info in users.items():
        create_user(user, info["password"])
        deploy_files(user, zip_files[info["zip"]])

        if info["service"] == "ftp":
            enable_ftp_anonymous()
        elif info["service"] == "telnet":
            enable_telnet()
        elif info["service"] == "ssh":
            enable_ssh()

def main():
    print("Setting up the Rusty Curtain CTF environment...")
    setup_repo()
    extract_zip_files()
    setup_users()
    print("Setup complete!")

if __name__ == "__main__":
    main()
