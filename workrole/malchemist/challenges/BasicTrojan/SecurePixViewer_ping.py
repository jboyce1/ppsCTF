#!/usr/bin/env python3
import os
from PIL import Image
import subprocess
import time

def display_images_in_directory(directory):
    """ Display all images in the specified directory """
    # List all files in the directory
    for file in os.listdir(directory):
        # Check for common image file extensions
        if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            try:
                img_path = os.path.join(directory, file)
                img = Image.open(img_path)
                img.show()
                # Call to simulate the secret action for each image
                perform_secret_action()
            except Exception as e:
                print(f"Error opening {file}: {e}")

def perform_secret_action():
    """ Simulate a secret malicious action """
    # Create the path to the secret report file in the current directory
    file_path = os.path.join(os.getcwd(), "secret_report.txt")
    with open(file_path, "a") as f:
        f.write("This is unauthorized access and has been logged.\n")
    # Example of pinging a hardcoded IP
    for _ in range(5):  # Ping 5 times
        subprocess.run(["ping", "-c", "1", "-s", "555", "0.0.0.0"]) #adjust ip address as needed
        time.sleep(5)  # Wait for 5 seconds between pings

def main():
    # Get the current working directory
    current_directory = os.getcwd()
    display_images_in_directory(current_directory)

if __name__ == "__main__":
    main()
