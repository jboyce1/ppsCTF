#!/usr/bin/env python3
import psutil
import time
import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
import pytz

def wait_until_start():
    """ Wait until a specific start time """
    target_time = datetime(2024, 4, 21, 15, 15, 0, tzinfo=pytz.timezone('America/New_York'))
    now = datetime.now(pytz.timezone('America/New_York'))
    wait_time = (target_time - now).total_seconds()
    if wait_time > 0:
        print(f"Waiting for {wait_time} seconds to start.")
        time.sleep(wait_time)

def monitor_cpu_usage():
    """ Monitor the CPU usage and notify when it exceeds a certain threshold """
    threshold = 60  # Set the CPU usage percentage threshold

    wait_until_start()  # Wait until the specified time to start the monitoring

    while True:
        cpu_usage = psutil.cpu_percent(interval=1)
        if cpu_usage > threshold:
            show_popup_message(cpu_usage)
        time.sleep(1)  # Check every 1 second

def show_popup_message(cpu_usage):
    """ Show a popup message about high CPU usage """
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    message = f"High CPU usage detected: {cpu_usage}%! Take a break!"
    messagebox.showinfo("CPU Alert!", message)
    root.destroy()

if __name__ == "__main__":
    monitor_cpu_usage()
