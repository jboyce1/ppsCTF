#!/usr/bin/env python3
import os
import pwd
import random
import subprocess
from pathlib import Path
from datetime import datetime

# =====================================================
# CONFIG
# =====================================================
CFG = {
    # Box scoring
    "BOX_VALUE": "1",
    "CHALLENGE_VALUE": "3",
    "FLAG_SALT": "auto",  # "auto" = generate 4 random chars; or set manually like "xk3q"

    # If blank -> default filename: pps{BOXxCHALLENGE_username_service:port}.txt
    "FLAG_FILENAME": "",

    # If blank -> default content will just be the flag string (plus newline)
    "FLAG_FILECONTENT": "",

    # Desktop drop extras (optional in addition to the flag file)
    "filename": "welcome.txt",
    "filecontent": "Welcome.\nYou found the flag.\n",

    # Services
    "ssh": True,
    "ssh_port": "22",          # "22" OR "range" (random 22000-33000)

    "ftp": True,
    "ftp_anon": True,
    "ftp_port": "21",          # "21" OR "range"

    "telnet": True,
    "telnet_c2_port": "23",    # "23" OR "range"

    # Output log
    "users_log": "users.txt",

    # Randomization
    "username_lastname_count": 100,
    "port_range_min": 22000,
    "port_range_max": 33000,
}

# =====================================================
# DATA LISTS
# =====================================================
LASTNAMES_100 = [
    "Smith","Johnson","Williams","Brown","Jones","Garcia","Miller","Davis","Rodriguez","Martinez",
    "Hernandez","Lopez","Gonzalez","Wilson","Anderson","Thomas","Taylor","Moore","Jackson","Martin",
    "Lee","Perez","Thompson","White","Harris","Sanchez","Clark","Ramirez","Lewis","Robinson",
    "Walker","Young","Allen","King","Wright","Scott","Torres","Nguyen","Hill","Flores",
    "Green","Adams","Nelson","Baker","Hall","Rivera","Campbell","Mitchell","Carter","Roberts",
    "Gomez","Phillips","Evans","Turner","Diaz","Parker","Cruz","Edwards","Collins","Reyes",
    "Stewart","Morris","Morales","Murphy","Cook","Rogers","Gutierrez","Ortiz","Morgan","Cooper",
    "Peterson","Bailey","Reed","Kelly","Howard","Ramos","Kim","Cox","Ward","Richardson",
    "Watson","Brooks","Chavez","Wood","James","Bennett","Gray","Mendoza","Ruiz","Hughes",
    "Price","Alvarez","Castillo","Sanders","Patel","Myers","Long","Ross","Foster","Jimenez"
]

THREE_LETTER_WORDS = [
    "fun","run","sky","net","cat","dog","red","blu","key","box",
    "spy","ops","tcp","udp","log","map","hex","bin","sol","tag",
    "ice","sun","fog","oak","ash","pip","git","apt","ssh","ftp",
    "war","rad","zen","nod","bit","pkt","dns","arp","ham","led"
]

# =====================================================
# UTIL
# =====================================================
def run(cmd, check=True, input_text=None):
    print(f"[cmd] {' '.join(cmd)}")
    return subprocess.run(cmd, check=check, text=True, input=input_text)

def must_be_root():
    if os.geteuid() != 0:
        raise SystemExit("Run this with sudo.")

def user_exists(username):
    try:
        pwd.getpwnam(username)
        return True
    except KeyError:
        return False

def random_high_port():
    return str(random.randint(CFG["port_range_min"], CFG["port_range_max"]))

def resolve_port(value):
    if str(value).lower() == "range":
        return random_high_port()
    return str(value)

def prompt_change_current_password():
    sudo_user = os.environ.get("SUDO_USER")
    if not sudo_user or sudo_user == "root":
        print("[*] Skipping current-password change (no valid SUDO_USER detected).")
        return

    choice = input(f"Change password for current user '{sudo_user}' now? [y/N]: ").strip().lower()
    if choice == "y":
        print("[*] Launching interactive passwd...")
        subprocess.run(["passwd", sudo_user], check=False)
    else:
        print("[*] Skipping password change.")

def gen_username():
    lastnames = LASTNAMES_100[: CFG["username_lastname_count"]]
    rand_letter = random.choice("abcdefghijklmnopqrstuvwxyz")
    lastname = random.choice(lastnames).lower()
    digit = str(random.randint(1, 9))
    return f"{rand_letter}{lastname}{digit}"

def gen_password():
    w1 = random.choice(THREE_LETTER_WORDS)
    w2 = random.choice(THREE_LETTER_WORDS)
    n = random.randint(10, 99)
    return f"{w1}{w2}{n}"

def gen_flag_salt():
    return "".join(random.choice("abcdefghijklmnopqrstuvwxyz123456789!@#$%^&*") for _ in range(4))

# =====================================================
# USER + FILES
# =====================================================
def create_user(username, password):
    if not user_exists(username):
        run(["useradd", "-m", "-s", "/bin/bash", username])
    run(["chpasswd"], input_text=f"{username}:{password}\n")

def ensure_desktop(username):
    desktop = Path(f"/home/{username}/Desktop")
    desktop.mkdir(parents=True, exist_ok=True)
    return desktop

def write_desktop_file(username, filename, content, mode="0644"):
    desktop = ensure_desktop(username)
    target = desktop / filename
    target.write_text(content, encoding="utf-8")
    run(["chown", f"{username}:{username}", str(target)])
    run(["chmod", mode, str(target)])
    return str(target)

# =====================================================
# SSH
# =====================================================
def setup_ssh(port):
    run(["apt-get", "update", "-y"], check=False)
    run(["apt-get", "install", "-y", "openssh-server"])

    sshd_config = Path("/etc/ssh/sshd_config")
    config = sshd_config.read_text(encoding="utf-8", errors="ignore").splitlines()

    # Remove existing Port lines (including commented ones) and insert a single Port line near top.
    new_lines = []
    inserted = False
    for line in config:
        stripped = line.strip()
        if stripped.startswith("Port ") or stripped.startswith("#Port "):
            continue
        if not inserted and stripped and not stripped.startswith("#") and stripped.startswith("Include"):
            # keep includes; we'll insert later
            new_lines.append(line)
            continue
        new_lines.append(line)

    # Put Port at the top (after any initial comments/blank lines)
    out = []
    placed = False
    for line in new_lines:
        if not placed and line.strip() and not line.strip().startswith("#"):
            out.append(f"Port {port}")
            placed = True
        out.append(line)
    if not placed:
        out.append(f"Port {port}")

    sshd_config.write_text("\n".join(out) + "\n", encoding="utf-8")

    run(["systemctl", "enable", "--now", "ssh"], check=False)
    run(["systemctl", "restart", "ssh"], check=False)


    # --- Force password authentication ---
    print("[*] Enabling SSH password authentication...")

    run([
        "sed",
        "-i",
        r"s/^#\?PasswordAuthentication .*/PasswordAuthentication yes/",
        "/etc/ssh/sshd_config"
    ], check=False)

    # Validate config before restart
    test = subprocess.run(["sshd", "-t"])
    if test.returncode != 0:
        raise SystemExit("[!] sshd config test failed (sshd -t). Not restarting SSH.")

    # Restart SSH service (covers both service names)
    subprocess.run(["systemctl", "restart", "ssh"], check=False)
    subprocess.run(["systemctl", "restart", "sshd"], check=False)
# =====================================================
# FTP (vsftpd)
# =====================================================
def setup_ftp(port, allow_anon):
    run(["apt-get", "install", "-y", "vsftpd"])

    conf_path = Path("/etc/vsftpd.conf")
    conf = conf_path.read_text(encoding="utf-8", errors="ignore").splitlines()

    def set_kv(lines, key, value):
        key_eq = f"{key}="
        replaced = False
        out = []
        for line in lines:
            if line.strip().startswith(key_eq):
                out.append(f"{key}={value}")
                replaced = True
            else:
                out.append(line)
        if not replaced:
            out.append(f"{key}={value}")
        return out

    conf = set_kv(conf, "listen", "YES")
    conf = set_kv(conf, "listen_ipv6", "NO")
    conf = set_kv(conf, "listen_port", port)
    conf = set_kv(conf, "anonymous_enable", "YES" if allow_anon else "NO")
    conf = set_kv(conf, "local_enable", "YES")
    conf = set_kv(conf, "write_enable", "YES")

    conf_path.write_text("\n".join(conf) + "\n", encoding="utf-8")

    run(["systemctl", "enable", "--now", "vsftpd"], check=False)
    run(["systemctl", "restart", "vsftpd"], check=False)

# =====================================================
# TELNET (openbsd-inetd + telnetd)
# =====================================================
def setup_telnet(port):
    run(["apt-get", "install", "-y", "openbsd-inetd", "telnetd"])

    inetd_conf = Path("/etc/inetd.conf")
    content = inetd_conf.read_text(encoding="utf-8", errors="ignore").splitlines()

    # Remove any existing telnet lines
    content = [ln for ln in content if "telnet" not in ln]

    # Standard inetd telnet service line
    content.append("telnet stream tcp nowait root /usr/sbin/tcpd /usr/sbin/in.telnetd")
    inetd_conf.write_text("\n".join(content) + "\n", encoding="utf-8")

    # Update /etc/services telnet port mapping
    services = Path("/etc/services")
    svc_lines = services.read_text(encoding="utf-8", errors="ignore").splitlines()
    svc_lines = [ln for ln in svc_lines if not ln.startswith("telnet\t") and not ln.startswith("telnet ")]
    svc_lines.append(f"telnet\t{port}/tcp")
    services.write_text("\n".join(svc_lines) + "\n", encoding="utf-8")

    run(["systemctl", "restart", "openbsd-inetd"], check=False)

# =====================================================
# FLAGS + LOGGING
# =====================================================
def make_flag_string(box_value, challenge_value, username, service, port):
    # You wrote .txt in the default format; keeping it.
    return f"pps{{{box_value}x{challenge_value}_{username}_{service}:{port}}}"

def default_flag_filename(flag_str):
    return f"{flag_str}.txt"

def flag_file_content(flag_str):
    # If user provided override, use it; else just return flag as content.
    if str(CFG.get("FLAG_FILECONTENT", "")).strip():
        return str(CFG["FLAG_FILECONTENT"]) + ("\n" if not str(CFG["FLAG_FILECONTENT"]).endswith("\n") else "")
    return flag_str + "\n"

def append_users_log(path, line):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8") as f:
        f.write(line + "\n")

# =====================================================
# MAIN
# =====================================================
def main():
    must_be_root()
    prompt_change_current_password()

    # Generate creds
    username = gen_username()
    password = gen_password()

    create_user(username, password)

    # Drop optional welcome file
    welcome_path = write_desktop_file(username, CFG["filename"], CFG["filecontent"])

    # Service setup
    services = []  # list of tuples (service, port)
    if CFG.get("ssh"):
        ssh_port = resolve_port(CFG.get("ssh_port", "22"))
        setup_ssh(ssh_port)
        services.append(("ssh", ssh_port))

    if CFG.get("ftp"):
        ftp_port = resolve_port(CFG.get("ftp_port", "21"))
        setup_ftp(ftp_port, bool(CFG.get("ftp_anon", False)))
        services.append(("ftp", ftp_port))

    if CFG.get("telnet"):
        tel_port = resolve_port(CFG.get("telnet_c2_port", "23"))
        setup_telnet(tel_port)
        services.append(("telnet", tel_port))

    # Pick one service to “name” the flag (or create multiple flags if you want)
    # Here: create ONE flag using the first enabled service.
    if not services:
        service, port = ("nosvc", "0")
    else:
        service, port = services[0]

    # Determine salt
    salt_cfg = str(CFG.get("FLAG_SALT", "auto")).strip()

    if salt_cfg.lower() == "auto" or salt_cfg == "":
        salt = gen_flag_salt()
    else:
        salt = salt_cfg

    flag_str = f"pps{{{CFG['BOX_VALUE']}x{CFG['CHALLENGE_VALUE']}_{username}_{service}:{port}_{salt}}}"

    # Flag filename/content rules
    fname = str(CFG.get("FLAG_FILENAME", "")).strip()
    if not fname:
        fname = default_flag_filename(flag_str)

    fcontent = flag_file_content(flag_str)

    flag_path = write_desktop_file(username, fname, fcontent)

    # Log line format
    services_str = ",".join([f"{svc}:{prt}" for svc, prt in services]) if services else "none"
    timestamp = datetime.now().isoformat(timespec="seconds")

    log_line = (
        f"{timestamp}\t"
        f"user={username}\tpass={password}\t"
        f"services={services_str}\t"
        f"flag={flag_str}\t"
        f"flag_path={flag_path}\t"
        f"welcome_path={welcome_path}"
    )

    append_users_log(CFG["users_log"], log_line)

    # Print summary
    print("\n==============================")
    print(" Box Created")
    print("==============================")
    print(f"Username: {username}")
    print(f"Password: {password}")
    print(f"Services: {services_str}")
    print(f"Flag:     {flag_str}")
    print(f"Flag file:{flag_path}")
    print(f"Log:      {Path(CFG['users_log']).resolve()}")
    print("==============================\n")
    print("[*] Student examples:")
    for svc, prt in services:
        if svc == "ssh":
            print(f"    ssh {username}@<box-ip> -p {prt}")
        elif svc == "ftp":
            print(f"    ftp <box-ip> {prt}   (client-dependent; many use ftp -p <port>)")
        elif svc == "telnet":
            print(f"    telnet <box-ip> {prt}")

if __name__ == "__main__":
    main()
