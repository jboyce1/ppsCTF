#!/usr/bin/env python3
import psutil
import time
import tkinter as tk
from tkinter import messagebox

def monitor_cpu_usage():
    """ Monitor the CPU usage and notify when it exceeds a certain threshold """
    threshold = 20  # Set the CPU usage percentage threshold

    # Wait for 30 minutes before starting the monitoring
    time.sleep(1800)  # 1800 seconds = 30 minutes

    while True:
        cpu_usage = psutil.cpu_percent(interval=1)
        if cpu_usage > threshold:
            show_popup_message(cpu_usage)
        time.sleep(10)  # Check every 10 seconds

def show_popup_message(cpu_usage):
    """ Show a popup message about high CPU usage """
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    message = f"High CPU usage detected: {cpu_usage}%! Take a break!"
    messagebox.showinfo("CPU Alert!", message)
    root.destroy()

if __name__ == "__main__":
    monitor_cpu_usage()
