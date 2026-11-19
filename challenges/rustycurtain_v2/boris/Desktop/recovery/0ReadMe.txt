BORIS'S ROSWELL RELAY — 3x3

Boris's archive contains a planted report and a deleted route card. Use the
JPEG carving method from MsDisin Part 7 to separate the two.

1. On Kali, create a folder named boris-recovery with the file manager. Open a
   terminal in that folder.

2. Copy the disk image. Replace <BOX_IP> with Boris's box address.
   scp -P 22 boris@<BOX_IP>:/home/boris/Desktop/recovery/recovery.img.gz .

3. Copy the JPEG recovery rule.
   scp -P 22 boris@<BOX_IP>:/home/boris/Desktop/recovery/scalpel-jpg.conf .

4. Expand the disk image.
   gunzip recovery.img.gz

5. Recover the deleted JPEGs into a separate folder.
   scalpel -c scalpel-jpg.conf -o recovered recovery.img

6. Open recovered and its JPEG subfolder in the file manager. Inspect both
   pictures, then record the real relay flag against Boris's box on the map.
