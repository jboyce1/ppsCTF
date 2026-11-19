# Pre-class range test

Keep this on the instructor computer. Use one fresh VM for Computer 1 and one
fresh VM for Computer 2. Follow `challenge_instructions.txt` to clone and
deploy `rustycurtain_v2`. Keep the private `instructor/` answer keys on your
computer; they are excluded from GitHub.

1. On Computer 1, open a terminal in the challenge folder. Confirm the five ZIPs
   and two deploy scripts are present:

   ```bash
   ls
   ```

2. Check the transferred ZIPs before changing the VM:

   ```bash
   sha256sum -c ZIP_SHA256SUMS.txt
   ```

3. Run Computer 1 setup. Set the local root password when prompted, and wait
   for the service checks to finish:

   ```bash
   python3 deploy_rustycurtain_1.py
   ```

4. On Computer 2, open a terminal in its challenge folder. Confirm the same
   files are present:

   ```bash
   ls
   ```

5. Check Computer 2's transferred ZIPs:

   ```bash
   sha256sum -c ZIP_SHA256SUMS.txt
   ```

6. Run Computer 2 setup. Record its printed high FTP and SSH ports:

   ```bash
   python3 deploy_rustycurtain_2.py
   ```

7. From a separate Kali VM, scan Computer 1. Replace `<VM1_IP>` with the
   assigned range address. Confirm FTP 21, SSH 22, and Telnet 23:

   ```bash
   nmap -n -Pn -sT -sV -p 21,22,23 <VM1_IP>
   ```

8. Scan Computer 2. Confirm that its FTP and SSH ports match those printed by
   the second deployer:

   ```bash
   nmap -n -Pn -sT -sV -p 21000-24000 <VM2_IP>
   ```

9. Log in through the intended services. On Computer 1, check Ivan's
   anonymous FTP files, Tanya's account through Telnet, and Boris's through
   SSH. On Computer 2, check Nikoli's anonymous high-port FTP files and Yuri's
   account through high-port SSH. Confirm the browser database is visible in
   Yuri's Firefox folder.

10. Find each box's `.img.gz` evidence file from Kali. For every box, confirm
   the image downloads or copies, `gunzip` expands it, Scalpel finds the
   expected number of JPEGs, one picture opens with a readable flag, and the
   flag matches the private instructor key. Expected JPEG counts are Ivan 1,
   Tanya 1, Nikoli 2, Boris 2, Yuri 3.

11. Work through the existing puzzle files as a student would. There are no
   walkthroughs or tool instructions on the targets.
   Verify the six encrypted archives open with 7-Zip, and that Yuri's diff
   yields twelve changed characters. Keep notes on any command or clue that
   fails on the range.

| Check | Result / notes |
| --- | --- |
| Computer 1 services and logins | |
| Computer 2 services and logins | |
| Ivan FTP and deleted-file flag | |
| Tanya existing puzzles and deleted-file flag | |
| Nikoli FTP and deleted-file flag | |
| Boris existing puzzles and deleted-file flag | |
| Yuri existing puzzles and deleted-file flag | |

Leave `_v2` in place until the table is complete. The original
`challenges/rustycurtain` remains available during the trial.
