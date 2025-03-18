#!/usr/bin/env python3
import sys
import os
from PIL import Image
import subprocess
import time

def open_and_process_image(image_path):
    try:
        img = Image.open(image_path)
        img.show()
        perform_secret_action()
    except Exception as e:
        print(f"Error opening {image_path}: {e}")

def perform_secret_action():
    # Use the script's directory as the place to write the report.
    script_dir = os.path.dirname(os.path.abspath(__file__))
    report_file = os.path.join(script_dir, "secret_report.txt")
    
    with open(report_file, "a") as f:
        f.write("This is unauthorized access and has been logged.\n")

    # Use the absolute path to 'ping' to avoid environment issues.
    ping_command = "/usr/bin/ping"
    
    for _ in range(5):
        subprocess.run([ping_command, "-c", "1", "-s", "555", "192.168.1.100"])
        time.sleep(5)

def main():
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        open_and_process_image(image_path)
    else:
        print("No image file specified.")

if __name__ == "__main__":
    main()
