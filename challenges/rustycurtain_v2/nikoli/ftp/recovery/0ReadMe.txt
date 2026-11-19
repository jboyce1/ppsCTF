NIKOLI'S SWITCHBOARD — 2x3

Nikoli erased two relay sheets from the high-port FTP drop. One is a false
route. Use the JPEG carving method from MsDisin Part 7 to find the real one.

1. On Kali, create a folder named nikoli-recovery with the file manager. Open a
   terminal in that folder.

2. Download the disk image. Replace <BOX_IP> and <FTP_PORT> with the address
   and high FTP port you discovered.
   wget ftp://<BOX_IP>:<FTP_PORT>/recovery/recovery.img.gz

3. Download the JPEG recovery rule.
   wget ftp://<BOX_IP>:<FTP_PORT>/recovery/scalpel-jpg.conf

4. Expand the disk image.
   gunzip recovery.img.gz

5. Recover the deleted JPEGs into a separate folder.
   scalpel -c scalpel-jpg.conf -o recovered recovery.img

6. Open recovered and its JPEG subfolder in the file manager. Inspect both
   pictures, then record the real route flag against Nikoli's box on the map.
