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

#### **Access O365 from cyber.org range VM**  
[SSHerlock SharePoint Page](https://mypps.sharepoint.com/sites/ppsCyberTacticsFest/SitePages/SSHerlock.aspx) [SSHerlock Github Page](https://jboyce1.github.io/ppsCTF/classes/SSHerlock/SSHerlock)

#### **To Copy and Paste into the Cyber.org Range:**  
1. Press **Ctrl + Alt + Shift** to open the side window.  
2. Paste this into the side window.  
3. Press **Ctrl + Alt + Shift** again to close the side window.  
4. Right-click and paste into the URL field at the top of your browser.
   
---   

## **Part 1: SSH into Another Computer with a Known Password**  

There is no flag-based challenge to complete this; however, it is good practice and will help you in follow-on challenges.  

To try this, you will need **both an Ubuntu VM and a Kali VM on the cyber.org range** (or any two Linux machines on the same LAN).  

### **Step 1: Establish the Connection**  
Follow these documents to set up an SSH server on the target machine and connect remotely from an SSH client.   
📄 **[Setting up SSH Server on Target Machine](./classes/SSHerlock/Setting%20up%20Secure%20Shell%20Server.pdf)**  
📄 **[Remotely Connecting to Remote Machine with SSH Client](./classes/SSHerlock/Setting%20up%20Secure%20Shell%20Client.pdf)**  



### **Step 2: Use the SSH Client (Kali) to Access Your Ubuntu Machine**  

Once the SSH server is configured, establish the connection and try the following exercises:

#### **While You're at It...**  

- **Create a new file** on your Ubuntu machine from your Kali machine. *(Usually just text files, sometimes CSV files as well.)*  

- **Modify a text file** on your Ubuntu machine from your Kali machine using:  
`nano filename.txt`

- Try to download and install a program using the sudo apt-get command from your kali machine to your Ubuntu machine.

- Try to run a program from on your Ubuntu machine from your kali machine. Try:    
  - set display environment (the screen they are using)    
   - `export DISPLAY=:1`
  - Open firefox to a specific page:    
   - `firefox -new-tab “https:www.picoctf.org”`

Try to change the system password from ‘ubuntu’ to something else.

### **Video Tutorials:**  

#### **Setting Up SSH on Target Server:**  
<div style="text-align: center;">
    <iframe src="https://mypps.sharepoint.com/sites/ppsCyberTacticsFest/_layouts/15/embed.aspx?UniqueId=e2f0ec71-7722-430a-a163-42a76dcfabe0&embed=%7B%22ust%22%3Atrue%2C%22hv%22%3A%22CopyEmbedCode%22%7D&referrer=StreamWebApp&referrerScenario=EmbedDialog.Create" 
    width="640" height="360" frameborder="0" scrolling="no" allowfullscreen title="SSH set up target server.mp4"></iframe>
</div>


#### **SSH into Target Machine:**  
<div style="text-align: center;">
    <iframe src="https://mypps.sharepoint.com/sites/ppsCyberTacticsFest/_layouts/15/embed.aspx?UniqueId=140ac197-d304-4650-9d25-18e8ee848259&embed=%7B%22ust%22%3Atrue%2C%22hv%22%3A%22CopyEmbedCode%22%7D&referrer=StreamWebApp&referrerScenario=EmbedDialog.Create" 
    width="640" height="360" frameborder="0" scrolling="no" allowfullscreen title="SSH into target.mp4"></iframe>
</div>

---

## **Part 2: SSH into Another Computer with an Unknown Password**  

### **Before You Start**  

#### **Kali - Files Required:**  
- Password list in a text file  
- Username list in a text file  

#### **Ubuntu - Setup Steps:**  

- **Pre-step 1:** Change Default Password (For Practice on Your Own)   
On the **Ubuntu target machine**, open a terminal and type:  
```bash
sudo passwd root
```    
- **Pre-step 2:** Turn on the password authentication for your Ubuntu Machine (see above)    
- **Pre-step 3:** Create a new user with your student name on the ubuntu machine (e.g. jboyce1) and set the password to a password on the password list you are using
- 
#### **Kali - Attack Steps:**
**Step 1:** Attempt to ssh the target machine to ensure that it has password authentication turned on (see setting up SSH server on target machine), after 3 failures the permission will be denied.  
**Step 2:** Ensure you are in root for your Kali box by using the following command:  
`sudo su` 
Step 3: To open the Metaspoitconsole run the following command:  
`msfconsole`  
**Step 4:** Open the ssh login scanner  
 - 4a: Use the following command to see all the possibilities of the Metasploit console dealing with SSH:  
`msf6 > search ssh`  
 - 4b:  `msf6 > use auxiliary/scanner/ssh/ssh_login`  
 - 4c:  `msf6 > show options`  
**Step 5:** Set the ssh_login tool to target the vulnerable machine   
 - 5a `msf6 > set RHOSTS 192.168.XX.XX` (vulnerable machine address)   
 - 5b`msf6 > set PASS_FILE /home/kali/Desktop/passwords.txt` (path of the passwords text file)   
 - 5c `msf6 > set USER_FILE /home/kali/Desktop/usernames.txt` (path of the usernames text file)   
 - 5d `msf6 > set VERBOSE true` (it will show the exactly matched combination of username and password) 
**Step 6** Check all of your options to ensure they look the way you want    
`msf6 > show options`
**Step 7:** Run and get some coffee (this takes some time, because it is an online brute force!)    
`msf6 > run`   

## **Challenges in Cyber.org (Must Be Set Up Ahead of Time)**  

- [Guest/Target (1)](https://forms.office.com/Pages/ResponsePage.aspx?id=mhxxjxzsu023kLsMdxsdzM6J33C5yQRJgc1SHWy_64dUQ01ZQjZNWjdYNEhKVkM3RjczRzIzM1RUTS4u)  
- [Guest/Target (2)](https://forms.office.com/Pages/ResponsePage.aspx?id=mhxxjxzsu023kLsMdxsdzM6J33C5yQRJgc1SHWy_64dUQVE5SVVUTVQ4RVc3VjdFOE1JWUgzOFVBRS4u)  
- [Guest/Target (3)](https://forms.office.com/Pages/ResponsePage.aspx?id=mhxxjxzsu023kLsMdxsdzM6J33C5yQRJgc1SHWy_64dUOVQxMDUzRE9TR0Q4SjlKMVZVR1haSlg1RC4u)  

## **More Resources**  

📖 [How to Brute-Force SSH in Kali Linux? - GeeksforGeeks](https://www.geeksforgeeks.org/how-to-brute-force-ssh-in-kali-linux/)  

### **Video Tutorial: SSH with Unknown Password**  

<div style="text-align: center;">
    <iframe src="https://mypps.sharepoint.com/sites/ppsCyberTacticsFest/_layouts/15/embed.aspx?UniqueId=750c9ed6-54fa-4467-a4a4-8472de8866c8&embed=%7B%22ust%22%3Atrue%2C%22hv%22%3A%22CopyEmbedCode%22%7D&referrer=StreamWebApp&referrerScenario=EmbedDialog.Create" 
    width="640" height="360" frameborder="0" scrolling="no" allowfullscreen title="SSH with Unknown Password.mp4"></iframe>
  </div>

---
   
## **Part 3: SCP files from the opponent computers**   
   
In order to complete this challenge, you will need to pull a file from the Ubuntu machine to decipher the flag.  

**Step 1:** scp the ‘SCPhash.txt’ and the ‘JohnnyPasswordList.txt’ 'from the Teacher Ubuntu Machine to your kali desktop
**Step 2:** Use john the ripper to crack the hash from the password text file
- 2a Navigate to the desktop in your kali machine (or wherever you put the SCPhash.txt and JohnnyPassword list files). 
 - The SCPhash.txt is hashed with md5sum
- 2b Use John the Ripper to extract the flag
 ```bash
john -format=raw-md5 -wordlist:JohnnyPasswordList.txt SCPhash.txt
```
## **Now You Try**   

- [SCPhash1](https://forms.office.com/Pages/ResponsePage.aspx?id=mhxxjxzsu023kLsMdxsdzM6J33C5yQRJgc1SHWy_64dUMjhJUVE0T1FBRDI1SFc5MDdVNVdBQVpNVC4u)  
- [SCPhash2](https://forms.office.com/Pages/ResponsePage.aspx?id=mhxxjxzsu023kLsMdxsdzM6J33C5yQRJgc1SHWy_64dUQ1VBMTc0Q1hGVTFVWjZKNDlQSU9YRUI1Sy4u)  
- [SCPhash3](https://forms.office.com/Pages/ResponsePage.aspx?id=mhxxjxzsu023kLsMdxsdzM6J33C5yQRJgc1SHWy_64dUOVZTM1dKVktUUUtONFVQUUZWNUxQTVdOVi4u)  
- **SCPhash4** *(Link not provided – please add if available)*  

### **More Details**  
📖 [Using SCP Command in Linux: 10 Practical Examples Explained - Linux Handbook](https://linuxhandbook.com/scp-command/)  

### **Part 4: SCP from Target and John with Password List**  

<div style="text-align: center;">
    <iframe src="https://mypps.sharepoint.com/sites/ppsCyberTacticsFest/_layouts/15/embed.aspx?UniqueId=e0d7b6c9-666f-4bcc-be65-464adeb135e1&embed=%7B%22ust%22%3Atrue%2C%22hv%22%3A%22CopyEmbedCode%22%7D&referrer=StreamWebApp&referrerScenario=EmbedDialog.Create" 
    width="640" height="360" frameborder="0" scrolling="no" allowfullscreen title="SCP from Target and John with Password List.mp4"></iframe>
</div>

---
  
## SCP files into the opponent computers    
This challenge will require you to send a file that only exists on your Kali box to an Ubuntu box.   
**Step 1:** Start up both your Kali box and Ubuntu boxes (or use the class target box given during the live session) and use SSH to access the Ubuntu box.   
ex. ssh ubuntu@10.15.43.43  
**Step 2:** Use SSH to create a directory on an Ubuntu machine with your student username_SCPractice/ (e.g. stjboyce1_SCPractice) on the desktop of the Ubuntu box
ex. `mkdir jboyce1`
**Step3:** Use SCP to push a picture from the stenography cyber.org lesson to the directory you created on the Ubuntu box 
Generic: 
```bash
scp    </PathToFile/LocalFile> <remote_username>@<IPorHost>:<PathToLocation>
```

Example:
`scp /home/kali/CourseFiles/Cybersecurity/steganography-lab/image1.jpg ubuntu@10.15.8.29:/home/ubuntu/Desktop/jboyce1/`

### **SCP File from Local to Remote**   

<div style="text-align: center;">
    <iframe src="https://mypps.sharepoint.com/sites/ppsCyberTacticsFest/_layouts/15/embed.aspx?UniqueId=92d01278-8af2-4d7c-812f-b2502550eefc&embed=%7B%22ust%22%3Atrue%2C%22hv%22%3A%22CopyEmbedCode%22%7D&referrer=StreamWebApp&referrerScenario=EmbedDialog.Create" 
    width="640" height="360" frameborder="0" scrolling="no" allowfullscreen title="SCP File from Local to Remote.mp4"></iframe>
</div>

---
