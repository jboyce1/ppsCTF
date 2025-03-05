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

---

## Part 1a: 
## Installing and using zenmap on the cyber.org range 
Switch to Root User: Begin by switching to the root user to perform administrative tasks.  
#### `sudo su`  
Update Package Repository: Ensure that the package repository is up to date to fetch the latest available packages.  
#### `sudo apt update`  
Download Zenmap: Download Zenmap
#### `wget https://github.com/jboyce1/ppsCTF/raw/main/classes/CyberCartographer/zenmap-7.91-1.noarch.rpm`
Install Alien Package Converter: Since the downloaded package is in RPM format, it needs to be converted to a Debian package (.deb) format. Install the Alien package converter tool to facilitate this conversion.
#### `sudo apt-get install alien` 
press y and enter when asked
Convert RPM to DEB: Use Alien to convert the RPM package to a DEB package.  
#### `sudo alien zenmap-7.94-1.noarch.rpm`  
Install Zenmap: After conversion, install Zenmap using the DEB package.   
#### `dpkg --install zenmap_7.94-2.all.deb`  
Install all the dependencies for python2
#### `sudo ln -s /usr/bin/python2 /usr/bin/python`
#### `sudo apt-get install python-gtk2`
#### `sudo apt-get install python-gnome2 libgnomecanvas2-0 libgdk-pixbuf2.0-0`
Start Zenmap: Launch Zenmap from the terminal with administrative privileges.
#### `sudo zenmap`  or Select application from the 

Explanation of flags:  
sudo: Execute the command with superuser privileges.  
apt-get install: Command to install packages from the Debian package repository.  
alien: A tool used to convert between different package formats.  
dpkg --install: Command to install a package (in this case, the DEB package).  
sudo: Execute the command with superuser privileges.  
  
<div style="text-align: center;">
<iframe width="560" height="315" src="https://www.youtube.com/embed/UrGKgu5HauE?si=ys1g6VsgT7xHxaxv" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</div>

## Part 1b: 
### Setting up drawio on the cyber.org range (10-12 minutes in the range)
Install the packages
#### `sudo apt-get update`
#### `sudo apt-get install default-jdk`
#### `wget https://github.com/jgraph/drawio-desktop/releases/download/v26.0.9/drawio-amd64-26.0.9.deb`

Ensure the drawio is in the folder you are in by using ls
#### `sudo apt-get install ./drawio-amd64-26.0.9.deb`  
Run by checking the applications menu or using `drawio` in terminal

Samba is not working in the range, so you will need to SCP for sharing
Download the template and start adding information to it
#### `wget https://github.com/jboyce1/ppsCTF/raw/main/classes/CyberCartographer/CyberCartographer_template.drawio`

Save the template locally (or in a shared shared folder)
Add valid targets to the draw.io template in the next steps   

<div style="text-align: center;">
<iframe width="560" height="315" src="https://www.youtube.com/embed/xKIVex4OhXg?si=weB48EIq3UdooMSj" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</div>  

---
## Part 2:  
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
#### `sudo nmap -n -sn <default.gate.way.address/subnet> -oG - | awk '/Up$/{print $2}'`    
To understand the command:      
 - -n: Turns off reverse name resolution for faster processing.      
 - -sn: Disables port scanning (equivalent to deprecated -sP).      
 - -oG -: Sends grepable output to stdout for piping.  
 - awk '/Up$/{print $2}': Selects lines ending with "Up" to capture online hosts' IP addresses. Prints the second whitespace-separated field, which is the IP address.  
Step 5) And to turn this into a text file:  
#### `sudo nmap -n -sn <default.gate.way.address/subnet> -oG - | awk '/Up$/{print $2}' > hosts.txt`   

<div style="text-align: center;">
<iframe width="560" height="315" src="https://www.youtube.com/embed/j-4UYbXKNVs?si=UsMmou5w9xgooYjM" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</div>
---  

## Part 3:
## Use nmap to identify and isolate hosts with password authentication OpenSSH  

**Step 1) Use Text File of IP Addresses** Utilizing the lua scripting language and nmap scripting library with flags to see the scripts from terminal: 
#### `cd /usr/share/nmap/scripts/`  
#### `ls`  
**Step 2 (hard)) Identify Hosts with OpenSSH** We'll use nmap to scan for hosts with OpenSSH running on port 22. Here's the command breakdown:  
#### `sudo nmap -p 22 --script ssh-auth-methods --script-args="ssh.user=*" <targetIP>`  

 Flags explained:  
-p 22: Specifies port 22, which is the default port for SSH.
--script ssh-auth-methods: Runs the SSH authentication methods script to determine the authentication methods supported by the SSH server.
--script-args="ssh.user=*": Specifies the username to be used for SSH authentication. The wildcard (*) indicates that any username can be used.    

**Step 2 (easy))** Using -iL Flag with Text File: To use the text file containing IP addresses, we'll employ the -iL flag.   
#### `sudo nmap -p 22 --script ssh-auth-methods --script-args="ssh.user=*" -iL hosts.txt`    
-iL hosts.txt: Specifies the input file containing a list of IP addresses. Adjust the filename (hosts.txt) according to your text file's name.    
    
OpenSSH hunt (1)
    
  <div style="text-align: center;">
<iframe width="560" height="315" src="https://www.youtube.com/embed/qb_wUWrZAo8?si=uf2W5RIsKQEXBDOz" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>  
  </div>
  

---

## Part 4:
## Identify and validate telnet services on the network
    
Install telnet on kali
### `sudo apt update && sudo apt install telnet`
- install the pacakage maintainer's version when asked
    
Use Nmap to Identify Hosts Running Telnet  
We'll use **Nmap** to scan the network and identify hosts with **Telnet open on port 23**.  
    
#### `sudo nmap -p 23 --open <targetIP>`  
    
Flags explained:  
- `-p 23`: Scans for Telnet services on port 23.  
- `--open`: Only shows hosts with **port 23 open** to filter out unnecessary data.  
    
Scan a List of IPs for Telnet  
To scan multiple hosts, use an input file containing **a list of IP addresses**:  
    
#### `sudo nmap -p 23 --open -iL hosts.txt`  

Flags explained:  
- `-iL hosts.txt`: Loads a file (`hosts.txt`) containing **multiple target IPs** for scanning.  
    
Log Into a Telnet Device to Validate Access  
Once you've identified a host running Telnet, use the **telnet command** to connect:  
#### `telnet <targetIP>`    
If telnet is running on another port    
#### `telnet <targetIP> <port#>`    

If authentication is required, **enter the username and password** when prompted.

Verify the Connection  
After logging in, confirm the Telnet session is active by running:  
#### `whoami`  
#### `hostname`  
#### `ls`  
This validates **successful access** to the remote system.   
    
Exit the Telnet Session  
To safely disconnect, type:  
#### `exit`  
    
This closes the Telnet session and returns you to the **Kali terminal**.
    
  
---
## Part 5:
## Identify and validate ftp services on the network

Install FTP Client on Kali    
In termial type `ftp --version`, if anything comes up, skip the install.
Ensure FTP client tools are installed before scanning:  
#### `sudo apt update && sudo apt install ftp`  

Use Nmap to Identify Hosts Running FTP  
We'll use **Nmap** to scan the network and identify hosts with **FTP open on port 21**.  

#### `sudo nmap -p 21 --open <targetIP>`  
#### `sudo nmap -p 21 --open hosts.txt'    

Flags explained:  
- `-p 21`: Scans for FTP services on port 21.  
- `--open`: Only shows hosts with **port 21 open** to filter out unnecessary data.  

Scan a List of IPs for FTP  
To scan **multiple hosts**, use an input file containing **a list of IP addresses**:  

#### `sudo nmap -p 21 --open -iL hosts.txt`  
`    
Flags explained:  
- `-iL hosts.txt`: Loads a file (`hosts.txt`) containing **multiple target IPs** for scanning.  
#### `sudo nmap -p 21 --open <targetIPlow>-<targetIPhigh> | grep "Nmap scan report for" | awk '{print $5}'    
Use Nmap to Check for Anonymous FTP Access  
Nmap has a built-in script to test for **anonymous FTP login**:  

#### `sudo nmap -p 21 --script ftp-anon <targetIP>`  
#### `sudo nmap -p 21 --script ftp-anon -iL hosts.txt`  
Flags explained:  
- `--script ftp-anon`: Runs a script that checks if **anonymous login is allowed** on the FTP server.  

Use FTP Client to Manually Validate Access  
Once you've identified an FTP server, connect to it:  

#### `ftp <targetIP>`  

Check if FTP is running on another port:  
#### 'sudo nmap -p 21000-24000 --script ftp-anon -iL Hosts.txt -oN ftp_high_ports.txt'    

To connect:    
#### `ftp <targetIP> <port#>`    

When prompted for login:  
- **Username:** `anonymous`  
- **Password:** Press **Enter**  

Verify Anonymous Access  
Once connected, check if you can list and retrieve files:  

#### `ls`  
#### `get <filename>`  

If the command succeeds, **anonymous FTP is enabled**.  

Exit the FTP Session  
To safely disconnect, type:  
#### `bye`  

This closes the FTP session and returns you to the **Kali terminal**.

Scan high ports for ftp services

---
## Part 6:
## Scan a range of high ports for services detected    
If you know the port range you want to scan
#### `sudo nmap -p 20000-24000 --open -sV 10.15.0.0/17`    

-p 20000-24000 → Scans only high ports 20000-24000.    
--open → Only show hosts with open ports.    
-sV → Service version detection to identify if FTP, SSH, or Telnet is running.    
10.15.0.0/16 → Replace with your target subnet.    

If you have a file of hosts.txt that you want to scan
#### `sudo nmap -p 20000-24000 --open -sV -iL hosts.txt`    
to save your results     
#### `sudo nmap -p 20000-24000 --open -sV -iL hosts.txt -oN high_port_scan_results.txt`   
---
## Practice and explore
   
### [TryHackMe-Independent-nmap]({{ 'classes/CyberCartographer/TryHackMe-Independent-nmap.pdf' | relative_url }})
Or just do the whole room    
https://tryhackme.com/room/networkservices    

 
### Find your own high ports    
### Best done with multiple teammates on the range   
Step 1:    Start your ubuntu machine from the cyber.org range and open up some services      
    
start telnet       
#### `wget https://raw.githubusercontent.com/jboyce1/ppsCTF/main/classes/CyberCartographer/flagscripts/deploy-telnet-23.py`    
#### `sudo python3 deploy-telnet-23.py`    
    
start an ftp server and place a file in it
#### `wget https://raw.githubusercontent.com/jboyce1/ppsCTF/main/classes/CyberCartographer/flagscripts/ftp-anon-login.py`
#### `sudo python3 ftp-anon-login.py`    
#### `nano test.txt`
#### `chmod 777 test.txt`
    
start ssh on a highport    
#### `wget https://raw.githubusercontent.com/jboyce1/ppsCTF/main/classes/CyberCartographer/flagscripts/ssh-highport-generator.py`    
#### `sudo python3 ssh-highport-generator.py`    

start ftp on a highport    
#### `wget https://raw.githubusercontent.com/jboyce1/ppsCTF/main/classes/CyberCartographer/flagscripts/ftp-anon-highport.py`    
#### `sudo python3 ftp-anon-highport.py`    

Step 2:    Start your kali machine from the cyber.org range try to find your open ports     

---
## Other useful scans
#### 'nmap -p 20000-24000 --open -sV 10.15.0.0/16'    
-p 20000-24000 → Scans only high ports 20000-24000.    
--open → Only show hosts with open ports.    
-sV → Service version detection to identify if FTP, SSH, or Telnet is running.    
10.15.0.0/16 → Replace with your target subnet.    

#### 'nmap -p 21,22,23 --open -sV -iL hosts.txt'  
-p 21,22,23 → Scan for FTP, SSH, and Telnet.  
--open → Only show hosts where a service is running.  
-sV → Detect service versions.  
-iL hosts.txt → Scan only IPs listed in hosts.txt.  

#### 'nmap -sC -sV -p 80,443 10.15.0.0/16'  
-sC → Runs default Nmap scripts.  
-sV → Service version detection.  
-p 80,443 → Scan for web servers on ports 80 (HTTP) and 443 (HTTPS).  

#### 'nmap --script ftp-anon -p 21 10.15.0.0/16'  
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

  
mkfifo /Desktop/remotecaptures/remotepacketcapture1
