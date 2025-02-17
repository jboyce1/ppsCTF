---
layout: default
title: CyberCartographer
---

# CyberCartographer    

**Focus**: Network Mapping  
**Skill**: Utilize nmap, zenmap and draw.io to develop actionable offensive and defensive maps  
**Activity**: Identification of the most vulnerable machines on a network  

<div style="text-align: center;">
  <img src="{{ 'classes/HashHound/90255-Hash-Hound.png' | relative_url }}" alt="Hash Hound Logo" style="max-width: 80%; height: auto;">
</div>

---
### CyberCartography with nmap and zenmap
## Here be Dragons

### Specific Skills
- Use nmap to identify all hosts on the network
- Use nmap to create a text file of all open hosts
- Use nmap to identify and isolate hosts with password authentication OpenSSH
- Installing and using zenmap on the cyber.org range
- Use draw.io to develop and annotate a network map

How this skill can be used:  
**Offensive:**  
In the realm of offensive cybersecurity, the Red Team plays a critical role in reconnaissance and vulnerability exploitation. During the Discovery Phase, their primary objective is to gather intelligence about the network infrastructure, including identifying all hosts connected to it. The ability to swiftly and accurately enumerate network hosts is crucial for expediting subsequent attack phases.    

Zenmap, a graphical front-end for Nmap, is a valuable tool for this purpose. Its comprehensive scanning capabilities enable the Red Team to efficiently discover active hosts, open ports, and services running on the network. By quickly identifying the scope of the network and potential entry points, the Red Team can prioritize their efforts towards exploiting vulnerabilities and gaining unauthorized access.    

Zenmap's reporting features provide the Red Team with a consolidated view of their findings, aiding in the documentation of vulnerable hosts and exploited services. This information allows them to track their progress and plan subsequent attack strategies effectively.    

In summary, proficiency in using Zenmap for host discovery is essential for the Red Team's success in identifying and exploiting vulnerabilities within the network infrastructure, thereby achieving their objectives in offensive operations.
 

**Defensive:**    
In the realm of defensive cybersecurity, the Blue Team plays a pivotal role in protecting network assets and mitigating cyber threats. Host hardening, the process of strengthening the security posture of individual hosts within a network, is a fundamental aspect of their responsibilities. By proactively securing hosts against potential threats, the Blue Team aims to reduce the attack surface and mitigate the impact of security incidents. Tools like nmap and Zenmap are instrumental for the Blue Team in conducting vulnerability assessments and identifying weaknesses in network hosts. By scanning for open ports, services, and potential vulnerabilities, nmap provides valuable insights into areas of security weakness that require attention.    

Once vulnerabilities are identified, the Blue Team can leverage Zenmap's reporting capabilities to prioritize remediation efforts. By focusing on hosts with the highest risk exposure, they can allocate resources effectively and address critical security issues promptly.    


### Setting up drawio on the cyber.org range (10-12 minutes in the range)
 - sudo apt-get update
 - sudo apt-get install default-jdk
 - wget https://github.com/jgraph/drawio-desktop/releases/download/v26.0.9/drawio-amd64-26.0.9.deb

Ensure the drawio is in the folder you are in by using ls
 - sudo apt-get install ./drawio-amd64-26.0.9.deb
Run by checking the applications menu or using drawio in terminal

Samba is not working in the range, so you will need to SCP for sharing

## Use nmap to identify all hosts on the network
## Use nmap to create a text file of all the open hosts



## **Walkthrough**
Step 1) Determine the IP Address Range: To begin, find the range of IP addresses. Start by locating the default gateway, which is the lowest IP address on the network.  
`arp -a`  
Step 2) Calculate Subnet Size: Once you've found the lowest IP address, determine the number of IP addresses in the subnet. Identify the subnet mask (CIDR) using  
`ip addr`
Look for the number of blocked bits in the subnet mask (e.g., /17, /24). This indicates the number of blocks in the subnet. Combine the first two components to scan the entire network.
`sudo nmap -sn 10.15.0.1/17`
Step 3) Generate a Text File of Open Hosts:
For convenience, create a text document containing all the hosts. Execute the following command:
`ls`
`cd Desktop`
`sudo nmap -sn 10.15.0.1/17 > hostsup.txt`  
Step 4) Extract only IP Addresses: To obtain only the IP addresses, use the following command:
`nmap -n -sn <default.gate.way.address/subnet> -oG - | awk '/Up$/{print $2}'`
To understand the command:  
 - -n: Turns off reverse name resolution for faster processing.  
 - -sn: Disables port scanning (equivalent to deprecated -sP).  
 - -oG -: Sends grepable output to stdout for piping.  
 - awk '/Up$/{print $2}': Selects lines ending with "Up" to capture online hosts' IP addresses. Prints the second whitespace-separated field, which is the IP address.  
Step 5) And to turn this into a text file:  
`nmap -n -sn <default.gate.way.address/subnet> -oG - | awk '/Up$/{print $2}' > HostsOnNetwork.txt`   

<div style="text-align: center;">
<iframe src="https://mypps.sharepoint.com/sites/ppsCyberTacticsFest/_layouts/15/embed.aspx?UniqueId=8b3b12a4-1dd6-4873-a155-78602d0ae6ac&embed=%7B%22ust%22%3Atrue%2C%22hv%22%3A%22CopyEmbedCode%22%7D&referrer=StreamWebApp&referrerScenario=EmbedDialog.Create" width="640" height="360" frameborder="0" scrolling="no" allowfullscreen title="Hash-Hound-Fun-New-Game.mp4"></iframe>
</div>
---

## Part 2: Needle in the Hayloft  
  
Here is your md5sum needle: c6fca9b96af058081fe4bfd89523f3f4  
  
step1: Navigate to the '2 Needle in the Hayloft' directory    
step2: Make a text file using the following command:  
**`find . -type f -exec md5sum {} \; > 01md5sums.txt`**  

- Explaination for command      
  - **`find .`** searches for files and directories starting from the current directory (.).    
  - **`-type f`** specifies that we are interested in files only, not directories.    
  - **`-exec md5sum {} \;`** executes the md5sum command on each file found by find. {} represents the current file being processed by find.    
  - **`> md5sums.txt`** redirects the output (MD5 checksums) to a file named md5sums.txt.    
  
step3: open the text file and search (ctrl+f) the needle you are looking for       
step4: open the file and find the flag  

For more informaiton on the find functions, read the manual:   
man find        

**Download Practice Files**:    
📥 [Practice 1](./Needle%20in%20the%20Hayloft%20Practice/2%20Needle%20in%20the%20Hayloft%20(practice%201).zip)    
📥 [Practice 2](./Needle%20in%20the%20Hayloft%20Practice/2%20Needle%20in%20the%20Hayloft%20(practice%202).zip)    
📥 [Practice 3](./Needle%20in%20the%20Hayloft%20Practice/2%20Needle%20in%20the%20Hayloft%20(practice%203).zip)    
  <div style="text-align: center;">
<iframe src="https://mypps.sharepoint.com/sites/ppsCyberTacticsFest/_layouts/15/embed.aspx?UniqueId=c5bd88bb-87aa-4db1-838a-64ff932260d6&embed=%7B%22ust%22%3Atrue%2C%22hv%22%3A%22CopyEmbedCode%22%7D&referrer=StreamWebApp&referrerScenario=EmbedDialog.Create" width="640" height="360" frameborder="0" scrolling="no" allowfullscreen title="Hash-Hound-Needle-in-the-Hayloft.mp4"></iframe>   
  </div>
  
---

## Part 3: Coming to Greps with the Past  
  
### Suspicious Needle Search  

You need to find the suspicious needle. They were all good when they left but something changed. The `knowngood_md5sums_filenames.txt` is a list of all the unsuspicious files.  
  
**step1:** Navigate to the directory containing `knowngood_md5sums_filenames.txt`  
**step2:** Extract all of the hashes from the `knowngood_md5sums_filenames.txt` using the command:  
`cut -d ' ' -f 1 knowngood_md5sums_filenames.txt > knowngood_hashes.txt`  
  
- Explanation for command
  - `cut -d ' '` specifies the delimiter as a space.
  - `-f 1` selects the first field, which is typically the hash value.
  - `> knowngood_hashes.txt` redirects the output to a file named `knowngood_hashes.txt`.  
  
**step3:** Find all the MD5 sums in the directory using the command:    
`find . -type f -exec md5sum {} \; > current_md5sums_filenames.txt`    
  
**step4:** Extract all hashes from the `current_md5sums_filenames.txt` using:  
`cut -d ' ' -f 1 current_md5sums_filenames.txt > current_hashes.txt`  

**step5:** Search for lines in `current_hashes.txt` that are not in `knowngood_hashes.txt` and write them to a new file called `non_matching_hashes.txt` using:    
`grep -vf knowngood_hashes.txt current_hashes.txt > non_matching_hashes.txt`    
  
**step6:** Find and inspect all the files in the `non_matching_hashes.txt` by finding (ctrl+f) the hashes in the `current_md5sums_filenames.txt` or use `grep` again to find these files:    
`grep -F -f non_matching_hashes.txt current_md5sums_filenames.txt`  
  
**Download Practice Files**:    
📥 [Practice 1](./Coming%20to%20greps%20with%20the%20past/3%20Coming%20to%20greps%20with%20the%20past%20(practice%201).zip)    
<div style="text-align: center;">
<iframe src="https://mypps.sharepoint.com/sites/ppsCyberTacticsFest/_layouts/15/embed.aspx?UniqueId=9f33c970-8bcc-4123-bd43-fdefbd355660&embed=%7B%22ust%22%3Atrue%2C%22hv%22%3A%22CopyEmbedCode%22%7D&referrer=StreamWebApp&referrerScenario=EmbedDialog.Create" width="640" height="360" frameborder="0" scrolling="no" allowfullscreen title="Hash Hound Coming to greps with the past.mp4"></iframe>
</div>

---

## Command Line Basics  
  
# Extracting Files  
To extract a `.zip` file, use:  
`unzip filename.zip`
