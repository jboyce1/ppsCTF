import os
import subprocess
import sys

def run_cmd(cmd, exit_on_fail=True):
    proc = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if proc.returncode != 0:
        print(f"[!] Error running: {cmd}")
        print(proc.stderr)
        if exit_on_fail:
            sys.exit(1)
    return proc.stdout

def remove_broken_repo():
    """Remove any broken Microsoft VSCode repo if it exists."""
    broken_repo = "/etc/apt/sources.list.d/vscode.list"
    if os.path.exists(broken_repo):
        print("[+] Removing broken Microsoft repo (vscode.list)...")
        run_cmd(f"sudo rm -f {broken_repo}", exit_on_fail=False)

def install_vsftpd():
    """Install vsftpd (FTP server) on Ubuntu/Debian."""
    print("[+] Installing vsftpd...")
    run_cmd("sudo apt update -y")
    run_cmd("sudo apt install -y vsftpd")

def configure_vsftpd():
    """
    Sets anonymous_enable=YES in /etc/vsftpd.conf
    Removing old lines to avoid duplicates.
    """
    conf_file = "/etc/vsftpd.conf"

    print("[+] Removing existing anonymous_enable lines...")
    run_cmd(f"sudo sed -i '/^anonymous_enable/d' {conf_file}", exit_on_fail=False)
    run_cmd(f"sudo sed -i '/^#anonymous_enable/d' {conf_file}", exit_on_fail=False)

    print("[+] Enabling anonymous FTP (read-only)...")
    # Append the new setting
    run_cmd(f"echo 'anonymous_enable=YES' | sudo tee -a {conf_file}")

    # Optionally ensure write is disabled (for read-only)
    # run_cmd(f"echo 'anon_upload_enable=NO' | sudo tee -a {conf_file}")
    # run_cmd(f"echo 'anon_mkdir_write_enable=NO' | sudo tee -a {conf_file}")

def restart_vsftpd():
    """Restart vsftpd service."""
    print("[+] Restarting vsftpd...")
    run_cmd("sudo systemctl restart vsftpd")

def verify_ftp_port():
    """Check if vsftpd is listening on port 21."""
    print("[+] Checking if vsftpd is listening on port 21...")
    out = run_cmd("sudo netstat -tulnp || sudo ss -tulnp", exit_on_fail=False)
    if ":21" not in out:
        print("[-] vsftpd does NOT appear to be listening on port 21!")
        print("    Possibly a firewall or config issue. Check /etc/vsftpd.conf or /var/log/syslog.")
        sys.exit(1)
    print("[+] vsftpd is listening on port 21!\n")

def main():
    remove_broken_repo()
    install_vsftpd()
    configure_vsftpd()
    restart_vsftpd()
    verify_ftp_port()

    print("[+] Anonymous FTP is now enabled. By default, this is read-only.")
    print("[+] Try: ftp <SERVER_IP>, then log in as 'anonymous' with any password.")

if __name__ == "__main__":
    main()
