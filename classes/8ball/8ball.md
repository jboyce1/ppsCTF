---
layout: default
title: 8ball
---

# 8 ball   

**Focus**: Malware  
**Skill**: Analyze, Create, and Deploy Basic Malware  
**Activity**:  

<div style="text-align: center;">
  <img src="{{ 'classes/8ball/images/8ballontable.jpg' | relative_url }}" alt="" style="max-width: 80%; height: auto;">
</div>    

## Some 8balls are magic
### others just contain secrets
---
play a game while I yap:    
    
#### `sudo apt install bastet`     
#### `bastet`    
    
#### `sudo apt install ninvaders`    
#### `ninvaders`    
    
#### `sudo apt install bsdgames`    
#### `man atc`    
#### `atc`    

Specific Skills:    
- Use zip to hide data inside of images    
- Use unzip discover data from images    
- Use zip -e to password protect data hidden inside of images    
- Use grep and dd to separate an encrypted file from an image    
- Use a john the ripper program to extract the hash of an encrypted file    
- Use Steghide to hide data inside of images    
- Use Stegcracker & Stegseek to discover the password of an encrypted file

## Offensive Operations:
Zip: Attackers could exploit the zip utility to craftily hide malicious data inside images, which can be uploaded to a target's system or network as seemingly benign files. By zipping a directory with harmful scripts or tools and merging them with images, they can bypass less sophisticated security measures that don't inspect the content within images. If the zip is password protected, it further complicates detection and analysis, allowing the payload to sit undetected until it’s executed.
    
Steghide: Utilizing Steghide, attackers can embed covert communications or exfiltrate data within images. This approach could be used for command and control (C2) operations, where commands are hidden within images hosted on publicly accessible websites, or for leaking sensitive information out of an organization without raising alarms. The payload is obscured within the image's bits and is not readily apparent without the correct passphrase, making it a stealthy method for preserving operational security.
    
John the Ripper: This tool could be used in offensive operations to crack encrypted files or password-protected zip files retrieved from target networks. By extracting hashes and running them through John the Ripper with custom rule sets, attackers can potentially unlock sensitive documents, key material, or access credentials, granting further access into secure systems.
    
Hashcat: As an advanced password recovery tool, Hashcat can be weaponized by cyber attackers to breach cryptographic password defenses. With access to GPU resources, attackers can rapidly attempt to break hashed passwords of captured password databases, potentially unlocking user accounts, encrypted files, or administrative access, thus compromising the entire system.
    

## Defensive Operations:      
Zip: On the defensive side, security teams can leverage zip utilities to encapsulate and quarantine suspicious files, thus reducing the risk of accidental execution. By using zip files with strong encryption (-e option), defenders can securely transport forensic evidence or sensitive data without risk of interception and unauthorized access.
    
Steghide: Defensively, Steghide can protect sensitive information by hiding it within images during transmission, reducing the likelihood of sensitive data being intercepted by unauthorized parties. Security teams can also use Steghide to watermark proprietary images, enabling them to track unauthorized distribution or manipulation.
    
John the Ripper: Defensively, John the Ripper can be used by security teams to audit password strength within their environment. By attempting to crack their own hashed password databases in controlled conditions, they can identify weak passwords and enforce stronger password policies to prevent brute-force attacks.
    
Hashcat: Defensively, Hashcat aids in assessing the strength of password hashes by attempting to crack them. This can be part of a security assessment or red team exercise to highlight weak passwords and improve an organization's password policies, thus hardening defenses against actual adversaries.    
    
**Both offensive and defensive cyber operations can benefit from the capabilities of these tools, either by exploiting their potential to penetrate and compromise systems or by leveraging their strengths to defend and fortify against such intrusions. It’s a digital arms race where the same tools can be purposed for attack or defense, depending on the hands they are in.**

---
# Part 1: Use zip to hide data inside of images    
    
Step 1) Navigate to the directory with your image in it     
either :    
open terminal from the directory you want to be in (get to folder, right click an select “open terminal here”)    
OR    
open terminal ( Ctrl + Alt + t) and ls cd your way to the directory        
    
Step 2) Create and edit the text document    
#### `nano secretmessage.txt`    
    
type your message    
save your message (ctrl+x, then Y then ENTER)    
    
Step 3) Create a directory    
#### `mkdir secretdirectory`    
    
Step 4) Move the message to the directory    
#### `mv secretmessage.txt secretdirectory`        
    
Step 5) zip the directory    
#### `zip -r secret.zip secretdirectory`        
    
Step 6) Remove old directory    
#### `rm secretdirectory -rf`        
    
Step 7) Concatenate the zipped file with the image    
#### `cat image.jpg secret.zip > definatlyjustapicture.jpg`        
  
Step 8) Delete the old zipped file    
#### `rm secret.zip`         

<div style="text-align: center;">
  <img src="{{ 'classes/8ball/images/2244832679-zip-to-hide-1.png' | relative_url }}" alt="" style="max-width: 80%; height: auto;">
</div>   
    
Try it now    
Add a secret message to this 8 ball image    
Call the this message 8ballpoem.jpg    

<div style="text-align: center;">
  <img src="{{ 'classes/8ball/images/1382340518-8ball_secrettojpg.jpg' | relative_url }}" alt="" style="max-width: 80%; height: auto;">
</div>    
    
The secretmessage.txt message inside the secretdirectory should contain (no quotes):    
    
"In whispers veiled by silence's soft shroud,     
Lies steganography's secretive art.     
Its missives swathed in the commonplace crowd,     
Concealing truth within its cunning heart.      

No brutish force, nor prying eye discerns     
The silent speech that silent ink imparts.     
Within a text, the hidden message burns,     
A dance of shadows on perceptive hearts.     

So too do lovers’ glances subtly pass,     
A ciphered look, a touch beneath the table.     
Invisible as footsteps on the grass,     
Yet telling tales the stars could not enable.    

O steganography, thou art the key     
To whisper love and revolution free."    
    
<div style="text-align: center;">
<iframe width="560" height="315" src="https://www.youtube.com/embed/4plMNYqKfxg?si=llHYgSudetIFF21b" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</div>

---     
# Part 2: use unzip to discover data from images  

Pre-steps: Must have an image with a zipped file embedded    
Step 1)  Open a terminal and navigate to the folder that your image with an embedded zip file is in    
Step 2) unzip the file    
#### `unzip imagefile.jpg`        
      
Step 3) Inspect/read the message    
Try it now:    

see if you can find the message you embedded in the 8 ball image you created above

<div style="text-align: center;">
<iframe width="560" height="315" src="https://www.youtube.com/embed/efkOXHRcnoo?si=waeDUTf2gPRNOLPN" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</div>

---    
# Part 3: embed a file inside an image with a password
    
<div style="text-align: center;">
<iframe width="560" height="315" src="https://www.youtube.com/embed/-DufcK8FAhk?si=SCXanuoSA_spXQrQ" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</div>
    
    
