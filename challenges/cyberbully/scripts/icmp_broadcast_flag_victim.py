import subprocess
import time
import signal
import sys
import re
from scapy.all import send, IP, ICMP, Raw

# === AUTO-INSTALL SCAPY IF MISSING ===
try:
    from scapy.all import send, IP, ICMP, Raw
except ImportError:
    print("[!] Scapy not found. Installing it now...")
    subprocess.run(["sudo", "apt", "update", "-y"], capture_output=True, text=True)
    subprocess.run(["sudo", "apt", "install", "python3-scapy", "-y"], capture_output=True, text=True)
    from scapy.all import send, IP, ICMP, Raw  # Retry import after installation

# === CONFIGURATION: Customize Your Flag and Timing Here ===
BOX_VALUE = "1"                # Change the box difficulty
CHALLENGE_VALUE = "2"          # Change the challenge level
INSERT_FLAG_CODE = "Vict1mIP-sisters"   # Change this to update the challenge flag

NETWORK_RESCAN_INTERVAL = 600  # Rescan every 10 minutes (600 seconds)
BROADCAST_INTERVAL = 10        # Time between each burst wave (seconds)
DETECTED_HOSTS_FILE = "hosts.txt"  # File to store detected live hosts
BURST_COUNT = 5  # Number of ICMP packets per host per burst
PACKET_SIZE = 64  # Number of bytes in the ICMP payload
TOTAL_BURSTS = NETWORK_RESCAN_INTERVAL // BROADCAST_INTERVAL  # Total bursts before rescanning

# Generate the flag format
FLAG = f"pps{{{BOX_VALUE}x{CHALLENGE_VALUE}_geist_{INSERT_FLAG_CODE}}}"

# Graceful shutdown on Ctrl+C
def handle_exit(sig, frame):
    print("\n[!] Stopping ICMP Broadcaster...")
    sys.exit(0)

signal.signal(signal.SIGINT, handle_exit)

# Function to find the lowest IP from ARP table
def get_lowest_arp_ip():
    print("[+] Checking ARP table for active hosts...")

    try:
        arp_output = subprocess.run(["arp", "-a"], capture_output=True, text=True)
        ip_matches = re.findall(r'\((\d+\.\d+\.\d+\.\d+)\)', arp_output.stdout)

        if ip_matches:
            lowest_ip = sorted(ip_matches, key=lambda ip: list(map(int, ip.split('.'))))[0]
            print(f"[+] Lowest IP from ARP: {lowest_ip}")
            return lowest_ip
        else:
            print("[-] No active hosts detected in ARP table.")
            return None

    except Exception as e:
        print(f"[!] Error checking ARP table: {e}")
        return None

# Function to get subnet mask from `ip addr show`
def get_subnet_mask(interface):
    try:
        ip_output = subprocess.run(["ip", "-o", "-f", "inet", "addr", "show", interface], capture_output=True, text=True)
        match = re.search(r'inet (\d+\.\d+\.\d+\.\d+)/(\d+)', ip_output.stdout)
        if match:
            subnet_mask = match.group(2)
            print(f"[+] Detected subnet mask: /{subnet_mask}")
            return subnet_mask
    except Exception as e:
        print(f"[!] Failed to detect subnet mask: {e}")
    
    return None

# Function to detect the real network subnet using ARP + IP
def detect_real_subnet():
    print("[+] Detecting the actual subnet...")

    base_ip = get_lowest_arp_ip()
    if not base_ip:
        print("[!] Could not determine base IP. Exiting.")
        sys.exit(1)

    try:
        ip_route_output = subprocess.run(["ip", "-o", "route", "show", "default"], capture_output=True, text=True)
        match = re.search(r'default via (\d+\.\d+\.\d+\.\d+) dev (\S+)', ip_route_output.stdout)
        if match:
            interface = match.group(2)
            subnet_mask = get_subnet_mask(interface)
            if subnet_mask:
                subnet = f"{base_ip}/{subnet_mask}"
                print(f"[+] Using network subnet: {subnet}")
                return subnet
    except Exception as e:
        print(f"[!] Failed to detect network: {e}")

    return None

# Function to discover live hosts using nmap
def discover_hosts(subnet):
    print(f"[+] Scanning network for live hosts in {subnet} (this may take a few minutes)...")

    try:
        subprocess.run(
            f"sudo nmap -n -sn {subnet} -oG - | awk '/Up$/{{print $2}}' > {DETECTED_HOSTS_FILE}",
            shell=True,
            capture_output=False
        )

        with open(DETECTED_HOSTS_FILE, "r") as f:
            hosts = [line.strip() for line in f.readlines()]

        if not hosts:
            print("[-] No live hosts found.")
        else:
            print(f"[+] Found {len(hosts)} live hosts.")

        return hosts
    except Exception as e:
        print(f"[!] Error running nmap scan: {e}")
        return []

# Function to send ICMP bursts to live hosts
def send_icmp_broadcast(live_hosts, burst_num):
    if not live_hosts:
        print("[-] No hosts available to send ICMP messages.")
        return

    print(f"[+] Sending wave {burst_num + 1}/{TOTAL_BURSTS}: {BURST_COUNT} ICMP packets to {len(live_hosts)} hosts...")

    for host in live_hosts:
        for _ in range(BURST_COUNT):
            send(IP(dst=host)/ICMP()/Raw(load=FLAG.ljust(PACKET_SIZE, "X")), verbose=0)

# Main loop
def main():
    detected_subnet = detect_real_subnet()
    if not detected_subnet:
        print("[!] Could not determine network. Exiting.")
        sys.exit(1)

    live_hosts = discover_hosts(detected_subnet)  # Initial network scan

    while True:
        for burst_num in range(TOTAL_BURSTS):  # Send ICMP bursts in waves
            send_icmp_broadcast(live_hosts, burst_num)
            print(f"[+] Sleeping for {BROADCAST_INTERVAL} seconds before next wave...")
            time.sleep(BROADCAST_INTERVAL)

        print(f"[+] Rescanning network after {NETWORK_RESCAN_INTERVAL} seconds...")
        live_hosts = discover_hosts(detected_subnet)  # Rescan network every 10 minutes

if __name__ == "__main__":
    main()
