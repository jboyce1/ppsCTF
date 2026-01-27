#!/usr/bin/env python3
"""
deploy_hamhunt.py

Runs the equivalent of:

  sudo git clone https://github.com/jboyce1/ppsCTF.git
  cd ppsCTF/challenges/hamhunt/
  sudo chmod +x deploy_hamhunt_v2.sh
  sudo ./deploy_hamhunt_v2.sh
  passwd
  (then deletes the cloned repo)

Notes:
- Run this as root (recommended): sudo python3 deploy_hamhunt.py
- For the password change, this script launches `passwd ubuntu` interactively.
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

REPO_URL = "https://github.com/jboyce1/ppsCTF.git"
CLONE_DIR = Path.cwd() / "ppsCTF"
DEPLOY_DIR = CLONE_DIR / "challenges" / "hamhunt"
DEPLOY_SCRIPT = DEPLOY_DIR / "deploy_hamhunt_v2.sh"
SUDO_USER_TO_CHANGE = "ubuntu"  # change if your sudoer username differs


def run(cmd, cwd=None, check=True):
    print(f"[+] Running: {' '.join(cmd)}" + (f"  (cwd={cwd})" if cwd else ""))
    return subprocess.run(cmd, cwd=str(cwd) if cwd else None, check=check)


def require_root():
    if os.geteuid() != 0:
        print("[!] This script must be run as root.")
        print("    Run: sudo python3 deploy_hamhunt.py")
        sys.exit(1)


def safe_rmtree(path: Path):
    if not path.exists():
        return
    # Guardrail: only delete if it's exactly the expected folder name in CWD
    if path.resolve() != (Path.cwd() / "ppsCTF").resolve():
        raise RuntimeError(f"Refusing to delete unexpected path: {path.resolve()}")
    print(f"[+] Deleting cloned repo: {path}")
    shutil.rmtree(path)


def main():
    require_root()

    # 1) Clone repo
    if CLONE_DIR.exists():
        print(f"[!] {CLONE_DIR} already exists. Removing it first to ensure a clean deploy.")
        safe_rmtree(CLONE_DIR)

    run(["git", "clone", REPO_URL, str(CLONE_DIR)])

    # 2) chmod +x deploy script
    if not DEPLOY_SCRIPT.exists():
        raise FileNotFoundError(f"Expected deploy script not found: {DEPLOY_SCRIPT}")
    run(["chmod", "+x", str(DEPLOY_SCRIPT)])

    # 3) run deploy script
    run([str(DEPLOY_SCRIPT)], cwd=DEPLOY_DIR)

    # 4) Force password change for ubuntu sudoer (interactive)
    print("\n[!] Next: change the password for the sudoer account.")
    print("    You'll be prompted interactively by `passwd`.\n")
    run(["passwd", SUDO_USER_TO_CHANGE])

    # 5) delete repo
    safe_rmtree(CLONE_DIR)

    print("[+] Done. Repo removed, deployment completed, password updated.")


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as e:
        print(f"\n[!] Command failed with exit code {e.returncode}: {e.cmd}")
        sys.exit(e.returncode)
    except Exception as e:
        print(f"\n[!] Error: {e}")
        sys.exit(1)
