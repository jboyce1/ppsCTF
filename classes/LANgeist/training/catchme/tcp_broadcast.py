#!/usr/bin/env python3
"""
tcp_broadcaster.py (flagless)

Goal:
- Discover live hosts on the local subnet (same ARP+route logic you used before).
- Validate "real SSH" by making an actual TCP connection to port 22 and confirming the server banner
  starts with "SSH-" (e.g., "SSH-2.0-OpenSSH_...").
- Only send the message to validated SSH hosts (and cap how many to avoid blasting 1100 hosts).
- Make the message readable via Wireshark "Follow TCP Stream" on port 22.

How the message stays readable:
- SSH allows "pre-banner" lines before the client sends its "SSH-2.0-..." identification string.
  Servers ignore these lines. They are plaintext and will show up in Follow TCP Stream.
- We send MANY pre-banner lines (not starting with "SSH-"), then send a valid client ID line, then close.

Run:
  python3 tcp_broadcaster.py
"""

import subprocess
import time
import signal
import sys
import re
import socket
import random
from typing import List, Optional

# =========================
# CONFIG (edit these)
# =========================
DEST_PORT = 22

# Make this LONG on purpose; it will be split into multiple pre-banner lines.
MESSAGE = (
    "CATCH-ME-IF-YOU-CAN :: TRAFFIC CLUE\n"
    "----------------------------------\n"
    "You are close. The next box is NOT on this machine.\n"
    "Your job: grab a flag off the desktop capture traffic w/ fifo and extract the next hop.\n"
    "\n"
    "NEXT BOX: \n"
    "If ssh does not work, you may need to enable PasswordAuthentication in sshd_config.\n"
    "\n"
    "Reminder:\n"
    "- tcpdump\n"
    "- Wireshark display filters:\n"
    "- Wireshark statistics > conversations > ipv4 > filter\n"
    "- Use CyberCartographer to scan of other ports/protocols. This is not all ssh\n"
    "\n"
    "END CLUE\n"
)

# How often to rescan and rebroadcast
NETWORK_RESCAN_INTERVAL = 600   # rescan every 10 minutes
BROADCAST_INTERVAL = 12         # seconds between waves

# How many SSH hosts to target per scan (prevents blasting huge networks)
MAX_TARGETS_PER_SCAN = 40

# How many times to send per host per wave
BURST_COUNT = 2

# Socket timeouts
CONNECT_TIMEOUT = 1.2
BANNER_TIMEOUT = 1.2
SEND_TIMEOUT = 1.2

# Files for visibility/debug
LIVE_HOSTS_FILE = "hosts.txt"
SSH_HOSTS_FILE = "ssh_hosts.txt"

# Pre-banner formatting constraints
# Keep each line modest so it reassembles cleanly in Follow Stream
PREBANNER_LINE_MAX = 160
CLIENT_ID = "SSH-2.0-CatchMeBroadcaster_1.0"

# =========================
# graceful shutdown
# =========================
def handle_exit(sig, frame):
    print("\n[!] Stopping TCP broadcaster...")
    sys.exit(0)

signal.signal(signal.SIGINT, handle_exit)

# =========================
# subnet detection (same logic style)
# =========================
def get_lowest_arp_ip() -> Optional[str]:
    print("[+] Checking ARP table for active hosts...")
    try:
        arp_output = subprocess.run(["arp", "-a"], capture_output=True, text=True, check=False)
        ip_matches = re.findall(r"\((\d+\.\d+\.\d+\.\d+)\)", arp_output.stdout)
        if ip_matches:
            lowest_ip = sorted(ip_matches, key=lambda ip: list(map(int, ip.split("."))))[0]
            print(f"[+] Lowest IP from ARP: {lowest_ip}")
            return lowest_ip
        print("[-] No active hosts detected in ARP table.")
        return None
    except Exception as e:
        print(f"[!] Error checking ARP table: {e}")
        return None

def get_subnet_mask(interface: str) -> Optional[str]:
    try:
        ip_output = subprocess.run(
            ["ip", "-o", "-f", "inet", "addr", "show", interface],
            capture_output=True,
            text=True,
            check=False
        )
        match = re.search(r"inet (\d+\.\d+\.\d+\.\d+)/(\d+)", ip_output.stdout)
        if match:
            subnet_mask = match.group(2)
            print(f"[+] Detected subnet mask: /{subnet_mask}")
            return subnet_mask
    except Exception as e:
        print(f"[!] Failed to detect subnet mask: {e}")
    return None

def detect_real_subnet() -> Optional[str]:
    print("[+] Detecting the actual subnet...")
    base_ip = get_lowest_arp_ip()
    if not base_ip:
        return None

    try:
        ip_route_output = subprocess.run(["ip", "-o", "route", "show", "default"], capture_output=True, text=True, check=False)
        match = re.search(r"default via (\d+\.\d+\.\d+\.\d+) dev (\S+)", ip_route_output.stdout)
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

# =========================
# discovery
# =========================
def discover_live_hosts(subnet: str) -> List[str]:
    print(f"[+] Scanning network for live hosts in {subnet} (nmap ping sweep)...")
    try:
        cmd = f"sudo nmap -n -sn {subnet} -oG - | awk '/Up$/{{print $2}}' > {LIVE_HOSTS_FILE}"
        subprocess.run(cmd, shell=True, check=False)

        with open(LIVE_HOSTS_FILE, "r") as f:
            hosts = [line.strip() for line in f if line.strip()]

        print(f"[+] Live hosts found: {len(hosts)}")
        return hosts
    except Exception as e:
        print(f"[!] Error running nmap scan: {e}")
        return []

# =========================
# SSH validation (REAL connect + banner check)
# =========================
def is_real_ssh_host(ip: str) -> bool:
    """
    Connect to ip:22, read a banner, validate it looks like SSH.
    Many non-SSH services won't speak; many filtered hosts won't respond.
    """
    try:
        with socket.create_connection((ip, DEST_PORT), timeout=CONNECT_TIMEOUT) as s:
            s.settimeout(BANNER_TIMEOUT)
            # SSH servers typically send their banner immediately after accept.
            banner = s.recv(256)
            if not banner:
                return False
            # Common: b"SSH-2.0-OpenSSH_..."
            return banner.startswith(b"SSH-")
    except Exception:
        return False

def validate_ssh_hosts(live_hosts: List[str]) -> List[str]:
    if not live_hosts:
        try:
            open(SSH_HOSTS_FILE, "w").close()
        except Exception:
            pass
        return []

    # To avoid hammering huge networks, randomly sample before validating
    candidates = live_hosts[:]
    random.shuffle(candidates)

    # Validate more than MAX_TARGETS_PER_SCAN so we can still end up with MAX_TARGETS after failures.
    validate_cap = min(len(candidates), max(MAX_TARGETS_PER_SCAN * 4, MAX_TARGETS_PER_SCAN))
    candidates = candidates[:validate_cap]

    print(f"[+] Validating real SSH on a sampled set of {len(candidates)} live hosts...")
    ssh_hosts = []
    checked = 0

    for ip in candidates:
        checked += 1
        if is_real_ssh_host(ip):
            ssh_hosts.append(ip)
            print(f"[+] SSH OK: {ip}  ({len(ssh_hosts)}/{MAX_TARGETS_PER_SCAN})")
            if len(ssh_hosts) >= MAX_TARGETS_PER_SCAN:
                break

    try:
        with open(SSH_HOSTS_FILE, "w") as f:
            for ip in ssh_hosts:
                f.write(ip + "\n")
    except Exception:
        pass

    print(f"[+] Real SSH hosts selected: {len(ssh_hosts)} (checked {checked})")
    return ssh_hosts

# =========================
# Pre-banner message sending
# =========================
def chunk_message_to_prebanner_lines(message: str) -> List[str]:
    """
    Turn MESSAGE into many lines that:
    - DO NOT start with "SSH-" (so they are pre-banner "comments")
    - end with \r\n
    Keep each line <= PREBANNER_LINE_MAX for clean reassembly.
    """
    # Normalize newlines, keep structure, then wrap long lines.
    raw_lines = message.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    out = []
    for line in raw_lines:
        if not line:
            out.append("#")  # blank line -> a harmless comment marker
            continue

        # Ensure it doesn't begin with SSH-
        if line.startswith("SSH-"):
            line = "# " + line

        # Hard wrap
        while len(line) > PREBANNER_LINE_MAX:
            out.append("# " + line[:PREBANNER_LINE_MAX])
            line = line[PREBANNER_LINE_MAX:]
            if line and not line.startswith("SSH-") and not line.startswith("#"):
                # keep everything clearly "comment"
                line = "# " + line
        if not line.startswith("#"):
            line = "# " + line
        out.append(line)
    return out

PREBANNER_LINES = chunk_message_to_prebanner_lines(MESSAGE)

def send_prebanner_message(ip: str) -> bool:
    """
    Open TCP connection to SSH, read banner to confirm,
    then send many pre-banner comment lines + a valid SSH client ID, then close.
    """
    try:
        with socket.create_connection((ip, DEST_PORT), timeout=CONNECT_TIMEOUT) as s:
            s.settimeout(BANNER_TIMEOUT)
            banner = s.recv(256)
            if not banner or not banner.startswith(b"SSH-"):
                return False

            s.settimeout(SEND_TIMEOUT)

            # Send pre-banner lines (plaintext, visible in Follow TCP Stream)
            for line in PREBANNER_LINES:
                s.sendall((line + "\r\n").encode("utf-8", errors="ignore"))

            # Send a proper SSH client ID line so it looks legitimate
            s.sendall((CLIENT_ID + "\r\n").encode("ascii", errors="ignore"))

            # Done. Close immediately.
            return True
    except Exception:
        return False

# =========================
# broadcast loop
# =========================
def broadcast_wave(ssh_hosts: List[str], wave_num: int):
    if not ssh_hosts:
        print("[-] No validated SSH hosts to send to.")
        return

    print(f"[+] Wave {wave_num}: sending to {len(ssh_hosts)} SSH hosts (burst={BURST_COUNT})...")
    successes = 0

    # Shuffle each wave so captures vary
    targets = ssh_hosts[:]
    random.shuffle(targets)

    for ip in targets:
        for _ in range(BURST_COUNT):
            ok = send_prebanner_message(ip)
            if ok:
                successes += 1

    print(f"[+] Wave {wave_num} complete. Successful sessions: {successes}")

def main():
    subnet = detect_real_subnet()
    if not subnet:
        print("[!] Could not determine subnet. Exiting.")
        sys.exit(1)

    live_hosts = discover_live_hosts(subnet)
    ssh_hosts = validate_ssh_hosts(live_hosts)

    last_scan = time.time()
    wave = 1

    while True:
        broadcast_wave(ssh_hosts, wave)
        wave += 1

        time.sleep(BROADCAST_INTERVAL)

        if (time.time() - last_scan) >= NETWORK_RESCAN_INTERVAL:
            print(f"[+] Rescanning network after {NETWORK_RESCAN_INTERVAL} seconds...")
            live_hosts = discover_live_hosts(subnet)
            ssh_hosts = validate_ssh_hosts(live_hosts)
            last_scan = time.time()

if __name__ == "__main__":
    main()
