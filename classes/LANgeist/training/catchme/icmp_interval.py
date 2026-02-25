#!/usr/bin/env python3
import time
import signal
import sys
import subprocess

# === AUTO-INSTALL SCAPY IF MISSING ===
try:
    from scapy.all import send, IP, ICMP, Raw
except ImportError:
    print("[!] Scapy not found. Installing it now...")
    subprocess.run("sudo apt update -y", shell=True)
    subprocess.run("sudo apt install scapy -y", shell=True)
    from scapy.all import send, IP, ICMP, Raw  # retry import

# =========================
# CONFIG
# =========================
TARGET_IP = "de.fa.ult.ip"
MESSAGE = "message here".ljust(128, "X")  # padded for visibility
INTERVAL = 10  # seconds between sends

# =========================
# graceful shutdown
# =========================
def handle_exit(sig, frame):
    print("\n[!] Stopping ICMP sender...")
    sys.exit(0)

signal.signal(signal.SIGINT, handle_exit)

print(f"[+] Sending ICMP message to {TARGET_IP} every {INTERVAL} seconds...")

while True:
    send(IP(dst=TARGET_IP)/ICMP()/Raw(load=MESSAGE), verbose=0)
    time.sleep(INTERVAL)
