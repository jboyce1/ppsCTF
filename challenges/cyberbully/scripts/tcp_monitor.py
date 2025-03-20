#!/usr/bin/env python3
import os
import time
import subprocess

TCP_PORT = 9876  # Change if needed
CHECK_INTERVAL = 5  # Check every 5 seconds
THRESHOLD_FAILURES = 3  # Number of consecutive failures before flag is placed
FLAG_CONTENT = "pps{3x2_tcp_blocked_83cky_success}"
FLAG_PATH = "/home/bully1/Desktop/tcp_flag.txt"  # This is where the flag will be placed

HIDDEN_MONITOR_PATH = "/usr/local/bin/.tcp_monitor_hidden"  # Hidden storage for the script

def check_tcp_traffic():
    """Returns True if TCP traffic is still active on the given port, False if it is blocked."""
    result = subprocess.run(["ss", "-t", "-a", "-n"], capture_output=True, text=True)
    return f":{TCP_PORT}" in result.stdout  # Checks if the port appears in active TCP connections

def main():
    failure_count = 0

    while True:
        if check_tcp_traffic():
            failure_count = 0  # Reset failure count if TCP traffic is still active
        else:
            failure_count += 1  # Increment if TCP traffic is missing

        if failure_count >= THRESHOLD_FAILURES:
            with open(FLAG_PATH, "w") as flag_file:
                flag_file.write(f"TCP attack successful!\nHere is your flag: {FLAG_CONTENT}\n")
            print(f"[+] Flag written to {FLAG_PATH}")
            break  # Stop the script after writing the flag

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
