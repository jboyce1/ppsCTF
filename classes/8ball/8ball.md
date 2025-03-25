---
layout: default
title: 8ball
---

# 8 ball   

**Focus**: Stegnography  
**Skill**: use zip, dd, stegseek, stegcracker to hide and extract data in of images  
**Activity**:  

<div style="text-align: center;">
  <img src="{{ 'classes/8ball/images/8ball-heading.jpg' | relative_url }}" alt="" style="max-width: 80%; height: auto;">
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
# Part 1: use zip to hide data inside of images    
    
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
## Use zip -e to password protect data hidden inside of images

Step 1) Navigate to the directory with your image in it     
    
open terminal from the directory you want to be in (get to folder, right click an select “open terminal here”)    
OR    
open terminal ( Ctrl + Alt + t) and ls cd your way to the directory    
      
Step 2) Create and edit the text document    
#### `nano secretmessage.txt`    
type your message    
save your message (ctrl+x, then Y then ENTER)    
    
Step 3) zip the directory    
#### `zip -e secret.zip secretmessage.txt`    
type your password (only use 3-4 lowercase letters if you want to try to crack it later)    
    
<div style="text-align: center;">
  <img src="{{ 'classes/8ball/images/1576872491-zip--e-to-password-protect.png' | relative_url }}" alt="" style="max-width: 80%; height: auto;">
</div>   
    
Step 4) Remove old directory    
#### `rm secretmessage.txt -rf`    
     
Step 5) Concatenate the zipped file with the image    
#### `cat image.jpg secret.zip > newimagename.jpg`    
    
Step 6) Delete the old zipped file    
#### `rm secret.zip`     
    
Try it now:    
Create a secretmessage.txt inside the 8 ball image    
Use the following in your text    
    
```
You are not worth another word, else I'd call you knave.    
-Bill Shakespeare
```   
    
<div style="text-align: center;">
  <img src="{{ 'classes/8ball/images/8ballontable.jpg' | relative_url }}" alt="" style="max-width: 50%; height: auto;">
</div>   

zip the secretmessage.txt to a secret.zip    
use the password "gyat"
call the image “8ball-e.jpg”

    
<div style="text-align: center;">
<iframe width="560" height="315" src="https://www.youtube.com/embed/-DufcK8FAhk?si=SCXanuoSA_spXQrQ" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</div>
    
---
# Part 4: extracting password protected files from an image    
## Use grep and dd to separate an encrypted file from an image    
## Use a john the ripper program to extract the hash of an encrypted file

Step 1) Navigate to the directory the suspicious file is in    
Open terminal in location     
OR    
ls and cd to the directory    
    
Step 2) Separate the jpg file from the zip file     
All zip files typically start with the same code, so you can search for the code using the following command:    
#### `grep -aobP ‘\x50\x48\x03\x04’ imagefile.jpg`    

- the byte pattern \x50\x48\x03\x04 corresponds to the magic number that marks the start of a ZIP file entry (more specifically, a local file header in a ZIP archive).    
 - 0x50 0x48 0x03 0x04 (in ASCII: PK\x03\x04)
 - "PK" are the initials of Phil Katz, the creator of the ZIP format.
    
Step 3) Use dd to separate the file based on the number of bits identified before the .zip file started (replace imagefile.jpg with the actual image file).    
#### `dd if=imagefile.jpg of=newzipfile.zip bs=1 skip=#numberfromlastcommand#`    
    
Step 4) now use zip2john to get the hash of the password protected file and turn it into a text file    
#### `zip2john newzipfile.zip > crackme.txt`    
    
Step 5) Use John the Ripper to crack the password based on its hash    
#### `john crackme.txt`    
    
OR if you have a wordlist (in the same directory as your crackme.txt):    
#### `john --wordlist=your_wordlist.txt crackme.txt`    

<div style="text-align: center;">
  <img src="{{ 'classes/8ball/images/zip2john-secretzip-screenshot.png' | relative_url }}" alt="" style="max-width: 80%; height: auto;">
</div>  
    
Try it now:    
Decrypt the 8ball-e.jpg you just created    

<div style="text-align: center;">
<iframe width="560" height="315" src="https://www.youtube.com/embed/YJ0uC9TyGbE?si=FpucmAlg6XS5cvQR" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</div>

---
# Part 5: use steghide to put data inside an image
    
Pre steps:    
install steghide (not needed on cyber.org range)    
sudo apt update    
sudo apt-get -y install steghide    
Read about the tool    
man steghide    
    
Step 1) Create (or identify) something to hide in the directory of your image    
#### `nano “message to hide.txt”`    
enter your secret message to be hidden    
save your message (ctrl+x, then Y then ENTER)    
    
Step 2) Embed your message inside of the HardaTack1.jpg    
#### `steghide embed -ef messagetohide.txt -cf HardaTack1.jpg`    
    
password: hardattack    
reenter: hardattack    
    
Step 3) Remove old message    
#### `rm messagetohide.txt`    
    
Try it now:    
Use the image to the right to create a steghide image  
The filename should be “message to hide.txt”    
use the passphrase: steg    
    
<div style="text-align: center;">
  <img src="{{ 'classes/8ball/images/steghide2-image.jpg' | relative_url }}" alt="" style="max-width: 50%; height: auto;">
</div>  

```
"In ancient lands, where dino footprints press,    
A creature roamed, quite large, yet less astute.    
Stegosaurus, with plates along its crest,    
A giant, yet its brain was minute.    
    
In forests lush, it wandered, dim and slow,    
Beside the ferns and cycads, lost in thought.    
Or lack thereof, for it was not to know    
The predators that in the shadows sought.    
    
Its tail, with spikes, a fearsome weapon made,    
Yet seldom used with cunning or with guile.    
In brute force battles, it could well persuade,    
But intellect? It barely walked a mile.    
    
Yet do not mock this beast for lack of wit,    
For in its time, it still found ways to fit.    
    
Its size and spikes, its very form and frame,    
Were just enough to play nature's game.    
Despite its brain, the size of walnut, small,    
Stegosaurus stood, quite proud and tall.    
    
So let us not the ancient beast deride,    
For in its world, it lived, it thrived, it died.    
A marvel of an era long passed by,    
Its legacy, in fossil beds, does lie.    
```
<div style="text-align: center;">
  <img src="{{ 'classes/8ball/images/steghide1-use-Steghide-to-hide-data-inside-of-images.png' | relative_url }}" alt="" style="max-width: 50%; height: auto;">
</div>    

---  
# Part 6a: use stegcracker and stegseek to crack steghide passphrases

Step 1) Install stegcracker    
#### `sudo apt update`    
#### `sudo apt-get –y install stegcracker`    
    
Step 2) Update permission to run as executable    
Either use terminal:    
#### `sudo chmod +x /bin/stegcracker`        
Or go to the permission of the file in /bin    
Go to the permissions tab and allow this to run as a program    

<div style="text-align: center;">
  <img src="{{ 'classes/8ball/images/Stegcracker1-update-permissions.png' | relative_url }}" alt="" style="max-width: 50%; height: auto;">
</div>  

<div style="text-align: center;">
  <img src="{{ 'classes/8ball/images/Stegcracker2-update-permissions.png' | relative_url }}" alt="" style="max-width: 50%; height: auto;">
</div>  

Step 3) Move your password list to the directory with the image in it    
SteggyWordList.txt    
#### `wget https://raw.githubusercontent.com/jboyce1/ppsCTF/ad7bff0d928c0427b1ed1d642f3273955afe4761/classes/8ball/SteggyWordList.txt`
    
Step 4) Open a terminal from the directory with both your image and 
password list    
Run the stegcracker    
#### `stegcracker imagefile.jpg wordlist.txt`    
    
<div style="text-align: center;">
  <img src="{{ 'classes/8ball/images/Stegcracker3-SteggyWordlist-screenshot.png' | relative_url }}" alt="" style="max-width: 80%; height: auto;">
</div>  
    
<div style="text-align: center;">
  <img src="{{ 'classes/8ball/images/Stegcracker4-haratack-out-screenshot.png' | relative_url }}" alt="" style="max-width: 80%; height: auto;">
</div>  

Try it now:    
Crack your “message to hide.txt”    

---
# Part 6b: crack directly with stegseek    
Install stegseek (no need on cyber.org range)
Finding if a file contains encrypted messages with stegseek    
This will not give you the data, but it will tell you if the image contains a hidden message.    

<div style="text-align: center;">
  <img src="{{ 'classes/8ball/images/stegseek2-determine-contents.png' | relative_url }}" alt="" style="max-width: 80%; height: auto;">
</div>  

Now crack the password using the password list:
#### `wget https://raw.githubusercontent.com/jboyce1/ppsCTF/ad7bff0d928c0427b1ed1d642f3273955afe4761/classes/8ball/SteggyWordList.txt`
    
<div style="text-align: center;">
  <img src="{{ 'classes/8ball/images/stegseek1-crack.png' | relative_url }}" alt="" style="max-width: 80%; height: auto;">
</div>  

---
# Steggy Team Challenge

In your teams:    
You will need to SSH into the same Ubuntu machine to make this happen:    
    
Step 1) Pick a mascot (any jpg, can be AI generated but may need to use online converter)    
Step 2) Pick a jpg image to be the mascot (this will be your stegomascot)    
Step 3) Pick a motto - create a file called “motto.txt”    
Step 4) Tell me what your strengths are - create a file called “stengths.txt”    
Step 5) Tell me what your weaknesses are- create a file called “weaknesses.txt”    
Step 6) Tell me why you're better than the other teams! (create a file called “better.txt”    
Step 7) zip them all, unencrypted into the image of your mascot (step 1 from tonight)    

