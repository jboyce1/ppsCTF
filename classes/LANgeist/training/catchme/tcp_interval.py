#!/usr/bin/env python3
import socket
import time
import signal
import sys

TARGET_IP = "10.15.14.123"
PORT = 22 #do not change unless nc listener is opened on target box w: nc -lkp 9001
MESSAGE = "next hop here. \n"   # include newline so nc displays cleanly
INTERVAL = 10                # seconds
CONNECT_TIMEOUT = 2.0

def handle_exit(sig, frame):
    print("\n[!] Stopping TCP sender...")
    sys.exit(0)

signal.signal(signal.SIGINT, handle_exit)

print(f"[+] Sending TCP message to {TARGET_IP}:{PORT} every {INTERVAL} seconds...")

while True:
    try:
        with socket.create_connection((TARGET_IP, PORT), timeout=CONNECT_TIMEOUT) as s:
            s.sendall(MESSAGE.encode("utf-8", errors="ignore"))
        print(f"[+] Sent {len(MESSAGE)} bytes to {TARGET_IP}:{PORT}")
    except ConnectionRefusedError:
        print(f"[-] Connection refused: nothing listening on {TARGET_IP}:{PORT} (or REJECT firewall).")
    except TimeoutError:
        print(f"[-] Timeout: cannot reach {TARGET_IP}:{PORT} (filtered firewall, routing issue, or host down).")
    except OSError as e:
        print(f"[-] OS error: {e} (check IP, route, firewall, listener bind).")

    time.sleep(INTERVAL)
