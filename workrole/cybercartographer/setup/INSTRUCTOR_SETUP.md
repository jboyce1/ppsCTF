---
layout: default
title: CyberCartographer instructor setup
---

# CyberCartographer instructor setup

This guide covers the current lesson, before a MOVE conversion. The classroom allocation is about 244 changing IP addresses. Based on the current classroom behavior, unused VMs expire after about 15 minutes. Capture the addresses and run the live exercise in one coordinated window; yesterday's file is not a current inventory.

## Before opening the VMs

Prepare draw.io and the team fileshares first. Walk through Part 2's address, route, and scan-writing discussion before starting the timed range setup where practical. Students can write their subnet commands while you prepare the live targets.

Have this checkout's `setup/` and `training/` folders open. Choose Ubuntu VMs for normal SSH, Telnet, normal FTP, high-port SSH, and high-port FTP. Use separate machines for normal and high-port versions: the existing generators reconfigure the service's port rather than adding a second independent server.

Choose the classroom username students will test with `ssh-auth-methods`. Keep a small instructor note of VM name, current IP, service, port, and last confirmed activity. Do not give students the service answers in advance.

## Live setup sequence

1. Open all available VMs. Note the time you begin. Work through batches if opening the whole allocation takes much of the 15-minute window; revisit early machines while finishing later ones.
2. Copy the VM inventory's IP addresses into `workrole/cybercartographer/cyberorg_classroom_targets_dirty.txt`. Paste the inventory text directly; it may include VM labels, repeated addresses, or other text. Save it.
3. Open a terminal in `workrole/cybercartographer/`. Run the cleaner:

```bash
python3 cyberorg_classroom_targets_cleaner.py
```

It reads the dirty file beside the script and writes `training/cyberorg_classroom_targets.txt`. It extracts valid IPv4 addresses, removes duplicates, and sorts numerically from lowest to highest. It does not test reachability or know which extracted addresses belong to assigned VMs. Check the list for gateways or unrelated addresses copied with the inventory. Expect roughly 244 unique addresses only when the whole allocation is present; duplicates or fewer active VMs may change the count. Missing input or no valid addresses produces an error and leaves any earlier output unchanged—do not distribute that earlier output as a fresh list.

4. The cleaner has updated the linked target file in `training/`. Review it, then place that same copy in the local team fileshares. Tell students when it was captured and have them replace old downloads. A local file replacement updates the local preview; it does not update the public website before an approved push.
5. On the selected Ubuntu machines, download the assigned script from the local [training guide](../training/README.html). Run one service setup at a time and record its actual port. Configure password SSH on the normal SSH VM and the high-port SSH VM using the supplied SSH instructions. Keep the VM consoles open and actively revisit them during the exercise.
6. Have students run the list-based discovery scan immediately. Check that the seeded service machines respond before moving on to Parts 3–6. Split service scans among teammates to make use of the same live window.

## Managing the 15-minute window

Use a reminder before 15 minutes elapse—for example, at 10 minutes—to revisit the target consoles and perform activity accepted by the range. Record when you last checked each seeded target. The service scripts install/configure services and exit; they are not keepalive loops. Do not assume an open port, a background daemon, or an incoming Nmap probe counts as user activity for CYBER.ORG. Confirm which activity resets the timer in the classroom before relying on it.

If machines expire, reopen them, recapture their addresses, rerun the cleaner to update the training copy, and replace the shared copies. Tell students to refresh the target file and rerun discovery. Keep earlier reports under time-stamped names such as `hostsup_1549.txt`; a changed IP may now describe a different VM.

The lesson deliberately uses the current target file in place of a large `/16` or `/17` sweep. Students still need to choose and explain the subnet command from their own route output. Live scanning then checks the supplied allocation while the machines are available.

## Service setup and checks

Use [training/README.md](../training/README.html) for downloads and individual run commands. The generators select high ports in 21000–24000; the lesson scans 20000–24000. The `-flag` variants also place challenge flags; use those when you want flags included.

From Kali, confirm at least one seeded target for each service you prepared. Use the same commands as Parts 3–6, substituting a single target IP when checking one VM. For SSH, verify `password` is actually offered for the assigned account. Record whether Telnet and FTP were merely detected or whether login succeeded. These checks validate the prepared targets; they do not validate a platform keepalive mechanism.

## What teams keep

There is no separate Part 2 submission. Teams keep a readable `hostsup.txt` (or a timed report) in their fileshare and reference it in an **On-network devices** note/list on the map. They make `hosts.txt` with only responding IPs for subsequent scans.

Parts 3–6 add individual computer shapes for hosts with password SSH, Telnet, or FTP, on normal or high ports. Each shape records the IP, service, port, and confirmed evidence. Multiple services on one IP belong on one computer shape. Teams save the service reports and updated draw.io map in their fileshare.
