---
layout: default
title: Hash Hound
---

# Hash Hound    

**Focus**: Understanding and utilizing cryptographic hashing for security and integrity verification.  
**Skill**: Practical use of hashing functions in various security contexts.  
**Activity**: Hands-on hashing challenges with real-world applications.

<div style="text-align: center;">
  <img src="{{ 'classes/HashHound/90255-Hash-Hound.png' | relative_url }}" alt="Hash Hound Logo" style="max-width: 80%; height: auto;">
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

1. **Click the link** to open a new page.  
2. **Download the `.zip` file** by clicking the ‘Download’ button on the top left of the page.  
3. **Go to your Downloads folder** and locate the file.  
4. **Right-click and extract** the file.  
5. **Find the Flag** (watch the video, remember flags look like `pps{someflag}`).  
6. **Click the “Flag” link** after the practice and paste your flag to see if it is correct.  


## **Download Practice Files**
📥 [Practice 1](./Fun%20New%20Game%20Practice/1%20Fun%20New%20Game%20(practice%201).zip)  
📥 [Practice 2](./Fun%20New%20Game%20Practice/1%20Fun%20New%20Game%20(practice%202).zip)  
📥 [Practice 3](./Fun%20New%20Game%20Practice/1%20Fun%20New%20Game%20(practice%203).zip)  


## **Walkthrough**
Follow these steps to complete the challenge:


`ctrl + alt + t`   
`cd /Desktop/`   
`ls`  
`cd Unit\ 1:\ Reverse\ Engineering/`  
`ls`  
`cd Checking\ Hash\ Functions/`  
`ls`  
`cd 1\ Fun\ New\ Game/`  
`md5sum FuNeWgAmE.sh`  
**`************************************ FuNeWgAmE.sh`**    
`md5sum funnewGAME.sh`  
**`************************************ funnewGAME.sh`**  
 
etc etc    
double click on game with match of:    
cf9406bee74516677ca364c682c96d90      
    
<div style="text-align: center;">
<iframe width="560" height="315" src="https://www.youtube.com/embed/rYW6l4Day8M?si=LrQ01odf0t_p2c7p" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</div>
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
📥 [Practice 1](./Needle%20in%20the%20Hayloft%20Practice/2%20Needle%20in%20the%20Hayloft%20(practice%201).zip)    
📥 [Practice 2](./Needle%20in%20the%20Hayloft%20Practice/2%20Needle%20in%20the%20Hayloft%20(practice%202).zip)    
📥 [Practice 3](./Needle%20in%20the%20Hayloft%20Practice/2%20Needle%20in%20the%20Hayloft%20(practice%203).zip)    
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
📥 [Practice 1](./Coming%20to%20greps%20with%20the%20past/3%20Coming%20to%20greps%20with%20the%20past%20(practice%201).zip)    
<div style="text-align: center;">
<iframe width="560" height="315" src="https://www.youtube.com/embed/8piZLy8QhGg?si=-NwNQLoRDKrkBomj" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</div>

---

## Command Line Basics  
  
# Extracting Files  
To extract a `.zip` file, use:  
`unzip filename.zip`
