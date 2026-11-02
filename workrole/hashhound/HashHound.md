---
layout: default
title: Hash Hound
---

# Hash Hound    

**Focus**: Understanding and utilizing cryptographic hashing for security and integrity verification.  
**Skill**: Practical use of hashing functions in various security contexts.  
**Activity**: Hands-on hashing challenges with real-world applications.

<div style="text-align: center;">
  <img src="{{ 'workrole/hashhound/images/90255-Hash-Hound.png' | relative_url }}" alt="Hash Hound Logo" style="max-width: 80%; height: auto;">
</div>

### Specific Skills:
- Use terminal to develop an md5sum hash of a string
- Determine the md5sum hash of a file
- Determine the md5sum hash of multiple files
- Create a text document from a command output
- Use `grep` to search for a specific output in a list
- Use `find`, `cut`, and `grep` to find an unknown hash from a list of known hashes
  
---

# Part 1: use md5sum in terminal   
## Fun New Game    

### Finding a Hash in Terminal
`echo -n YourStringHere | md5sum`

  Output looks like: `26617986d9bafa5795a2c63fe209781e -`    

### To complete the challenges, you will need to download them on a Linux device (e.g. Kali through cyber.org)

1. Open a terminal where you want the file to download
2. Copy the wget command into shared clipboard (ctrl, alt, shift for the cyber.org range)
3. Paste the wget command into terminal (ctrl, shift, v)
4. Hit enter 


## **Download Practice Files**
`wget -O hashhound_practice1.zip https://github.com/jboyce1/ppsCTF/raw/main/workrole/hashhound/challenges/Fun%20New%20Game%20Practice/1%20Fun%20New%20Game%20\(practice%201\).zip`

`wget -O hashhound_practice2.zip https://github.com/jboyce1/ppsCTF/raw/main/workrole/hashhound/challenges/Fun%20New%20Game%20Practice/1%20Fun%20New%20Game%20\(practice%202\).zip`

`wget -O hashhound_practice3.zip https://github.com/jboyce1/ppsCTF/raw/main/workrole/hashhound/challenges/Fun%20New%20Game%20Practice/1%20Fun%20New%20Game%20\(practice%203\).zip`

## Command Line Basics  
Extracting Files  
To extract a `.zip` file, use:  
`unzip filename.zip`

## **Walkthrough**

These practices use five HTML game files. Double-clicking one opens it in your
web browser. First, use the terminal to find the file you should open.

1. Extract `hashhound_practice1.zip` in your file manager (right-click, then **Extract Here**).
2. Open the extracted `1 Fun New Game (practice 1)` folder.
3. Right-click an empty space in that folder and choose **Open Terminal Here**.
4. Type `ls` and press Enter to see the filenames.
5. Type `md5sum FUNNEWGAME.html` and press Enter. You do not need `sudo`.
6. Compare the 32-character hash at the start of the output with the target for your practice below.
7. Repeat `md5sum` for each of the other four HTML files, **one file at a time**.
   Capital letters matter: type each filename exactly as `ls` shows it.
   Write down each filename and its hash.
8. After checking all five files, return to the file manager and **double-click only
   the file with the matching hash**. Your browser will display the flag.

| Practice | Target MD5 |
| --- | --- |
| 1 | `e96f22f4891f6751af7f9450557e4ffe` |
| 2 | `6ca532bbbea3943300dda165038aac52` |
| 3 | `d4159e802ea95773914ec60b9440a5e4` |

For practices 2 and 3, extract that practice's ZIP and follow the same steps in
its own folder. Each practice has a different target. The `1 README.txt` inside
each folder also gives that practice's target and instructions.

Leave the HTML files unchanged and unopened until you finish comparing their hashes.
No programs need installing; the game works offline in your browser.


---

# Part 2: use find with the -type and -exec flags to create a file of md5sums
## Needle in the Hayloft  
  
Here is your md5sum needle: c6fca9b96af058081fe4bfd89523f3f4  
  
step1: Navigate to the '2 Needle in the Hayloft' directory    
step2: Make a text file using the following command:  
**`find . -type f -exec md5sum {} \; > 01md5sums.txt`**  

- Explaination for command      
  - **`find .`** searches for files and directories starting from the current directory (.).    
  - **`-type f`** specifies that we are interested in files only, not directories.    
  - **`-exec md5sum {} \;`** executes the md5sum command on each file found by find. {} represents the current file being processed by find.    
  - **`> md5sums.txt`** redirects the output (MD5 checksums) to a file named md5sums.txt.    
  
step3: open the text file and search (ctrl+f) the needle you are looking for       
step4: open the file and find the flag  

For more informaiton on the find functions, read the manual:   
man find        

**Download Practice Files**:    
`wget -O needle_hayloft_practice1.zip https://github.com/jboyce1/ppsCTF/raw/main/workrole/hashhound/challenges/Needle%20in%20the%20Hayloft%20Practice/2%20Needle%20in%20the%20Hayloft%20\(practice%201\).zip`

`wget -O needle_hayloft_practice2.zip https://github.com/jboyce1/ppsCTF/raw/main/workrole/hashhound/challenges/Needle%20in%20the%20Hayloft%20Practice/2%20Needle%20in%20the%20Hayloft%20\(practice%202\).zip`

`wget -O needle_hayloft_practice3.zip https://github.com/jboyce1/ppsCTF/raw/main/workrole/hashhound/challenges/Needle%20in%20the%20Hayloft%20Practice/2%20Needle%20in%20the%20Hayloft%20\(practice%203\).zip`

  <div style="text-align: center;">
<iframe width="560" height="315" src="https://www.youtube.com/embed/iDQTr-loTe0?si=j5mmNbN_vddz3_Ig" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
  </div>
  
---

# Part 3: use find, cut, and grep to isolate suspcious files 
## Coming to Greps with the Past  
  
### Suspicious Needle Search  

You need to find the suspicious needle. They were all good when they left but something changed. The `knowngood_md5sums_filenames.txt` is a list of all the unsuspicious files.  
  
**step1:** Navigate to the directory containing `knowngood_md5sums_filenames.txt`  
**step2:** Extract all of the hashes from the `knowngood_md5sums_filenames.txt` using the command:  
`cut -d ' ' -f 1 knowngood_md5sums_filenames.txt > knowngood_hashes.txt`  
  
- Explanation for command
  - `cut -d ' '` specifies the delimiter as a space.
  - `-f 1` selects the first field, which is typically the hash value.
  - `> knowngood_hashes.txt` redirects the output to a file named `knowngood_hashes.txt`.  
  
**step3:** Find all the MD5 sums in the directory using the command:    
`find . -type f -exec md5sum {} \; > current_md5sums_filenames.txt`    
  
**step4:** Extract all hashes from the `current_md5sums_filenames.txt` using:  
`cut -d ' ' -f 1 current_md5sums_filenames.txt > current_hashes.txt`  

**step5:** Search for lines in `current_hashes.txt` that are not in `knowngood_hashes.txt` and write them to a new file called `non_matching_hashes.txt` using:    
`grep -vf knowngood_hashes.txt current_hashes.txt > non_matching_hashes.txt`    
  
**step6:** Find and inspect all the files in the `non_matching_hashes.txt` by finding (ctrl+f) the hashes in the `current_md5sums_filenames.txt` or use `grep` again to find these files:    
`grep -F -f non_matching_hashes.txt current_md5sums_filenames.txt`  
  
**Download Practice Files**:    

`wget -O coming_to_greps_practice1.zip https://github.com/jboyce1/ppsCTF/raw/main/workrole/hashhound/challenges/Coming%20to%20greps%20with%20the%20past/3%20Coming%20to%20greps%20with%20the%20past%20\(practice%201\).zip`

<div style="text-align: center;">
<iframe width="560" height="315" src="https://www.youtube.com/embed/8piZLy8QhGg?si=-NwNQLoRDKrkBomj" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</div>

---

