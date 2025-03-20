#!/usr/bin/env python3
import time
import psutil  # Requires the 'psutil' package
import os

THRESHOLD_PERCENT = 85       # % memory usage to trigger
REQUIRED_CONSECUTIVE_CHECKS = 2  # e.g. must exceed threshold twice in a row
CHECK_INTERVAL = 5           # seconds between checks
FLAG_CONTENT = "pps{4x4_memory_bully-B3kah_n3utra1ized}"

def main():
    consecutive_exceeds = 0

    while True:
        mem = psutil.virtual_memory()
        if mem.percent >= THRESHOLD_PERCENT:
            consecutive_exceeds += 1
        else:
            consecutive_exceeds = 0

        # If memory usage has exceeded the threshold enough times,
        # write the flag to /tmp/bullies_neutralized.txt and exit.
        if consecutive_exceeds >= REQUIRED_CONSECUTIVE_CHECKS:
            with open("/tmp/bullies_neutralized.txt", "w") as f:
                f.write(f"Memory usage threshold reached! The bullies have been neutralized.\n")
                f.write(f"Final Flag: {FLAG_CONTENT}\n")
            break

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()

