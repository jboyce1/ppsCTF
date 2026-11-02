#!/usr/bin/env python3

try:
    from scapy.all import send, IP, ICMP, Raw
except ImportError:
    print("[!] Scapy not found. Installing it now...")
    subprocess.run("sudo apt update -y", shell=True)
    subprocess.run("sudo apt install scapy -y", shell=True)
    from scapy.all import send, IP, ICMP, Raw  # retry import

from scapy.all import send, IP, ICMP, Raw

# ICMP message
TARGET_IP = "de.fa.ult.ip"
MESSAGE = "message here"


send(IP(dst=TARGET_IP)/ICMP()/Raw(load=MESSAGE), verbose=0)
