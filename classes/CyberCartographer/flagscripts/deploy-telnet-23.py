import os
import subprocess
import sys

def run_cmd(cmd, exit_on_fail=True):
    """Run a shell command, optionally exiting on error."""
    proc = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if proc.returncode != 0:
        print(f"[!] Error running: {cmd}")
        print(proc.stderr)
        if exit_on_fail:
            sys.exit(1)
    return proc.stdout

def main():
    print("[+] Removing any broken Microsoft VSCode repo (if present)...")
    if os.path.exists("/etc/apt/sources.list.d/vscode.list"):
        run_cmd("sudo rm -f /etc/apt/sources.list.d/vscode.list")

    print("[+] Updating package lists...")
    run_cmd("sudo apt update -y")

    print("[+] Installing telnetd, xinetd, net-tools...")
    run_cmd("sudo apt install -y telnetd xinetd net-tools")

    print("[+] Stopping conflicting telnet.socket if running...")
    run_cmd("sudo systemctl stop telnet.socket || true", exit_on_fail=False)
    run_cmd("sudo systemctl disable telnet.socket || true", exit_on_fail=False)

    print("[+] Stopping xinetd before applying new config...")
    run_cmd("sudo systemctl stop xinetd", exit_on_fail=False)

    # Write a basic telnet config to /etc/xinetd.d/telnet
    print("[+] Creating /etc/xinetd.d/telnet config for port 23...")
    telnet_config = """service telnet
{
    disable         = no
    socket_type     = stream
    protocol        = tcp
    wait            = no
    user            = root
    server          = /usr/sbin/in.telnetd
    log_on_failure  += USERID
    bind            = 0.0.0.0
    port            = 23
}
"""
    with open("/tmp/telnet_xinetd.conf", "w") as f:
        f.write(telnet_config)

    run_cmd("sudo mv /tmp/telnet_xinetd.conf /etc/xinetd.d/telnet")

    print("[+] Enabling xinetd at startup...")
    run_cmd("sudo systemctl enable xinetd")

    print("[+] Restarting xinetd to apply telnet config...")
    run_cmd("sudo systemctl restart xinetd")

    print("[+] Checking if telnet is listening on port 23...")
    netstat_output = run_cmd("sudo netstat -tuln || sudo ss -tulnp", exit_on_fail=False)
    if ":23" not in netstat_output:
        print("[-] Telnet does NOT appear to be running on port 23.")
        print("    Possibly an IPv6 issue or xinetd didn't load properly.")
        sys.exit(1)

    print("\n Telnet is running on port 23")
    print("Try: telnet localhost 23")
    print("\nAll done.")

if __name__ == "__main__":
    main()
