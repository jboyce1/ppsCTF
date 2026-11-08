---
layout: default
title: CyberCartographer training targets
---

# CyberCartographer training targets

Use these on the Ubuntu practice VMs assigned by the instructor. Open the folder where you want to save the scripts, then right-click and open a terminal. Copy and paste the download command for the assigned script. Run only the script assigned to that machine.

These scripts configure services on the practice VM; they are not keepalive scripts.

## SSH password setup

Download the password SSH instructions:

```bash
wget https://raw.githubusercontent.com/jboyce1/ppsCTF/main/workrole/cybercartographer/training/flagscripts/0_allow_ssh_password.txt
```

Open the downloaded text file. Apply them to the VM used for normal SSH and to any high-port SSH VM where password authentication is required. Use the assigned account when checking authentication from Kali.

## Telnet on port 23

Download the script:

```bash
wget https://raw.githubusercontent.com/jboyce1/ppsCTF/main/workrole/cybercartographer/training/flagscripts/1_deploy-telnet-23.py
```

Run it:

```bash
sudo python3 1_deploy-telnet-23.py
```

## Anonymous FTP on port 21

Download the script:

```bash
wget https://raw.githubusercontent.com/jboyce1/ppsCTF/main/workrole/cybercartographer/training/flagscripts/4_ftp-anon-login.py
```

Run it:

```bash
sudo python3 4_ftp-anon-login.py
```

## Anonymous FTP on a random high port

Download the script:

```bash
wget https://raw.githubusercontent.com/jboyce1/ppsCTF/main/workrole/cybercartographer/training/flagscripts/3_ftp-anon-highport.py
```

Run it:

```bash
sudo python3 3_ftp-anon-highport.py
```

## Anonymous FTP on a high port with a flag

Download the script:

```bash
wget https://raw.githubusercontent.com/jboyce1/ppsCTF/main/workrole/cybercartographer/training/flagscripts/2_ftp-anon-highport-flag.py
```

Run it:

```bash
sudo python3 2_ftp-anon-highport-flag.py
```

## SSH on a random high port

Download the script:

```bash
wget https://raw.githubusercontent.com/jboyce1/ppsCTF/main/workrole/cybercartographer/training/flagscripts/6_ssh-highport-generator.py
```

Run it:

```bash
sudo python3 6_ssh-highport-generator.py
```

## SSH on a high port with a flag

Download the script:

```bash
wget https://raw.githubusercontent.com/jboyce1/ppsCTF/main/workrole/cybercartographer/training/flagscripts/5_ssh-highport-generator-flag.py
```

Run it:

```bash
sudo python3 5_ssh-highport-generator-flag.py
```

The high-port generators select a port in 21000–24000. Record the port printed by the script. FTP generators reconfigure the same vsftpd service; use different VMs for normal and high-port FTP. SSH generators change the configured SSH port; use a separate VM for normal-port SSH.

For flag variants, review the configuration values at the top of the downloaded script before running it. Keep the VM console available when changing its SSH port.

After setup, use Kali to discover the host and identify its service as described in Parts 2–6. The instructor manages VM activity and refreshes the target list when addresses change.

## Current classroom targets

Download the current target list:

```bash
wget -O cyberorg_classroom_targets.txt https://raw.githubusercontent.com/jboyce1/ppsCTF/main/workrole/cybercartographer/training/cyberorg_classroom_targets.txt
```
 This file must be replaced from the current VM allocation before each live exercise. Its presence in the repository does not mean its addresses are still active.
