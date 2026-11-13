---
layout: move
title: CyberCartographer
---

<p><strong>MOVE edition.</strong> <a href="{{ '/workrole/cybercartographer/CyberCartographer' | relative_url }}">Open the original lesson</a>.</p>

# CyberCartographer



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



# Part 1: Set up draw.io and a shared team fileserver

<section class="move-card" aria-label="Part 1 MOVE">
<dl>
<dt><span>M</span> Mission</dt><dd>Set up communication routes on the LAN for file sharing and knowledge repositories.</dd>
<dt><span>O</span> Objective</dt><dd>Download draw.io and the base map for each team member. Set up a simple share with http.server, a knowledge share with miniserve, and establish version control.</dd>
<dt><span>V</span> Verification</dt><dd>An updated draw.io map with your group name, available in the shared directory. Bring the share’s IP address and port.</dd>
<dt><span>E</span> Explain / Elaborate</dt><dd>Explain possible uses for miniserve and the usefulness of a draw.io map.</dd>
</dl>
<p class="move-return">Return to the main meeting when you’re done.</p>
</section>

## Resources

Download draw.io:

**Short form — choose either form:**

```bash
wget -L https://github.com/jgraph/drawio-desktop/releases/download/v29.3.6/drawio-x86_64-29.3.6.AppImage
```

**Long form — same result:**

```bash
wget --relative https://github.com/jgraph/drawio-desktop/releases/download/v29.3.6/drawio-x86_64-29.3.6.AppImage
```

| Short option | Long option | Meaning |
| --- | --- | --- |
| `-L` | `--relative` | Follow relative links only. |

Download the base map:

**Short form — choose either form:**

```bash
wget -O team-network-map.drawio https://raw.githubusercontent.com/jboyce1/ppsCTF/main/workrole/cybercartographer/challenges/CyberTacticsFest_Scenerio_Base.drawio
```

**Long form — same result:**

```bash
wget --output-document=team-network-map.drawio https://raw.githubusercontent.com/jboyce1/ppsCTF/main/workrole/cybercartographer/challenges/CyberTacticsFest_Scenerio_Base.drawio
```

| Short option | Long option | Meaning |
| --- | --- | --- |
| `-O FILE` | `--output-document=FILE` | Write the download to FILE. |

Install miniserve:

```bash
sudo apt install miniserve
```

<details class="move-help" markdown="1">
<summary>Part 1 walkthrough</summary>

By the end of this part, everyone should be able to open draw.io and reach the team's shared folder. Choose one teammate's machine to host the share and keep that machine running throughout the activity.

## Part 1a: Install and launch draw.io

On each teammate's Kali desktop, open the folder where you want to keep draw.io. Right-click an empty area and choose **Open Terminal Here**. You can also use `cd` and `ls` to navigate there.

Download draw.io:

**Short form — choose either form:**

```bash
wget -L https://github.com/jgraph/drawio-desktop/releases/download/v29.3.6/drawio-x86_64-29.3.6.AppImage
```

**Long form — same result:**

```bash
wget --relative https://github.com/jgraph/drawio-desktop/releases/download/v29.3.6/drawio-x86_64-29.3.6.AppImage
```

| Short option | Long option | Meaning |
| --- | --- | --- |
| `-L` | `--relative` | Follow relative links only. |

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

**Short form — choose either form:**

```bash
wget -O team-network-map.drawio https://raw.githubusercontent.com/jboyce1/ppsCTF/main/workrole/cybercartographer/challenges/CyberTacticsFest_Scenerio_Base.drawio
```

**Long form — same result:**

```bash
wget --output-document=team-network-map.drawio https://raw.githubusercontent.com/jboyce1/ppsCTF/main/workrole/cybercartographer/challenges/CyberTacticsFest_Scenerio_Base.drawio
```

| Short option | Long option | Meaning |
| --- | --- | --- |
| `-O FILE` | `--output-document=FILE` | Write the download to FILE. |

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

**Short form — choose either form:**

```bash
miniserve . -p 8080 -u -U
```

**Long form — same result:**

```bash
miniserve . --port 8080 --upload-files --mkdir
```

| Short option | Long option | Meaning |
| --- | --- | --- |
| `-p PORT` | `--port PORT` | Port to use. |
| `-u` | `--upload-files` | Enable file uploading. |
| `-U` | `--mkdir` | Enable creating directories. |

`.` shares the current folder. Replace `8080` with your team's chosen port if needed.

Everyone returns to `http://<host_ip>:8080`. Create a folder for scan results and have each teammate upload a small notes file to confirm that uploads and downloads work. Keep the server terminal open; **Ctrl+C** stops the share. If the port is already in use, stop the earlier server or choose another port and tell the team.

Keep `team-network-map.drawio` in the shared space. Choose a map editor to download it, make changes in draw.io, and upload a newly named version such as `team-network-map-v2.drawio`. A fileserver does not provide live coediting or automatically save local draw.io changes back to the share. Use versioned names so teammates can identify the current map without overwriting one another's work.

This share allows reachable users to download and upload files without signing in. Serve only the team activity folder on the classroom LAN or range network and stop the server when finished.

**Part 1 checkpoint:** Every teammate can launch draw.io, reach the share, download the template, and upload a file through miniserve.

---


</details>

## Instructor example: CCTC training maps

Open this example to see how your instructor used draw.io during training. Look through its pages for ways to organize your team's map.

<a href="{{ '/workrole/cybercartographer/cctc_network_maps.drawio' | relative_url }}" download>Download cctc_network_maps.drawio</a>

From a range terminal, download the same file:

```bash
wget https://raw.githubusercontent.com/jboyce1/ppsCTF/main/workrole/cybercartographer/cctc_network_maps.drawio
```

Open `cctc_network_maps.drawio` in draw.io to explore the example.

# Part 2: Choose a discovery scan and save the results

<section class="move-card" aria-label="Part 2 MOVE">
<dl>
<dt><span>M</span> Mission</dt><dd>Discover the devices your team can investigate.</dd>
<dt><span>O</span> Objective</dt><dd>Read your addresses and routes, choose a discovery scan for the scenario, and use the current classroom target list on CYBER.ORG. Save and share the results.</dd>
<dt><span>V</span> Verification</dt><dd>hostsup.txt in the team fileshare.</dd>
<dt><span>E</span> Explain / Elaborate</dt><dd>Explain how your routes informed your scan and how your team will use the saved results.</dd>
</dl>
<p class="move-return">Return to the main meeting when you’re done.</p>
</section>

## Required files

Current classroom targets:

**Short form — choose either form:**

```bash
wget -O cyberorg_classroom_targets.txt https://raw.githubusercontent.com/jboyce1/ppsCTF/main/workrole/cybercartographer/cyberorg_classroom_targets.txt
```

**Long form — same result:**

```bash
wget --output-document=cyberorg_classroom_targets.txt https://raw.githubusercontent.com/jboyce1/ppsCTF/main/workrole/cybercartographer/cyberorg_classroom_targets.txt
```

| Short option | Long option | Meaning |
| --- | --- | --- |
| `-O FILE` | `--output-document=FILE` | Write the download to FILE. |

<details class="move-help" markdown="1">
<summary>Part 2 walkthrough</summary>

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

| Short option | Long option | Meaning |
| --- | --- | --- |
| `-n` | — | Never do DNS resolution. |
| `-sn` | — | Host discovery; disable port scan. |

If they identify `10.15.0.0/16`, use that prefix instead. Choose based on the network you have been assigned, rather than copying the example's prefix.

Save the output so your team can use it later:

```bash
nmap -n -sn 10.15.0.0/17 > discovery-report.txt
```

| Short option | Long option | Meaning |
| --- | --- | --- |
| `-n` | — | Never do DNS resolution. |
| `-sn` | — | Host discovery; disable port scan. |

`>` writes the output to a file in your current folder and replaces an existing file with that name. The results appear in the file instead of the terminal. Wait for the prompt to return, then open the file.

To keep an earlier scan from the same day, use the time in the filename. For a scan at 15:49:

```bash
nmap -n -sn 10.15.0.0/17 > discovery-report_1549.txt
```

| Short option | Long option | Meaning |
| --- | --- | --- |
| `-n` | — | Never do DNS resolution. |
| `-sn` | — | Host discovery; disable port scan. |

## Step 4: Use the current classroom list on CYBER.ORG

Boyce will provide a fresh target list because the classroom VMs have changing addresses and may be on different subnets. For this exercise, write the subnet command you would use, then run the list-based version below in place of the broad subnet scan.

Open a terminal in your team's shared folder. Download the current target file:

**Short form — choose either form:**

```bash
wget -O cyberorg_classroom_targets.txt https://raw.githubusercontent.com/jboyce1/ppsCTF/main/workrole/cybercartographer/cyberorg_classroom_targets.txt
```

**Long form — same result:**

```bash
wget --output-document=cyberorg_classroom_targets.txt https://raw.githubusercontent.com/jboyce1/ppsCTF/main/workrole/cybercartographer/cyberorg_classroom_targets.txt
```

| Short option | Long option | Meaning |
| --- | --- | --- |
| `-O FILE` | `--output-document=FILE` | Write the download to FILE. |

I'll try to keep the newest one updated on the github, but may just give it to you on an simple file share.

To see the format a file needs to be in to run it as -iL:

```bash
head cyberorg_classroom_targets.txt
```

Run discovery and save a readable report. `-iL` reads the classroom targets; `-oN` saves the report:

```bash
nmap -n -sn -iL cyberorg_classroom_targets.txt -oN discovery-report.txt
```

| Short option | Long option | Meaning |
| --- | --- | --- |
| `-n` | — | Never do DNS resolution. |
| `-sn` | — | Host discovery; disable port scan. |
| `-iL` | — | Read targets from a file. |
| `-oN` | — | Save normal-format output. |

After the scan finishes, extract only the responding IP addresses:

```bash
awk '/^Nmap scan report for / {ip=$NF} /Host is up/ {print ip}' discovery-report.txt > hostsup.txt
```

`awk` remembers each reported IP and prints it when the next line says `Host is up`. `>` saves that list, replacing an older `hostsup.txt`.

Display the saved list:

```bash
cat hostsup.txt
```

You should see one responding IP per line, with no headings, latency, or scan summary. This file can be used with `-iL` in later scans. To keep a timed copy, use a filename such as `hostsup_1549.txt` in the extraction command.

## Step 5: Share the on-network device list

Put the IP-only `hostsup.txt` (or your timed version) in the team fileshare and add a note or list labeled **On-network devices** to the draw.io map that points teammates to that list.

 
Use `hostsup.txt` directly for the scans in Parts 3–6. Keep `discovery-report.txt` as the original discovery report.

 You **could** go ahead and get fancy and write a python script that would continually scan and rescan the network and update the hostsup with a timestamp... but that might be a little much.


 In Parts 3–6, add individual computers for to the draw.io with password SSH, Telnet, or FTP, including services on high ports. It's not worth adding any computer you do not have potenital access to for this. 

---


</details>

## Reading command options

Use `hostsup.txt`, the IP-only list from Part 2, for the service scans below. Use rows marked `open` for follow-up; the simple commands also show closed and filtered ports.

A single dash does not always have a double-dash equivalent. Nmap documents `-p`, `-iL`, and `-oN` only in those forms; `--open` and a named `--script` have no short equivalents. The tables below show the documented spellings. **—** means no equivalent is listed in Nmap's help/man page. [Nmap option summary](https://nmap.org/book/man-briefoptions.html)

# Part 3: Find SSH hosts that offer password authentication

<section class="move-card" aria-label="Part 3 MOVE">
<dl>
<dt><span>M</span> Mission</dt><dd>Find SSH hosts that offer password authentication.</dd>
<dt><span>O</span> Objective</dt><dd>Identify SSH services offering password authentication and add them to the team map. Record any flags you find.</dd>
<dt><span>V</span> Verification</dt><dd>An updated draw.io map showing matching hosts, ports, and any flags found on those hosts.</dd>
<dt><span>E</span> Explain / Elaborate</dt><dd>Explain what your findings tell the team about possible SSH access.</dd>
</dl>
<p class="move-return">Return to the main meeting when you’re done.</p>
</section>

## Required files

Use your team’s target list and draw.io map from the earlier parts.

<details class="move-help" markdown="1">
<summary>Part 3 walkthrough</summary>

Open a terminal in the folder containing your team's `hostsup.txt` from Part 2.

Scan SSH on port 22:

```bash
nmap -p 22 --script ssh-auth-methods -iL hostsup.txt -oN ssh_auth_method_results.txt
```

| Short option | Long option | Meaning |
| --- | --- | --- |
| `-p` | — | Only scan specified ports. |
| — | `--script` | Run the selected NSE script. |
| `-iL` | — | Read targets from a file. |
| `-oN` | — | Save normal-format output. |


Look for `password` in the supported authentication methods. An open SSH port alone does not establish that password authentication is available.

For each match, add a computer to the draw.io map, or update its existing shape. Label it with the IP, port, **SSH — password offered**, and the username tested. Share the scan report.


Optional: after the SSH scan finishes, extract IPs whose report offers password authentication:

```bash
awk '/^Nmap scan report for / {ip=$NF; gsub(/[()]/,"",ip)} /^[|][ _\t]*password[ \t]*$/ {print ip}' ssh_auth_method_results.txt > ssh_password_hosts.txt
```

Open `ssh_password_hosts.txt` to inspect those matches. Continue using `hostsup.txt` as the main input list for the next parts.


Reference: [Nmap ssh-auth-methods](https://nmap.org/nsedoc/scripts/ssh-auth-methods.html).

---


</details>

# Part 4: Find and validate Telnet

<section class="move-card" aria-label="Part 4 MOVE">
<dl>
<dt><span>M</span> Mission</dt><dd>Find Telnet services your team can access.</dd>
<dt><span>O</span> Objective</dt><dd>Identify and validate Telnet services. Update the team map and record any flags you find.</dd>
<dt><span>V</span> Verification</dt><dd>An updated draw.io map showing Telnet hosts, ports, access confirmed, and any flags found on those hosts.</dd>
<dt><span>E</span> Explain / Elaborate</dt><dd>Explain what you confirmed about each Telnet service.</dd>
</dl>
<p class="move-return">Return to the main meeting when you’re done.</p>
</section>

## Required files

Use your team’s target list and draw.io map from the earlier parts.

<details class="move-help" markdown="1">
<summary>Part 4 walkthrough</summary>

Scan for Telnet on its usual port:

```bash
nmap -p 23 -iL hostsup.txt -oN telnet_results.txt
```

| Short option | Long option | Meaning |
| --- | --- | --- |
| `-p` | — | Only scan specified ports. |
| `-iL` | — | Read targets from a file. |
| `-oN` | — | Save normal-format output. |

This first scan finds open TCP port 23 without waiting for version detection. A `telnet` label based only on the port number is not proof of the service. For each IP with port 23 marked `open`, check its service:

```bash
nmap -sV -p 23 <targetIP> -oN telnet_service_results.txt
```

| Short option | Long option | Meaning |
| --- | --- | --- |
| `-sV` | — | Probe open ports for service/version information. |
| `-p` | — | Only scan specified ports. |
| `-oN` | — | Save normal-format output. |

Replace `<targetIP>` with one IP from `telnet_results.txt`. `-sV` probes the open port for service/version information. Use a different result filename when checking another host to preserve earlier evidence.

Connect to validate the Telnet service and assigned login:

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

Now... add anyone you find to the draw.io

---


</details>

# Part 5: Find and validate FTP

<section class="move-card" aria-label="Part 5 MOVE">
<dl>
<dt><span>M</span> Mission</dt><dd>Find FTP services and accessible files.</dd>
<dt><span>O</span> Objective</dt><dd>Identify FTP services, check available access, and update the team map. Record any flags you find.</dd>
<dt><span>V</span> Verification</dt><dd>An updated draw.io map showing FTP hosts, ports, access confirmed, and any flags found on those hosts.</dd>
<dt><span>E</span> Explain / Elaborate</dt><dd>Explain which FTP services allowed access and what your team learned from their files.</dd>
</dl>
<p class="move-return">Return to the main meeting when you’re done.</p>
</section>

## Required files

Use your team’s target list and draw.io map from the earlier parts.

<details class="move-help" markdown="1">
<summary>Part 5 walkthrough</summary>

Scan the usual FTP port and check anonymous access:

```bash
nmap -p 21 -sV --script ftp-anon -iL hostsup.txt -oN ftp_results.txt
```

| Short option | Long option | Meaning |
| --- | --- | --- |
| `-p` | — | Only scan specified ports. |
| `-sV` | — | Probe open ports for service/version information. |
| — | `--script` | Run the selected NSE script. |
| `-iL` | — | Read targets from a file. |
| `-oN` | — | Save normal-format output. |

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

Now... add anyone you find to the draw.io


---


</details>

# Part 6: Find services on high ports

<section class="move-card" aria-label="Part 6 MOVE">
<dl>
<dt><span>M</span> Mission</dt><dd>Find services and flags beyond the usual ports.</dd>
<dt><span>O</span> Objective</dt><dd>Find SSH, FTP, and Telnet on high ports. Validate access and update the team map with any flags you find, including SSH high-port and anonymous FTP high-port flags when present.</dd>
<dt><span>V</span> Verification</dt><dd>An updated draw.io map showing hosts, actual service ports, access confirmed, and any flags found on those hosts, including additional flags placed for this exercise.</dd>
<dt><span>E</span> Explain / Elaborate</dt><dd>Explain how you identified each service and connected its flags to the right host.</dd>
</dl>
<p class="move-return">Return to the main meeting when you’re done.</p>
</section>

## Required files

Use your team’s target list and draw.io map from the earlier parts.

<details class="move-help" markdown="1">
<summary>Part 6 walkthrough</summary>

The classroom generators choose ports between 21000 and 24000. Search the exercise's wider range for services:

```bash
nmap -p 20000-24000 -iL hostsup.txt -oN high_port_scan_results.txt
```

| Short option | Long option | Meaning |
| --- | --- | --- |
| `-p` | — | Only scan specified ports. |
| `-iL` | — | Read targets from a file. |
| `-oN` | — | Save normal-format output. |

This first scan finds open ports without waiting for service probes across the entire list. The displayed service names are port-number guesses. Identify each open port on one host before labeling it on the map:

```bash
nmap -sV -p <port#> <targetIP> -oN high_port_service_results.txt
```

| Short option | Long option | Meaning |
| --- | --- | --- |
| `-sV` | — | Probe open ports for service/version information. |
| `-p` | — | Only scan specified ports. |
| `-oN` | — | Save normal-format output. |

Replace the IP and port with one finding from `high_port_scan_results.txt`. Preserve each host's report under a different filename. An unidentified service needs follow-up. For a competition scenario, choose the port range based on that scenario.

For SSH found on a high port, check authentication methods on that port:

```bash
nmap -sV -p <port#> --script ssh-auth-methods --script-args="ssh.user=<username>" <targetIP> -oN ssh_high_port_results.txt
```

| Short option | Long option | Meaning |
| --- | --- | --- |
| `-sV` | — | Probe open ports for service/version information. |
| `-p` | — | Only scan specified ports. |
| — | `--script` | Run the selected NSE script. |
| — | `--script-args` | Provide arguments to NSE scripts. |
| `-oN` | — | Save normal-format output. |

Replace the port, username, and IP with your findings and assigned account. Look for `password` as in Part 3.


For SSH on a high port:

```bash
ssh -p <port#> username@TARGET_IP
```

For FTP found on a high port, check anonymous access:

```bash
nmap -sV -p <port#> --script ftp-anon <targetIP> -oN ftp_high_port_results.txt
```

| Short option | Long option | Meaning |
| --- | --- | --- |
| `-sV` | — | Probe open ports for service/version information. |
| `-p` | — | Only scan specified ports. |
| — | `--script` | Run the selected NSE script. |
| `-oN` | — | Save normal-format output. |

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

</details>

# Practice and explore

### Run your own practice target

Use a fresh assigned Ubuntu practice VM to set up services you can discover from Kali. This practice copy creates no challenge files or banners. It does not remove files or services from earlier exercises.

On **Ubuntu**, open your download folder in the file manager, then right-click and open a terminal there. Download the practice script; choose either equivalent form:

**Short form:**

```bash
wget -O deploy-practice.py https://raw.githubusercontent.com/jboyce1/ppsCTF/main/workrole/cybercartographer/challenges/practice/deploy-practice.py
```

**Long form — same result:**

```bash
wget --output-document=deploy-practice.py https://raw.githubusercontent.com/jboyce1/ppsCTF/main/workrole/cybercartographer/challenges/practice/deploy-practice.py
```

| Short option | Long option | Meaning |
| --- | --- | --- |
| `-O FILE` | `--output-document=FILE` | Write the download to FILE. |

After the download finishes, run it from the Ubuntu VM console:

```bash
sudo python3 deploy-practice.py
```

Enter `135` for standard SSH, FTP, and Telnet, or `246` for all three on random high ports. Choose the FTP login mode and confirm the setup when prompted. Use an existing VM account; the script does not create passwords.

| Option | Service |
| --- | --- |
| 1 | SSH on 22 |
| 2 | SSH on a random high port |
| 3 | FTP on 21 |
| 4 | FTP on a random high port |
| 5 | Telnet on 23 |
| 6 | Telnet on a random high port |

Read and save the final IP/port summary. On **Kali**, repeat the discovery and service scans from Parts 2–6 against your assigned Ubuntu VM. Compare your scan results with the summary, then test the logins. Keep this practice setup on your assigned range VMs.

   
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

**Short form — choose either form:**

```bash
wget -O cyberorg_classroom_targets.txt https://raw.githubusercontent.com/jboyce1/ppsCTF/main/workrole/cybercartographer/cyberorg_classroom_targets.txt
```

**Long form — same result:**

```bash
wget --output-document=cyberorg_classroom_targets.txt https://raw.githubusercontent.com/jboyce1/ppsCTF/main/workrole/cybercartographer/cyberorg_classroom_targets.txt
```

| Short option | Long option | Meaning |
| --- | --- | --- |
| `-O FILE` | `--output-document=FILE` | Write the download to FILE. |

In Zenmap, paste each scan below into **Command**, then click **Scan**. The command includes its targets, so you do not need to choose a preset profile or add targets separately. Typing a full command clears the selected profile. [Zenmap scanning guide](https://nmap.org/book/zenmap-scanning.html)

The blocks labeled **Zenmap Command** go in that field. Blocks labeled **Terminal** run in your terminal. Zenmap runs Nmap directly: use Nmap output options rather than shell redirection (`>`) or pipelines in its Command field.

### 3. Discover hosts and save discovery-report.txt

**Zenmap Command — CYBER.ORG classroom list:**

```text
nmap -n -sn -iL cyberorg_classroom_targets.txt -oN discovery-report.txt
```

| Short option | Long option | Meaning |
| --- | --- | --- |
| `-n` | — | Never do DNS resolution. |
| `-sn` | — | Host discovery; disable port scan. |
| `-iL` | — | Read targets from a file. |
| `-oN` | — | Save normal-format output. |

For the LAN scenario, the equivalent subnet command is below. Replace the example network and prefix with the choice supported by your routes; on CYBER.ORG use the classroom-list command above in place of this broad scan.

**Zenmap Command — subnet example:**

```text
nmap -n -sn 10.15.0.0/17 -oN discovery-report.txt
```

| Short option | Long option | Meaning |
| --- | --- | --- |
| `-n` | — | Never do DNS resolution. |
| `-sn` | — | Host discovery; disable port scan. |
| `-oN` | — | Save normal-format output. |

When the scan finishes, read **Nmap Output** for hosts reported as up. `-oN discovery-report.txt` saves a readable discovery report while the output remains visible in Zenmap. To keep a timed version, replace the output filename with one such as `discovery-report_1549.txt`. [Nmap output options](https://nmap.org/book/man-output.html)

Keep that report in the team fileshare and reference it from **On-network devices** on the draw.io map.

**Terminal — after discovery finishes, refresh the same IP-only list used in Parts 3–6:**

```bash
awk '/^Nmap scan report for / {ip=$NF} /Host is up/ {print ip}' discovery-report.txt > hostsup.txt
```

**Terminal — inspect the list before scanning:**

```bash
cat hostsup.txt
```

The scans below use `hostsup.txt`. Never pass `discovery-report.txt` or another formatted report to `-iL`. [Nmap target-file format](https://nmap.org/book/man-target-specification.html)

### 4. Find password SSH, Telnet, and FTP

Run these scans one at a time in the same Zenmap window.

**Zenmap Command — SSH on port 22:**

```text
nmap -p 22 --script ssh-auth-methods -iL hostsup.txt -oN ssh_auth_method_results.txt
```

| Short option | Long option | Meaning |
| --- | --- | --- |
| `-p` | — | Only scan specified ports. |
| — | `--script` | Run the selected NSE script. |
| `-iL` | — | Read targets from a file. |
| `-oN` | — | Save normal-format output. |

In **Nmap Output**, find `ssh-auth-methods` and look for `password` under its supported methods. This indicates an offered authentication method, not a successful login. [SSH authentication script](https://nmap.org/nsedoc/scripts/ssh-auth-methods.html)

**Zenmap Command — Telnet on port 23:**

```text
nmap -p 23 -iL hostsup.txt -oN telnet_results.txt
```

| Short option | Long option | Meaning |
| --- | --- | --- |
| `-p` | — | Only scan specified ports. |
| `-iL` | — | Read targets from a file. |
| `-oN` | — | Save normal-format output. |

Use the rows marked `open` from the port-23 scan. Identify each of those services separately:

**Zenmap Command — identify one port-23 service:**

```text
nmap -sV -p 23 <targetIP> -oN telnet_service_results.txt
```

| Short option | Long option | Meaning |
| --- | --- | --- |
| `-sV` | — | Probe open ports for service/version information. |
| `-p` | — | Only scan specified ports. |
| `-oN` | — | Save normal-format output. |

Replace `<targetIP>` with one reported IP. Then validate with the Telnet client from Part 4.

**Zenmap Command — FTP on port 21:**

```text
nmap -p 21 -sV --script ftp-anon -iL hostsup.txt -oN ftp_results.txt
```

| Short option | Long option | Meaning |
| --- | --- | --- |
| `-p` | — | Only scan specified ports. |
| `-sV` | — | Probe open ports for service/version information. |
| — | `--script` | Run the selected NSE script. |
| `-iL` | — | Read targets from a file. |
| `-oN` | — | Save normal-format output. |

For FTP, look for `Anonymous FTP login allowed` and any files shown by the script. It checks anonymous access and lists the server's root directory when permitted. [Anonymous FTP script](https://nmap.org/nsedoc/scripts/ftp-anon.html)

Select an IP under **Hosts**, then use **Ports / Hosts** to review its ports and detected services. Select **Services** to review hosts grouped by service. Read authentication and FTP script details in **Nmap Output**. Add the matching computers, actual ports, and findings to draw.io. [Reading Zenmap results](https://nmap.org/book/zenmap-results.html)

### 5. Find services on high ports

**Zenmap Command — the same exercise range as Part 6:**

```text
nmap -p 20000-24000 -iL hostsup.txt -oN high_port_scan_results.txt
```

| Short option | Long option | Meaning |
| --- | --- | --- |
| `-p` | — | Only scan specified ports. |
| `-iL` | — | Read targets from a file. |
| `-oN` | — | Save normal-format output. |

After the identification check below, use the detected service to choose the SSH or FTP check. Replace placeholders with the reported port, IP, and assigned username.

The range scan finds open ports first. Identify each host/port separately before choosing an authentication check:

**Zenmap Command — identify one high-port service:**

```text
nmap -sV -p <port#> <targetIP> -oN high_port_service_results.txt
```

| Short option | Long option | Meaning |
| --- | --- | --- |
| `-sV` | — | Probe open ports for service/version information. |
| `-p` | — | Only scan specified ports. |
| `-oN` | — | Save normal-format output. |

**Zenmap Command — check SSH authentication:**

```text
nmap -sV -p <port#> --script ssh-auth-methods --script-args="ssh.user=<username>" <targetIP> -oN ssh_high_port_results.txt
```

| Short option | Long option | Meaning |
| --- | --- | --- |
| `-sV` | — | Probe open ports for service/version information. |
| `-p` | — | Only scan specified ports. |
| — | `--script` | Run the selected NSE script. |
| — | `--script-args` | Provide arguments to NSE scripts. |
| `-oN` | — | Save normal-format output. |

For a high-port FTP service, replace the port and IP.

**Zenmap Command — check anonymous FTP:**

```text
nmap -sV -p <port#> --script ftp-anon <targetIP> -oN ftp_high_port_results.txt
```

| Short option | Long option | Meaning |
| --- | --- | --- |
| `-sV` | — | Probe open ports for service/version information. |
| `-p` | — | Only scan specified ports. |
| — | `--script` | Run the selected NSE script. |
| `-oN` | — | Save normal-format output. |

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
#### 'nmap -p 20000-24000 --open -sV -iL hostsup.txt'
-p 20000-24000 → Scans only high ports 20000-24000.    
--open → Only show hosts with open ports.    
-sV → Service version detection to identify if FTP, SSH, or Telnet is running.    
-iL hostsup.txt → Scan the responding classroom hosts saved in Part 2.

#### 'nmap -p 21,22,23 --open -sV -iL hostsup.txt'
-p 21,22,23 → Scan for FTP, SSH, and Telnet.  
--open → Only show hosts where a service is running.  
-sV → Detect service versions.  
-iL hostsup.txt → Scan only IPs listed in hostsup.txt.<br>

#### 'nmap -sC -sV -p 80,443 -iL hostsup.txt'
-sC → Runs default Nmap scripts.  
-sV → Service version detection.  
-p 80,443 → Scan for web servers on ports 80 (HTTP) and 443 (HTTPS).  

#### 'nmap --script ftp-anon -p 21 -iL hostsup.txt'
--script ftp-anon → Checks if anonymous FTP login is allowed.  
-p 21 → Scan only FTP port.  

#### 'nmap --script ssh-auth-methods -p 22 --open -iL hostsup.txt'
--script ssh-auth-methods → Checks available SSH authentication methods.  
-p 22 → Scan SSH port.  
--open → Only show hosts with open ports.  
-iL hostsup.txt → Scan a list of known hosts.<br>

#### 'nmap -p- --open -T4 -sV -iL hostsup.txt'
-p- → Scan **all** 65,535 ports.  
--open → Show only hosts with open ports.  
-T4 → Faster scan timing.  
-sV → Service version detection.  

#### 'nmap -p 135,137,445 --script smb-enum-shares -iL hostsup.txt'
-p 135,137,445 → Scan SMB ports.  
--script smb-enum-shares → Enumerate SMB shares.  
-iL hostsup.txt → Use a list of known hosts.<br>

#### 'nmap -p 3389 --open --script rdp-enum-encryption -iL hostsup.txt'
-p 3389 → Scan for Remote Desktop Protocol (RDP).  
--script rdp-enum-encryption → Detect RDP security settings.  
-iL hostsup.txt → Use a list of known hosts.<br>

#### 'nmap -sU -p 161 --open --script=snmp-info -iL hostsup.txt'
-sU → Scan UDP ports.  
-p 161 → Scan for SNMP services.  
--script=snmp-info → Extract SNMP system details.  
-iL hostsup.txt → Use a list of known hosts.


<details markdown="1">
<summary>Only if a scan appears stuck</summary>

Press **Enter** in the running terminal to display its status. Wait for **Nmap done** before calling a scan complete.

If the instructor asks you to retry, add only the option needed:

| Option | Meaning |
| --- | --- |
| `-v` | Increase verbosity. |
| `--stats-every 5s` | Print periodic timing statistics. |
| `--host-timeout 60s` | Give up on a host after this long. |
| `--script-timeout 15s` | Limit each script instance's execution time. |
| `-Pn` | Skip host discovery; treat all hosts as online. |

A timed-out or interrupted check is **INCOMPLETE**. Missing script output is **UNKNOWN**, not proof that authentication or access is unavailable. A per-host timeout is not a deadline for the entire class list. [Nmap timing](https://nmap.org/book/man-performance.html)

</details>
