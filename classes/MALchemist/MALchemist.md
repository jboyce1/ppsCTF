---
layout: default
title: MALchemist
---

# MALchemist   

**Focus**: Malware  
**Skill**: Analyze, Create, and Deploy Basic Malware  
**Activity**:  

<div style="text-align: center;">
  <img src="{{ 'classes/MALchemist/images/Malchemist-header.jpg' | relative_url }}" alt="" style="max-width: 80%; height: auto;">
</div>    

## Some wizards cast spells that seem like magic
### that other wizards craft in code
---
**play a game while I yap**:
sudo apt install greed
greed

sudo apt install pacman4console
pacman4console

sudo apt install zangband
man atc
atc

Specific Skills:
- Deploy a basic trojan horse
- Use IDLE to conduct malware analysis
- Use IDLE any to modify python based malware
- Use SSH and SCP to deploy and run scripts on remote devices
- Use psutil to monitor actions on remote computer
    
**Thing to experiment with on the range**:
VNC
msfconsole payloads
    
#### Offensive Operations:
Deploying Trojans: Malchemists can craft and deploy Trojan horses, disguising them within seemingly legitimate software or scripts. These Trojans can be used to establish backdoors, exfiltrate data, or disrupt operations within an enemy's network.     
    
Script Deployment via SSH/SCP: With SSH and SCP, Malchemists can remotely deploy and execute scripts on target systems. These scripts could range from reconnaissance tools to actual payloads, enabling further penetration into the network or system. For the competition, deploying and executing basic trojans on the opponents' range will count for points.    
    
Monitoring with Psutil: Utilizing Psutil, Malchemists monitor systems for unusual activities that might indicate the presence of malware or unauthorized processes. By scrutinizing system behavior, they can spot and halt malicious actions before they cause significant damage. For the competition, deploying and monitoring basic spyware on the opponents' range will count for points.    
    
### Defensive Operations:
Malware Analysis with IDLE: On defense, Malchemists employ IDLE for detailed malware analysis, dissecting suspicious Python scripts to understand their structure, functionality, and potential impact. By understanding the threat, they can develop countermeasures and remove the malicious elements from their systems. For the competition, the discovery and removal of malware on your systems will prevent them from being accessed by your opponent.    
    
Malware Decontamination: The defensive Malchemist is skilled in identifying, classifying, and eradicating malware infections within their network. This includes quarantining infected systems, analyzing and reverse-engineering malware samples, and patching vulnerabilities to prevent future attacks. Additional points are achieved by classifying the malware that has infected your system.    
    
Both offensive and defensive cyber operations can benefit from the capabilities of these tools, either by exploiting their potential to penetrate and compromise systems or by leveraging their strengths to defend and fortify against such intrusions. It’s a digital arms race where the same tools can be purposed for attack or defense, depending on the hands they are in.

---
# part 1: deploy a basic trojan horse    

Start a Kali machine and Ubuntu machine
    
On Kali    
Download the SecurePixViewer-ping.py file to your downloads folder on the kali machine into the Downloads folder:
#### `wget https://raw.githubusercontent.com/jboyce1/ppsCTF/main/classes/MALchemist/BasicTrojan/SecurePixViewer_ping.py`  
or add the flag to direct it to go to the downloads folder    
#### `wget -P ~/Downloads https://raw.githubusercontent.com/jboyce1/ppsCTF/main/classes/MALchemist/BasicTrojan/SecurePixViewer_ping.py`
      
Download the Trojan_Horse.jpg to the Downloads folder    
#### `wget https://raw.githubusercontent.com/jboyce1/ppsCTF/main/classes/MALchemist/BasicTrojan/Trojan_Horse.jpg`    

Navigate to the Downloads directory from terminal (or open a terminal from the Downloads directory)    
run the program from terminal using the following command:    
#### `python3 SecurePixViewer-ping.py`    
Ctrl + C to quit the process    

**Now lets get it to ping your ubuntu machine**:    
On Ubuntu open a terminal, write down its ip address and start wireshark with superuser priviledges   
sudo wireshark    
Click on the network interface that is connecting to the internet (activity on line graph next to it)    
On Kali    
Open terminal and open the SecurePixViewer-ping.py    
nano SecurePixViewer-ping.py    
Replace the 192.168.1.100 with the ip address of your ubuntu machine    
Run the program again    
python3 SecurePixViewer-ping.py    
On Ubuntu    
Stop Wireshark by clicking on the red box in the top left    
In the search bar look for the pings by searching    
ip.addr == your.kali.ip.here    
Try it now    
Change some of the parameters (ping size/timing or message) and run it again.
