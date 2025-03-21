#!/usr/bin/env python3
import multiprocessing
import time

def memory_hog():
    """
    Consumes system memory indefinitely by appending strings to a list.
    Each loop appends about 1 MB of data, then sleeps briefly.
    """
    data = []
    while True:
        data.append("X" * 10**6)  # Allocate ~1MB
        time.sleep(0.5)

if __name__ == "__main__":
    """
    Spawns as many processes as there are CPU cores.
    Each process will run memory_hog() in an infinite loop.
    """
    for _ in range(multiprocessing.cpu_count()):
        p = multiprocessing.Process(target=memory_hog)
        p.start()
