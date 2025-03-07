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
    
#### `sudo apt install moon-buggy    
#### `moon-buggy`    
    
#### `sudo apt install bsdgames    
#### `man atc    
#### `atc`    
    

**Specific Skills:**    
- Use TCP dump to identify traffic, gather detailed information about each packet sent    
- Use TCP dump to gather the entire packet, to include the packet payload    
- Use TCP dump to isolate attackers on your network with known IP addresses    
- Use SSH and Wireshark to remotely capture network traffic    
- Use Wireshark to capture traffic in promiscuous mode    
- Use the Dsniff tool Macof to conduct a MAC Flood attack    
    
## **Offensive Operations:**   
In the context of offensive cyber operations, tools like TCPdump, Wireshark, and Dsniff are integral to the toolkit of a skilled attacker or Red Team member. These tools serve multiple purposes, from reconnaissance to active network disruption.    
    
**Reconnaissance and Data Exfiltration:**    
TCPdump is a powerful command-line packet analyzer that allows for the capture of packets flowing through a network. In an offensive scenario, an attacker could use TCPdump to monitor and analyze traffic in real-time, identifying patterns, vulnerabilities, or valuable data. For instance, capturing packets to and from a target server could reveal unencrypted credentials, session tokens, or proprietary information being transmitted over the network. By gathering detailed packet payloads, attackers can reconstruct user sessions or exfiltrate sensitive data undetected. In a team vs team scenerio, knowing what the defenders are doing is going to help you know where you to attack.    
    
**Man-in-the-Middle (MitM) and Network Disruption:**    
Further exploiting network vulnerabilities, an attacker could employ the Dsniff tool suite, specifically the Macof tool, to conduct a MAC Flood attack. This type of attack overwhelms a switch's MAC address table, causing it to behave like a hub and broadcast packets to all ports. In this compromised state, an attacker can use TCPdump or Wireshark to capture a broad swath of network traffic, intercepting sensitive information that would normally not be accessible. This approach not only aids in information gathering but also disrupts normal network operations, potentially masking other malicious activities or creating a diversion. At the higher levels of point scale, you will have to get past a switch to get into the other teams network. This may not be in the 2024 session so do not spend cycles on it unless explicitly told.
    
**Remote Traffic Capture:**
Combining SSH with Wireshark provides an attacker the ability to remotely capture network traffic in a stealthy manner. By establishing an SSH tunnel to a compromised host within the target network, attackers can remotely execute Wireshark or TCPdump, funneling captured traffic back through the tunnel for analysis. This method allows for the monitoring of network traffic without being physically present on the network, reducing the risk of detection. This is going to be critical to get into the other teams network to see how their defenders are trying to protect their computers.    
    
## **Defensive Operations:**    
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

Step 1) Find your internet connection
#### `tcpdump -D`
  
 
