#!/usr/bin/env python3
import psutil
import tkinter as tk
from tkinter import messagebox
import time

def monitor_wireshark():
    """ Continuously check if Wireshark is running and display a popup when found """
    wireshark_is_running = False  # Flag to track if Wireshark was already running

    while True:
        # Check all processes to see if Wireshark is one of them
        if "wireshark" in (p.name().lower() for p in psutil.process_iter(attrs=['name'])):
            if not wireshark_is_running:
                # Wireshark has started running and was not running before
                wireshark_is_running = True
                show_popup_message()
        else:
            # Reset flag if Wireshark is not running
            wireshark_is_running = False

        time.sleep(1)  # Check every second

def show_popup_message():
    """ Show a popup message about being a lifeguard """
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    messagebox.showinfo("Lifeguard Alert!", "Monitoring the waves? Make sure to keep the data safe, lifeguard!")
    root.destroy()

if __name__ == "__main__":
    monitor_wireshark()
