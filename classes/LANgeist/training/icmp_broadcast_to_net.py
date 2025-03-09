import subprocess
import time
import signal
import sys
import re

# === AUTO-INSTALL SCAPY IF MISSING ===
try:
    from scapy.all import send, IP, ICMP
except ImportError:
    print("[!] Scapy not found. Installing it now...")
    subprocess.run(["sudo", "apt", "update", "-y"], capture_output=True, text=True)
    subprocess.run(["sudo", "apt", "install", "python3-scapy", "-y"], capture_output=True, text=True)
    from scapy.all import send, IP, ICMP  # Retry import after installation

# === CONFIGURATION: Customize Your Flag and Timing Here ===
BOX_VALUE = "1"                # Change the box difficulty
CHALLENGE_VALUE = "1"          # Change the challenge level
INSERT_FLAG_CODE = "geist01"   # Change this to update the challenge flag
BROADCAST_INTERVAL = 5         # Time in seconds between broadcasts

# Generate the flag format
FLAG = f"pps{{{BOX_VALUE}x{CHALLENGE_VALUE}_geist_{INSERT_FLAG_CODE}}}"

# Graceful shutdown on Ctrl+C
def handle_exit(sig, frame):
    print("\n[!] Stopping ICMP Broadcaster...")
    sys.exit(0)

signal.signal(signal.SIGINT, handle_exit)

# Function to detect the real subnet using `ip route`
def detect_real_subnet():
    print("[+] Detecting the actual subnet...")

    try:
        ip_route_output = subprocess.run(["ip", "-o", "route", "show", "default"], capture_output=True, text=True)
        match = re.search(r'default via (\d+\.\d+\.\d+\.\d+) dev (\S+)', ip_route_output.stdout)

        if match:
            gateway_ip, interface = match.groups()
            print(f"[+] Detected gateway: {gateway_ip} on interface: {interface}")

            # Get subnet details
            ip_addr_output = subprocess.run(["ip", "-o", "-f", "inet", "addr", "show", interface], capture_output=True, text=True)
            subnet_match = re.search(r'inet (\d+\.\d+\.\d+\.\d+)/(\d+)', ip_addr_output.stdout)
            
            if subnet_match:
                subnet_ip, cidr = subnet_match.groups()
                subnet = f"{subnet_ip}/{cidr}"
                print(f"[+] Adjusted subnet based on interface {interface}: {subnet}")
                return subnet

    except Exception as e:
        print(f"[!] Failed to detect network via `ip route`: {e}")
    
    return None

# Function to verify live hosts using `arp -a`
def verify_live_hosts():
    print("[+] Checking ARP table for active hosts...")

    try:
        arp_output = subprocess.run(["arp", "-a"], capture_output=True, text=True)
        ip_matches = re.findall(r'\((\d+\.\d+\.\d+\.\d+)\)', arp_output.stdout)

        if ip_matches:
            print(f"[+] Found {len(ip_matches)} potential live hosts from ARP cache.")
            return ip_matches
        else:
            print("[-] No active hosts detected in ARP table.")
            return []

    except Exception as e:
        print(f"[!] Error checking ARP table: {e}")
        return []

# Function to discover live hosts using `nmap`
def discover_hosts(subnet):
    print(f"[+] Scanning network for live hosts in range: {subnet} (this may take a moment)...")

    try:
        result = subprocess.run(["nmap", "-sn", subnet], capture_output=True, text=True)
        hosts = [line.split()[4] for line in result.stdout.split("\n") if "Nmap scan report for" in line]

        if not hosts:
            print("[-] No live hosts found.")
        else:
            print(f"[+] Found {len(hosts)} live hosts: {', '.join(hosts[:5])}...")

        return hosts
    except Exception as e:
        print(f"[!] Error running nmap scan: {e}")
        return []

# Function to broadcast ICMP packets with the flag
def send_icmp_broadcast(live_hosts, flag):
    if not live_hosts:
        print("[-] No hosts available to send ICMP messages.")
        return

    print(f"[+] Sending ICMP packets to {len(live_hosts)} hosts...")
    for host in live_hosts:
        send(IP(dst=host)/ICMP()/flag, verbose=0)

# Main loop
def main():
    detected_subnet = detect_real_subnet()
    if not detected_subnet:
        print("[!] Could not determine network. Exiting.")
        sys.exit(1)

    # First, check ARP for already known live hosts
    live_hosts = verify_live_hosts()

    # If ARP didn't find anything, fall back to an nmap scan
    if not live_hosts:
        live_hosts = discover_hosts(detected_subnet)

    # Broadcast flag to discovered hosts
    send_icmp_broadcast(live_hosts, FLAG)

    while True:
        print(f"[+] Sleeping for {BROADCAST_INTERVAL} seconds before next scan...")
        time.sleep(BROADCAST_INTERVAL)
        live_hosts = verify_live_hosts() or discover_hosts(detected_subnet)
        send_icmp_broadcast(live_hosts, FLAG)

if __name__ == "__main__":
    main()
