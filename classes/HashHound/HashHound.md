---
layout: default
title: Hash Hound
---

# Hash Hound

**Focus**: Understanding and utilizing cryptographic hashing for security and integrity verification.  
**Skill**: Practical use of hashing functions in various security contexts.  
**Activity**: Hands-on hashing challenges with real-world applications.

<div style="text-align: center;">
  <img src="{{ 'classes/HashHound/90255-Hash-Hound.png' | relative_url }}" alt="Hash Hound Logo" style="max-width: 80%; height: auto;">
</div>




## Fun New Game


### Specific Skills
- Use terminal to develop an md5sum hash of a string
- Determine the md5sum hash of a file
- Determine the md5sum has of multiple files
- Create a text document from a command output
- Use grep to search for a specific output in a list
- Use find, cut, and grep to find a unknown hash from a list of known hashes

**To find a hash in terminal:**     
```bash
echo -n YourStingHere | md5sum
```      
Output looks like: 26617986d9bafa5795a2c63fe209781e -

### To complete the challenges, you will need to download them on a Linux device (e.g. Kali through cyber.org) 
- Step 1: Click the link to open a new page
- Step 2: Download the .zip file by clicking the ‘Download’ button on the top left of the page
- Step 3: Go to your Downloads folder and find the file
- Step 4: Right click and extract the file
- Step 5: Go and find the Flag (watch the video, remember flags look like;
pps{someflag}
- Step 6: Click the “Flag” link after the practice and paste your flag to see if is correct


**Download Practice Files**:  
📥 [Practice 1](./Fun%20New%20Game%20Practice/1%20Fun%20New%20Game%20(practice%201).zip)  

📥 [Practice 2](./Fun%20New%20Game%20Practice/1%20Fun%20New%20Game%20(practice%202).zip)  
📥 [Practice 3](./Fun%20New%20Game%20Practice/1%20Fun%20New%20Game%20(practice%203).zip)    

Walkthrough:
ctrl + alt + t
`cd /Desktop/`    
`ls`    
`cd Unit 1: Reverse Engineering`    
`ls`    
`cd Checking Hash Functions/`    
`ls`    
`cd 1 Fun New Game`    
`md5sum FuNeWgAmE.sh`    
************************************ FuNeWgAmE.sh    
`md5sum funnewGAME.sh`    
************************************ funnewGAME.sh    
etc etc    
double click on game with match of:    
cf9406bee74516677ca364c682c96d90        

<iframe src="https://mypps.sharepoint.com/sites/ppsCyberTacticsFest/_layouts/15/embed.aspx?UniqueId=8b3b12a4-1dd6-4873-a155-78602d0ae6ac&embed=%7B%22ust%22%3Atrue%2C%22hv%22%3A%22CopyEmbedCode%22%7D&referrer=StreamWebApp&referrerScenario=EmbedDialog.Create" width="640" height="360" frameborder="0" scrolling="no" allowfullscreen title="Hash-Hound-Fun-New-Game.mp4"></iframe>
  
  <div style="text-align: center;">
  <p>-------------------------------------------------------------------------</p>
</div>    

## Needle in the Hayloft

<iframe src="https://mypps.sharepoint.com/sites/ppsCyberTacticsFest/_layouts/15/embed.aspx?UniqueId=c5bd88bb-87aa-4db1-838a-64ff932260d6&embed=%7B%22ust%22%3Atrue%2C%22hv%22%3A%22CopyEmbedCode%22%7D&referrer=StreamWebApp&referrerScenario=EmbedDialog.Create" width="640" height="360" frameborder="0" scrolling="no" allowfullscreen title="Hash-Hound-Needle-in-the-Hayloft.mp4"></iframe>

**Download Practice Files**:  
📥 [Practice 1](./Needle%20in%20the%20Hayloft%20Practice/2%20Needle%20in%20the%20Hayloft%20(practice%201).zip)  
📥 [Practice 2](./Needle%20in%20the%20Hayloft%20Practice/2%20Needle%20in%20the%20Hayloft%20(practice%202).zip)  
📥 [Practice 3](./Needle%20in%20the%20Hayloft%20Practice/2%20Needle%20in%20the%20Hayloft%20(practice%203).zip)  

---

## Coming to Greps with the Past

<iframe src="https://mypps.sharepoint.com/sites/ppsCyberTacticsFest/_layouts/15/embed.aspx?UniqueId=9f33c970-8bcc-4123-bd43-fdefbd355660&embed=%7B%22ust%22%3Atrue%2C%22hv%22%3A%22CopyEmbedCode%22%7D&referrer=StreamWebApp&referrerScenario=EmbedDialog.Create" width="640" height="360" frameborder="0" scrolling="no" allowfullscreen title="Hash Hound Coming to greps with the past.mp4"></iframe>

**Download Practice Files**:  
📥 [Practice 1](./Coming%20to%20greps%20with%20the%20past/3%20Coming%20to%20greps%20with%20the%20past%20(practice%201).zip)  

---

## Command Line Basics

### Extracting Files
To extract a `.zip` file, use:
```bash
unzip filename.zip
