#!/usr/bin/env python3
import psutil
import subprocess
import time

def check_firefox_activity():
  """ 
  Monitor the number of Firefox processes and notify when a new one opens.
  Write the notification message to a text file and open it on detection.
  """
  firefox_count = 0
  filename = "new_firefox_activity.txt"  # Name of the text file

  while True:
    try:
      current_count = sum(1 for proc in psutil.process_iter(attrs=['name']) if 'firefox' in proc.info['name'].lower())
    except (psutil.NoSuchProcess, psutil.AccessDenied):
      current_count = 0

    if current_count > firefox_count:
      message = f"New Firefox activity detected! You now have {current_count} windows open. I cant imagine what your utility bills look like on that machine!"
      firefox_count = current_count  # Update the count

      # Write the message to a text file
      with open(filename, "w") as file:
        file.write(message)

      # Open the text file with the default program
      subprocess.run(["xdg-open", filename])  # Uses xdg-open for broader compatibility

    time.sleep(.1)  # Check every second

if __name__ == "__main__":
  check_firefox_activity()