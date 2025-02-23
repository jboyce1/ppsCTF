---
layout: default
title: Ms. Disin
---

# Ms. Disin   

**Focus**: Text manipulation  
**Skill**: Use grep, sed, awk, diff, and sort to extract and manipulate text
**Activity**: Discover the most   

<div style="text-align: center;">
  <img src="{{ 'classes/MsDisin/Ms_Disin Banner2.jpg' | relative_url }}" alt="Hash Hound Logo" style="max-width: 80%; height: auto;">
</div>

---
### Sometimes the world can be a web of lies
## Be a spider

**play a game while I yap**:     
sudo apt install greed    
greed    
  
sudo apt install zangband    
man atc    
atc    

### Specific Skills
- Use cat to combine multiple text files and display their contents quickly
- Use grep and find to locate specific patterns of text within files across different directories
- Use sed to edit text files directly in the terminal
- Combine awk and sed to extract and transform specific data from files
- Use sort and uniq for sorting data and finding duplicates
- Use diff to compare files
- Use tail and head to view just the beginning or end of files


### Things to experiment with on the range:     
Regex with grep: Mastering regular expressions to refine search criteria and pinpoint exact data sets.    
Stream editing with sed: Practice on-the-fly file content manipulations during competitive scenarios.    
Data manipulation with awk: Leverage awk's programming capabilities to analyze and report on data extracted during competitions.    

 
### How this skill can be used:  
Offensive Operations:
 - Data Extraction Tactics: Utilize combinations of grep, awk, and sed to extract sensitive information from opponent’s files, which could range from passwords to strategic plans.
 - Script Manipulation: Through direct file editing using sed and cat, alter scripts or configurations in the enemy's network to disrupt their operations or misdirect their strategies.

Defensive Operations:
 - File Integrity Checks: Use grep and awk to monitor files for unauthorized changes that could indicate infiltration attempts.
 - Rapid Response Editing: Employ sed to quickly revert any unauthorized changes or to patch vulnerabilities in script configurations during live competitions.

 


---
## Use cat to combine multiple text files and display their contents quickly
### “cat” the cat and “grep” the dog (because who names a cat?)

<div style="text-align: center;">
  <img src="{{ 'classes/MsDisin/msdisins_dog.webp' | relative_url }}" alt="Hash Hound Logo" style="max-width: 80%; height: auto;">
</div>

Start a Kali machine    
Level 1:    
On Kali    
Download the cat observations   
Unzip the contents of the folder.    
Open a terminal inside the cat_observations folder    
use the cat command to read each passage    
cat cat_1    
(hint: use the up arrow key and backspace to quickly advance in the journal  

Level 2:    
On Kali

From  inside the cat_observations folder, open a terminal    
    
To display all of the text in the files:    
#### `find . -type f -exec cat {} +`    
To display all of the text in the files with their file names in order and get really fancy?:    
#### `find . -type f -name "*" | sort | xargs cat`    
Explaination of flags:    
 -  `find . -type f -name "*."`  Search for all files with an extension in the current directory (.) and its subdirectories.    
 - `| sort` pipes the output to sort in order to list of filenames alphabetically.    
 - `| xargs cat`  Pass the sorted list of filenames to the cat command to display their contents in order.   

<div style="text-align: center;">
  <img src="{{ 'classes/MsDisin/msdisins_cat.webp' | relative_url }}" alt="Hash Hound Logo" style="max-width: 80%; height: auto;">
</div>    

### Try it now    
use the dog_oberservations.zip to do the same thing    
Write a synopsis of what you think is happening here    

<div style="text-align: center;">
<iframe width="560" height="315" src="https://www.youtube.com/embed/jmTVwNt24Sk?si=6UXLuTWlRTuxneLB" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</div>
--- 

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

## Part 3:
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

## Part 4:
## Identify and validate telnet services on the network
    
Install telnet on kali
### `sudo apt update && sudo apt install telnet`
- install the pacakage maintainer's version when asked
    
Use Nmap to Identify Hosts Running Telnet  
We'll use **Nmap** to scan the network and identify hosts with **Telnet open on port 23**.  
    
#### `nmap -p 23 --open <targetIP>`  
    
Flags explained:  
- `-p 23`: Scans for Telnet services on port 23.  
- `--open`: Only shows hosts with **port 23 open** to filter out unnecessary data.  
    
Scan a List of IPs for Telnet  
To scan multiple hosts, use an input file containing **a list of IP addresses**:  
    
#### `nmap -p 23 --open -iL hosts.txt`  

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
    
  

## Part 5:
## Identify and validate ftp services on the network

Install FTP Client on Kali    
In termial type `ftp --version`, if anything comes up, skip the install.
Ensure FTP client tools are installed before scanning:  
#### `sudo apt update && sudo apt install ftp`  

Use Nmap to Identify Hosts Running FTP  
We'll use **Nmap** to scan the network and identify hosts with **FTP open on port 21**.  

#### `nmap -p 21 --open <targetIP>`  

Flags explained:  
- `-p 21`: Scans for FTP services on port 21.  
- `--open`: Only shows hosts with **port 21 open** to filter out unnecessary data.  

Scan a List of IPs for FTP  
To scan **multiple hosts**, use an input file containing **a list of IP addresses**:  

#### `nmap -p 21 --open -iL hosts.txt`  
`    
Flags explained:  
- `-iL hosts.txt`: Loads a file (`hosts.txt`) containing **multiple target IPs** for scanning.  
#### `nmap -p 21 --open <targetIPlow>-<targetIPhigh> | grep "Nmap scan report for" | awk '{print $5}'    
Use Nmap to Check for Anonymous FTP Access  
Nmap has a built-in script to test for **anonymous FTP login**:  

#### `nmap -p 21 --script ftp-anon <targetIP>`  
#### `nmap -p 21 --script ftp-anon -iL hosts.txt`  
Flags explained:  
- `--script ftp-anon`: Runs a script that checks if **anonymous login is allowed** on the FTP server.  

Use FTP Client to Manually Validate Access  
Once you've identified an FTP server, connect to it:  

#### `ftp <targetIP>`  

If FTP is running on another port:  
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

## Part 6:
## Scan a range of high ports for services detected    
If you know the port range you want to scan
#### `nmap -p 20000-24000 --open -sV 10.15.0.0/16`    
-p 20000-24000 → Scans only high ports 20000-24000.    
--open → Only show hosts with open ports.    
-sV → Service version detection to identify if FTP, SSH, or Telnet is running.    
10.15.0.0/16 → Replace with your target subnet.    

If you have a file of hosts.txt that you want to scan
#### `nmap -p 20000-24000 --open -sV -iL hosts.txt`    
to save your results     
#### `nmap -p 20000-24000 --open -sV -iL hosts.txt -oN high_port_scan_results.txt`   

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
