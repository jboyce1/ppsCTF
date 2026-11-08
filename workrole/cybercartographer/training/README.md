---
layout: default
title: CyberCartographer training targets
---

# CyberCartographer training targets

Use these on the Ubuntu practice VMs assigned by the instructor. Each linked filename downloads that script. Save it in a folder, then right-click in that folder and open a terminal. Run only the script assigned to that machine.

The links here use the local lesson site, so they work for reviewing these changes before a push. These scripts configure real services on the practice VM; they are not keepalive scripts.

## SSH password setup

[Open the password SSH instructions](flagscripts/0_allow_ssh_password.txt). Apply them to the VM used for normal SSH and to any high-port SSH VM where password authentication is required. Use the assigned account when checking authentication from Kali.

## Telnet on port 23

[Download 1_deploy-telnet-23.py](flagscripts/1_deploy-telnet-23.py).

```bash
sudo python3 1_deploy-telnet-23.py
```

## Anonymous FTP on port 21

[Download 4_ftp-anon-login.py](flagscripts/4_ftp-anon-login.py).

```bash
sudo python3 4_ftp-anon-login.py
```

## Anonymous FTP on a random high port

[Download 3_ftp-anon-highport.py](flagscripts/3_ftp-anon-highport.py).

```bash
sudo python3 3_ftp-anon-highport.py
```

## Anonymous FTP on a high port with a flag

[Download 2_ftp-anon-highport-flag.py](flagscripts/2_ftp-anon-highport-flag.py).

```bash
sudo python3 2_ftp-anon-highport-flag.py
```

## SSH on a random high port

[Download 6_ssh-highport-generator.py](flagscripts/6_ssh-highport-generator.py).

```bash
sudo python3 6_ssh-highport-generator.py
```

## SSH on a high port with a flag

[Download 5_ssh-highport-generator-flag.py](flagscripts/5_ssh-highport-generator-flag.py).

```bash
sudo python3 5_ssh-highport-generator-flag.py
```

The high-port generators select a port in 21000–24000. Record the port printed by the script. FTP generators reconfigure the same vsftpd service; use different VMs for normal and high-port FTP. SSH generators change the configured SSH port; use a separate VM for normal-port SSH.

For flag variants, review the configuration values at the top of the downloaded script before running it. Keep the VM console available when changing its SSH port.

After setup, use Kali to discover the host and identify its service as described in Parts 2–6. The instructor manages VM activity and refreshes the target list when addresses change.

## Current classroom targets

[Download cyberorg_classroom_targets.txt](cyberorg_classroom_targets.txt). This file must be replaced from the current VM allocation before each live exercise. Its presence in the repository does not mean its addresses are still active.
