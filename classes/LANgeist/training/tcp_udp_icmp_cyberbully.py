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
UDP_PORT = 9999           # Port for UDP messages
TCP_PORT = 2222           # Port for TCP messages
INTERVAL = 1              # Time in seconds between messages

# Funny cyber insults
MESSAGES = [
    "Your packets are so slow, even a dial-up modem pities you.",
    "404: Your relevance not found.",
    "You're so insecure, even Telnet has better encryption than you.",
    "You drop more packets than a bad Wi-Fi connection.",
    "Your security is so weak, even my grandma brute-forced your password.",
    "Even an unpatched Windows XP machine laughs at your firewall.",
    "Your IP address belongs in a deny list.",
    "I’ve seen botnets more organized than your system logs.",
    "If incompetence were a protocol, you’d be running it on port 0.",
    "Your encryption is as solid as ROT13."
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
