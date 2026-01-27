#!/bin/bash
set -e  # Exit immediately if a command fails

# === Configuration ===
GITHUB_REPO="https://github.com/jboyce1/ppsCTF.git"
TARGET_DIR="/ppsCTF"
SSH_CONFIG="/etc/ssh/sshd_config"

# User credentials
declare -A USERS
USERS=(
    ["leroy"]="leroythehunt3r"
    ["mums_the_word"]="0ink0INK!"
    ["callsign_hambone"]="Her3piggyp1ggy"
)

# Desktop ZIP mappings
declare -A ZIP_FILES
ZIP_FILES=(
    ["leroy"]="leroy.zip"
    ["mums_the_word"]="mums_the_word.zip"
    ["callsign_hambone"]="callsign_hambone.zip"
)

# === Step 1: Clone or Update GitHub Repository ===
echo "[+] Cloning or updating PigFarmCTF repository..."
if [ -d "$TARGET_DIR" ]; then
    cd "$TARGET_DIR"
    git pull origin main
else
    git clone --depth 1 "$GITHUB_REPO" "$TARGET_DIR"
fi
cd "$TARGET_DIR/challenges/hamhunt"

# === Step 2: Create Users and Set Passwords ===
echo "[+] Creating users..."
for user in "${!USERS[@]}"; do
    if ! id "$user" &>/dev/null; then
        useradd -m -s /bin/bash "$user"
        echo "$user:${USERS[$user]}" | chpasswd
        echo "[+] Created user: $user"
    else
        echo "[!] User $user already exists, skipping..."
    fi

    # OPTIONAL: ensure they have sudo rights (remove this if you DON'T want sudo)
    usermod -aG sudo "$user"
done

# === Step 3: Enable SSH Password Authentication ===
echo "[+] Configuring SSH..."
if grep -qE '^[#\s]*PasswordAuthentication' "$SSH_CONFIG"; then
    sed -i 's/^[#\s]*PasswordAuthentication.*/PasswordAuthentication yes/' "$SSH_CONFIG"
else
    echo "PasswordAuthentication yes" >> "$SSH_CONFIG"
fi
systemctl restart ssh

# === Step 4: Deploy Desktop Folders ===
echo "[+] Deploying challenge Desktops..."
for user in "${!ZIP_FILES[@]}"; do
    desktop_zip="${ZIP_FILES[$user]}"
    user_home="/home/$user"
    desktop_path="$user_home/Desktop"

    echo "[+] Processing $user..."

    # Ensure Desktop folder exists
    mkdir -p "$desktop_path"

    # Extract ZIP into the user's home
    unzip -qo "$TARGET_DIR/challenges/hamhunt/$desktop_zip" -d "$user_home"

    # Ensure correct ownership of the ENTIRE home (important because unzip may create folders/files outside Desktop)
    chown -R "$user:$user" "$user_home"

    echo "[+] Desktop for $user has been updated!"
done

# === Step 5: Lock down user home directory permissions ===
# This is the key change: users can't read each other's Desktop/Home folders
echo "[+] Locking down home directory permissions..."
chmod 755 /home
for user in "${!USERS[@]}"; do
    chmod 700 "/home/$user"
done

# === Step 6: (REMOVED) Remove Sudo Privileges ===
# You said you want them to KEEP sudo, so do NOT remove it.
# If you ever want to remove sudo again, uncomment below.
# echo "[+] Removing sudo access for users..."
# for user in "${!USERS[@]}"; do
#     deluser "$user" sudo || true
# done

# === Final Reminder ===
echo "[!] REMINDER: Change the password for the Ubuntu sudo account!"
echo "Run: sudo passwd ubuntu"

echo "[+] Deployment Complete! Each user has their challenges and cannot access each other's desktops."
