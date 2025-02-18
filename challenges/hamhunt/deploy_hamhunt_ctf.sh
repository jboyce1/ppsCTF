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

# === Step 1: Clone GitHub Repository ===
echo "[+] Cloning the PigFarmCTF repository..."
rm -rf $TARGET_DIR
git clone --depth 1 $GITHUB_REPO $TARGET_DIR
cd $TARGET_DIR/challenges/hamhunt

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
done

# === Step 3: Enable SSH Password Authentication ===
echo "[+] Configuring SSH..."
sed -i '/^PasswordAuthentication no/c\PasswordAuthentication yes' $SSH_CONFIG
systemctl restart ssh

# === Step 4: Deploy Desktop Folders ===
echo "[+] Deploying challenge Desktops..."
for user in "${!ZIP_FILES[@]}"; do
    desktop_zip="${ZIP_FILES[$user]}"
    user_home="/home/$user"
    desktop_path="$user_home/Desktop"

    echo "[+] Processing $user..."

    # Ensure old Desktop is removed
    rm -rf "$desktop_path"

    # Extract ZIP directly to the user's home directory
    unzip -q "$TARGET_DIR/challenges/hamhunt/$desktop_zip" -d "$user_home"

    # Ensure correct ownership
    chown -R "$user:$user" "$user_home/Desktop"

    echo "[+] Desktop for $user has been updated!"
done

# === Step 5: Remove Sudo Privileges from Users ===
echo "[+] Removing sudo access for users..."
for user in "${!USERS[@]}"; do
    deluser "$user" sudo || true
done

# === Final Reminder ===
echo "[!] REMINDER: Change the password for the Ubuntu sudo account!"
echo "Run: sudo passwd ubuntu"

echo "[+] Deployment Complete! Each user has their challenges."
