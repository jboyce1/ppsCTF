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
# 1 using remote ssh
1. using remote ssh to connect back to a students localhost and get around ufw rules set up in the environment.

<div class="scroll-box">
sudo ufw reset
sudo ufw allow 23
sudo ufw deny 22
sudo ufw enable
</div>   

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
