import os
import random
import subprocess
import sys

# === CONFIGURATION (Edit These Values) ===
BOX_VALUE = "1"          # e.g. "1"
CHALLENGE_VALUE = "3"    # e.g. "3"
PORT_LOW = 3000          # Minimum random port
PORT_HIGH = 10000        # Maximum random port

def run_cmd(cmd, exit_on_fail=True):
    proc = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if proc.returncode != 0 and exit_on_fail:
        print(f"[!] Error running: {cmd}")
        print(proc.stderr)
        sys.exit(1)
    return proc.stdout

def remove_broken_repo():
    """Remove any broken Microsoft repository if present."""
    broken_repo = "/etc/apt/sources.list.d/vscode.list"
    if os.path.exists(broken_repo):
        print("[+] Removing broken Microsoft repo...")
        run_cmd(f"sudo rm -f {broken_repo}", exit_on_fail=False)

def install_vsftpd():
    """Install vsftpd and net-tools to check ports with netstat/ss."""
    print("[+] Installing vsftpd and net-tools...")
    run_cmd("sudo apt update -y")
    run_cmd("sudo apt install -y vsftpd net-tools")

def stop_vsftpd():
    """Stop vsftpd before reconfiguring."""
    print("[+] Stopping vsftpd if running...")
    run_cmd("sudo systemctl stop vsftpd", exit_on_fail=False)

def configure_vsftpd(random_port):
    """
    Remove old lines referencing listen, listen_ipv6, anonymous_enable, and listen_port
    Then set up vsftpd to bind to random_port with anonymous access.
    """
    vsftpd_conf = "/etc/vsftpd.conf"
    print("[+] Removing old config lines for 'listen', 'listen_ipv6', 'anonymous_enable', 'listen_port'...")
    run_cmd(f"sudo sed -i '/^listen_port/d' {vsftpd_conf}", exit_on_fail=False)
    run_cmd(f"sudo sed -i '/^listen/d' {vsftpd_conf}", exit_on_fail=False)
    run_cmd(f"sudo sed -i '/^listen_ipv6/d' {vsftpd_conf}", exit_on_fail=False)
    run_cmd(f"sudo sed -i '/^anonymous_enable/d' {vsftpd_conf}", exit_on_fail=False)
    run_cmd(f"sudo sed -i '/^#anonymous_enable/d' {vsftpd_conf}", exit_on_fail=False)

    print(f"[+] Configuring vsftpd to listen on port {random_port}, enable anonymous FTP...")

    # We'll append the following lines:
    # listen=YES
    # listen_ipv6=NO
    # listen_port=<random_port>
    # anonymous_enable=YES (read-only)
    config_lines = [
        "listen=YES",
        "listen_ipv6=NO",
        f"listen_port={random_port}",
        "anonymous_enable=YES"
    ]

    for line in config_lines:
        run_cmd(f"echo '{line}' | sudo tee -a {vsftpd_conf}", exit_on_fail=False)

def restart_vsftpd():
    """Restart vsftpd to apply new config."""
    print("[+] Enabling vsftpd to start on boot...")
    run_cmd("sudo systemctl enable vsftpd")
    print("[+] Restarting vsftpd...")
    run_cmd("sudo systemctl restart vsftpd")

def verify_ftp_port(random_port):
    """Check if vsftpd is listening on the chosen random port."""
    print(f"[+] Checking if vsftpd is listening on port {random_port}...")
    out = run_cmd("sudo netstat -tulnp || sudo ss -tulnp", exit_on_fail=False)
    if f":{random_port}" not in out:
        print(f"[-] vsftpd does NOT appear on port {random_port}.")
        print("    Possibly IPv6 binding or environment limitations. Check /var/log/syslog or /etc/vsftpd.conf.")
        sys.exit(1)
    print(f"[+] vsftpd is running on port {random_port}!\n")

def main():
    # 1) Remove broken repos, install vsftpd
    remove_broken_repo()
    install_vsftpd()

    # 2) Stop vsftpd for reconfig
    stop_vsftpd()

    # 3) Pick random port in [PORT_LOW, PORT_HIGH]
    random_port = random.randint(PORT_LOW, PORT_HIGH)

    # 4) Configure vsftpd to bind to that random port with anonymous
    configure_vsftpd(random_port)

    # 5) Restart vsftpd
    restart_vsftpd()

    # 6) Verify vsftpd on the random port
    verify_ftp_port(random_port)

    # 7) Print final flag
    flag = f"pps{{{BOX_VALUE}x{CHALLENGE_VALUE}_ftp0rt#{random_port}}}"
    print(f"🎯 FLAG: {flag}\n")
    print("[+] Anonymous FTP is now enabled on that random port (read-only).")

if __name__ == "__main__":
    main()
