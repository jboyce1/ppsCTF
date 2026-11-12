---
layout: default
title: CyberCartographer training targets
---

# CyberCartographer training targets

Use these on the Ubuntu practice VMs assigned by the instructor. Open the folder where you want to save the scripts, then right-click and open a terminal. Copy and paste the download command for the assigned script. Run only the script assigned to that machine.

These scripts configure services on the practice VM; they are not keepalive scripts.

For the complete classroom workflow, use the [instructor run sheet](INSTRUCTOR_SETUP.txt): refresh the class list, configure a target, copy its validation plan, verify from Kali, and give students the current list. It starts with recipe `148` (SSH 22, FTP 21 with flag, Telnet 23 with flag). The individual scripts below remain an alternative to the menu.

## Combined setup menu (instructor)

On the assigned Ubuntu or Kali target VM, open a terminal in your download folder and download the launcher:

```bash
wget -O deploy-target.py https://raw.githubusercontent.com/jboyce1/ppsCTF/26979c6b5f4ba58a16ac30ad64e49e7f6a291b5d/workrole/cybercartographer/challenges/flagscripts/deploy-target.py
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

Installed packages are reused without reinstalling OpenSSH or running an update each time. When a required package is missing, the launcher updates package lists once and installs only the missing packages. Commands show progress, have time limits, and save their output. Setup failures are reported per service so the remaining services can still be checked. If SSH setup fails, the launcher attempts to restore the previous SSH configuration and unit state; inspect the report to confirm recovery.

The launcher ends with a compact inventory showing the VM IP addresses and each selected service, TCP port, login mode, local check result, and flag. Copy that terminal block to your classroom notes. It is also saved as `inventory.txt` and appended to `target-summary.txt`. Failed or untested services are marked explicitly; flags describe the selected configuration and require a passing check. Version 2.2 also prints a ready-to-copy `scp` command for Kali with the target IP, SSH port, invoking username, and report path filled in. This is saved in `validation-handoff.txt`; use the classroom fileshare if SSH or account access is unavailable.

The launcher prints a report directory in the folder where you ran it. Save that directory: `target-summary.txt` is the short report, `run.log` contains command output, `diagnostics.txt` includes service status, recent journals, listeners, and firewall rules, and `results.json` contains structured results. `backups` contains prior configurations. No login passwords are collected by the target launcher.

To recheck without configuring services again, replace `<REPORT_FOLDER>` with the printed directory:

```bash
sudo python3 deploy-target.py --check <REPORT_FOLDER>/expectations.json
```

Local checks verify SSH/FTP greetings, anonymous FTP access or denial, FTP flag retrieval, and Telnet negotiation/login prompts and flags. They do not prove user login or network access; use the student-side validator below. Internet access is needed only for missing packages. A running systemd-based Ubuntu/Kali VM is required. Rerunning changes selected services; earlier flags and other listeners may remain. Keep the VM console available when changing SSH ports.

## Validate the trial VM from Kali (instructor)

On a separate Kali/Ubuntu machine with the same access students have, download the validator:

```bash
wget -O validate-target.py https://raw.githubusercontent.com/jboyce1/ppsCTF/main/workrole/cybercartographer/challenges/flagscripts/validate-target.py
```

Run it and enter the target VM's IP when prompted:

```bash
python3 validate-target.py
```

Enter one existing non-root target account and password to test SSH, FTP user access when applicable, and Telnet. Press Enter at the username prompt to skip user logins; those checks are explicitly marked `SKIP`. Passwords are entered without echo and are not saved. The tool tests that supplied account once per applicable service; it does not guess passwords. SSH connections use a temporary un-pinned classroom host-key policy, print the fingerprint, and leave `known_hosts` unchanged.

If SSH login is marked `SKIP` because Paramiko is missing, install this package on the validation machine, then run the validator again:

```bash
sudo apt-get install -y python3-paramiko
```

The default TCP connect scan covers 21, 22, 23, and 21000–24000. It identifies protocol greetings and attempts real access: FTP login/listing and flag download, SSH login/command execution, and Telnet negotiation/login/command execution. It saves `student-summary.txt` and `student-results.json` in the printed report directory. No root access or Nmap installation is required.

For an exact comparison, run the target's printed `scp` command on Kali, or copy `expectations.json` through the classroom fileshare. Continue only after the transfer succeeds. Confirm the copied file is in the same folder as the validator:

```bash
ls -l expectations.json
```

Then run:

```bash
python3 validate-target.py --expect expectations.json
```

Expected ports outside the default range are added automatically. Missing expected ports, wrong protocols, failed logins, and missing flags are failures. Unexpected open ports within the scan scope are warnings. Without the expectations file, the tool can check discovered services but cannot identify a service that should exist and is missing.

For a full TCP inventory, including old listeners outside the classroom port range, run:

```bash
python3 validate-target.py --expect expectations.json --ports 1-65535
```

A full scan takes longer. Discovery defaults to a 0.7-second connection timeout per port; expected ports are retried with the longer protocol timeout. Increase `--connect-timeout` on a slow range. The scan does not test UDP or firewall changes. FTP passive data connections use TCP 30000–30020 on newly configured targets; a successful remote listing/download validates that data path. The scripts do not change firewall rules.

Overall results are `PASS`, `FAIL`, or `INCOMPLETE`; missing credentials, unsupported protocols, unexpected listeners, or no expectations file prevent an overall `PASS`. Exit codes are 0, 1, and 2 respectively (130 for interruption). These are instructor troubleshooting tools, not replacements for the student Nmap exercises.

For an independent Nmap view, replace `<TARGET_IP>` with the trial VM address:

```bash
nmap -n -Pn -sT -sV -p 21,22,23,21000-24000 --open -oN trial-vm-nmap.txt <TARGET_IP>
```

Nmap's [official options reference](https://nmap.org/book/man-briefoptions.html) explains TCP connect scans, service detection, port ranges, and saved output. For troubleshooting, share the target's `target-summary.txt`, `diagnostics.txt`, and `run.log`, plus the validator's `student-summary.txt`. Reports contain range addresses, account names, configuration, and challenge flags; share them with the instructor.

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
