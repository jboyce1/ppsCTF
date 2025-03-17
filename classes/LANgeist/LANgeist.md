---
layout: default
title: LANgeist
---

# LANgeist    

**Focus**: Network attacks  
**Skill**:   
**Activity**:   

<div style="text-align: center;">
  <img src="{{ 'classes/LANgeist/images/GhostofLAN.png' | relative_url }}" alt="LANgeist Logo" style="max-width: 80%; height: auto;">
</div>

## You can talk about us...
### `but you can't talk without us` 
---

**play a game while I yap:**    
#### `sudo apt install nsnake`    
#### `nsnake`    
    
#### `sudo apt install moon-buggy`    
#### `moon-buggy`    
    
#### `sudo apt install bsdgames`    
#### `man atc`    
#### `atc`    
    

**Specific Skills:**    
- Use TCP dump to identify traffic, gather detailed information about each packet sent    
- Use TCP dump to gather the entire packet, to include the packet payload    
- Use TCP dump to isolate attackers on your network with known IP addresses    
- Use SSH and Wireshark to remotely capture network traffic    
- Use Wireshark to capture traffic in promiscuous mode    
- Use the Dsniff tool Macof to conduct a MAC Flood attack    
    
### **Offensive Operations:**   
In the context of offensive cyber operations, tools like TCPdump, Wireshark, and Dsniff are integral to the toolkit of a skilled attacker or Red Team member. These tools serve multiple purposes, from reconnaissance to active network disruption.    
    
**Reconnaissance and Data Exfiltration:**    
TCPdump is a powerful command-line packet analyzer that allows for the capture of packets flowing through a network. In an offensive scenario, an attacker could use TCPdump to monitor and analyze traffic in real-time, identifying patterns, vulnerabilities, or valuable data. For instance, capturing packets to and from a target server could reveal unencrypted credentials, session tokens, or proprietary information being transmitted over the network. By gathering detailed packet payloads, attackers can reconstruct user sessions or exfiltrate sensitive data undetected. In a team vs team scenerio, knowing what the defenders are doing is going to help you know where you to attack.    
    
**Man-in-the-Middle (MitM) and Network Disruption:**    
Further exploiting network vulnerabilities, an attacker could employ the Dsniff tool suite, specifically the Macof tool, to conduct a MAC Flood attack. This type of attack overwhelms a switch's MAC address table, causing it to behave like a hub and broadcast packets to all ports. In this compromised state, an attacker can use TCPdump or Wireshark to capture a broad swath of network traffic, intercepting sensitive information that would normally not be accessible. This approach not only aids in information gathering but also disrupts normal network operations, potentially masking other malicious activities or creating a diversion. At the higher levels of point scale, you will have to get past a switch to get into the other teams network. This may not be in the 2024 session so do not spend cycles on it unless explicitly told.
    
**Remote Traffic Capture:**
Combining SSH with Wireshark provides an attacker the ability to remotely capture network traffic in a stealthy manner. By establishing an SSH tunnel to a compromised host within the target network, attackers can remotely execute Wireshark or TCPdump, funneling captured traffic back through the tunnel for analysis. This method allows for the monitoring of network traffic without being physically present on the network, reducing the risk of detection. This is going to be critical to get into the other teams network to see how their defenders are trying to protect their computers.    
    
### **Defensive Operations:**    
On the flip side, the same tools can be invaluable for defensive cyber operations, aiding Blue Team members in monitoring, diagnosing, and responding to threats.    
    
**Network Monitoring and Anomaly Detection:**
TCPdump and Wireshark are essential for Blue Teams for continuous network monitoring. By capturing and analyzing traffic, defenders can spot unusual patterns that may indicate a breach, such as unexpected data flows or communications with known malicious IP addresses. For instance, using TCPdump to isolate traffic from or to known malicious actors can help in quickly identifying compromised systems. TCPdump is going to be the best way to see if someone from the other team is lurking or acting on your network.     
    
**Incident Response and Forensics:**    
During an incident, detailed packet captures are invaluable. They allow defenders to reconstruct the actions of an attacker, understand the scope of a breach, and identify exactly what data may have been compromised or exfiltrated. Capturing payloads enables a detailed forensic analysis, which is crucial for understanding the attack vector, the extent of the damage, and for preventing future breaches. This is will help you identify what the attackers are looking for to know if you need to stop them, kick them off, or let them waste time.     
      
**Ensuring Network Resilience:**    
From a defensive perspective, understanding and simulating attack techniques like MAC Flood attacks enables teams to reinforce their networks against such threats. By testing their own networks with tools like Dsniff, defenders can identify vulnerabilities in their infrastructure and apply necessary mitigations, such as improving switch security settings or implementing intrusion detection systems that can alert on such attack patterns. By practicing the offense, you will see what configurations need to be made (or unmade) to prevent the attacks. The network starts as vulnerable and you patch holes as you go.      
      
**Secure Configuration and Encryption:**    
The use of SSH for secure communication exemplifies best practices in encryption and secure configuration management. Encouraging the use of encrypted protocols for remote administration and data transfer can significantly reduce the risk of credential interception and unauthorized access. This is hard to get around as your students and staff will need to be able to log in and you cannot choose multifactor authentication for students or expect them to have RSA tokens on their devices.    

---

# Part 1: tcp dump to identify traffic and capture packets    

## TCP Dump 
### A Data-network packet analyzer program that runs inside the Terminal 

**Step 1) Find your internet connection**
#### `tcpdump -D`    

 <div style="text-align: center;">
  <img src="{{ 'classes/LANgeist/images/tcpdump--D.png' | relative_url }}" alt="" style="max-width: 80%; height: auto;">
</div>

**Step 2) Run the packet capture**    
sudo tcpdump -i eth0    
hit Ctrl + C to stop the packet   
 <div style="text-align: center;">
  <img src="{{ 'classes/LANgeist/images/tcpdump-packet-description.png' | relative_url }}" alt="" style="max-width: 80%; height: auto;">
</div>
    
    
**Step 3) Dig a bit deeper into TCP dump (v stands for verbose)**    
#### `sudo tcpdump -i eth0 -c 10 -v`    
#### `sudo tcpdump -i eth0 -c 100 -v | grep “tcp 8949”`    
    
**Step 4) To get un-human readable, such as we will use later, see what looks like (capturing the whole packet)**    
#### `sudo tcpdump -s 0 -U -n -w - -i eth0`    
    
**Step 5) Print the output to a text file**    
First, navigate to the Desktop directory using the following command:    
#### `cd Desktop`
    
Now, capture the packets as a txt file use the > redirection tool:    
#### `sudo tcpdump -c 10 -q > localtcpdump.txt`    
is redirecting the output from the screen to a file named localtcpdump.txt    
    
To read the file, use the following command:    
#### `cat localtcpdump.txt` 

    
### Try it now:
Create a localtcpdump.txt file on your desktop
Open the file and read its contents

### Explanation of flags in step 3 of TCP Dump
**Skip this if you're not curious- it is just information and less relevant**    
    
**1**: This is the packet number in the sequence of captured packets.    
**16:27:02.202246**: The timestamp when the packet was captured, given in hours, minutes, seconds, and microseconds.    
**IP**: Indicates that this is an IP packet.    
**tos 0x0**: The Type of Service (ToS) field (now known as the Differentiated Services Field, DSCP), here showing a value of 0, indicating default precedence.    
**ttl 64**: Time To Live, the remaining hops before the packet is discarded. Here, it's set to 64.    
**id 45646**: Identification number of the IP packet. This is used to help piece together data fragments.    
**offset 0**: The fragment offset in the packet. An offset of 0 indicates this is the first (or only) fragment.    
**flags [DF]**: Flags set on the packet. DF stands for "Don't Fragment," indicating that this packet should not be fragmented.    
**proto TCP (6)**: The protocol used, TCP, with a protocol number of 6.    
**length 89**: The total length of the IP packet, including headers and data, in bytes.    
**10.15.128.194.38886 > 10.15.23.143.5901**: Source and destination IP addresses and ports. The packet is from IP 10.15.128.194, port 38886, to IP 10.15.23.143, port 5901.    
**Flags [P.]**: TCP flags. P stands for PSH (Push Function), indicating the sender wants the receiving application to be prompted to read this data immediately. The dot represents the ACK flag, acknowledging receipt of a packet.    
**cksum 0x1dde (correct)**: The checksum of the TCP segment, which is used to detect data corruption in the header and payload. "Correct" indicates the checksum is valid.    
**seq 1829878155:1829878192**: The sequence number of the first byte in this packet and the sequence number the next packet will start with, indicating the order of the packets.    
**ack 1760819870**: The acknowledgment number, indicating the next sequence number expected from the other side, confirming receipt of packets up to this number.    
**win 3983**: The window size, indicating how many bytes of data the sender of this packet is willing to receive (TCP flow control).    
**options [nop,nop,TS val 1036420066 ecr 270331338]**: TCP options present in this packet. "nop" stands for "No Operation" and is used for alignment. "TS val" and "ecr" are related to TCP timestamps for RTT measurement and PAWS (Protection Against Wrapped Sequence numbers). The value after "TS val" is the timestamp, and "ecr" is the echo reply of the timestamp.    
**length 37**: The length of the TCP payload, in bytes. This does not include the IP or TCP header sizes.d:    

<div style="text-align: center;">
<iframe width="560" height="315" src="https://www.youtube.com/embed/j3yEfOxOHTU?si=eeobo7EP1nzXN8df" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</div>

---
# Part 2: use iftop and tcpdump to isolate attackers on your network with a known IP address    

Download iftop
#### `sudo apt update && sudo apt install -y iftop`

Find your interface using    
#### `ip addr`    
 - Look for the interface name (usually something like eth0 or ens5)    

Now run iftop:
#### `sudo iftop -i <interface>`

 - This will give you all of the active connections of the box you are on:

    
## Narrow down and investigate the connections with tcpdump

**Precise Capture with TCP dump:**    
Use -q and --number to make output more human readable. You can use -c to limit the number of packets captured       
#### `sudo tcpdump -i eth0 -q --number`    
        
Grep the command to see only what you are looking for:    
#### `sudo tcpdump -i eth0 -q --number | grep “10.15.23”` 
This will only return IP addresses between 10.15.23.0- 10.15.23.255     

Use a reverse grep commmand to filter out the traffic that we do not care to see, such as ssh and domain traffic
    
#### `sudo tcpdump -i <interface> | grep -v ssh | grep -v domain`    
or    
#### `sudo tcpdump -i <interface> | grep -Ev "ssh|domain"`    
    
Combine these commands to futher narrow down your searches and look at the precise packets being sent:    
#### `sudo tcpdump -i <interface> | grep grep -Ev "ssh|domain|10.15.171.53"`

       


 <div style="text-align: center;">
  <img src="{{ 'classes/LANgeist/images/Use--q-and---number-to-make-it-more-human-readable.png' | relative_url }}" alt="" style="max-width: 80%; height: auto;">
</div>
    
**Try it now**:    
Open your Ubuntu machine and get its IP address    
Open your Kali machine and get its IP address    
Now, from your Ubuntu machine, ping your Kali ip address (ping 10.15.x.x)    
Now, from your Kali machine, try to use tcpdump and grep to see find the ip address of your Ubuntu machine    

    
**So... fight back**   
**Slow down the attackers network traffic with a ping flood**    
Once you get attackers ip address, send them a ping flood as a warning    
#### `sudo ping -f <attacker ip address>`    
or send a larger message (as in packet size)    
#### `sudo ping -f -s 65000 <attacker ip address>`    


Take a look at the iftop from the ubuntu machine you have sent a ping flood to.
<div style="text-align: center;">
<iframe width="560" height="315" src="https://www.youtube.com/embed/Q55KTQj5FGw?si=PQLeyg79d7GaNXHi" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</div>

---
# Part 3: setting up  Wireshark   
    
**Step 1) Set Wireshark to promiscuous mode:**    
    
#### `sudo ifconfig eth0 promisc`    
OR    
#### `sudo ip link set eth0 promisc on`    
    
**Step 2) verify the state of promiscuous mode:**
Looks  like this:  
    
2: eth0: <BROADCAST,MULTICAST,PROMISC,UP,LOWER_UP> mtu 9001 qdisc mq state UP group default qlen 1000 link/ether 0a:f7:a7:09:d9:1b brd ff:ff:ff:ff:ff:ff inet 10.15.75.96/17 brd 10.15.127.255 scope global dynamic eth0 valid_lft 2134sec preferred_lft 2134sec inet6 fe80::8f7:a7ff:fe09:d91b/64 scope link valid_lft forever preferred_lft forever    
    
The presence of PROMISC indicates that the eth0 inferface is running in promiscuous mode    
    
**Step 3) Open wireshark as a superuser:**    
#### `sudo wireshark`

select the eth0    
    
**Step 4) Select filters from the drop-down menu at the top of the Wireshark GUI**    
delete all filters    

**PCAP challenges:**      
From wireshark, go to File > Open > find/your/pcap.pcap    
    
1. simplehttp.pcap: **Find the password that was submitted via http protocol**
#### `wget https://github.com/jboyce1/ppsCTF/raw/main/classes/LANgeist/simplehttp.pcap`
 - Hint: You can search for things in the search bar, protocols in particular
submit PacketCAPture1 response here:    
  
[LANgeustPackCAPture1](https://forms.office.com/Pages/ResponsePage.aspx?id=mhxxjxzsu023kLsMdxsdzM6J33C5yQRJgc1SHWy_64dUNTk4WlI5QjQyMVdPVlI5VUg0SlhWTzBMQy4u)


   
2. SSH_10-15-17-162-to-10.15.2.-29.pcapng: Describe what happens in this PCAP  
#### `wget https://github.com/jboyce1/ppsCTF/raw/main/classes/LANgeist/SSH_10-15-17-162-to-10.15.2.-29.pcapng`  
submit PacketCapture2 response here:    
  
[LANgeustPackCAPture2](https://forms.office.com/Pages/ResponsePage.aspx?id=mhxxjxzsu023kLsMdxsdzM6J33C5yQRJgc1SHWy_64dURVlWV00xUEE0RFc4R01OVTA1RzZJTFUyQy4u)
    

<div style="text-align: center;">
<iframe width="560" height="315" src="https://www.youtube.com/embed/TYqdU9GPRDE?si=raK3NlXORXF6iOtP" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</div>


---
# Part 4: remote wireshark capture with ssh    
    
**Pre-steps) set up ssh server to password authenticate**   
From the ubuntu machine:
#### `sudo sed -i 's/^#\?PasswordAuthentication .*/PasswordAuthentication yes/' /etc/ssh/sshd_config && sudo systemctl restart ssh`    

## Method 1: more versitile and more complicated    
**Step 1) Create a named pipe (called a FIFO)**    
create directory for the captured files:    
#### `mkdir -p ~/Desktop/rc/`
#### `mkfifo ~/Desktop/rc/capture_pipe`

    
Here, you're creating a named pipe called remotepacketcapture1 in the /Desktop/tmp/ directory. This named pipe acts as a communication channel or endpoint for passing data between processes.    
    
**Step 2) Starting Wireshark with -k and -i options**    
#### `sudo wireshark -k -i ~/Desktop/rc/capture_pipe`   

This command starts Wireshark with the -k option to prepare it for packet capture without actually capturing packets immediately, and the -i option specifies the interface from which Wireshark should capture packets, in this case, the named pipe capture_pipe.    

**Step 3: Capturing Packets with tcpdump over SSH**    
#### `ssh <user>@<target.ip.address> “sudo tcpdump -s 0 -U -n -w - -i ens5 not port 22” > ~/Desktop/rc/capture_pipe` 
 - ex. ssh -t ubuntu@10.15.62.207 "sudo tcpdump -s 0 -U -n -w - -i ens5 not port 22" > ~/Desktop/rc/capture_pipe
    
Here, you're SSHing into <target.ip.address> as <user> and running tcpdump with sudo privileges to capture packets on interface eth5. The captured packets are then streamed through SSH and redirected (>) into the named pipe capture_pipe.
    
**sudo**: This command is used to execute tcpdump with superuser (root) privileges. This is necessary because capturing packets typically requires elevated permissions.    
    
**tcpdump**: This is the command-line packet analyzer. It allows you to capture or filter network traffic.    
    
**-s 0**: This flag sets the snapshot length to 0, which means tcpdump will capture the entire packet. By default, tcpdump captures only the first 68 bytes of each packet, but -s 0 ensures that the entire packet is captured.    
    
**-U**: This flag sets the output to be unbuffered. Without this flag, tcpdump might buffer its output, which can cause delays in displaying packets, especially in real-time scenarios.    
    
**-n**: This flag tells tcpdump not to resolve IP addresses to hostnames. Instead of resolving IP addresses to hostnames using DNS, tcpdump will display numeric IP addresses.    
    
**-w -**: This flag specifies the file to which tcpdump should write the captured packets. In this case, - indicates that tcpdump should write the packets to standard output (stdout) instead of a file. This is important because the output is then redirected to the SSH connection and subsequently to the named pipe.    
    
With this setup, Wireshark is reading packets from the named pipe remotepacketcapture, while tcpdump is capturing packets on the remote system and streaming them into the same named pipe. This allows you to effectively capture and view network traffic in real-time using Wireshark.    
**-i eth0**: This flag specifies the interface on which tcpdump should capture packets. In this case, eth0 is specified, indicating the first Ethernet interface.    
**not port 22**: This is a filter expression used to exclude packets with a destination or source port of 22 (SSH). It means tcpdump will capture all packets except those associated with SSH traffic. This can be useful to avoid capturing your own SSH traffic, which might flood the output.    


<div style="text-align: center;">
<iframe width="560" height="315" src="https://www.youtube.com/embed/STaGzIRAZG8?si=6Iq3ddsSPJmtm5MV" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</div>
    
## Method 2: wireshark sshdump feature
## less versitile fewer complications   
Step 1: open wireshark with sudo 
#### `sudo wireshark`    

 <div style="text-align: center;">
  <img src="{{ 'classes/LANgeist/images/sshwireshark1-openwireshark.png' | relative_url }}" alt="" style="max-width: 80%; height: auto;">
</div>

Step 2: Select Capture > Options > SSH remote capture: sshdump    

Step 3a: Add in the IP address and the port # for the device you are trying to capture from

 <div style="text-align: center;">
  <img src="{{ 'classes/LANgeist/images/sshwireshark2-server-address.png' | relative_url }}" alt="" style="max-width: 80%; height: auto;">
</div>

Step 3b: Add in authentication    
Username: ubuntu    
Password: password    
    
Step 3c: Add in capture data    
Because we are still in a virtual environment and you are using ssh into the box you are getting into, filter out port 22      
##### `sudo tcpdump -s 0 -U -n -w - -i ens5 not port 22`    
      
 <div style="text-align: center;">
  <img src="{{ 'classes/LANgeist/images/sshwireshark2-server-address.png' | relative_url }}" alt="" style="max-width: 80%; height: auto;">
</div>

Step 4: Select Start    




Defense:    
Developing RSA key pair for more secure remote log-in    
 

### Try it now    
Log into your Ubuntu box    
Ensure sshd is running and password enabled (see SSHerlock)    
Log into your Kali box    
Remote SSH capture with Wireshark from your Kali box    
In a different terminal on your Kali box, ping your Ubuntu box    
ping 10.15.x.x    
See if you can read the pings on your Kali box from the perspective of the ubuntu box    
 
## Remote Wireshark Capture with SSH Practice
**Must be pre-set up in lab**  
    
LANgeist Target7:    
IP:10.15.34.250    
Username: agent    
Password: agent    
What IP address is pinging Target7?
    
LANgeist Target6:    
IP:10.15.69.25    
Username: agent    
Password: agent    
What IP address is pinging Target6?

**Attacking the attacker**    
ICMP (ping flood)	Overloads bully’s ICMP traffic    
#### `ping -f -s 65507 <bully-ip>`	    
#### `hping3 --flood --icmp <bully-ip>`	    
    
TCP RST attack: Closes TCP connections on specific ports    
#### `hping3 --rst -p <port#> -c 10000 <bully-ip>`	  
#### `iptables -A OUTPUT -p tcp --dport <port#> -d <bully-ip> -j DROP`	  

UDP attack: Overload and Block    
#### `hping3 --flood --udp -p <port#> <bully-ip>`	    
#### `iptables -A INPUT -p udp --sport <port#> -s <bully-ip> -j DROP`	    
    
    

 
---

# Use the Dsniff tool Macof to conduct a MAC Flood attack     

https://charlesreid1.com/wiki/MITM/Wired/MAC_Flood#MAC_Flood_Attack

---

# Part 5: on-path attack with ettercap
## does not work on cyber.org range    

    
**Step 1: Allow IP forwarding in on the attack machine (Kali2)**    
### `echo 1 > /proc/sys/net/ipv4/ip_forward`    
to verify:    
#### `cat /proc/sys/net/ipv4/ip_forward`    

 <div style="text-align: center;">
  <img src="{{ 'classes/LANgeist/images/ettercap-1.png' | relative_url }}" alt="" style="max-width: 80%; height: auto;">
</div>
    
set ethernet to promiscuous mode      
#### `set eth0 to promisc`    

 <div style="text-align: center;">
  <img src="{{ 'classes/LANgeist/images/ettercap2.png' | relative_url }}" alt="" style="max-width: 80%; height: auto;">
</div>
    
**Step 2: Setup Ettercap on the Attacker Machine (Kali2)**    
Open Ettercap: Launch Ettercap in graphical mode on Kali2 (the attacking machine) by searching for it in the application menu or running    
    
Get the routers IP address (if arping to the internet and not just on LAN)    
#### `ip r`

 <div style="text-align: center;">
  <img src="{{ 'classes/LANgeist/images/ettercap3.png' | relative_url }}" alt="" style="max-width: 80%; height: auto;">
</div>
    
open ettercap on terminal    
#### `sudo ettercap -G`    
    
<div style="text-align: center;">
  <img src="{{ 'classes/LANgeist/images/ettercap4.png' | relative_url }}" alt="" style="max-width: 80%; height: auto;">
</div>
    

Select the Network Interface: In Ettercap, select the network interface connected to the 10.15.0.1/17 network.     

Click the checkmark up in the corner that says “accept” when you hover over it    
    
Click the Magnify glass in the top left of the Ettercap window to scan for hosts    
    
Scan for Hosts: Use Ettercap to scan the network for hosts. This can typically be done under the "Hosts" menu, selecting "Scan for hosts". After scanning, you should see a list of detected hosts in your network, including the Ubuntu server (10.15.109.49) and Kali1 (10.15.39.9).    
    
If you know the hosts you are targeting, you can select the three dots in the top right, select ‘current tagets’ add the IP addresses and then select “Scan for hosts”, this takes a great deal less time on larger networks.     
    
Add Targets: In Ettercap, add your targets. Target 1 should be the Ubuntu SSH server (10.15.109.49), and Target 2 should be Kali1 (10.15.39.9), the machine attempting to SSH into the Ubuntu server.    
    
<div style="text-align: center;">
  <img src="{{ 'classes/LANgeist/images/ettercap5.png' | relative_url }}" alt="" style="max-width: 80%; height: auto;">
</div>
    
**Step 3: ARP Poisoning**    
    
ARP Poisoning: With both targets set, initiate ARP poisoning to place Kali2 in the communication path between Kali1 and the Ubuntu server. This is typically done from the "MitM" (Man in The Middle) menu, selecting "ARP poisoning". Make sure to check the option to "Sniff remote connections" if available.    
    
Start Sniffing: After initiating ARP poisoning, start sniffing the network traffic by selecting the "Start Sniffing" option. This action enables Ettercap to capture the packets passing between Kali1 and the Ubuntu server.    
<div style="text-align: center;">
  <img src="{{ 'classes/LANgeist/images/ettercap6.png' | relative_url }}" alt="" style="max-width: 80%; height: auto;">
</div>
    
**Step 3: Monitor and Analyze Traffic**
    
Monitor SSH Attempts: On Kali2, watch the traffic captured by Ettercap for any SSH login attempts from Kali1 to the Ubuntu server. Remember, SSH traffic will be encrypted, including authentication attempts, so capturing the password directly is not possible through this method.    

<div style="text-align: center;">
  <img src="{{ 'classes/LANgeist/images/ettercap7.png' | relative_url }}" alt="" style="max-width: 80%; height: auto;">
</div>

<div style="text-align: center;">
  <img src="{{ 'classes/LANgeist/images/ettercap8.png' | relative_url }}" alt="" style="max-width: 80%; height: auto;">
</div>

<div style="text-align: center;">
  <img src="{{ 'classes/LANgeist/images/ettercap9.png' | relative_url }}" alt="" style="max-width: 80%; height: auto;">
</div>
    
 Use Wireshark: For a more detailed analysis, you might also use Wireshark in parallel to Ettercap on Kali2 to capture and analyze the traffic. This can give you insights into the encryption and protocol negotiation, but, as with Ettercap, decrypting SSH traffic to reveal passwords is not feasible without the encryption keys.    
    
**Post-Attack Steps**    
    
Stop the Attack: When your analysis is complete, remember to stop ARP poisoning and sniffing in Ettercap to restore normal network operation.    
    
Analyze Findings: Reflect on the implications of your findings and the importance of securing network communications against on-path attacks.    
    
Report: In a real-world ethical hacking scenario, you would now report your findings, including the techniques used, the data captured, and recommendations for mitigating such attacks.    

**Conclusion**    
While Ettercap can demonstrate the ease of conducting on-path attacks and capturing network traffic, the secure nature of SSH encryption highlights the challenges of intercepting sensitive information such as passwords. This exercise underscores the importance of securing networks and educating about the potential vulnerabilities and the effectiveness of encryption in protecting data.    

.
