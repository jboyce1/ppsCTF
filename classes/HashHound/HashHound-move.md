---
layout: move
title: Hash Hound
---

<p><strong>MOVE edition.</strong> <a href="{{ '/classes/HashHound/HashHound' | relative_url }}">Open the original lesson</a>.</p>


# Hash Hound<br>

**Focus**: Understanding and utilizing cryptographic hashing for security and integrity verification.<br>
**Skill**: Practical use of hashing functions in various security contexts.<br>
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

# Part 1: Fun New Game

<p class="move-skill">Use md5sum in terminal</p>
<section class="move-card" aria-label="Part 1 MOVE">
<dl>
<dt><span>M</span> Mission</dt><dd>Find the game that matches the supplied hash so your team can identify the correct file.</dd>
<dt><span>O</span> Objective</dt><dd>Identify and open the game whose MD5 hash is <code>cf9406bee74516677ca364c682c96d90</code>.</dd>
<dt><span>V</span> Validation</dt><dd>A terminal screenshot showing the matching MD5 hash and filename.</dd>
<dt><span>E</span> Explain / Expand / Explore</dt><dd><strong>Explain:</strong> How did you check the files and choose the matching game?<br><strong>Expand:</strong> Where else could comparing a file’s hash help you choose the right file?<br><strong>Explore:</strong> What could a matching hash tell you, and what questions about the file would remain?</dd>
</dl>
<p class="move-return">Return from your breakout room with your evidence and be ready to discuss your steps and ideas.</p>
</section>

## Required tools and practice files

Tools for this Part: `md5sum` to identify the matching game.

Use a Linux terminal (Kali on cyber.org works), `wget`, and `unzip`, plus the tools listed for this Part below. Download a practice ZIP below, extract it with `unzip filename.zip`, and open a terminal in the extracted challenge directory.

[Download hashhound_practice1.zip](https://github.com/jboyce1/ppsCTF/raw/main/classes/HashHound/Fun%20New%20Game%20Practice/1%20Fun%20New%20Game%20%28practice%201%29.zip)

```bash
wget -O hashhound_practice1.zip https://github.com/jboyce1/ppsCTF/raw/main/classes/HashHound/Fun%20New%20Game%20Practice/1%20Fun%20New%20Game%20\(practice%201\).zip
```


[Download hashhound_practice2.zip](https://github.com/jboyce1/ppsCTF/raw/main/classes/HashHound/Fun%20New%20Game%20Practice/1%20Fun%20New%20Game%20%28practice%202%29.zip)

```bash
wget -O hashhound_practice2.zip https://github.com/jboyce1/ppsCTF/raw/main/classes/HashHound/Fun%20New%20Game%20Practice/1%20Fun%20New%20Game%20\(practice%202\).zip
```


[Download hashhound_practice3.zip](https://github.com/jboyce1/ppsCTF/raw/main/classes/HashHound/Fun%20New%20Game%20Practice/1%20Fun%20New%20Game%20%28practice%203%29.zip)

```bash
wget -O hashhound_practice3.zip https://github.com/jboyce1/ppsCTF/raw/main/classes/HashHound/Fun%20New%20Game%20Practice/1%20Fun%20New%20Game%20\(practice%203\).zip
```


<details class="move-help" markdown="1">
<summary>Expand: additional guidance</summary>

### Finding a Hash in Terminal

```bash
echo -n YourStringHere | md5sum
```


  Output looks like: `26617986d9bafa5795a2c63fe209781e -`<br>

### To complete the challenges, you will need to download them on a Linux device (e.g. Kali through cyber.org)

1. Open a terminal where you want the file to download
2. Copy the wget command into shared clipboard (double ^ at the bottom for the cyber.org range)
3. Paste the wget command into terminal (ctrl, shift, v)
4. Hit enter



## Command Line Basics

Extracting Files<br>
To extract a `.zip` file, use:<br>

```bash
unzip filename.zip
```


## **Walkthrough**
Follow these steps to complete the challenge:


`ctrl + alt + t`<br>

```bash
cd /Desktop/
```


```bash
ls
```


```bash
cd Unit\ 1:\ Reverse\ Engineering/
```


```bash
ls
```


```bash
cd Checking\ Hash\ Functions/
```


```bash
ls
```


```bash
cd 1\ Fun\ New\ Game/
```


```bash
md5sum FuNeWgAmE.sh
```

**`************************************ FuNeWgAmE.sh`**<br>

```bash
md5sum funnewGAME.sh
```

**`************************************ funnewGAME.sh`**<br>

etc etc<br>
double click on game with match of:<br>
cf9406bee74516677ca364c682c96d90<br>

<div style="text-align: center;">
<iframe width="560" height="315" src="https://www.youtube.com/embed/rYW6l4Day8M?si=LrQ01odf0t_p2c7p" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</div>

</details>


---

# Part 2: Needle in the Hayloft

<p class="move-skill">Use find with the -type and -exec flags to create a file of md5sums</p>
<section class="move-card" aria-label="Part 2 MOVE">
<dl>
<dt><span>M</span> Mission</dt><dd>Find the file matching the needle hash so your team can recover its flag.</dd>
<dt><span>O</span> Objective</dt><dd>Locate the file with MD5 <code>c6fca9b96af058081fe4bfd89523f3f4</code> and find the flag inside.</dd>
<dt><span>V</span> Validation</dt><dd>Your <code>01md5sums.txt</code> file, the matching filename and hash, and the recovered flag.</dd>
<dt><span>E</span> Explain / Expand / Explore</dt><dd><strong>Explain:</strong> How did you search the directory, save its hashes, and find the flag?<br><strong>Expand:</strong> What other search tasks could use a saved list of file hashes?<br><strong>Explore:</strong> How could this approach help when a file’s name or location changes?</dd>
</dl>
<p class="move-return">Return from your breakout room with your evidence and be ready to discuss your steps and ideas.</p>
</section>

## Required tools and practice files

Tools for this Part: `find` and `md5sum` to build a hash list, and a text editor or `grep` to find the matching hash.

Use a Linux terminal (Kali on cyber.org works), `wget`, and `unzip`, plus the tools listed for this Part below. Download a practice ZIP below, extract it with `unzip filename.zip`, and open a terminal in the extracted challenge directory.

[Download needle_hayloft_practice1.zip](https://github.com/jboyce1/ppsCTF/raw/main/classes/HashHound/Needle%20in%20the%20Hayloft%20Practice/2%20Needle%20in%20the%20Hayloft%20%28practice%201%29.zip)

```bash
wget -O needle_hayloft_practice1.zip https://github.com/jboyce1/ppsCTF/raw/main/classes/HashHound/Needle%20in%20the%20Hayloft%20Practice/2%20Needle%20in%20the%20Hayloft%20\(practice%201\).zip
```


[Download needle_hayloft_practice2.zip](https://github.com/jboyce1/ppsCTF/raw/main/classes/HashHound/Needle%20in%20the%20Hayloft%20Practice/2%20Needle%20in%20the%20Hayloft%20%28practice%202%29.zip)

```bash
wget -O needle_hayloft_practice2.zip https://github.com/jboyce1/ppsCTF/raw/main/classes/HashHound/Needle%20in%20the%20Hayloft%20Practice/2%20Needle%20in%20the%20Hayloft%20\(practice%202\).zip
```


[Download needle_hayloft_practice3.zip](https://github.com/jboyce1/ppsCTF/raw/main/classes/HashHound/Needle%20in%20the%20Hayloft%20Practice/2%20Needle%20in%20the%20Hayloft%20%28practice%203%29.zip)

```bash
wget -O needle_hayloft_practice3.zip https://github.com/jboyce1/ppsCTF/raw/main/classes/HashHound/Needle%20in%20the%20Hayloft%20Practice/2%20Needle%20in%20the%20Hayloft%20\(practice%203\).zip
```


<details class="move-help" markdown="1">
<summary>Expand: additional guidance</summary>

Here is your md5sum needle: c6fca9b96af058081fe4bfd89523f3f4<br>

step1: Navigate to the '2 Needle in the Hayloft' directory<br>
step2: Make a text file using the following command:<br>

```bash
find . -type f -exec md5sum {} \; > 01md5sums.txt
```


- Explaination for command<br>
  - **`find .`** searches for files and directories starting from the current directory (.).<br>
  - **`-type f`** specifies that we are interested in files only, not directories.<br>
  - **`-exec md5sum {} \;`** executes the md5sum command on each file found by find. {} represents the current file being processed by find.<br>
  - **`> md5sums.txt`** redirects the output (MD5 checksums) to a file named md5sums.txt.<br>

step3: open the text file and search (ctrl+f) the needle you are looking for<br>
step4: open the file and find the flag<br>

For more informaiton on the find functions, read the manual:<br>
man find<br>


<div style="text-align: center;">
<iframe width="560" height="315" src="https://www.youtube.com/embed/iDQTr-loTe0?si=j5mmNbN_vddz3_Ig" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
  </div>

</details>


---

# Part 3: Coming to Greps with the Past

<p class="move-skill">Use find, cut, and grep to isolate suspicious files</p>
<section class="move-card" aria-label="Part 3 MOVE">
<dl>
<dt><span>M</span> Mission</dt><dd>Compare the current files with the known-good hashes so your team can investigate what changed.</dd>
<dt><span>O</span> Objective</dt><dd>Identify and inspect files whose current hashes are missing from <code>knowngood_md5sums_filenames.txt</code>.</dd>
<dt><span>V</span> Validation</dt><dd>Your <code>non_matching_hashes.txt</code> file and terminal output linking the non-matching hashes to the files you inspected.</dd>
<dt><span>E</span> Explain / Expand / Explore</dt><dd><strong>Explain:</strong> How did you compare the lists and trace a non-matching hash to its file?<br><strong>Expand:</strong> Where else could a known-good list help you investigate changes?<br><strong>Explore:</strong> Does every non-matching hash mean a file is malicious? What would you investigate next?</dd>
</dl>
<p class="move-return">Return from your breakout room with your evidence and be ready to discuss your steps and ideas.</p>
</section>

## Required tools and practice files

Tools for this Part: `find`, `md5sum`, `cut`, and `grep` to compare current files with the known-good hash list.

Use a Linux terminal (Kali on cyber.org works), `wget`, and `unzip`, plus the tools listed for this Part below. Download a practice ZIP below, extract it with `unzip filename.zip`, and open a terminal in the extracted challenge directory.

[Download coming_to_greps_practice1.zip](https://github.com/jboyce1/ppsCTF/raw/main/classes/HashHound/Coming%20to%20greps%20with%20the%20past/3%20Coming%20to%20greps%20with%20the%20past%20%28practice%201%29.zip)

```bash
wget -O coming_to_greps_practice1.zip https://github.com/jboyce1/ppsCTF/raw/main/classes/HashHound/Coming%20to%20greps%20with%20the%20past/3%20Coming%20to%20greps%20with%20the%20past%20\(practice%201\).zip
```


<details class="move-help" markdown="1">
<summary>Expand: additional guidance</summary>

### Suspicious Needle Search<br>

You need to find the suspicious needle. They were all good when they left but something changed. The `knowngood_md5sums_filenames.txt` is a list of all the unsuspicious files.<br>

**step1:** Navigate to the directory containing `knowngood_md5sums_filenames.txt`<br>
**step2:** Extract all of the hashes from the `knowngood_md5sums_filenames.txt` using the command:<br>

```bash
cut -d ' ' -f 1 knowngood_md5sums_filenames.txt > knowngood_hashes.txt
```


- Explanation for command
  - `cut -d ' '` specifies the delimiter as a space.
  - `-f 1` selects the first field, which is typically the hash value.
  - `> knowngood_hashes.txt` redirects the output to a file named `knowngood_hashes.txt`.<br>

**step3:** Find all the MD5 sums in the directory using the command:<br>

```bash
find . -type f -exec md5sum {} \; > current_md5sums_filenames.txt
```


**step4:** Extract all hashes from the `current_md5sums_filenames.txt` using:<br>

```bash
cut -d ' ' -f 1 current_md5sums_filenames.txt > current_hashes.txt
```


**step5:** Search for lines in `current_hashes.txt` that are not in `knowngood_hashes.txt` and write them to a new file called `non_matching_hashes.txt` using:<br>

```bash
grep -vf knowngood_hashes.txt current_hashes.txt > non_matching_hashes.txt
```


**step6:** Find and inspect all the files in the `non_matching_hashes.txt` by finding (ctrl+f) the hashes in the `current_md5sums_filenames.txt` or use `grep` again to find these files:<br>

```bash
grep -F -f non_matching_hashes.txt current_md5sums_filenames.txt
```



<div style="text-align: center;">
<iframe width="560" height="315" src="https://www.youtube.com/embed/8piZLy8QhGg?si=-NwNQLoRDKrkBomj" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</div>

</details>
