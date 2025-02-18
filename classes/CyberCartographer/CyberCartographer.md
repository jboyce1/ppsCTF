---
layout: default
title: CyberCartographer
---

# CyberCartographer    

**Focus**: Network Mapping  
**Skill**: Utilize nmap, zenmap and draw.io to develop actionable offensive and defensive maps  
**Activity**: Identification of the most vulnerable machines on a network  

<div style="text-align: center;">
  <img src="{{ 'classes/CyberCartographer/93909-CyberCartography-with-nmap-banner.png' | relative_url }}" alt="Hash Hound Logo" style="max-width: 80%; height: auto;">
</div>

---
### CyberCartography with nmap, zenmap and draw.io
## Here be Dragons

### Specific Skills
- Use nmap to identify all hosts on the network
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


### Setting up drawio on the cyber.org range (10-12 minutes in the range)
####  - `sudo apt-get update`
####  - `sudo apt-get install default-jdk`
####  - `wget https://github.com/jgraph/drawio-desktop/releases/download/v26.0.9/drawio-amd64-26.0.9.deb`

Ensure the drawio is in the folder you are in by using ls
####  - `sudo apt-get install ./drawio-amd64-26.0.9.deb`  
Run by checking the applications menu or using `drawio` in terminal

Samba is not working in the range, so you will need to SCP for sharing  

---
## Part 1:  
## Use nmap to identify all hosts on the network
## Use nmap to create a text file of all the open hosts



### **Walkthrough**
Step 1) Determine the IP Address Range: To begin, find the range of IP addresses. Start by locating the default gateway, which is the lowest IP address on the network.  
#### `arp -a`  
Step 2) Calculate Subnet Size: Once you've found the lowest IP address, determine the number of IP addresses in the subnet. Identify the subnet mask (CIDR) using   
#### `ip addr`    
Look for the number of blocked bits in the subnet mask (e.g., /17, /24). This indicates the number of blocks in the subnet. Combine the first two components to scan the entire network.    
#### `sudo nmap -sn 10.15.0.1/17`    
Step 3) Generate a Text File of Open Hosts:    
For convenience, create a text document containing all the hosts. Execute the following command:    
#### `ls`  
#### `cd Desktop`  
#### `sudo nmap -sn 10.15.0.1/17 > hostsup.txt`    
Step 4) Extract only IP Addresses: To obtain only the IP addresses, use the following command:    
#### `nmap -n -sn <default.gate.way.address/subnet> -oG - | awk '/Up$/{print $2}'`    
To understand the command:      
 - -n: Turns off reverse name resolution for faster processing.      
 - -sn: Disables port scanning (equivalent to deprecated -sP).      
 - -oG -: Sends grepable output to stdout for piping.  
 - awk '/Up$/{print $2}': Selects lines ending with "Up" to capture online hosts' IP addresses. Prints the second whitespace-separated field, which is the IP address.  
Step 5) And to turn this into a text file:  
#### `nmap -n -sn <default.gate.way.address/subnet> -oG - | awk '/Up$/{print $2}' > HostsOnNetwork.txt`   

<div style="text-align: center;">
<iframe width="560" height="315" src="https://www.youtube.com/embed/j-4UYbXKNVs?si=UsMmou5w9xgooYjM" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</div>
---  

## Part 2:
## Use nmap to identify and isolate hosts with password authentication OpenSSH  

**Step 1) Use Text File of IP Addresses** Utilizing the lua scripting language and nmap scripting library with flags to see the scripts from terminal: 
#### `cd /usr/share/nmap/scripts/`  
#### `ls`  
**Step 2 (hard)) Identify Hosts with OpenSSH** We'll use nmap to scan for hosts with OpenSSH running on port 22. Here's the command breakdown:  
#### `nmap -p 22 --script ssh-auth-methods --script-args="ssh.user=*" <targetIP>`  

 Flags explained:  
-p 22: Specifies port 22, which is the default port for SSH.
--script ssh-auth-methods: Runs the SSH authentication methods script to determine the authentication methods supported by the SSH server.
--script-args="ssh.user=*": Specifies the username to be used for SSH authentication. The wildcard (*) indicates that any username can be used.    

**Step 2 (easy))** Using -iL Flag with Text File: To use the text file containing IP addresses, we'll employ the -iL flag.   
#### `nmap -p 22 --script ssh-auth-methods --script-args="ssh.user=*" -iL hosts.txt`    
-iL hosts.txt: Specifies the input file containing a list of IP addresses. Adjust the filename (hosts.txt) according to your text file's name.    
    
OpenSSH hunt (1)
    
  <div style="text-align: center;">
<iframe width="560" height="315" src="https://www.youtube.com/embed/qb_wUWrZAo8?si=uf2W5RIsKQEXBDOz" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>  
  </div>
  
---

## Part 3: 
## Installing and using zenmap on the cyber.org range  
  
Switch to Root User: Begin by switching to the root user to perform administrative tasks.  
#### `sudo su`  
Update Package Repository: Ensure that the package repository is up to date to fetch the latest available packages.  
#### `sudo apt update`  
Download Zenmap: Download Zenmap  
Install Alien Package Converter: Since the downloaded package is in RPM format, it needs to be converted to a Debian package (.deb) format. Install the Alien package converter tool to facilitate this conversion.  
#### `sudo apt-get install alien`  
Convert RPM to DEB: Use Alien to convert the RPM package to a DEB package.  
#### `sudo alien zenmap-7.94-1.noarch.rpm`  
Install Zenmap: After conversion, install Zenmap using the DEB package.   
#### `dpkg --install zenmap_7.94-2.all.deb`  
Start Zenmap: Launch Zenmap from the terminal with administrative privileges.  
#### `sudo zenmap`  

Explanation of flags:  
sudo: Execute the command with superuser privileges.  
apt-get install: Command to install packages from the Debian package repository.  
alien: A tool used to convert between different package formats.  
dpkg --install: Command to install a package (in this case, the DEB package).  
sudo: Execute the command with superuser privileges.  
  
<div style="text-align: center;">
<iframe width="560" height="315" src="https://www.youtube.com/embed/UrGKgu5HauE?si=ys1g6VsgT7xHxaxv" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</div>

---

## Command Line Extras:  
  
mkfifo /Desktop/remotecaptures/remotepacketcapture1
