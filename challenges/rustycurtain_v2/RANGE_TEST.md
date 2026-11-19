# Pre-class range test

After running the TWO setup commands in `challenge_instructions.txt` on each
new Ubuntu target VM, test from Kali. Keep private answer keys on the
instructor computer.

1. Scan Computer 1. Confirm FTP 21, SSH 22, and Telnet 23:

   ```bash
   nmap -n -Pn -sT -sV -p 21,22,23 <VM1_IP>
   ```

2. Scan Computer 2. Confirm its FTP and SSH ports match those printed by
   the setup script:

   ```bash
   nmap -n -Pn -sT -sV -p 21000-24000 <VM2_IP>
   ```

3. Check Ivan's anonymous FTP, Tanya's Telnet, Boris's SSH, Nikoli's
   high-port FTP, and Yuri's high-port SSH. Check that Yuri's browser
   database is in his Firefox folder.

4. From each account, find its `.img.gz` evidence file. Download or copy it,
   expand it, carve the deleted JPEGs with the MsDisin Part 7 method, and
   compare the authorization code with the private answer key. Expected
   JPEG counts: Ivan 1, Tanya 1, Nikoli 2, Boris 2, Yuri 3.

5. Try each existing sedsearch, spacerace, fedcount, browser, and diff puzzle
   as a student. All six encrypted ZIPs should open with their intended
   passwords. Yuri's diff should yield 12 changed characters.

| Check | Result / notes |
| --- | --- |
| Computer 1 services and logins | |
| Computer 2 services and logins | |
| Ivan flags | |
| Tanya flags | |
| Nikoli flags | |
| Boris flags | |
| Yuri flags | |

Leave `_v2` in place until this range test passes. The original
`challenges/rustycurtain` remains available.
