import subprocess
import time
import random

# === INSTALL REQUIRED TOOLS ===
def install_tools():
    print("[+] Installing required tools (Scapy, tcpdump, iftop)...")
    subprocess.run(["sudo", "apt", "update", "-y"], capture_output=True, text=True)
    subprocess.run(["sudo", "apt", "install", "-y", "tcpdump", "iftop", "python3-scapy"], capture_output=True, text=True)
    print("[+] Required tools installed!")

# Install tools before importing Scapy
install_tools()

from scapy.all import send, IP, ICMP, UDP, TCP, Raw

# === CONFIGURATION ===
VICTIM_IP = "10.15.62.5"  # Replace with actual victim's IP
UDP_PORT = 5678           # Port for UDP messages
TCP_PORT = 6789           # Port for TCP messages
INTERVAL = 1              # Time in seconds between messages

# Funny cyber insults
MESSAGES = [
    "Your config is so messed, I'd trust /dev/null before trusting you.",
    "You're slower than an ARP request on a dropped cable.",
    "Your password complexity is so low, I'd let my cat guess it.",
    "Your system is so full of holes, netstat found 127.0.0.1 vulnerabilities.",
    "Your code is so buggy, even a honeypot won't talk to it.",
    "Your encryption is weaker than a WEP key from 1999.",
    "Your firewall is as open as a public library Wi-Fi hotspot.",
    "Your system logs are more confused than a DNS lookup in a black hole.",
    "You cause more trouble on the network than broadcast storms do.",
    "I've seen viruses with better version control than your scripts."
]

# === ATTACK FUNCTION ===
def send_bullying_messages():
    print(f"[+] Attacking {VICTIM_IP} with cyber insults over ICMP, UDP, and TCP... (Press Ctrl+C to stop)")
    while True:
        message = random.choice(MESSAGES)

        # Send ICMP message
        send(IP(dst=VICTIM_IP)/ICMP()/Raw(load=message), verbose=0)

        # Send UDP message
        send(IP(dst=VICTIM_IP)/UDP(dport=UDP_PORT)/Raw(load=message), verbose=0)

        # Send TCP message
        send(IP(dst=VICTIM_IP)/TCP(dport=TCP_PORT)/Raw(load=message), verbose=0)

        time.sleep(INTERVAL)

# === RUN ATTACK ===
if __name__ == "__main__":
    send_bullying_messages()
