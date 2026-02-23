#!/usr/bin/env python3
import socket


TARGET_IP = "de.fa.ult.ip"
MESSAGE = "message here"


PORT = 9001  # receiving should run: nc -lvnp 9001

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((TARGET_IP, PORT))
    s.sendall(MESSAGE.encode())
