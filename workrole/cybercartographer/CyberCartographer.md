---
layout: default
title: CyberCartographer
---

# CyberCartographer    

**Focus**: Network Mapping  
**Skill**: Utilize nmap, zenmap and draw.io to develop actionable offensive and defensive maps  
**Activity**: Identification of the most vulnerable machines on a network  

<div style="text-align: center;">
  <img src="{{ 'workrole/cybercartographer/images/93909-CyberCartography-with-nmap-banner.png' | relative_url }}" alt="Hash Hound Logo" style="max-width: 80%; height: auto;">
</div>

---
### CyberCartography with nmap, zenmap and draw.io
## Here be Dragons

### Specific Skills
- Identify your local subnet and its size; use nmap to discover responding classroom targets
- Set up a team fileserver with Python and miniserve
- Use nmap to create a text file of all open hosts
- Use nmap to identify and isolate hosts with password authentication OpenSSH
- Installing and using zenmap on the cyber.org range
- Use draw.io to develop and annotate a network map

### How this skill can be used:  
### **Offensive:**  
In the realm of offensive cybersecurity, the Red Team plays a critical role in reconnaissance and vulnerability exploitation. During the Discovery Phase, their primary objective is to gather intelligence about the network infrastructure, including identifying all hosts connected to it. The ability to swiftly and accurately enumerate network hosts is crucial for expediting subsequent attack phases.    

Zenmap, a graphical front-end for Nmap, is a valuable tool for this purpose. Its comprehensive scanning capabilities enable the Red Team to efficiently discover active hosts, open ports, and services running on the network. By quickly identifying the scope of the network and potential entry points, the Red Team can prioritize their efforts towards exploiting vulnerabilities and gaining unauthorized access.    

Zenmap's reporting features provide the Red Team with a consolidated view of their findings, aiding in the documentation of vulnerable hosts and exploited services. This information allows them to track their progress and plan subsequent attack strategies effectively.    

In summary, proficiency in using Zenmap for host discovery is essential for the Red Team's success in identifying and exploiting vulnerabilities within the network infrastructure, thereby achieving their objectives in offensive operations.
 

### **Defensive:**    
In the realm of defensive cybersecurity, the Blue Team plays a pivotal role in protecting network assets and mitigating cyber threats. Host hardening, the process of strengthening the security posture of individual hosts within a network, is a fundamental aspect of their responsibilities. By proactively securing hosts against potential threats, the Blue Team aims to reduce the attack surface and mitigate the impact of security incidents. Tools like nmap and Zenmap are instrumental for the Blue Team in conducting vulnerability assessments and identifying weaknesses in network hosts. By scanning for open ports, services, and potential vulnerabilities, nmap provides valuable insights into areas of security weakness that require attention.    

Once vulnerabilities are identified, the Blue Team can leverage Zenmap's reporting capabilities to prioritize remediation efforts. By focusing on hosts with the highest risk exposure, they can allocate resources effectively and address critical security issues promptly.    

---

<!-- Preserve existing lesson bookmarks. -->
<span id="cd-desktop"></span>
<span id="cd-desktop-1"></span>
<span id="cd-teamshare"></span>
<span id="chmod-x-drawio-x86_64-2936appimage"></span>
<span id="curl--o-httphost_ip8080scanxml"></span>
<span id="drawio-x86_64-2936appimage"></span>
<span id="httphost_ip8080"></span>
<span id="ls"></span>
<span id="ls-1"></span>
<span id="ls-2"></span>
<span id="ls-3"></span>
<span id="mkdir-teamshare"></span>
<span id="nmap--sc--sv--p-80443-10150016"></span>
<span id="part-1a-setting-up-drawio-on-the-cyberorg-range"></span>
<span id="part-1b-setting-up-a-simple-team-share--one-way-team-communication"></span>
<span id="python3--m-httpserver-8080"></span>
<span id="walkthrough"></span>
<span id="wget--l-httpsgithubcomjgraphdrawio-desktopreleasesdownloadv2936drawio-x86_64-2936appimage"></span>
<span id="wget-httphost_ip8080notestxt"></span>
<span id="wget-httpsrawgithubusercontentcomjboyce1ppsctfmainclassescybercartographercybertacticsfest_scenerio_basedrawio"></span>

# Part 1: Set up draw.io and a shared team fileserver

By the end of this part, everyone should be able to open draw.io and reach the team's shared folder. Choose one teammate's machine to host the share and keep that machine running throughout the activity.

## Part 1a: Install and launch draw.io

On each teammate's Kali desktop, open the folder where you want to keep draw.io. Right-click an empty area and choose **Open Terminal Here**. You can also use `cd` and `ls` to navigate there.

Download draw.io:

```bash
wget -L https://github.com/jgraph/drawio-desktop/releases/download/v29.3.6/drawio-x86_64-29.3.6.AppImage
```

Allow the downloaded file to run:

```bash
chmod +x drawio-x86_64-29.3.6.AppImage
```

Launch draw.io:

```bash
./drawio-x86_64-29.3.6.AppImage
```

## Part 1b: Prepare the shared folder and template

On the team's fileserver machine, create a folder named `teamshare`. Open that folder, right-click an empty area, and choose **Open Terminal Here**. You can also use `cd` and `ls` to navigate there.

Download the template into this folder:

```bash
wget -O team-network-map.drawio https://raw.githubusercontent.com/jboyce1/ppsCTF/main/workrole/cybercartographer/challenges/CyberTacticsFest_Scenerio_Base.drawio
```

`-O team-network-map.drawio` saves the download with the filename your team will use.

Find the server's IPv4 address:

```bash
ip -br -4 addr
```

Use the address on the interface that reaches your teammates, without the `/prefix`. Do not use the loopback address `127.0.0.1`. Share the server IP and chosen port with your team. On the CYBER.ORG range, machines may be on different subnets; use the range IP that teammates can reach. If a teammate cannot connect, check the IP, port, server terminal, and range connectivity with your instructor.

## Part 1c: Start a quick download share with Python

Open a terminal in the `teamshare` folder. Start the download share:

```bash
python3 -m http.server 8080
```

Keep this terminal open. Teammates open `http://<host_ip>:8080` in their browsers, replacing `<host_ip>` with the server's reachable IP. Download `team-network-map.drawio` using **Save link as**, then open it in draw.io.

Python's basic HTTP server lets teammates browse and download files; it does not provide browser uploads. Once everyone can download the template, press **Ctrl+C** in the server terminal to stop it before using the same port for miniserve.

## Part 1d: Use miniserve for the shared team workspace

On the fileserver machine, update the package list:

```bash
sudo apt update
```

When that finishes, install miniserve:

```bash
sudo apt install miniserve
```

Open a terminal in the `teamshare` folder. Start miniserve:

```bash
miniserve . -p 8080 --upload-files --mkdir
```

The general command is `miniserve . -p <port#> --upload-files --mkdir`. Replace `<port#>` with your team's port, such as `8080`; do not type the angle brackets. `.` shares the current folder, `-p` selects the port, `--upload-files` allows uploads, and `--mkdir` allows teammates to create folders in the browser.

Everyone returns to `http://<host_ip>:8080`. Create a folder for scan results and have each teammate upload a small notes file to confirm that uploads and downloads work. Keep the server terminal open; **Ctrl+C** stops the share. If the port is already in use, stop the earlier server or choose another port and tell the team.

Keep `team-network-map.drawio` in the shared space. Choose a map editor to download it, make changes in draw.io, and upload a newly named version such as `team-network-map-v2.drawio`. A fileserver does not provide live coediting or automatically save local draw.io changes back to the share. Use versioned names so teammates can identify the current map without overwriting one another's work.

This share allows reachable users to download and upload files without signing in. Serve only the team activity folder on the classroom LAN or range network and stop the server when finished.

**Part 1 checkpoint:** Every teammate can launch draw.io, reach the share, download the template, and upload a file through miniserve.

---

<!-- Preserve existing lesson bookmarks. -->
<span id="arp--a"></span>
<span id="ip-addr"></span>
<span id="part-2-use-nmap-to-identify-all-hosts-on-the-network-and-output-a-file"></span>
<span id="sudo-nmap--n--sn-defaultgatewayaddresssubnet--og----awk-upprint-2"></span>
<span id="sudo-nmap--n--sn-defaultgatewayaddresssubnet--og----awk-upprint-2--hoststxt"></span>
<span id="sudo-nmap--sn-10150117"></span>
<span id="sudo-nmap--sn-10150117--hostsuptxt"></span>

# Part 2: Choose a discovery scan and save the results

Everyone practices identifying the network from their own machine. You will need this on the competition LAN and when you enter another box. There is no separate turn-in for this part. Keep the discovery results in your team's fileshare for use in the map and later scans.

## Step 1: Read your addresses, routes, and neighbors

Show your IPv4 address and prefix:

```bash
ip -br -4 addr
```

Find the interface you are using. What is its IP address? What prefix follows the `/`?

Show your routes:

```bash
ip -4 route
```

Find the connected network and its prefix. Find the default gateway after `default via`. A default route is a way out of your network; it does not mean every destination is part of your local subnet.

Show all routing tables:

```bash
ip -4 route show table all
```

Compare the local addresses and connected routes with the previous output. Which route describes the network you need to discover?

Show cached neighbors:

```bash
ip neigh
```

These are neighbors your machine has learned about, not a complete inventory. Repeat these checks when you move to another box; its network may differ.

## Step 2: Work out the network size

**Total IPv4 addresses = 2^(32 − prefix length).** A `/17` contains 32,768 addresses; a `/16` contains 65,536. A larger address count does not mean that many computers are running.

For example, a connected route for `10.15.0.0/17` covers `10.15.0.0` through `10.15.127.255`. A route for `10.15.0.0/16` covers `10.15.0.0` through `10.15.255.255`.

Use your own output to choose the network and prefix. Explain to a teammate which line supports your choice.

## Step 3: Write a scan for the scenario

Write a host discovery command based on your routes. `-n` skips DNS lookups; `-sn` discovers hosts without scanning their ports.

If the scenario and output identify `10.15.0.0/17`, a suitable command is:

```bash
nmap -n -sn 10.15.0.0/17
```

If they identify `10.15.0.0/16`, use that prefix instead. Choose based on the network you have been assigned, rather than copying the example's prefix.

Save the output so your team can use it later:

```bash
nmap -n -sn 10.15.0.0/17 > hostsup.txt
```

`>` writes the output to a file in your current folder and replaces an existing file with that name. The results appear in the file instead of the terminal. Wait for the prompt to return, then open the file.

To keep an earlier scan from the same day, use the time in the filename. For a scan at 15:49:

```bash
nmap -n -sn 10.15.0.0/17 > hostsup_1549.txt
```

## Step 4: Use the current classroom list on CYBER.ORG

The instructor will provide a fresh target list because the classroom VMs have changing addresses and may be on different subnets. For this exercise, write the subnet command you would use, then run the list-based version below in place of the broad subnet scan.

Open a terminal in your team's shared folder. Download the instructor's current target file:

```bash
wget -O cyberorg_classroom_targets.txt https://raw.githubusercontent.com/jboyce1/ppsCTF/main/workrole/cybercartographer/cyberorg_classroom_targets.txt
```

If the instructor supplies a newer copy through the team fileshare, use that copy instead. Use today's list; an older download may contain different machines.

Open a terminal in the folder containing the file. Inspect it:

```bash
head cyberorg_classroom_targets.txt
```

Run discovery and save the results:

```bash
nmap -n -sn -iL cyberorg_classroom_targets.txt > hostsup.txt
```

`-iL` replaces the subnet target with addresses read from a file. You can use a time suffix here too, such as `hostsup_1549.txt`.

## Step 5: Share the on-network device list

Open the saved report and find the addresses reported as up. Put `hostsup.txt` (or your timed version) in the team fileshare and add a note or list labeled **On-network devices** to the draw.io map that points teammates to that report. On CYBER.ORG, this means responding classroom targets; it does not prove they all share a subnet.

For the next parts, use a text editor to create `hosts.txt`: one responding IP per line, with no Nmap report text. Save it beside your scan files and share it with your team. `hostsup.txt` is the report; `hosts.txt` is the input list for later scans.

A target in the instructor's list is not necessarily online. If targets disappear, tell the instructor; the VMs may need to be reopened and the list refreshed.

You do not need to draw an individual computer for every discovery response. In Parts 3–6, add individual computers for hosts with password SSH, Telnet, or FTP, including services on high ports.

---

<!-- Preserve existing lesson bookmarks. -->
<span id="cd-usrsharenmapscripts"></span>
<span id="part-3-use-nmap-to-identify-and-isolate-hosts-with-password-authentication-openssh"></span>
<span id="sudo-nmap--p-22---script-ssh-auth-methods---script-argssshuser--il-hoststxt"></span>
<span id="sudo-nmap--p-22---script-ssh-auth-methods---script-argssshuser-targetip"></span>

# Part 3: Find SSH hosts that offer password authentication

Open a terminal in the folder containing your team's `hosts.txt`.

Scan SSH on port 22:

```bash
nmap -n -p 22 --open --script ssh-auth-methods --script-args="ssh.user=<username>" -iL hosts.txt -oN ssh_password_results.txt
```

Replace `<username>` with the classroom username supplied by the instructor. `ssh.user` is a username to test, not a wildcard search for users. Authentication methods can depend on the account.

`-p 22` selects the usual SSH port. `--script ssh-auth-methods` asks which authentication methods the server offers. `-oN` saves the results while also showing them in the terminal.

Look for `password` in the supported authentication methods. An open SSH port alone does not establish that password authentication is available.

For each match, add a computer to the draw.io map, or update its existing shape. Label it with the IP, port, **SSH — password offered**, and the username tested. Share the scan report.

Reference: [Nmap ssh-auth-methods](https://nmap.org/nsedoc/scripts/ssh-auth-methods.html).

---

<!-- Preserve existing lesson bookmarks. -->
<span id="exit"></span>
<span id="hostname"></span>
<span id="part-4-identify-and-validate-telnet-services-on-the-network"></span>
<span id="sudo-apt-update--sudo-apt-install-telnet"></span>
<span id="sudo-nmap--p-23---open--il-hoststxt"></span>
<span id="sudo-nmap--p-23---open-targetip"></span>
<span id="telnet-targetip"></span>
<span id="telnet-targetip-port"></span>
<span id="whoami"></span>

# Part 4: Find and validate Telnet

Scan for Telnet on its usual port:

```bash
nmap -n -p 23 --open -sV -iL hosts.txt -oN telnet_results.txt
```

`-sV` checks the service on the open port. For a host identified as Telnet, connect:

```bash
telnet <targetIP>
```

If the client is missing, update the package list:

```bash
sudo apt update
```

Then install it:

```bash
sudo apt install telnet
```

Use the assigned credentials if prompted. If you reach a shell, check the machine name:

```bash
hostname
```

Leave the shell when finished:

```bash
exit
```

Add or update the computer on the map with its IP, Telnet port, and what you confirmed: service detected, login prompt reached, or successful login. Share `telnet_results.txt`.

---

<!-- Preserve existing lesson bookmarks. -->
<span id="bye"></span>
<span id="ftp-targetip"></span>
<span id="ftp-targetip-port"></span>
<span id="get-filename"></span>
<span id="nmap-script-ftp-anon--p-21-10150016"></span>
<span id="part-5-identify-and-validate-ftp-services-on-the-network"></span>
<span id="sudo-apt-update--sudo-apt-install-ftp"></span>
<span id="sudo-nmap--p-21---open--il-hoststxt"></span>
<span id="sudo-nmap--p-21---open-targetip"></span>
<span id="sudo-nmap--p-21---script-ftp-anon--il-hoststxt"></span>
<span id="sudo-nmap--p-21---script-ftp-anon-targetip"></span>
<span id="sudo-nmap--p-21-open----grep-nmap-scan-report-for--awk-print-5"></span>
<span id="sudo-nmap--p-21-open-hoststxt"></span>
<span id="sudo-nmap--p-21000-24000-script-ftp-anon--il-hoststxt--on-ftp_high_portstxt"></span>

# Part 5: Find and validate FTP

Scan the usual FTP port and check anonymous access:

```bash
nmap -n -p 21 --open -sV --script ftp-anon -iL hosts.txt -oN ftp_results.txt
```

`--script ftp-anon` checks whether anonymous login is allowed. An FTP service is worth mapping even when it requires a login.

Connect to one FTP host:

```bash
ftp <targetIP>
```

If the client is missing, update the package list:

```bash
sudo apt update
```

Then install it:

```bash
sudo apt install ftp
```

When anonymous login is offered, use `anonymous` as the username and press Enter for the password. Otherwise use assigned credentials.

List the available files:

```bash
ls
```

Download a file you want to inspect:

```bash
get <filename>
```

Disconnect:

```bash
bye
```

Add or update the computer on the map with its IP, FTP port, and whether anonymous login or file retrieval worked. Share `ftp_results.txt`.

---

<!-- Preserve existing lesson bookmarks. -->
<span id="nmap--p-20000-24000-open--sv-10150016"></span>
<span id="part-6-scan-a-range-of-high-ports-for-services-detected"></span>
<span id="sudo-nmap--p-20000-24000---open--sv--il-hoststxt"></span>
<span id="sudo-nmap--p-20000-24000---open--sv--il-hoststxt--on-high_port_scan_resultstxt"></span>
<span id="sudo-nmap--p-20000-24000---open--sv-10150017"></span>

# Part 6: Find services on high ports

The classroom generators choose ports between 21000 and 24000. Search the exercise's wider range for services:

```bash
nmap -n -p 20000-24000 --open -sV -iL hosts.txt -oN high_port_scan_results.txt
```

Use the service detection results rather than assuming a port number tells you the service. For a competition scenario, choose the port range based on that scenario.

For SSH found on a high port, check authentication methods on that port:

```bash
nmap -n -sV -p <port#> --script ssh-auth-methods --script-args="ssh.user=<username>" <targetIP> -oN ssh_high_port_results.txt
```

Replace the port, username, and IP with your findings and assigned account. Look for `password` as in Part 3.

For FTP found on a high port, check anonymous access:

```bash
nmap -n -sV -p <port#> --script ftp-anon <targetIP> -oN ftp_high_port_results.txt
```

Connect to validate FTP:

```bash
ftp <targetIP> <port#>
```

For Telnet found on a high port, connect:

```bash
telnet <targetIP> <port#>
```

Update the existing computer shape if you already mapped that IP. Otherwise add a computer for each host with password SSH, Telnet, or FTP. Label each service with its actual port and your evidence. Keep the on-network device report and service results in the fileshare, and upload the updated draw.io map.

Your team should now have an on-network device list plus individual mapped computers for the services you found, on both normal and high ports.

---
<!-- Preserve existing lesson bookmarks. -->
<span id="best-done-with-multiple-teammates-on-the-range"></span>
<span id="chmod-777-testtxt"></span>
<span id="nano-testtxt"></span>
<span id="sudo-python3-deploy-telnet-23py"></span>
<span id="sudo-python3-ftp-anon-highportpy"></span>
<span id="sudo-python3-ftp-anon-loginpy"></span>
<span id="sudo-python3-ssh-highport-generatorpy"></span>
<span id="wget-httpsrawgithubusercontentcomjboyce1ppsctfmainclassescybercartographerflagscriptsdeploy-telnet-23py"></span>
<span id="wget-httpsrawgithubusercontentcomjboyce1ppsctfmainclassescybercartographerflagscriptsftp-anon-highportpy"></span>
<span id="wget-httpsrawgithubusercontentcomjboyce1ppsctfmainclassescybercartographerflagscriptsftp-anon-loginpy"></span>
<span id="wget-httpsrawgithubusercontentcomjboyce1ppsctfmainclassescybercartographerflagscriptsssh-highport-generatorpy"></span>

# Practice and explore
   
### [TryHackMe-Independent-nmap]({{ 'workrole/cybercartographer/challenges/TryHackMe-Independent-nmap.pdf' | relative_url }})
Or just do the whole room    
https://tryhackme.com/room/networkservices    

 
### Find your own high ports

On Ubuntu practice VMs, use the [training service scripts]({{ '/workrole/cybercartographer/challenges/README.html' | relative_url }}) to set up targets. Download one script at a time into a folder, open a terminal there, and run the matching command from the guide. The instructor will assign machines and services.

Return to Kali and repeat discovery and service scanning. Add your findings to the shared map.

<div style="text-align: center;">
<iframe width="560" height="315" src="https://www.youtube.com/embed/jxwBPS5FCdc?si=SbFmfsg7CaUZW0mQ" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</div>

## Repeat the activity with Zenmap

Use Zenmap to repeat the discovery and service scans from Parts 2–6, then update the same team draw.io map. Keep using the fileshare and map versioning from Part 1. Zenmap supplies the scanning interface; draw.io remains your team's annotated map.

### 1. Install and open Zenmap on Kali

Install Zenmap from Kali's package repository:

```bash
sudo apt install zenmap
```

This is the installation command in the current [Kali tool documentation](https://www.kali.org/tools/nmap/#zenmap).

Open the folder containing your team's scan files, right-click an empty area, and choose **Open Terminal Here**. Launch Zenmap from that terminal so relative input and output filenames refer to this folder:

```bash
zenmap
```

### 2. Set up the targets and Command field

Use the address, route, and neighbor checks from Part 2 to choose the subnet command appropriate to your machine. Zenmap does not replace those terminal checks.

On CYBER.ORG, download the current classroom list in the same terminal folder:

```bash
wget -O cyberorg_classroom_targets.txt https://raw.githubusercontent.com/jboyce1/ppsCTF/main/workrole/cybercartographer/cyberorg_classroom_targets.txt
```

In Zenmap, paste each scan below into **Command**, then click **Scan**. The command includes its targets, so you do not need to choose a preset profile or add targets separately. Typing a full command clears the selected profile. [Zenmap scanning guide](https://nmap.org/book/zenmap-scanning.html)

The blocks labeled **Zenmap Command** go in that field. Blocks labeled **Terminal** run in your terminal. Zenmap runs Nmap directly: use Nmap output options rather than shell redirection (`>`) or pipelines in its Command field.

### 3. Discover hosts and save hostsup.txt

**Zenmap Command — CYBER.ORG classroom list:**

```text
nmap -n -sn -iL cyberorg_classroom_targets.txt -oN hostsup.txt
```

For the LAN scenario, the equivalent subnet command is below. Replace the example network and prefix with the choice supported by your routes; on CYBER.ORG use the classroom-list command above in place of this broad scan.

**Zenmap Command — subnet example:**

```text
nmap -n -sn 10.15.0.0/17 -oN hostsup.txt
```

When the scan finishes, read **Nmap Output** for hosts reported as up. `-oN hostsup.txt` saves a readable discovery report while the output remains visible in Zenmap. To keep a timed version, replace the output filename with one such as `hostsup_1549.txt`. [Nmap output options](https://nmap.org/book/man-output.html)

Keep that report in the team fileshare and reference it from **On-network devices** on the draw.io map.

For the scans below, continue using `cyberorg_classroom_targets.txt` as the input address list. `hostsup.txt` contains a formatted scan report, not the address-only list expected by `-iL`. [Nmap target-file format](https://nmap.org/book/man-target-specification.html)

### 4. Find password SSH, Telnet, and FTP

Run these scans one at a time in the same Zenmap window.

**Zenmap Command — SSH on port 22:**

```text
nmap -n -p 22 --open --script ssh-auth-methods -iL cyberorg_classroom_targets.txt -oN ssh_auth_method_results.txt
```

In **Nmap Output**, find `ssh-auth-methods` and look for `password` under its supported methods. This indicates an offered authentication method, not a successful login. [SSH authentication script](https://nmap.org/nsedoc/scripts/ssh-auth-methods.html)

**Zenmap Command — Telnet on port 23:**

```text
nmap -n -p 23 --open -sV -iL cyberorg_classroom_targets.txt -oN telnet_results.txt
```

**Zenmap Command — FTP on port 21:**

```text
nmap -n -p 21 --open -sV --script ftp-anon -iL cyberorg_classroom_targets.txt -oN ftp_results.txt
```

For FTP, look for `Anonymous FTP login allowed` and any files shown by the script. It checks anonymous access and lists the server's root directory when permitted. [Anonymous FTP script](https://nmap.org/nsedoc/scripts/ftp-anon.html)

Select an IP under **Hosts**, then use **Ports / Hosts** to review its ports and detected services. Select **Services** to review hosts grouped by service. Read authentication and FTP script details in **Nmap Output**. Add the matching computers, actual ports, and findings to draw.io. [Reading Zenmap results](https://nmap.org/book/zenmap-results.html)

### 5. Find services on high ports

**Zenmap Command — the same exercise range as Part 6:**

```text
nmap -n -p 20000-24000 --open -sV -iL cyberorg_classroom_targets.txt -oN high_port_scan_results.txt
```

Read the detected service names. For a high-port SSH service, replace the placeholders with the port, IP, and assigned username.

**Zenmap Command — check SSH authentication:**

```text
nmap -n -sV -p <port#> --script ssh-auth-methods --script-args="ssh.user=<username>" <targetIP> -oN ssh_high_port_results.txt
```

For a high-port FTP service, replace the port and IP.

**Zenmap Command — check anonymous FTP:**

```text
nmap -n -sV -p <port#> --script ftp-anon <targetIP> -oN ftp_high_port_results.txt
```

### 6. Validate access and collect flags

Use the clients from Parts 4–6 to connect to the services Zenmap found. Replace the placeholders with your findings. For high-port SSH:

**Terminal:**

```bash
ssh -p <port#> username@TARGET_IP
```

For FTP on a discovered port:

**Terminal:**

```bash
ftp <targetIP> <port#>
```

Use the FTP login and file-listing/download steps from Part 5. For Telnet on a discovered port:

**Terminal:**

```bash
telnet <targetIP> <port#>
```

Use the credentials and validation steps from the earlier parts. Record any flags you find on the corresponding draw.io computer, including SSH high-port, anonymous FTP high-port, or other flags placed for the exercise. Update existing computers rather than adding duplicate shapes for the same IP.

### 7. Save, reopen, and share the results

Zenmap combines scans run in one window into an inventory. Use **Scans** to review the individual runs and the selector in **Nmap Output** to read a particular report. [Scan inventories](https://nmap.org/book/zenmap-scanning.html)

Choose **Scan → Save Scan** and select **Nmap XML format** to keep a scan you can reopen. Choose the scan you want when prompted. Give it a descriptive name such as `ssh_auth_method_results.xml`. The `.txt` reports remain useful for reading and sharing; XML preserves the results for reopening in Zenmap.

To save the whole inventory, choose **Scan → Save All Scans to Directory** and select a new folder for those scans. Use **Scan → Open Scan** to reopen an XML file; choose **Open Scan in This Window** when you want to merge saved results into the current inventory. [Saving and loading scans](https://nmap.org/book/zenmap-saving.html)

You can inspect **Topology**, but these scans do not request traceroute information. Without that information, the view does not establish paths between the discovered hosts. Keep the team's service labels, flags, and map updates in draw.io. [Zenmap topology](https://nmap.org/book/zenmap-topology.html)

Put the saved reports and XML scans in the team fileshare and upload the updated version of the draw.io map.

---
# Other useful scans
#### 'nmap -p 20000-24000 --open -sV -iL hosts.txt'
-p 20000-24000 → Scans only high ports 20000-24000.    
--open → Only show hosts with open ports.    
-sV → Service version detection to identify if FTP, SSH, or Telnet is running.    
-iL hosts.txt → Scan the responding classroom hosts saved in Part 2.

#### 'nmap -p 21,22,23 --open -sV -iL hosts.txt'  
-p 21,22,23 → Scan for FTP, SSH, and Telnet.  
--open → Only show hosts where a service is running.  
-sV → Detect service versions.  
-iL hosts.txt → Scan only IPs listed in hosts.txt.  

#### 'nmap -sC -sV -p 80,443 -iL hosts.txt'
-sC → Runs default Nmap scripts.  
-sV → Service version detection.  
-p 80,443 → Scan for web servers on ports 80 (HTTP) and 443 (HTTPS).  

#### 'nmap --script ftp-anon -p 21 -iL hosts.txt'
--script ftp-anon → Checks if anonymous FTP login is allowed.  
-p 21 → Scan only FTP port.  

#### 'nmap --script ssh-auth-methods -p 22 --open -iL hosts.txt'  
--script ssh-auth-methods → Checks available SSH authentication methods.  
-p 22 → Scan SSH port.  
--open → Only show hosts with open ports.  
-iL hosts.txt → Scan a list of known hosts.  

#### 'nmap -p- --open -T4 -sV -iL hosts.txt'  
-p- → Scan **all** 65,535 ports.  
--open → Show only hosts with open ports.  
-T4 → Faster scan timing.  
-sV → Service version detection.  

#### 'nmap -p 135,137,445 --script smb-enum-shares -iL hosts.txt'  
-p 135,137,445 → Scan SMB ports.  
--script smb-enum-shares → Enumerate SMB shares.  
-iL hosts.txt → Use a list of known hosts.  

#### 'nmap -p 3389 --open --script rdp-enum-encryption -iL hosts.txt'  
-p 3389 → Scan for Remote Desktop Protocol (RDP).  
--script rdp-enum-encryption → Detect RDP security settings.  
-iL hosts.txt → Use a list of known hosts.  

#### 'nmap -sU -p 161 --open --script=snmp-info -iL hosts.txt'  
-sU → Scan UDP ports.  
-p 161 → Scan for SNMP services.  
--script=snmp-info → Extract SNMP system details.  
-iL hosts.txt → Use a list of known hosts.
