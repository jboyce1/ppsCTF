#!/usr/bin/env python3
import os
import subprocess
import time
import signal
import sys
import re
import random

def install_tools():
    print("[+] Installing required tools (Scapy, tcpdump, iftop, nmap)...")
    # Set the environment variable to force noninteractive mode.
    env = os.environ.copy()
    env["DEBIAN_FRONTEND"] = "noninteractive"
    # Use apt-get which is more suitable for scripting.
    subprocess.run(["sudo", "apt-get", "update"], env=env, check=True)
    subprocess.run(["sudo", "apt-get", "install", "-y", "tcpdump", "iftop", "nmap", "python3-scapy"], env=env, check=True)
    print("[+] Required tools installed!")

def check_and_import_scapy():
    """
    Attempts to import Scapy. If it fails, installs the necessary packages
    and then restarts the script.
    """
    try:
        from scapy.all import send, IP, TCP, Raw
        return send, IP, TCP, Raw
    except ImportError:
        print("[!] Scapy not installed. Installing now...")
        install_tools()
        print("[+] Tools installed. Restarting the script...")
        # Restart the script with the same interpreter and command-line arguments.
        os.execv(sys.executable, [sys.executable] + sys.argv)

# Now import scapy functions after ensuring they are installed.
send, IP, TCP, Raw = check_and_import_scapy()

# === CONFIGURATION: Customize Your Message & Port ===
BOX_VALUE = "1"                      # Change the box difficulty as desired
CHALLENGE_VALUE = "2"                # Change the challenge level as desired
INSERT_FLAG_CODE = "tcpv1cP@ass-sister"    # Adjust the challenge flag
TCP_PORT = 5555                      # Change the TCP port if needed

MESSAGE = (f"pps{{{BOX_VALUE}x{CHALLENGE_VALUE}_geist_{INSERT_FLAG_CODE}}} "
           "I would really appreciate some help from anyone who can see this, our family is being bullied..."
           "a group of sisters, who all have the same stupid first letter of their name" 
           " has been harrassing our computer. My brother stopped using the computer so "
           " I am giving his username and password in case you can help u:victoria2 p:V1ct0ry!" 
           " Thanks for any help -vera")

NETWORK_RESCAN_INTERVAL = 600  # Rescan network every 10 minutes (600 seconds)
BROADCAST_INTERVAL = 10        # Time between each burst in seconds
DETECTED_HOSTS_FILE = "hosts.txt"  # File to store detected live hosts

# Graceful shutdown on Ctrl+C
def handle_exit(sig, frame):
    print("\n[!] Stopping TCP Broadcaster...")
    sys.exit(0)

signal.signal(signal.SIGINT, handle_exit)

# ... the remainder of your code follows ...

# === NETWORK DETECTION FUNCTIONS ===
def get_lowest_arp_ip():
    """Finds the lowest IP address in the ARP table (best guess at network base)."""
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

def get_subnet_mask(interface):
    """Detects the subnet mask using `ip addr show`."""
    try:
        ip_output = subprocess.run(["ip", "-o", "-f", "inet", "addr", "show", interface],
                                   capture_output=True, text=True)
        match = re.search(r'inet (\d+\.\d+\.\d+\.\d+)/(\d+)', ip_output.stdout)
        if match:
            subnet_mask = match.group(2)
            print(f"[+] Detected subnet mask: /{subnet_mask}")
            return subnet_mask
    except Exception as e:
        print(f"[!] Failed to detect subnet mask: {e}")
    return None

def detect_real_subnet():
    """Detects the actual network subnet using ARP and IP routing."""
    print("[+] Detecting the actual subnet...")
    base_ip = get_lowest_arp_ip()
    if not base_ip:
        print("[!] Could not determine base IP. Exiting.")
        sys.exit(1)
    try:
        ip_route_output = subprocess.run(["ip", "-o", "route", "show", "default"],
                                         capture_output=True, text=True)
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

# === HOST DISCOVERY ===
def discover_hosts(subnet):
    """Scans the network using nmap and stores live hosts in a file."""
    print(f"[+] Scanning network for live hosts in {subnet} (this may take a few minutes)...")
    try:
        # Use nmap ping scan; output only live hosts
        subprocess.run(
            f"sudo nmap -n -sn {subnet} -oG - | awk '/Up$/{{print $2}}' > {DETECTED_HOSTS_FILE}",
            shell=True
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

# === TCP PACKET BROADCAST VIA SCAPY ===
def send_tcp_message(host, message):
    """
    Crafts a fake TCP handshake sequence to send a message to the target host.
    Even though no listener is running, this generates traffic that students
    can follow in Wireshark.
    """
    # Choose a random source port and base sequence number
    sport = random.randint(1024, 65535)
    seq_base = random.randint(1000, 5000)
    
    # Craft and send a SYN packet
    syn_pkt = IP(dst=host)/TCP(sport=sport, dport=TCP_PORT, flags="S", seq=seq_base)
    send(syn_pkt, verbose=0)
    
    # Craft and send a PSH/ACK packet with the message payload
    psh_pkt = IP(dst=host)/TCP(sport=sport, dport=TCP_PORT, flags="PA", seq=seq_base+1, ack=1)/Raw(load=message)
    send(psh_pkt, verbose=0)
    
    # Craft and send a FIN packet to ?close? the session
    fin_pkt = IP(dst=host)/TCP(sport=sport, dport=TCP_PORT, flags="FA", seq=seq_base+1+len(message), ack=1)
    send(fin_pkt, verbose=0)
    
    print(f"[+] Sent fake TCP session to {host}:{TCP_PORT}")

# === MAIN LOOP ===
def main():
    detected_subnet = detect_real_subnet()
    if not detected_subnet:
        print("[!] Could not determine network. Exiting.")
        sys.exit(1)
    
    live_hosts = discover_hosts(detected_subnet)  # Initial network scan
    if not live_hosts:
        print("[-] No live hosts found. Exiting.")
        sys.exit(1)
    
    TOTAL_BURSTS = NETWORK_RESCAN_INTERVAL // BROADCAST_INTERVAL
    while True:
        for burst_num in range(TOTAL_BURSTS):  # Send bursts of messages
            for host in live_hosts:
                send_tcp_message(host, MESSAGE)
            print(f"[+] Completed burst {burst_num+1}/{TOTAL_BURSTS}. Sleeping for {BROADCAST_INTERVAL} seconds...")
            time.sleep(BROADCAST_INTERVAL)
        print("[+] Rescanning network for live hosts...")
        live_hosts = discover_hosts(detected_subnet)

if __name__ == "__main__":
    main()

