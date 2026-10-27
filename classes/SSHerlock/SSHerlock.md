---
layout: default
title: SSHerlock
---

# SSHerlock  
<div style="text-align: center;">
  <img src="{{ 'classes/SSHerlock/22258-Edwardian-era-British-detective.png' | relative_url }}" alt="Edwardian-era British Detective" style="max-width: 80%; height: auto;">
</div>

## **SSHerlock Work Role**  

### **Offensive:**  
**This role is all about establishing connections with your opponent's computers, navigating their file structure, and extracting files for your team to analyze.**  

#### **Specific Skills:**  
- SSH into another computer with a known password  
- SSH into another computer with an unknown password  
- SCP files from the opponent computers  
- SCP files from your computers onto your opponents  
- Use terminal for directory and file navigation  

### **Defensive:**  
**This role is about preventing your opponent from connecting to your computers while ensuring you can access them to clean out malicious files.**  

#### **Specific Skills:**  
- Update and adjust SSH configuration file  
- Find and replace weak passwords to prevent SSH with unknown passwords  
- Use terminal for directory and file navigation *(same link as above)*
    
---

# Part 1: SSH into Another Computer with a Known Password

There is no flag-based challenge to complete this; however, it is good practice and will help you in follow-on challenges.  

To try this, you will need **both an Ubuntu VM and a Kali VM on the cyber.org range** (or any two Linux machines on the same LAN).  

### **Step 1: Establish the Connection**  
Follow these documents to set up an SSH server on the target machine and connect remotely from an SSH client.   
📄 **[Setting up SSH Server on Target Machine](./SettingSecureShellServer.pdf)**  
📄 **[Remotely Connecting to Remote Machine with SSH Client](./SettingSecureShellClient.pdf)**  
    
    
### **Step 2: Use the SSH Client (Kali) to Access Your Ubuntu Machine**  

Once the SSH server is configured, establish the connection and try the following exercises:

#### **While You're at It...**  

- **Create a new file** on your Ubuntu machine from your Kali machine. *(Usually just text files, sometimes CSV files as well.)*  

- **Modify a text file** on your Ubuntu machine from your Kali machine using:  

<div class="scroll-box">
nano filename.txt
</div>

- Try to download and install a program using the sudo apt-get command from your kali machine to your Ubuntu machine.

- Try to run a program on your Ubuntu machine from your Kali machine. Try:
Set the display environment (the screen they are using):

<div class="scroll-box">
export DISPLAY=:1
</div>

Open Firefox to a specific page:

<div class="scroll-box">
firefox -new-tab "https://cyber.org"
</div>

Try to change the system password from ‘ubuntu’ to something else.

#### **Setting Up SSH on Target Server:**  
<div style="text-align: center;">
<iframe width="560" height="315" src="https://www.youtube.com/embed/WT5G5rkebxQ?si=6jxLBtwDpSfh0OkX" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</div>

#### **SSH into Target Machine:**  
<div style="text-align: center;">
<iframe width="560" height="315" src="https://www.youtube.com/embed/MhwCwABMktA?si=YOru8ARGgpBE8XGg" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</div>

---

# Part 2: SSH into Another Computer with X11 Forwarding

X11 (the X Window System) is a network-transparent graphics system that allows programs to run on one computer while displaying their graphical interface on another. When used over SSH with X11 forwarding, every window update, mouse movement, and keyboard event is sent across the network, making it much louder, slower, and more bandwidth-intensive than a simple text terminal. Because of this overhead, X11 is rarely the best default choice for remote work; experienced users rely on the terminal for speed and stealth, using X11 only when a graphical tool is truly necessary.

On Ubuntu, turn on X11 forwarding and adjust the config file.

On Ubuntu, check to see if you have sudo privileges to adjust the sshd_config file:

<div class="scroll-box">
whoami
</div>

Gives the output of what your device knows you as.

<div class="scroll-box">
sudo -l
</div>

Lists the commands your user can run with sudo.

<div style="text-align: center;">
  <img src="{{ 'classes/SSHerlock/whoami-sudo-l.png' | relative_url }}" alt="whoami and sudo-l" style="max-width: 80%; height: auto;">
</div>

If you have sudo permissions, open the config file:

<div class="scroll-box">
sudo nano /etc/ssh/sshd_config
</div>

Set these options (remove the # at the start if needed):

<div class="scroll-box">
X11Forwarding yes
</div>

<div class="scroll-box">
X11DisplayOffset 10
</div>

<div class="scroll-box">
X11UseLocalhost yes
</div>

<div style="text-align: center;">
  <img src="{{ 'classes/SSHerlock/config_x11_sshdconfig.png' | relative_url }}" alt="config_x11_sshdconfig" style="max-width: 80%; height: auto;">
</div>

Now save out and restart SSH.

Ctrl + X, Y, Enter

<div class="scroll-box">
sudo systemctl restart ssh
</div>

On Kali, open a new terminal and use an -X flag (capitalization matters) to get back into the target machine:

<div class="scroll-box">
ssh -X user@x.x.x.x
</div>

Now, programs you run in the SSH session show up on Kali instead of the Ubuntu screen.

<div class="scroll-box">
firefox -new-tab "https://cyber.org"
</div>

or open the file structure by running the file manager that exists on the target machine:

<div class="scroll-box">
nautilus
</div>

Play around with this, try to copy & paste or open txt files or pictures. 
---

# Part 3: Use SSH keys to connect without the need for a password.

Use SSH keys instead of passwords to log into a remote machine.

On Kali, open a terminal and make your key pair:

<div class="scroll-box">
ssh-keygen -t ed25519
</div>

Press enter to put your keys where SSH will look for them. Do not overwrite an existing key.
A key passphrase is optional; it is separate from the Ubuntu password.

This makes two keys on Kali:

- Private key: ~/.ssh/id_ed25519 (keep this on Kali)
- Public key: ~/.ssh/id_ed25519.pub

Still on Kali, copy your public key to Ubuntu. Replace username and x.x.x.x with your Ubuntu username and IP:

<div class="scroll-box">
ssh-copy-id username@x.x.x.x
</div>

Enter the Ubuntu account password when asked.

Now try connecting from Kali:

<div class="scroll-box">
ssh username@x.x.x.x
</div>

You should not need the Ubuntu account password. If you set a key passphrase, you may still be asked for it.

A couple of things to keep in mind:

If the Ubuntu account password changes, your key will still let you in.

On Ubuntu (or in your SSH session), you can see the public keys allowed into that account with:

<div class="scroll-box">
cat ~/.ssh/authorized_keys
</div>

To remove a key, delete its line from this file:

<div class="scroll-box">
nano ~/.ssh/authorized_keys
</div>

Consider the offense and defense of this.

---

# Part 4: SSH into Another Computer with an Unknown Password    

#### Before You Start

#### **Kali - Files Required:**  
- [Password list](https://raw.githubusercontent.com/jboyce1/ppsCTF/main/workroles/ssherlock/challenges/msfconsole_to_ssh_challenges/msfconsole_to_ssh_passwordlist.txt)
- [Username list](https://raw.githubusercontent.com/jboyce1/ppsCTF/main/workroles/ssherlock/challenges/msfconsole_to_ssh_challenges/msfconsole_to_ssh_userlist.txt)

On Kali, download both files to your Desktop:

<div class="scroll-box">
wget -P ~/Desktop https://raw.githubusercontent.com/jboyce1/ppsCTF/main/workroles/ssherlock/challenges/msfconsole_to_ssh_challenges/msfconsole_to_ssh_passwordlist.txt
</div>

<div class="scroll-box">
wget -P ~/Desktop https://raw.githubusercontent.com/jboyce1/ppsCTF/main/workroles/ssherlock/challenges/msfconsole_to_ssh_challenges/msfconsole_to_ssh_userlist.txt
</div>

#### **Ubuntu - Setup Steps:**  

- **Pre-step 1:** Change Default Password (For Practice on Your Own)   
On the **Ubuntu target machine**, open a terminal and type:  

<div class="scroll-box">
sudo passwd root
</div>

- **Pre-step 2:** Turn on the password authentication for your Ubuntu Machine (see above)    
- **Pre-step 3:** Create a new user with your student name on the ubuntu machine (e.g. jboyce1) and set the password to a password on the password list you are using

#### **Kali - Attack Steps:**
**Step 1:** Attempt to ssh the target machine to ensure that it has password authentication turned on (see setting up SSH server on target machine), after 3 failures the permission will be denied.  
**Step 2:** Ensure you are in root for your Kali box by using the following command:  

<div class="scroll-box">
sudo su
</div>

Step 3: To open the Metasploit console run the following command:

<div class="scroll-box">
msfconsole
</div>

**Step 4:** Open the ssh login scanner    
4a: Use the following command to see all the possibilities of the Metasploit console dealing with SSH:

<div class="scroll-box">
search ssh
</div>

4b: Open the SSH login scanner.

<div class="scroll-box">
use auxiliary/scanner/ssh/ssh_login
</div>

4c: Show its options.

<div class="scroll-box">
show options
</div>

**Step 5:** Set the ssh_login tool to target the vulnerable machine:     

5a (vulnerable machine address)

<div class="scroll-box">
set RHOSTS 192.168.XX.XX
</div>

5b (path of the passwords text file)

<div class="scroll-box">
set PASS_FILE /home/kali/Desktop/msfconsole_to_ssh_passwordlist.txt
</div>

5c (path of the usernames text file)

<div class="scroll-box">
set USER_FILE /home/kali/Desktop/msfconsole_to_ssh_userlist.txt
</div>

5d (it will show the exactly matched combination of username and password)

<div class="scroll-box">
set VERBOSE true
</div>

**Step 6** Check all of your options to ensure they look the way you want    

<div class="scroll-box">
show options
</div>

**Step 7:** Run and get some coffee (this takes some time, because it is an online brute force!)        

<div class="scroll-box">
run
</div>

## **Challenges in Cyber.org (Must Be Set Up Ahead of Time)**  

Part 1:

On the teacher Ubuntu target, download and run:

<div class="scroll-box">
wget https://raw.githubusercontent.com/jboyce1/ppsCTF/main/classes/SSHerlock/ssherlock_fixed_targets.py
</div>

<div class="scroll-box">
sudo python3 ssherlock_fixed_targets.py
</div>

This creates all 3 accounts on one box and turns on SSH password authentication.
For separate boxes, add --target 1, --target 2, or --target 3 when running the script on each box.
Give students the target IP shown at the end.

- [Guest/Target (1)](https://forms.office.com/Pages/ResponsePage.aspx?id=mhxxjxzsu023kLsMdxsdzM6J33C5yQRJgc1SHWy_64dUQ01ZQjZNWjdYNEhKVkM3RjczRzIzM1RUTS4u)  
- [Guest/Target (2)](https://forms.office.com/Pages/ResponsePage.aspx?id=mhxxjxzsu023kLsMdxsdzM6J33C5yQRJgc1SHWy_64dUQVE5SVVUTVQ4RVc3VjdFOE1JWUgzOFVBRS4u)  
- [Guest/Target (3)](https://forms.office.com/Pages/ResponsePage.aspx?id=mhxxjxzsu023kLsMdxsdzM6J33C5yQRJgc1SHWy_64dUOVQxMDUzRE9TR0Q4SjlKMVZVR1haSlg1RC4u)  

Part 2:

One box, 3 users, 15 passwords that rotate every 5 minutes; your goal is to log into the box and set up an SSH key pair to maintain persistence as the passwords rotate.

Kali - Files Required:

- [Password list](./ssherlock_pt4_pass.txt)
- [Username list](./ssherlock_pt4_user.txt)

On Kali, download both files to your Desktop:

<div class="scroll-box">
wget -P ~/Desktop https://raw.githubusercontent.com/jboyce1/ppsCTF/main/classes/SSHerlock/ssherlock_pt4_pass.txt
</div>

<div class="scroll-box">
wget -P ~/Desktop https://raw.githubusercontent.com/jboyce1/ppsCTF/main/classes/SSHerlock/ssherlock_pt4_user.txt
</div>


For this box, change the Metasploit file paths:

<div class="scroll-box">
set PASS_FILE /home/kali/Desktop/ssherlock_pt4_pass.txt
</div>

<div class="scroll-box">
set USER_FILE /home/kali/Desktop/ssherlock_pt4_user.txt
</div>

to set up:

<div class="scroll-box">
wget https://raw.githubusercontent.com/jboyce1/ppsCTF/main/classes/SSHerlock/ssherlock_edwardian_rotator.py
</div>

to see who has been using ssh to access the machine:

<div class="scroll-box">
cat /var/log/auth.log | grep ssh2
</div>

## More Resources 

📖 [How to Brute-Force SSH in Kali Linux? - GeeksforGeeks](https://www.geeksforgeeks.org/how-to-brute-force-ssh-in-kali-linux/)  

### **Video Tutorial: SSH with Unknown Password**  

<div style="text-align: center;">
<iframe width="560" height="315" src="https://www.youtube.com/embed/9CldeyP_RDE?si=DZtJe5NUbAvBbfMI" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
  </div>

---
   
# Part 5: scp from target and use john the ripper with password list  
   
In order to complete this challenge, you will need to pull a file from the Ubuntu machine to decipher the flag.      

📄 **[Setting up SCP](./SettingSecureCopyProtocol.pdf)**          

**Step 1:** scp the ‘SCPhash.txt’ and the ‘JohnnyPasswordList.txt’ from the Teacher Ubuntu Machine to your kali desktop
**Step 2:** Use john the ripper to crack the hash from the password text file
- 2a Navigate to the desktop in your kali machine (or wherever you put the SCPhash.txt and JohnnyPassword list files). 
 - The SCPhash.txt is hashed with md5sum
- 2b Use John the Ripper to extract the flag

<div class="scroll-box">
john --format=raw-md5 --wordlist=JohnnyPasswordList.txt SCPhash.txt
</div>

### **Now You Try:**   

- [SCPhash1](https://forms.office.com/Pages/ResponsePage.aspx?id=mhxxjxzsu023kLsMdxsdzM6J33C5yQRJgc1SHWy_64dUMjhJUVE0T1FBRDI1SFc5MDdVNVdBQVpNVC4u)  
- [SCPhash2](https://forms.office.com/Pages/ResponsePage.aspx?id=mhxxjxzsu023kLsMdxsdzM6J33C5yQRJgc1SHWy_64dUQ1VBMTc0Q1hGVTFVWjZKNDlQSU9YRUI1Sy4u)  
- [SCPhash3](https://forms.office.com/Pages/ResponsePage.aspx?id=mhxxjxzsu023kLsMdxsdzM6J33C5yQRJgc1SHWy_64dUOVZTM1dKVktUUUtONFVQUUZWNUxQTVdOVi4u)     

### **More Details**  
📖 [Using SCP Command in Linux: 10 Practical Examples Explained - Linux Handbook](https://linuxhandbook.com/scp-command/)  
    
<div style="text-align: center;">
<iframe width="560" height="315" src="https://www.youtube.com/embed/QUhyGpYgZi4?si=wRDW_igQop2cl5tU" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</div>    

--- 
# Part 6: scp files into a target computer

### SCP files into the opponent computers    
This challenge will require you to send a file that only exists on your Kali box to an Ubuntu box.   
**Step 1:** Start up both your Kali box and Ubuntu boxes (or use the class target box given during the live session) and use SSH to access the Ubuntu box.   
Example:

<div class="scroll-box">
ssh ubuntu@10.15.43.43
</div>

**Step 2:** Use SSH to create a directory on an Ubuntu machine with your student username_SCPractice/ (e.g. stjboyce1_SCPractice) on the desktop of the Ubuntu box
Example:

<div class="scroll-box">
mkdir jboyce1
</div>

**Step3:** Use SCP to push a picture from the stenography cyber.org lesson to the directory you created on the Ubuntu box 
Generic: 

<div class="scroll-box">
scp    &lt;/PathToFile/LocalFile&gt; &lt;remote_username&gt;@&lt;IPorHost&gt;:&lt;PathToLocation&gt;
</div>

Example:

<div class="scroll-box">
scp /home/kali/CourseFiles/Cybersecurity/steganography-lab/image1.jpg ubuntu@10.15.8.29:/home/ubuntu/Desktop/jboyce1/
</div>

### **SCP File from Local to Remote**   

<div style="text-align: center;">
<iframe width="560" height="315" src="https://www.youtube.com/embed/lGtF_6nWL0Y?si=zW5Ix83BepMDKdFK" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</div>

---
