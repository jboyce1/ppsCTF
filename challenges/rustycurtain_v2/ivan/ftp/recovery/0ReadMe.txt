IVAN'S ERASED DEAD DROP — 1x2

Ivan deleted a route card from his anonymous FTP drop. Use the JPEG carving
method from MsDisin Part 7. The flag is visible in the recovered picture.

1. On Kali, create a folder named ivan-recovery with the file manager. Open a
   terminal in that folder.

2. Download Ivan's disk image. Replace <BOX_IP> with Ivan's box address.
   wget ftp://<BOX_IP>/recovery/recovery.img.gz

3. Download the same JPEG rule used in the MsDisin exercise.
   wget ftp://<BOX_IP>/recovery/scalpel-jpg.conf

4. Expand the disk image.
   gunzip recovery.img.gz

5. Recover the deleted JPEG into a separate folder.
   scalpel -c scalpel-jpg.conf -o recovered recovery.img

6. Open recovered and its JPEG subfolder in the file manager. Read the flag in
   the picture and record it against Ivan's box on the team map.
