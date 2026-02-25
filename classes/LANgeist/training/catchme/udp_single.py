#!/usr/bin/env python3
import socket

# UDP
TARGET_IP = "de.fa.ult.ip"
MESSAGE = "message here"


PORT = 9002  # receiving student should run: nc -luvnp 9002

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(MESSAGE.encode(), (TARGET_IP, PORT))
sock.close()
