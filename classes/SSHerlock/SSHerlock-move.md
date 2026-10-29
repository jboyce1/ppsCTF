---
layout: move
title: SSHerlock
---

<p><strong>MOVE edition.</strong> <a href="{{ '/classes/SSHerlock/SSHerlock' | relative_url }}">Open the original lesson</a>.</p>


# SSHerlock<br>
<div style="text-align: center;">
  <img src="{{ 'classes/SSHerlock/22258-Edwardian-era-British-detective.png' | relative_url }}" alt="Edwardian-era British Detective" style="max-width: 80%; height: auto;">
</div>

## **SSHerlock Work Role**<br>

### **Offensive:**<br>
**This role is all about establishing connections with your opponent's computers, navigating their file structure, and extracting files for your team to analyze.**<br>

#### **Specific Skills:**<br>
- SSH into another computer with a known password<br>
- SSH into another computer with an unknown password<br>
- SCP files from the opponent computers<br>
- SCP files from your computers onto your opponents<br>
- Use terminal for directory and file navigation<br>

### **Defensive:**<br>
**This role is about preventing your opponent from connecting to your computers while ensuring you can access them to clean out malicious files.**<br>

#### **Specific Skills:**<br>
- Update and adjust SSH configuration file<br>
- Find and replace weak passwords to prevent SSH with unknown passwords<br>
- Use terminal for directory and file navigation *(same link as above)*

---


# Part 1: SSH into Another Computer with a Known Password

<section class="move-card" aria-label="Part 1 MOVE">
<dl>
<dt><span>M</span> Mission</dt><dd>Use SSH to work on your Ubuntu machine from Kali so your team can operate it remotely.</dd>
<dt><span>O</span> Objective</dt><dd>Connect from Kali to Ubuntu with a known password; create and modify a text file, install and run a program remotely, and change the Ubuntu account password.</dd>
<dt><span>V</span> Validation</dt><dd>Screenshots of the remote session and the created or modified file, plus terminal output showing the program and password-change tasks completed; no flag is required.</dd>
<dt><span>E</span> Explain / Expand / Explore</dt>
<dd><strong>Explain:</strong> How did you know commands were running on Ubuntu rather than Kali?<br><strong>Expand:</strong> Where else could remote terminal access save you a trip to another computer?<br><strong>Explore:</strong> Which tasks needed administrator privileges, and what could a remote user do with those privileges?</dd>
</dl>
<p class="move-return">Return from your breakout room with your evidence and be ready to discuss your steps and ideas.</p>
</section>

There is no flag-based challenge to complete this; however, it is good practice and will help you in follow-on challenges.<br>

To try this, you will need **both an Ubuntu VM and a Kali VM on the cyber.org range** (or any two Linux machines on the same LAN).<br>


### Required setup and tools

Use Kali and an Ubuntu target with SSH enabled. Setup guides: [SSH server](./SettingSecureShellServer.pdf) and [SSH client](./SettingSecureShellClient.pdf).

<details class="move-help" markdown="1">
<summary>Expand: additional guidance</summary>

### **Step 1: Establish the Connection**<br>
Follow these documents to set up an SSH server on the target machine and connect remotely from an SSH client.<br>


### **Step 2: Use the SSH Client (Kali) to Access Your Ubuntu Machine**<br>

Once the SSH server is configured, establish the connection and try the following exercises:

#### **While You're at It...**<br>

- **Create a new file** on your Ubuntu machine from your Kali machine. *(Usually just text files, sometimes CSV files as well.)*<br>

- **Modify a text file** on your Ubuntu machine from your Kali machine using:<br>


```text
nano filename.txt
```


- Try to download and install a program using the sudo apt-get command from your kali machine to your Ubuntu machine.

- Try to run a program on your Ubuntu machine from your Kali machine. Try:
Set the display environment (the screen they are using):


```text
export DISPLAY=:1
```


Open Firefox to a specific page:


```text
firefox -new-tab "https://cyber.org"
```


Try to change the system password from ‘ubuntu’ to something else.

#### **Setting Up SSH on Target Server:**<br>
<div style="text-align: center;">
<iframe width="560" height="315" src="https://www.youtube.com/embed/WT5G5rkebxQ?si=6jxLBtwDpSfh0OkX" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</div>

#### **SSH into Target Machine:**<br>
<div style="text-align: center;">
<iframe width="560" height="315" src="https://www.youtube.com/embed/MhwCwABMktA?si=YOru8ARGgpBE8XGg" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</div>

</details>

---

# Part 2: SSH into Another Computer with X11 Forwarding

<section class="move-card" aria-label="Part 2 MOVE">
<dl>
<dt><span>M</span> Mission</dt><dd>Display an Ubuntu application on Kali through SSH so your team can use a remote graphical tool.</dd>
<dt><span>O</span> Objective</dt><dd>Enable X11 forwarding on Ubuntu, reconnect from Kali with X11 forwarding, and open Firefox or the target’s file manager on Kali.</dd>
<dt><span>V</span> Validation</dt><dd>A screenshot showing the SSH session and the remotely running application displayed on Kali.</dd>
<dt><span>E</span> Explain / Expand / Explore</dt>
<dd><strong>Explain:</strong> Which computer ran the program, and which computer displayed its window?<br><strong>Expand:</strong> When would you choose a graphical application over a terminal for remote work?<br><strong>Explore:</strong> What differences in speed or responsiveness do you notice compared with a text-only SSH session?</dd>
</dl>
<p class="move-return">Return from your breakout room with your evidence and be ready to discuss your steps and ideas.</p>
</section>


### Required setup and tools

Use **Kali with a graphical desktop**, an **Ubuntu SSH target**, an account with **sudo** permission on Ubuntu, and **SSH with X11 forwarding** (`ssh -X`). Have the Ubuntu username, password, and IP ready. Use Firefox or the target’s file manager for the graphical test. No lesson files to download.

<details class="move-help" markdown="1">
<summary>Expand: additional guidance</summary>

X11 (the X Window System) is a network-transparent graphics system that allows programs to run on one computer while displaying their graphical interface on another. When used over SSH with X11 forwarding, every window update, mouse movement, and keyboard event is sent across the network, making it much louder, slower, and more bandwidth-intensive than a simple text terminal. Because of this overhead, X11 is rarely the best default choice for remote work; experienced users rely on the terminal for speed and stealth, using X11 only when a graphical tool is truly necessary.

On Ubuntu, turn on X11 forwarding and adjust the config file.

On Ubuntu, check to see if you have sudo privileges to adjust the sshd_config file:


```text
whoami
```


Gives the output of what your device knows you as.


```text
sudo -l
```


Lists the commands your user can run with sudo.

<div style="text-align: center;">
  <img src="{{ 'classes/SSHerlock/whoami-sudo-l.png' | relative_url }}" alt="whoami and sudo-l" style="max-width: 80%; height: auto;">
</div>

If you have sudo permissions, open the config file:


```text
sudo nano /etc/ssh/sshd_config
```


Set these options (remove the # at the start if needed):


```text
X11Forwarding yes
```



```text
X11DisplayOffset 10
```



```text
X11UseLocalhost yes
```


<div style="text-align: center;">
  <img src="{{ 'classes/SSHerlock/config_x11_sshdconfig.png' | relative_url }}" alt="config_x11_sshdconfig" style="max-width: 80%; height: auto;">
</div>

Now save out and restart SSH.

Ctrl + X, Y, Enter


```text
sudo systemctl restart ssh
```


On Kali, open a new terminal and use an -X flag (capitalization matters) to get back into the target machine:


```text
ssh -X user@x.x.x.x
```


Now, programs you run in the SSH session show up on Kali instead of the Ubuntu screen.


```text
firefox -new-tab "https://cyber.org"
```


or open the file structure by running the file manager that exists on the target machine:


```text
nautilus
```


Play around with this, try to copy & paste or open txt files or pictures.

</details>

---

# Part 3: Use SSH keys to connect without the need for a password.

<section class="move-card" aria-label="Part 3 MOVE">
<dl>
<dt><span>M</span> Mission</dt><dd>Set up SSH key access so your team can reconnect without the Ubuntu account password.</dd>
<dt><span>O</span> Objective</dt><dd>Create a key pair on Kali, install its public key on Ubuntu, and reconnect without entering the Ubuntu account password; locate the account’s authorized keys.</dd>
<dt><span>V</span> Validation</dt><dd>Terminal evidence of a successful key-based connection and the matching public-key entry in authorized_keys; keep the private key private.</dd>
<dt><span>E</span> Explain / Expand / Explore</dt>
<dd><strong>Explain:</strong> Which key stayed on Kali, which key went to Ubuntu, and how is a key passphrase different from the account password?<br><strong>Expand:</strong> How could key-based access help with repeated remote work?<br><strong>Explore:</strong> Why can a key still work after a password change, and how would a defender remove that access?</dd>
</dl>
<p class="move-return">Return from your breakout room with your evidence and be ready to discuss your steps and ideas.</p>
</section>


### Required setup and tools

Use **Kali**, an **Ubuntu SSH target**, **ssh-keygen**, **ssh-copy-id**, and **ssh**. Have a working password login and the target IP ready. Generate your own key pair; there is no key file to download. Keep your private key on Kali.

<details class="move-help" markdown="1">
<summary>Expand: additional guidance</summary>

Use SSH keys instead of passwords to log into a remote machine.

On Kali, open a terminal and make your key pair:


```text
ssh-keygen -t ed25519
```


Press enter to put your keys where SSH will look for them. Do not overwrite an existing key.
A key passphrase is optional; it is separate from the Ubuntu password.

This makes two keys on Kali:

- Private key: ~/.ssh/id_ed25519 (keep this on Kali)
- Public key: ~/.ssh/id_ed25519.pub

Still on Kali, copy your public key to Ubuntu. Replace username and x.x.x.x with your Ubuntu username and IP:


```text
ssh-copy-id username@x.x.x.x
```


Enter the Ubuntu account password when asked.

Now try connecting from Kali:


```text
ssh username@x.x.x.x
```


You should not need the Ubuntu account password. If you set a key passphrase, you may still be asked for it.

A couple of things to keep in mind:

If the Ubuntu account password changes, your key will still let you in.

On Ubuntu (or in your SSH session), you can see the public keys allowed into that account with:


```text
cat ~/.ssh/authorized_keys
```


To remove a key, delete its line from this file:


```text
nano ~/.ssh/authorized_keys
```


Consider the offense and defense of this.

</details>

---

# Part 4: SSH into Another Computer with an Unknown Password

<section class="move-card" aria-label="Part 4 practice MOVE">
<dl>
<dt><span>M</span> Mission</dt><dd>Find a working SSH login on your practice Ubuntu target so your team can access an account without knowing its password in advance.</dd>
<dt><span>O</span> Objective</dt><dd>Use the supplied username and password lists with the SSH login scanner to find a valid login on the assigned Ubuntu target, then connect with SSH.</dd>
<dt><span>V</span> Validation</dt><dd>Scanner output showing a successful login and a screenshot of the resulting SSH session on the assigned target.</dd>
<dt><span>E</span> Explain / Expand / Explore</dt>
<dd><strong>Explain:</strong> How did the target address, username list, password list, and authentication settings affect your attempt?<br><strong>Expand:</strong> How could you use this exercise to evaluate weak account passwords on a practice system?<br><strong>Explore:</strong> What would you expect a defender to notice about repeated online login attempts?</dd>
</dl>
<p class="move-return">Return from your breakout room with your evidence and be ready to discuss your steps and ideas.</p>
</section>

#### Before You Start

#### **Kali - Files Required:**<br>
- [Password list](https://raw.githubusercontent.com/jboyce1/ppsCTF/main/workroles/ssherlock/challenges/msfconsole_to_ssh_challenges/msfconsole_to_ssh_passwordlist.txt)
- [Username list](https://raw.githubusercontent.com/jboyce1/ppsCTF/main/workroles/ssherlock/challenges/msfconsole_to_ssh_challenges/msfconsole_to_ssh_userlist.txt)

On Kali, download both files to your Desktop:


```text
wget -P ~/Desktop https://raw.githubusercontent.com/jboyce1/ppsCTF/main/workroles/ssherlock/challenges/msfconsole_to_ssh_challenges/msfconsole_to_ssh_passwordlist.txt
```



```text
wget -P ~/Desktop https://raw.githubusercontent.com/jboyce1/ppsCTF/main/workroles/ssherlock/challenges/msfconsole_to_ssh_challenges/msfconsole_to_ssh_userlist.txt
```


### Required tool

Use **Metasploit (`msfconsole`)** on Kali, with the SSH login scanner `auxiliary/scanner/ssh/ssh_login`. Have the assigned target IP address ready. The username and password files above are for this practice target and the fixed-account challenge; the rotating-password challenge has its own lists below.

<details class="move-help" markdown="1">
<summary>Expand: additional guidance</summary>

#### **Ubuntu - Setup Steps:**<br>

- **Pre-step 1:** Change Default Password (For Practice on Your Own)<br>
On the **Ubuntu target machine**, open a terminal and type:<br>


```text
sudo passwd root
```


- **Pre-step 2:** Turn on the password authentication for your Ubuntu Machine (see above)<br>
- **Pre-step 3:** Create a new user with your student name on the ubuntu machine (e.g. jboyce1) and set the password to a password on the password list you are using

#### **Kali - Attack Steps:**
**Step 1:** Attempt to ssh the target machine to ensure that it has password authentication turned on (see setting up SSH server on target machine), after 3 failures the permission will be denied.<br>
**Step 2:** Ensure you are in root for your Kali box by using the following command:<br>


```text
sudo su
```


Step 3: To open the Metasploit console run the following command:


```text
msfconsole
```


**Step 4:** Open the ssh login scanner<br>
4a: Use the following command to see all the possibilities of the Metasploit console dealing with SSH:


```text
search ssh
```


4b: Open the SSH login scanner.


```text
use auxiliary/scanner/ssh/ssh_login
```


4c: Show its options.


```text
show options
```


**Step 5:** Set the ssh_login tool to target the vulnerable machine:<br>

5a (vulnerable machine address)


```text
set RHOSTS 192.168.XX.XX
```


5b (path of the passwords text file)


```text
set PASS_FILE /home/kali/Desktop/msfconsole_to_ssh_passwordlist.txt
```


5c (path of the usernames text file)


```text
set USER_FILE /home/kali/Desktop/msfconsole_to_ssh_userlist.txt
```


5d (it will show the exactly matched combination of username and password)


```text
set VERBOSE true
```


**Step 6** Check all of your options to ensure they look the way you want<br>


```text
show options
```


**Step 7:** Run and get some coffee (this takes some time, because it is an online brute force!)<br>


```text
run
```


</details>

## Fixed-account challenge

<section class="move-card" aria-label="Fixed-account challenge MOVE">
<dl>
<dt><span>M</span> Mission</dt><dd>Use the existing fixed-account targets to prove your team can apply the login technique independently.</dd>
<dt><span>O</span> Objective</dt><dd>Find a working SSH login on the teacher’s assigned target and complete the existing Guest/Target challenges.</dd>
<dt><span>V</span> Validation</dt><dd>Successful SSH session evidence and the evidence or answers requested by the existing Guest/Target forms.</dd>
<dt><span>E</span> Explain / Expand / Explore</dt>
<dd><strong>Explain:</strong> How did your team move from scanner results to a working SSH session?<br><strong>Expand:</strong> What would you reuse from this process on another assigned practice target?<br><strong>Explore:</strong> Which setup choices made these accounts vulnerable?</dd>
</dl>
<p class="move-return">Return from your breakout room with your evidence and be ready to discuss your steps and ideas.</p>
</section>

### Required tools and files

Use **Kali**, **Metasploit (`msfconsole`)**, the **SSH login scanner** (`auxiliary/scanner/ssh/ssh_login`), and **SSH**. Ask the teacher for the assigned fixed-account target IP.

- [Fixed-account password list]({{ '/workroles/ssherlock/challenges/msfconsole_to_ssh_challenges/msfconsole_to_ssh_passwordlist.txt' | relative_url }})
- [Fixed-account username list]({{ '/workroles/ssherlock/challenges/msfconsole_to_ssh_challenges/msfconsole_to_ssh_userlist.txt' | relative_url }})

Use these files with the scanner, then connect with a working login and submit the forms below.

- [Guest/Target (1)](https://forms.office.com/Pages/ResponsePage.aspx?id=mhxxjxzsu023kLsMdxsdzM6J33C5yQRJgc1SHWy_64dUQ01ZQjZNWjdYNEhKVkM3RjczRzIzM1RUTS4u)<br>
- [Guest/Target (2)](https://forms.office.com/Pages/ResponsePage.aspx?id=mhxxjxzsu023kLsMdxsdzM6J33C5yQRJgc1SHWy_64dUQVE5SVVUTVQ4RVc3VjdFOE1JWUgzOFVBRS4u)<br>
- [Guest/Target (3)](https://forms.office.com/Pages/ResponsePage.aspx?id=mhxxjxzsu023kLsMdxsdzM6J33C5yQRJgc1SHWy_64dUOVQxMDUzRE9TR0Q4SjlKMVZVR1haSlg1RC4u)
**Teacher setup file:** [ssherlock_fixed_targets.py](./ssherlock_fixed_targets.py) (Ubuntu target; Python 3).

<details class="move-help" markdown="1">
<summary>Expand: teacher setup for fixed-account targets</summary>

On the teacher Ubuntu target, download and run:


```text
wget https://raw.githubusercontent.com/jboyce1/ppsCTF/main/classes/SSHerlock/ssherlock_fixed_targets.py
```



```text
sudo python3 ssherlock_fixed_targets.py
```


This creates all 3 accounts on one box and turns on SSH password authentication.
For separate boxes, add --target 1, --target 2, or --target 3 when running the script on each box.
Give students the target IP shown at the end.

</details>

## Rotating-password challenge

One box, 3 users, 15 passwords that rotate every 5 minutes; your goal is to log into the box and set up an SSH key pair to maintain persistence as the passwords rotate.

<section class="move-card" aria-label="Rotating-password challenge MOVE">
<dl>
<dt><span>M</span> Mission</dt><dd>Keep access to the rotating-password practice box so your team can test how SSH keys behave when account passwords change.</dd>
<dt><span>O</span> Objective</dt><dd>Find a valid login, install your public key, and reconnect using that key after the next five-minute password rotation.</dd>
<dt><span>V</span> Validation</dt><dd>Successful key-based SSH connections before and after a password rotation, with timestamps and SSH authentication-log evidence from the target.</dd>
<dt><span>E</span> Explain / Expand / Explore</dt>
<dd><strong>Explain:</strong> How did you gain initial access, and why did the key continue to work after the password rotated?<br><strong>Expand:</strong> How would changing an account password affect other existing ways of accessing that account?<br><strong>Explore:</strong> What would you inspect in authorized_keys and the SSH logs to understand or remove that access?</dd>
</dl>
<p class="move-return">Return from your breakout room with your evidence and be ready to discuss your steps and ideas.</p>
</section>

### Kali - Files Required

Use **Metasploit (`msfconsole`)** and `auxiliary/scanner/ssh/ssh_login` for the initial login, then **ssh-keygen** and **ssh-copy-id** from Part 3 for key access. Use the assigned rotating target IP and these lists instead of the earlier practice lists.

- [Password list](./ssherlock_pt4_pass.txt)
- [Username list](./ssherlock_pt4_user.txt)

On Kali, download both files to your Desktop:


```text
wget -P ~/Desktop https://raw.githubusercontent.com/jboyce1/ppsCTF/main/classes/SSHerlock/ssherlock_pt4_pass.txt
```



```text
wget -P ~/Desktop https://raw.githubusercontent.com/jboyce1/ppsCTF/main/classes/SSHerlock/ssherlock_pt4_user.txt
```



For this box, change the Metasploit file paths:


```text
set PASS_FILE /home/kali/Desktop/ssherlock_pt4_pass.txt
```



```text
set USER_FILE /home/kali/Desktop/ssherlock_pt4_user.txt
```


<details class="move-help" markdown="1">
<summary>Expand: additional guidance</summary>

to see who has been using ssh to access the machine:



```text
cat /var/log/auth.log | grep ssh2
```



## More Resources

📖 [How to Brute-Force SSH in Kali Linux? - GeeksforGeeks](https://www.geeksforgeeks.org/how-to-brute-force-ssh-in-kali-linux/)<br>

### **Video Tutorial: SSH with Unknown Password**<br>

<div style="text-align: center;">
<iframe width="560" height="315" src="https://www.youtube.com/embed/9CldeyP_RDE?si=DZtJe5NUbAvBbfMI" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
  </div>

</details>

**Teacher setup file:** [ssherlock_edwardian_rotator.py](./ssherlock_edwardian_rotator.py) (Ubuntu target; Python 3).

<details class="move-help" markdown="1">
<summary>Expand: teacher setup for the rotating-password target</summary>

to set up:



```text
wget https://raw.githubusercontent.com/jboyce1/ppsCTF/main/classes/SSHerlock/ssherlock_edwardian_rotator.py
```


</details>

---

# Part 5: scp from target and use john the ripper with password list

<section class="move-card" aria-label="Part 5 MOVE">
<dl>
<dt><span>M</span> Mission</dt><dd>Retrieve and crack the supplied hash file so your team can recover its flag.</dd>
<dt><span>O</span> Objective</dt><dd>Use SCP to copy SCPhash.txt and JohnnyPasswordList.txt from the teacher Ubuntu machine to Kali, then use John the Ripper with the supplied wordlist to recover the flag.</dd>
<dt><span>V</span> Validation</dt><dd>The copied files on Kali and John’s recovered flag; use the existing SCPhash challenge forms for your submissions.</dd>
<dt><span>E</span> Explain / Expand / Explore</dt>
<dd><strong>Explain:</strong> How did SCP get the files to Kali, and how did John use the wordlist against the hash?<br><strong>Expand:</strong> How is testing a copied password hash different from trying passwords through SSH?<br><strong>Explore:</strong> What could prevent a supplied wordlist from recovering a password?</dd>
</dl>
<p class="move-return">Return from your breakout room with your evidence and be ready to discuss your steps and ideas.</p>
</section>

### **Now You Try:**<br>

- [SCPhash1](https://forms.office.com/Pages/ResponsePage.aspx?id=mhxxjxzsu023kLsMdxsdzM6J33C5yQRJgc1SHWy_64dUMjhJUVE0T1FBRDI1SFc5MDdVNVdBQVpNVC4u)<br>
- [SCPhash2](https://forms.office.com/Pages/ResponsePage.aspx?id=mhxxjxzsu023kLsMdxsdzM6J33C5yQRJgc1SHWy_64dUQ1VBMTc0Q1hGVTFVWjZKNDlQSU9YRUI1Sy4u)<br>
- [SCPhash3](https://forms.office.com/Pages/ResponsePage.aspx?id=mhxxjxzsu023kLsMdxsdzM6J33C5yQRJgc1SHWy_64dUOVZTM1dKVktUUUtONFVQUUZWNUxQTVdOVi4u)<br>


### Required files and tools

Use **SCP** to retrieve `SCPhash.txt` and `JohnnyPasswordList.txt` from the teacher’s Ubuntu target, then use **John the Ripper** on Kali. Ask your teacher for the target IP, account, and file location. [SCP setup guide](./SettingSecureCopyProtocol.pdf).

<details class="move-help" markdown="1">
<summary>Expand: additional guidance</summary>

In order to complete this challenge, you will need to pull a file from the Ubuntu machine to decipher the flag.<br>


**Step 1:** scp the ‘SCPhash.txt’ and the ‘JohnnyPasswordList.txt’ from the Teacher Ubuntu Machine to your kali desktop
**Step 2:** Use john the ripper to crack the hash from the password text file
- 2a Navigate to the desktop in your kali machine (or wherever you put the SCPhash.txt and JohnnyPassword list files).
 - The SCPhash.txt is hashed with md5sum
- 2b Use John the Ripper to extract the flag


```text
john --format=raw-md5 --wordlist=JohnnyPasswordList.txt SCPhash.txt
```


### **More Details**<br>
📖 [Using SCP Command in Linux: 10 Practical Examples Explained - Linux Handbook](https://linuxhandbook.com/scp-command/)<br>

<div style="text-align: center;">
<iframe width="560" height="315" src="https://www.youtube.com/embed/QUhyGpYgZi4?si=wRDW_igQop2cl5tU" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</div>

</details>

---

# Part 6: scp files into a target computer

<section class="move-card" aria-label="Part 6 MOVE">
<dl>
<dt><span>M</span> Mission</dt><dd>Send a picture from Kali to Ubuntu so your team can place a local file on a remote computer.</dd>
<dt><span>O</span> Objective</dt><dd>Connect to Ubuntu, create your student directory on its desktop, and use SCP to send the existing steganography lesson picture into that directory.</dd>
<dt><span>V</span> Validation</dt><dd>SCP transfer output and a screenshot showing the picture in the destination directory on Ubuntu.</dd>
<dt><span>E</span> Explain / Expand / Explore</dt>
<dd><strong>Explain:</strong> Which path was local, which was remote, and how did you choose the destination account and directory?<br><strong>Expand:</strong> What other kinds of team files could you transfer this way?<br><strong>Explore:</strong> How would you check that a transfer went to the intended machine and directory?</dd>
</dl>
<p class="move-return">Return from your breakout room with your evidence and be ready to discuss your steps and ideas.</p>
</section>


### Required files and tools

Use Kali, your assigned Ubuntu target, **SSH**, and **SCP**. The picture is `/home/kali/CourseFiles/Cybersecurity/steganography-lab/image1.jpg` from the cyber.org steganography lesson. Have your Ubuntu username, target IP, and destination directory ready. [SCP setup guide](./SettingSecureCopyProtocol.pdf).

<details class="move-help" markdown="1">
<summary>Expand: additional guidance</summary>

### SCP files into the opponent computers<br>
This challenge will require you to send a file that only exists on your Kali box to an Ubuntu box.<br>
**Step 1:** Start up both your Kali box and Ubuntu boxes (or use the class target box given during the live session) and use SSH to access the Ubuntu box.<br>
Example:


```text
ssh ubuntu@10.15.43.43
```


**Step 2:** Use SSH to create a directory on an Ubuntu machine with your student username_SCPractice/ (e.g. stjboyce1_SCPractice) on the desktop of the Ubuntu box
Example:


```text
mkdir jboyce1
```


**Step3:** Use SCP to push a picture from the stenography cyber.org lesson to the directory you created on the Ubuntu box
Generic:


```text
scp    </PathToFile/LocalFile> <remote_username>@<IPorHost>:<PathToLocation>
```


Example:


```text
scp /home/kali/CourseFiles/Cybersecurity/steganography-lab/image1.jpg ubuntu@10.15.8.29:/home/ubuntu/Desktop/jboyce1/
```


### **SCP File from Local to Remote**<br>

<div style="text-align: center;">
<iframe width="560" height="315" src="https://www.youtube.com/embed/lGtF_6nWL0Y?si=zW5Ix83BepMDKdFK" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</div>

</details>

---
