#!/usr/bin/env python3
import psutil
import subprocess
import time

def monitor_cpu_usage():
    """ Monitor the CPU usage and notify when it exceeds a certain threshold """
    threshold = 50  # Set the CPU usage percentage threshold

    while True:
        cpu_usage = psutil.cpu_percent(interval=1)
        if cpu_usage > threshold:
            message = f"High CPU usage detected: {cpu_usage}%! Take a break!"
            subprocess.run(["notify-send", "CPU Alert!", message])
        time.sleep(10)  # Check every 10 seconds

if __name__ == "__main__":
    monitor_cpu_usage()
