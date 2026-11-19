YURI'S VOSTOK TELEMETRY — 4x4

Yuri deleted the telemetry route card and left two misleading sheets. Use the
JPEG carving method from MsDisin Part 7 to find the real route.

1. On Kali, create a folder named yuri-recovery with the file manager. Open a
   terminal in that folder.

2. Copy the disk image. Replace <BOX_IP> and <SSH_PORT> with Yuri's box address
   and high SSH port.
   scp -P <SSH_PORT> yuri@<BOX_IP>:/home/yuri/Desktop/recovery/recovery.img.gz .

3. Copy the JPEG recovery rule.
   scp -P <SSH_PORT> yuri@<BOX_IP>:/home/yuri/Desktop/recovery/scalpel-jpg.conf .

4. Expand the disk image.
   gunzip recovery.img.gz

5. Recover the deleted JPEGs into a separate folder.
   scalpel -c scalpel-jpg.conf -o recovered recovery.img

6. Open recovered and its JPEG subfolder in the file manager. Inspect all
   pictures, then record the telemetry flag against Yuri's box on the map.
