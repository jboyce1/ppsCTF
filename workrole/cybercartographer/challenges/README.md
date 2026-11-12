---
layout: default
title: CyberCartographer training targets
---

# CyberCartographer training targets

Use these on the Ubuntu practice VMs assigned by the instructor. Open the folder where you want to save the scripts, then right-click and open a terminal. Copy and paste the download command for the assigned script. Run only the script assigned to that machine.

These scripts configure services on the practice VM; they are not keepalive scripts.

## Combined setup menu (instructor)

Publish `flagscripts/deploy-target.py` before using this download command. On the assigned Ubuntu or Kali target VM, open a terminal in your download folder and download the launcher:

```bash
wget -O deploy-target.py https://raw.githubusercontent.com/jboyce1/ppsCTF/main/workrole/cybercartographer/challenges/flagscripts/deploy-target.py
```

Run it from the VM console:

```bash
sudo python3 deploy-target.py
```

Enter option digits together: `136` sets up SSH on 22, FTP on 21, and Telnet on 23. Choose the FTP login mode when prompted, review the plan, and type `y` to apply it.

| Option | Service |
| --- | --- |
| 1 | SSH, port 22 |
| 2 | SSH, random high port |
| 3 | FTP, port 21 |
| 4 | FTP with downloadable flag, port 21 |
| 5 | FTP, random high port; asks whether to add a flag |
| 6 | Telnet, port 23 |
| 7 | Telnet, random high port |
| 8 | Telnet with banner flag, port 23 |
| 9 | Telnet with banner flag, random high port |

High ports are chosen from 21000–24000. Choose one FTP option per run; SSH options 1 and 2 can run together. FTP login choices are `anonymous`, `user`, or `both`; FTP flags require `anonymous` or `both`. User login uses existing non-root VM accounts and their current passwords; the launcher does not create accounts or change passwords. Telnet flags appear in the connection banner before login.

Record the final summary: it includes the VM addresses, ports, flags, failures, and backup location. A copy is saved as `target-summary.txt` in the printed backup folder. Anonymous FTP login, listing, and flag retrieval are checked locally; SSH/user logins and access from Kali still need classroom verification. The launcher does not change firewall rules.

The launcher reuses existing SSH/FTP helper functions and downloads those helpers automatically if they are not beside it. Internet access and a systemd-based Ubuntu/Kali VM are required. Rerunning changes the selected service configuration; earlier flags and other listeners may remain. Keep the VM console available when changing SSH ports. Initial automated tests use mocked services; live Ubuntu/Kali verification is still required.

## SSH password setup

Download the password SSH instructions:

```bash
wget https://raw.githubusercontent.com/jboyce1/ppsCTF/main/workrole/cybercartographer/challenges/flagscripts/0_allow_ssh_password.txt
```

Open the downloaded text file. Apply them to the VM used for normal SSH and to any high-port SSH VM where password authentication is required. Use the assigned account when checking authentication from Kali.

## Telnet on port 23

Download the script:

```bash
wget https://raw.githubusercontent.com/jboyce1/ppsCTF/main/workrole/cybercartographer/challenges/flagscripts/1_deploy-telnet-23.py
```

Run it:

```bash
sudo python3 1_deploy-telnet-23.py
```

## Anonymous FTP on port 21

Download the script:

```bash
wget https://raw.githubusercontent.com/jboyce1/ppsCTF/main/workrole/cybercartographer/challenges/flagscripts/4_ftp-anon-login.py
```

Run it:

```bash
sudo python3 4_ftp-anon-login.py
```

## Anonymous FTP on a random high port

Download the script:

```bash
wget https://raw.githubusercontent.com/jboyce1/ppsCTF/main/workrole/cybercartographer/challenges/flagscripts/3_ftp-anon-highport.py
```

Run it:

```bash
sudo python3 3_ftp-anon-highport.py
```

## Anonymous FTP on a high port with a flag

Download the script:

```bash
wget https://raw.githubusercontent.com/jboyce1/ppsCTF/main/workrole/cybercartographer/challenges/flagscripts/2_ftp-anon-highport-flag.py
```

Run it:

```bash
sudo python3 2_ftp-anon-highport-flag.py
```

## SSH on a random high port

Download the script:

```bash
wget https://raw.githubusercontent.com/jboyce1/ppsCTF/main/workrole/cybercartographer/challenges/flagscripts/6_ssh-highport-generator.py
```

Run it:

```bash
sudo python3 6_ssh-highport-generator.py
```

## SSH on a high port with a flag

Download the script:

```bash
wget https://raw.githubusercontent.com/jboyce1/ppsCTF/main/workrole/cybercartographer/challenges/flagscripts/5_ssh-highport-generator-flag.py
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
wget -O cyberorg_classroom_targets.txt https://raw.githubusercontent.com/jboyce1/ppsCTF/main/workrole/cybercartographer/cyberorg_classroom_targets.txt
```
 This file must be replaced from the current VM allocation before each live exercise. Its presence in the repository does not mean its addresses are still active.
