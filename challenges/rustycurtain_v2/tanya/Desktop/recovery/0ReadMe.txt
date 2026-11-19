TANYA'S IRON CURTAIN FIELD NOTE — 2x2

Tanya erased a field note after the first handoff. Use the JPEG carving method
from MsDisin Part 7. The flag is visible in the recovered picture.

1. On Kali, create a folder named tanya-recovery with the file manager. Open a
   terminal in that folder.

2. Copy the disk image from Tanya's Desktop. Replace <BOX_IP> with her box IP.
   scp -P 22 tanya@<BOX_IP>:/home/tanya/Desktop/recovery/recovery.img.gz .

3. Copy the JPEG recovery rule.
   scp -P 22 tanya@<BOX_IP>:/home/tanya/Desktop/recovery/scalpel-jpg.conf .

4. Expand the disk image.
   gunzip recovery.img.gz

5. Recover the deleted JPEG into a separate folder.
   scalpel -c scalpel-jpg.conf -o recovered recovery.img

6. Open recovered and its JPEG subfolder in the file manager. Read the flag in
   the picture and record it against Tanya's box on the team map.
