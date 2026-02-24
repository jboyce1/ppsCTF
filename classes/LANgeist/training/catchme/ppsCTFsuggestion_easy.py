#!/usr/bin/env python3
import os
import re
import socket
import sys
import tempfile
from datetime import datetime

import paramiko  

def get_local_ip(dest_ip: str) -> str:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((dest_ip, 1))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "0.0.0.0"

def safe_filename(s: str) -> str:
    s = s.strip()
    s = re.sub(r"\s+", "_", s)
    s = re.sub(r"[^A-Za-z0-9_\-]", "", s)
    return (s[:40] if s else "anon")

def sftp_mkdir_p(sftp: paramiko.SFTPClient, remote_dir: str):
    parts = remote_dir.strip("/").split("/")
    path = ""
    for part in parts:
        path += "/" + part
        try:
            sftp.stat(path)
        except FileNotFoundError:
            sftp.mkdir(path)

DEST_HOST = "10.1.1.50"                 
DEST_USER = "kali"                      
DEST_PASS = "kalikalikali"
DEST_DIR  = "/home/kali/Desktop/Suggestions"

def main():
    print("=== ppsCTF Suggestion Box (EASY) ===")
    print("Submit a suggestion to the class server.\n")

    name = input("Enter your name: ").strip()
    if not name:
        print("Name cannot be blank.")
        sys.exit(1)

    suggestion = input("Enter your suggestion: ").strip()
    if not suggestion:
        print("Suggestion cannot be blank.")
        sys.exit(1)

    suggestion = suggestion.replace("\n", " ").replace("\r", " ").strip()

    local_ip = get_local_ip(DEST_HOST)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    record_line = f"{name}:{local_ip}: {timestamp}: {suggestion}\n"

    token = safe_filename(name)
    ts_token = datetime.now().strftime("%Y%m%d_%H%M%S")
    remote_filename = f"{ts_token}_{token}.txt"
    remote_fullpath = f"{DEST_DIR.rstrip('/')}/{remote_filename}"

    with tempfile.NamedTemporaryFile("w", delete=False, prefix="ppsctf_suggestion_", suffix=".txt") as tf:
        tf.write(record_line)
        temp_path = tf.name

    ssh = None
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(
            hostname=DEST_HOST,
            username=DEST_USER,
            password=DEST_PASS,
            port=22,
            timeout=5,
            banner_timeout=5,
            auth_timeout=5,
            allow_agent=False,
            look_for_keys=False,
        )

        sftp = ssh.open_sftp()
        sftp_mkdir_p(sftp, DEST_DIR)
        sftp.put(temp_path, remote_fullpath)
        sftp.close()

    except Exception as e:
        print("\n[ERROR] Could not submit suggestion.")
        print(str(e))
        print("\nDo Better:")
        sys.exit(2)

    finally:
        try:
            os.remove(temp_path)
        except Exception:
            pass
        try:
            if ssh:
                ssh.close()
        except Exception:
            pass

    print("\n[OK] Suggestion submitted!")
    print(f"Saved as: {remote_filename} to /dev/null/")

if __name__ == "__main__":
    main()