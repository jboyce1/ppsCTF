#!/usr/bin/env python3
from scapy.all import send, IP, ICMP, Raw

# ICMP message
TARGET_IP = "de.fa.ult.ip"
MESSAGE = "message here"


send(IP(dst=TARGET_IP)/ICMP()/Raw(load=MESSAGE), verbose=0)
