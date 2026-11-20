---
layout: default
title: Ms. Disin
---

<p><a href="{{ '/workrole/msdisin/MsDisin-move' | relative_url }}">Open the MOVE edition</a>.</p>

# Ms. Disin   

**Focus**: Text manipulation  
**Skill**: Use grep, sed, awk, diff, xxd and sort to extract and manipulate text and data  
**Activity**: Extract and manipulate files that are text based   

<div style="text-align: center;">
  <img src="{{ 'workrole/msdisin/images/Ms_Disin Banner2.jpg' | relative_url }}" alt="Ms_Disin Banner2" style="max-width: 80%; height: auto;">
</div>    

## Sometimes the world is a web of lies
### Be a spider
---
    
**play a game while I yap**:     
sudo apt install greed    
greed    
  
sudo apt install zangband    
man atc    
atc    

### Specific Skills
- Use cat to combine multiple text files and display their contents quickly
- Use grep and find to locate specific patterns of text within files across different directories
- Use sed to edit text files directly in the terminal
- Combine awk and sed to extract and transform specific data from files
- Use sort and uniq for sorting data and finding duplicates
- Use diff to compare files
- Use tail and head to view just the beginning or end of files
- Use sqlite to query webbrowser history

### Things to experiment with on the range:     
- Regex with grep: Mastering regular expressions to refine search criteria and pinpoint exact data sets.    
- Stream editing with sed: Practice on-the-fly file content manipulations during competitive scenarios.    
- Data manipulation with awk: Leverage awk's programming capabilities to analyze and report on data extracted during competitions.    

 
### How this skill can be used:  
**Offensive Operations:**
 - Data Extraction Tactics: Utilize combinations of grep, awk, and sed to extract sensitive information from opponent’s files, which could range from passwords to strategic plans.
 - Script Manipulation: Through direct file editing using sed and cat, alter scripts or configurations in the enemy's network to disrupt their operations or misdirect their strategies.

**Defensive Operations:**
 - File Integrity Checks: Use grep and awk to monitor files for unauthorized changes that could indicate infiltration attempts.
 - Rapid Response Editing: Employ sed to quickly revert any unauthorized changes or to patch vulnerabilities in script configurations during live competitions.
    
    
---
# Part 1: Use cat to combine multiple text files and display their contents quickly
### “cat” the cat and “grep” the dog (because who names a cat?)

<div style="text-align: center;">
  <img src="{{ 'workrole/msdisin/images/msdisins_dog.webp' | relative_url }}" alt="Hash Hound Logo" style="max-width: 80%; height: auto;">
</div>

Start a Kali machine    
**Step 1:**      
Download the cat observations     
<span id="wget-httpsgithubcomjboyce1ppsctfrawmainclassesmsdisincat_observationszip"></span>

<div class="terminal lesson-command" id="wget-httpsgithubcomjboyce1ppsctfrawmainworkrolemsdisinchallengescat_observationszip"><pre><code>wget https://github.com/jboyce1/ppsCTF/raw/main/workrole/msdisin/challenges/cat_observations.zip</code></pre></div>

Unzip the contents of the folder.    
Open a terminal inside the cat_observations folder    
use the cat command to read each passage    
cat cat_1    
(hint: use the up arrow key and backspace to quickly advance in the journal)    
    
**Step 2:**    
From  inside the cat_observations folder, open a terminal    
To display all of the text in the files:    

<div class="terminal lesson-command" id="find---type-f--exec-cat--"><pre><code>find . -type f -exec cat {} +</code></pre></div>

To display all of the text in the files with their file names in order and get really fancy?:    

<div class="terminal lesson-command" id="find---type-f--name---sort--xargs-cat"><pre><code>find . -type f -name "*" | sort | xargs cat</code></pre></div>

Explaination of flags:    
 -  `find . -type f -name "*."`  Search for all files with an extension in the current directory (.) and its subdirectories.    
 - `| sort` pipes the output to sort in order to list of filenames alphabetically.    
 - `| xargs cat`  Pass the sorted list of filenames to the cat command to display their contents in order.   

<div style="text-align: center;">
  <img src="{{ 'workrole/msdisin/images/msdisins_cat.webp' | relative_url }}" alt="Hash Hound Logo" style="max-width: 80%; height: auto;">
</div>    

### Try it now    
use the dog_oberservations.zip to do the same thing  
<span id="wget-httpsgithubcomjboyce1ppsctfrawmainclassesmsdisindog_observationszip"></span>

<div class="terminal lesson-command" id="wget-httpsgithubcomjboyce1ppsctfrawmainworkrolemsdisinchallengesdog_observationszip"><pre><code>wget https://github.com/jboyce1/ppsCTF/raw/main/workrole/msdisin/challenges/dog_observations.zip</code></pre></div>

Write a synopsis of what you think is happening <a href="https://forms.office.com/Pages/ResponsePage.aspx?id=mhxxjxzsu023kLsMdxsdzM6J33C5yQRJgc1SHWy_64dUOFYxN1JKSUExN09WVzY3VzE0WFU1VU1IUC4u" target="_blank">here</a>  

<div style="text-align: center;">
<iframe width="560" height="315" src="https://www.youtube.com/embed/jmTVwNt24Sk?si=6UXLuTWlRTuxneLB" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</div>
--- 

# Part 2: use cat and grep to find text in files and directories    
    
### Use grep to find specific instances of strings    
### Use grep and awk to find locations of strings within a text    
### Use sed to change all instances of a string to another string    
### Combine awk and sed to identify instances of a string and change them    
### Use grep and wc to count how many instances of a string are in a text    
### Use diff to determine the differences between two files    
### Use diff to determine the differences between two directories    

<div style="text-align: center;">
  <img src="{{ 'workrole/msdisin/images/worldsgreatestspies_cover.jpg' | relative_url }}" alt="worldsgreatestspies_cover" style="max-width: 80%; height: auto;">
</div>  

get the file:
<span id="wget-httpsgithubcomjboyce1ppsctfrawmainclassesmsdisinthe_worlds_greatest_military_spies_and_secret_service_agentstxt"></span>

<div class="terminal lesson-command" id="wget-httpsgithubcomjboyce1ppsctfrawmainworkrolemsdisinchallengesthe_worlds_greatest_military_spies_and_secret_service_agentstxt"><pre><code>wget https://github.com/jboyce1/ppsCTF/raw/main/workrole/msdisin/challenges/The_Worlds_Greatest_Military_Spies_and_Secret_Service_Agents.txt</code></pre></div>

### grep overview:     
grep searches for items and returns the entire line that contains the item    

To search non-case sensitive:    

<div class="terminal lesson-command" id="grep--i--napoleon-filetxt"><pre><code>grep -i  "napoleon" file.txt</code></pre></div>

    
To search recursively (all files) in directories:    

<div class="terminal lesson-command" id="grep--r-napoleon-pathtodirectory"><pre><code>grep -r "Napoleon" /path/to/directory/</code></pre></div>

    
To get the file names that contain an item:    

<div class="terminal lesson-command" id="grep--l-napoleon-txt"><pre><code>grep -l "Napoleon" *.txt</code></pre></div>

    
To include the file names that contain an item:    

<div class="terminal lesson-command" id="grep--h-napoleon-txt"><pre><code>grep -H "Napoleon" *.txt</code></pre></div>

    
To invert the search and search of lines that do not contain the item:        

<div class="terminal lesson-command" id="grep--v-napoleon-filetxt"><pre><code>grep -v "Napoleon" file.txt</code></pre></div>

    
To count the matches:    

<div class="terminal lesson-command" id="grep--c-napoleon-filetxt"><pre><code>grep -c "Napoleon" file.txt</code></pre></div>

    
To see the lines before and after, use -B and -A      

<div class="terminal lesson-command" id="grep--b-2-napoleon-filetxt"><pre><code>grep -B 2 "Napoleon" file.txt</code></pre></div>

<div class="terminal lesson-command" id="grep--a-2-napoleon-filetxt"><pre><code>grep -A 2 "Napoleon" file.txt</code></pre></div>

    
To highlight matches in the text    

<div class="terminal lesson-command" id="grep---colorauto-napoleon-filetxt"><pre><code>grep --color=auto "Napoleon" file.txt</code></pre></div>

---
# Part 3: use awk to perform complex searches

### awk overview:
General pattern: awk 'pattern {action}' file    
 - pattern: The condition you want to match (optional).    
 - action: The operation to perform on the matched lines (optional).    
- file: The file you're processing.    

Use similar to grep

<div class="terminal lesson-command" id="awk-prince-of-spies-the_worlds_greatest_military_spies_and_secret_service_agentstxt"><pre><code>awk '/Prince of Spies/' The_Worlds_Greatest_Military_Spies_and_Secret_Service_Agents.txt</code></pre></div>

 - similar to grep

Add conditional logical controls    

<div class="terminal lesson-command" id="awk-belle-boyd--1917-the_worlds_greatest_military_spies_and_secret_service_agentstxt"><pre><code>awk '/Belle Boyd/ &amp;&amp; /1917/' The_Worlds_Greatest_Military_Spies_and_Secret_Service_Agents.txt</code></pre></div>

 - find lines containing "Belle Boyd" and  "1917"

This is an example of more powerful application of awk 

<div class="terminal lesson-command" id="awk-the-battle-ofconfederate--if-index0-belle-boyd--0-print-0--the_worlds_greatest_military_spies_and_secret_service_agentstxt"><pre><code>awk '/The Battle of/,/Confederate/ { if (index($0, "Belle Boyd") &gt; 0) print $0 }' The_Worlds_Greatest_Military_Spies_and_Secret_Service_Agents.txt</code></pre></div>

 - `/The Battle of/,/Confederate/` is an awk range pattern. It tells awk to start processing lines when it encounters a line containing "The Battle of", and stop processing once it encounters a line containing "Confederate".
So, awk will process all lines in between these two patterns.    
 - `{ if (index($0, "Belle Boyd") > 0) print $0 }:`
 - `$0`: This refers to the entire current line in awk.
`index($0, "Belle Boyd")`: The `index()` function returns the position of the first occurrence of "Belle Boyd" in the current line. If "Belle Boyd" is found, it returns a position (a number greater than 0), otherwise it returns 0.
 - `if (index($0, "Belle Boyd") > 0)`: This checks if "Belle Boyd" exists in the line (i.e., the position is greater than 0).
print $0: If "Belle Boyd" is found, the entire line is printed.

Find out who:
Use grep to find the name of the person who was called the "Prince of Spies".    

<div class="terminal lesson-command"><pre><code>grep -i "Prince of Spies" The_Worlds_Greatest_Military_Spies_and_Secret_Service_Agents.txt</code></pre></div>

    
When did:    
Use grep to discover when the book "The World's Greatest Military Spies and Secret Service Agents" was first published.    

<div class="terminal lesson-command"><pre><code>grep -i "first impression" The_Worlds_Greatest_Military_Spies_and_Secret_Service_Agents.txt</code></pre></div>

    
Where did:    
Use grep and awk to find the location where "Belle Boyd" saved Stonewall Jackson.    

<div class="terminal lesson-command"><pre><code>grep -i "Belle Boyd" The_Worlds_Greatest_Military_Spies_and_Secret_Service_Agents.txt | awk '{print $0}'</code></pre></div>

    
What event:    
Use grep to identify the event described as "the capture of Major André".    

<div class="terminal lesson-command"><pre><code>grep -i "Major André" The_Worlds_Greatest_Military_Spies_and_Secret_Service_Agents.txt</code></pre></div>

    
Manipulate names:        
Use sed to change all instances of "Napoleon" to "Roger Rabbit"      

<div class="terminal lesson-command"><pre><code>sed -i 's/Napoleon/Roger Rabbit/g' The_Worlds_Greatest_Military_Spies_and_Secret_Service_Agents.txt</code></pre></div>

    
Alter dates:    
Use sed to change all instances of the year "1917" to "1947".    

<div class="terminal lesson-command"><pre><code>sed -i 's/1917/1947/g' The_Worlds_Greatest_Military_Spies_and_Secret_Service_Agents.txt</code></pre></div>

    
Combine awk and sed:    
Use awk to find lines containing "King Philip" and then sed to change "King Philip" to "King Roger".    

<div class="terminal lesson-command"><pre><code>awk '/King Philip/' The_Worlds_Greatest_Military_Spies_and_Secret_Service_Agents.txt | sed 's/King Philip/King Roger/g'</code></pre></div>

    
 Extracting sentences:    
Use grep to extract sentences that mention "Confederate spy"    

<div class="terminal lesson-command"><pre><code>grep -i "Confederate spy" The_Worlds_Greatest_Military_Spies_and_Secret_Service_Agents.txt</code></pre></div>

    
Count occurrences:    
Use grep and wc to count how many times the word "secret" appears in the text.    

<div class="terminal lesson-command"><pre><code>grep -o -i "secret" The_Worlds_Greatest_Military_Spies_and_Secret_Service_Agents.txt | wc -l</code></pre></div>

      
---
# Part 4: use wc tr sort uniq to derive data from text strings    

Here's how you can get the 100 most common words in a text file directly in the terminal:    

<div class="terminal lesson-command" id="tr--cs-a-za-z-n--inputtxt--tr-a-z-a-z--sort--uniq--c--sort--nr--head--100"><pre><code>tr -cs 'A-Za-z' '\n' &lt; input.txt | tr 'A-Z' 'a-z' | sort | uniq -c | sort -nr | head -100</code></pre></div>

    
Explanation of Each Command:    
 - **`tr -cs 'A-Za-z' '\n'`**: This translates all sequences of characters that are not alphabets into newlines, effectively putting each word on a new line.      
 - **`tr 'A-Z' 'a-z'`**: This converts all uppercase letters to lowercase.    
 - **`sort`**: This sorts the words alphabetically, which is necessary for uniq to count all occurrences properly.    
 - **`uniq -c`**: This counts the number of occurrences of each word. The words need to be sorted as uniq only matches consecutive duplicate lines.    
 - **`sort -nr`**: This sorts the list numerically in reverse order, placing the most frequent words at the top.    
 - **`head -100`**: This displays only the top 100 results.    
    
Or add in awk capabilities to filter out small words    

<div class="terminal lesson-command" id="tr--cs-a-za-z-n--inputtxt--tr-a-z-a-z--awk-length0--3--sort--uniq--c--sort--nr--head--100"><pre><code>tr -cs 'A-Za-z' '\n' &lt; input.txt | tr 'A-Z' 'a-z' | awk 'length($0) &gt; 3' | sort | uniq -c | sort -nr | head -100</code></pre></div>

Try to use what you have learned so far to get the flags in these files:
<span id="wget-httpsrawgithubusercontentcomjboyce1ppsctfmainclassesmsdisintrainingspy_traffic_historydbmsdis_practice1zip"></span>

<div class="terminal lesson-command" id="wget-httpsrawgithubusercontentcomjboyce1ppsctfmainworkrolemsdisinchallengesmsdis_practice1zip"><pre><code>wget https://raw.githubusercontent.com/jboyce1/ppsCTF/main/workrole/msdisin/challenges/msdis_practice1.zip</code></pre></div>

<span id="wget-httpsrawgithubusercontentcomjboyce1ppsctfmainclassesmsdisintrainingspy_traffic_historydbmsdis_practice2zip"></span>

<div class="terminal lesson-command" id="wget-httpsrawgithubusercontentcomjboyce1ppsctfmainworkrolemsdisinchallengesmsdis_practice2zip"><pre><code>wget https://raw.githubusercontent.com/jboyce1/ppsCTF/main/workrole/msdisin/challenges/msdis_practice2.zip</code></pre></div>

<span id="wget-httpsrawgithubusercontentcomjboyce1ppsctfmainclassesmsdisintrainingspy_traffic_historydbmsdis_practice3zip"></span>

<div class="terminal lesson-command" id="wget-httpsrawgithubusercontentcomjboyce1ppsctfmainworkrolemsdisinchallengesmsdis_practice3zip"><pre><code>wget https://raw.githubusercontent.com/jboyce1/ppsCTF/main/workrole/msdisin/challenges/msdis_practice3.zip</code></pre></div>

    
--- 
### Turn recorded word counts into a passphrase

Download a practice book.

<div class="terminal lesson-command"><pre><code>wget https://raw.githubusercontent.com/jboyce1/ppsCTF/main/workrole/msdisin/challenges/With_the_Swamp_Fox_A_Story_of_General_Marions_Young_Spies.txt</code></pre></div>

For this example, the recorded counts are **975, 779, 539**, in that order. Split the book into words and normalize the case.

<div class="terminal lesson-command"><pre><code>LC_ALL=C tr -cs 'A-Za-z' '\n' &lt; With_the_Swamp_Fox_A_Story_of_General_Marions_Young_Spies.txt &gt; words.txt</code></pre></div>

<div class="terminal lesson-command"><pre><code>LC_ALL=C tr 'A-Z' 'a-z' &lt; words.txt &gt; lowercase-words.txt</code></pre></div>

<div class="terminal lesson-command"><pre><code>sort lowercase-words.txt &gt; sorted-words.txt</code></pre></div>

<div class="terminal lesson-command"><pre><code>uniq -c sorted-words.txt &gt; word-counts.txt</code></pre></div>

<div class="terminal lesson-command"><pre><code>awk '$1 == 975 || $1 == 779 || $1 == 539' word-counts.txt</code></pre></div>

Match each count to its word and read the words in the order on the card. Join them with hyphens to get `by-that-with`. With several candidate texts, count each one separately and look for all the recorded counts in the same book.

# Part 5: Use diff and xxd to compare files  

Spot the Differences:    
Use diff to extract what has changed in the two files line by line    

<div class="terminal lesson-command"><pre><code>diff -y original_file.txt modified_file.txt</code></pre></div>

or    

<div class="terminal lesson-command"><pre><code>diff -u original_file.txt modified_file.txt</code></pre></div>

or for directories:    

<div class="terminal lesson-command"><pre><code>diff -r original_directory modified_directory</code></pre></div>

Use xxd to determine the hexidecimal difference between files

<div class="terminal lesson-command" id="xxd-originaltxt--originalhex"><pre><code>xxd original.txt &gt; original.hex</code></pre></div>

<div class="terminal lesson-command" id="xxd-modifiedtxt--modifiedhex"><pre><code>xxd modified.txt &gt; modified.hex</code></pre></div>

<div class="terminal lesson-command" id="diff--u-originalhex-modifiedhex"><pre><code>diff -u original.hex modified.hex</code></pre></div>

<div style="text-align: center;">
  <img src="{{ 'workrole/msdisin/images/xxd_screenshot.png' | relative_url }}" alt="worldsgreatestspies_cover" style="max-width: 80%; height: auto;">
</div>  

---
### Read replacement characters in file order

Create two short practice files.

<div class="terminal lesson-command"><pre><code>printf '%s\n' 'The gate is open.' 'Report to post two.' &gt; original.txt</code></pre></div>

<div class="terminal lesson-command"><pre><code>printf '%s\n' 'The gate is Qpen.' 'Report to post t7o.' &gt; modified.txt</code></pre></div>

<div class="terminal lesson-command"><pre><code>diff -u original.txt modified.txt</code></pre></div>

Compare each changed original line (`-`) with its modified line (`+`). In this example, `o` becomes `Q` and `w` becomes `7`. Read the characters from the modified file in line order to get `Q7`. Keep case and spacing visible when you compare files.

# Part 6: Use sqlite to query web browser history
    
If Kali does not have the SQLite command-line client, install it.

<div class="terminal lesson-command"><pre><code>sudo apt install sqlite3</code></pre></div>

For a history saved under a hidden directory in a user home, use `ls -a` to show dot directories. Look for the supplied `.db` file in the browser folder and open that file with SQLite.

### Determine the visited sites in the database
Navigate the the directory with the .db file in it

    
In terminal, open sqlite

<div class="terminal lesson-command" id="sqlite3-whatever_the_traffic_database_is_calleddb"><pre><code>sqlite3 whatever_the_traffic_database_is_called.db</code></pre></div>

Verify database is open and you are able to access the tables    

<div class="terminal lesson-command" id="tables"><pre><code>.tables</code></pre></div>

 - you should see something like browsing_history
   
Inspect the stucture of the tables    

<div class="terminal lesson-command" id="pragma-table_infobrowsing_history"><pre><code>PRAGMA table_info(browsing_history);</code></pre></div>

  - commands will execute once they end with a semi-colon `;`

    
Test a basic query from the browsing_history table    

<div class="terminal lesson-command" id="select--from-browsing_history-limit-1000"><pre><code>SELECT * FROM browsing_history LIMIT 1000;</code></pre></div>

    
Quit out of the sqlite3    

<div class="terminal lesson-command" id="quit"><pre><code>.quit</code></pre></div>

    
Now you try it:
Download the sample database
<span id="wget-httpsrawgithubusercontentcomjboyce1ppsctfmainclassesmsdisintrainingspy_traffic_historydb"></span>

<div class="terminal lesson-command" id="wget-httpsrawgithubusercontentcomjboyce1ppsctfmainworkrolemsdisinchallengesspy_traffic_historydb"><pre><code>wget https://raw.githubusercontent.com/jboyce1/ppsCTF/main/workrole/msdisin/challenges/spy_traffic_history.db</code></pre></div>

Query the most visited sites:    
    

<div class="terminal lesson-command"><pre><code>SELECT url, COUNT(url) AS visit_count
FROM browsing_history
GROUP BY url
ORDER BY visit_count DESC
LIMIT 100;</code></pre></div>

    

<div style="text-align: center;">
<iframe width="560" height="315" src="https://www.youtube.com/embed/uemcs2H9uMw?si=F20xyvQccYlW7MAi" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</div>

### Identify and determine spikes in web traffic

Download the sample database:
<span id="wget-httpsrawgithubusercontentcomjboyce1ppsctfmainclassesmsdisintrainingspykid_traffic_historydb"></span>

<div class="terminal lesson-command" id="wget-httpsrawgithubusercontentcomjboyce1ppsctfmainworkrolemsdisinchallengesspykid_traffic_historydb"><pre><code>wget https://raw.githubusercontent.com/jboyce1/ppsCTF/main/workrole/msdisin/challenges/spykid_traffic_history.db</code></pre></div>

    
Open the database

<div class="terminal lesson-command" id="sqlite3-spykid_traffic_historydb"><pre><code>sqlite3 spykid_traffic_history.db</code></pre></div>

Look for spikes in activity that seem excessively high or low on a weekly basis:

<div class="terminal lesson-command"><pre><code>SELECT strftime('%Y-%W', timestamp) AS week, COUNT(*) AS visit_count
FROM browsing_history
GROUP BY week
ORDER BY week ASC;</code></pre></div>

Here the number 94 stands out:
<div style="text-align: center;">
  <img src="{{ 'workrole/msdisin/images/high_activity_in_method1.png' | relative_url }}" alt="worldsgreatestspies_cover" style="max-width: 80%; height: auto;">
</div>  
    
    
Look find the average web traffic and the highest web traffic:
    

<div class="terminal lesson-command"><pre><code>SELECT AVG(visit_count) AS avg_visits, MAX(visit_count) AS max_visits
FROM (
    SELECT strftime('%Y-%W', timestamp) AS week, COUNT(*) AS visit_count
    FROM browsing_history
    GROUP BY week
);</code></pre></div>

Here we see the average of 37.03 with a max of 94
<div style="text-align: center;">
  <img src="{{ 'workrole/msdisin/images/screenshot-avg-visit-most-visit.png' | relative_url }}" alt="worldsgreatestspies_cover" style="max-width: 80%; height: auto;">
</div>  

Find traffic that is above or below the average visits by a certain threshold

<div class="terminal lesson-command"><pre><code>WITH weekly_traffic AS (
    SELECT strftime('%Y-%W', timestamp) AS week, COUNT(*) AS visit_count
    FROM browsing_history
    GROUP BY week
),
stats AS (
    SELECT AVG(visit_count) AS avg_visits FROM weekly_traffic
)
SELECT wt.week, wt.visit_count
FROM weekly_traffic wt, stats s
WHERE wt.visit_count &gt; s.avg_visits * 1.5
ORDER BY wt.visit_count DESC;</code></pre></div>

    
You can ajust the `WHERE wt.visit_count > s.avg_visits * 1.5` to define your own thresholds
Here we see the week of high activity was 2025-00
<div style="text-align: center;">
  <img src="{{ 'workrole/msdisin/images/above_average_browser_activity.png' | relative_url }}" alt="worldsgreatestspies_cover" style="max-width: 80%; height: auto;">
</div>  

Investigate specific weeks by getting a count of the sites visited during that week:

<div class="terminal lesson-command"><pre><code>SELECT url, COUNT(*) AS visit_count
FROM browsing_history
WHERE strftime('%Y-%W', timestamp) = '2025-00'
GROUP BY url
ORDER BY visit_count DESC
LIMIT 5;</code></pre></div>

    
The first row shows the most visited URL during the selected week. If the task asks for the busiest week, use the week with the highest count from the weekly results. Read the URL from SQLite and use the challenge’s flag template to determine which part to submit.
<div style="text-align: center;">
  <img src="{{ 'workrole/msdisin/images/investigate_week_by_traffic.png' | relative_url }}" alt="worldsgreatestspies_cover" style="max-width: 80%; height: auto;">
</div>  

<div style="text-align: center;">
<iframe width="560" height="315" src="https://www.youtube.com/embed/_l9exLe5sG8?si=TA1FQflvVs8oHDW_" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</div>

---
# Part 7: Recover deleted files

**First range test:** recover one deleted picture with Scalpel. Deleting a file
can leave its contents behind until that space is reused. Scalpel searches for
file signatures to recover those contents. This small filesystem image already
has a picture deleted from it.

**Step 1:** In the file manager, create a folder named `deleted-picture-test`.
Open it, then right-click an empty area and open a terminal there.

**Step 2:** Install Scalpel. Wait for installation to finish.

<div class="terminal lesson-command"><pre><code>sudo apt install scalpel</code></pre></div>

**Step 3:** Download the filesystem image. Wait for Wget to report success.

<div class="terminal lesson-command"><pre><code>wget https://raw.githubusercontent.com/jboyce1/ppsCTF/main/workrole/msdisin/challenges/carving/deleted-picture.img.gz</code></pre></div>

**Step 4:** Decompress it. Wait for the prompt to return.

<div class="terminal lesson-command"><pre><code>gunzip deleted-picture.img.gz</code></pre></div>

**Step 5:** Download the JPEG recovery configuration. Wait for Wget to report success.

<div class="terminal lesson-command"><pre><code>wget https://raw.githubusercontent.com/jboyce1/ppsCTF/main/workrole/msdisin/challenges/carving/scalpel-jpg.conf</code></pre></div>

**Step 6:** Recover the picture. `-c` selects the configuration; `-o` names a new
output folder. Recovered files are saved outside the source image.
Wait for Scalpel to finish.

<div class="terminal lesson-command"><pre><code>scalpel -c scalpel-jpg.conf -o recovered deleted-picture.img</code></pre></div>

**Step 7:** In the file manager, open `recovered`, then its JPEG subfolder.
Open the recovered picture. You should see the cover of *The World's Greatest
Military Spies and Secret Service Agents*. Scalpel gives it a generated filename.

**Step 8:** Open a terminal in that JPEG subfolder. Check the recovered file's hash.

<div class="terminal lesson-command"><pre><code>sha256sum *.jpg</code></pre></div>

The hash should be:

<div class="terminal lesson-command"><pre><code>36cf7df21d30068f2e75f04078a2ec2bcb6c37a3c0afb40ff34e82d7447e7614</code></pre></div>

A matching hash confirms recovery of the original picture's bytes. This example
was checked locally; the full CYBER.ORG walkthrough is awaiting this range test.
For another attempt, use a new output folder name in step 6, such as `recovered2`.
Real deleted files may be overwritten or fragmented, so recovery is not guaranteed.

### File recovery command references

**Manual carving with dd — PNG, JPEG, PDF, and ZIP:**

<div class="terminal lesson-command"><pre><code>wget https://raw.githubusercontent.com/jboyce1/ppsCTF/main/workrole/msdisin/challenges/carving/dd-cheatsheet.txt</code></pre></div>

**Scalpel commands and configuration rules — PNG, JPEG, PDF, and ZIP:**

<div class="terminal lesson-command"><pre><code>wget https://raw.githubusercontent.com/jboyce1/ppsCTF/main/workrole/msdisin/challenges/carving/scalpel-cheatsheet.txt</code></pre></div>

### Next investigation: the City Point flash drive

Recover missing historical photographs and investigate the proposed exhibition
caption. Use PNG headers, IEND offsets, and your own byte-length calculations to
recover the pictures manually with dd, then compare the results with Scalpel.

[Open the City Point flash-drive investigation]({{ 'workrole/msdisin/Grant-flashdrive.html' | relative_url }})

### Independent investigations

Examine the published material, recover deleted records, and report findings
supported by the evidence. Each page provides its own downloadable evidence image;
the collections contain PDFs and PNGs. These cases do not repeat the recovery walkthrough.

- [Cottingley: the beck photographs]({{ 'workrole/msdisin/Cottingley-investigation.html' | relative_url }})
- [The observatory dispatch]({{ 'workrole/msdisin/Lunar-dispatch-investigation.html' | relative_url }})
- [The international press circuit]({{ 'workrole/msdisin/Press-circuit-investigation.html' | relative_url }})
- [A disk and a laboratory]({{ 'workrole/msdisin/Disk-lead-investigation.html' | relative_url }}) — recovery case; non-graphic violent-crime records.
- [The payload archive]({{ 'workrole/msdisin/Flight-records-investigation.html' | relative_url }}) — recovery case.

---
# Practice and Explore      

### Situation 1: use the sed-key to alter the contents of the file to reveal a researchable event:    
 - sed-key:    
<span id="wget-httpsrawgithubusercontentcomjboyce1ppsctfmainclassesmsdisintrainingsedsearchsed-keytxt"></span>

<div class="terminal lesson-command" id="wget-httpsrawgithubusercontentcomjboyce1ppsctfmainworkrolemsdisinchallengessedsearchsed-keytxt"><pre><code>wget https://raw.githubusercontent.com/jboyce1/ppsCTF/main/workrole/msdisin/challenges/sedsearch/sed-key.txt</code></pre></div>

 - file to alter:    
<span id="wget-httpsrawgithubusercontentcomjboyce1ppsctfmainclassesmsdisintrainingsedsearchthe_worlds_greatest_military_spies_and_secret_service_agentstxt"></span>

<div class="terminal lesson-command" id="wget-httpsrawgithubusercontentcomjboyce1ppsctfmainworkrolemsdisinchallengessedsearchthe_worlds_greatest_military_spies_and_secret_service_agentstxt"><pre><code>wget https://raw.githubusercontent.com/jboyce1/ppsCTF/main/workrole/msdisin/challenges/sedsearch/The_Worlds_Greatest_Military_Spies_and_Secret_Service_Agents.txt</code></pre></div>

Apply the key to the downloaded text. `-f` reads the rules from the key file and `-n` suppresses the usual output. Rules that end in `p` print matching lines. The source file stays intact.

<div class="terminal lesson-command"><pre><code>sed -n -f sed-key.txt The_Worlds_Greatest_Military_Spies_and_Secret_Service_Agents.txt</code></pre></div>

Read the changed phrases together and research the historical event they point to. If the challenge supplies an encrypted ZIP and asks for the event year, enter the four-digit year at the password prompt. Replace `challenge.zip` with the supplied filename and quote filenames that contain spaces.

<div class="terminal lesson-command"><pre><code>unzip "challenge.zip"</code></pre></div>

    
### Situation 2: put the "altered words" in order, and use the first letter in each word to develop a code    
<span id="wget-httpsrawgithubusercontentcomjboyce1ppsctfmainclassesmsdisintrainingaltered_the_worlds_greatest_military_spies_and_secret_service_agentstxt"></span>

<div class="terminal lesson-command" id="wget-httpsrawgithubusercontentcomjboyce1ppsctfmainworkrolemsdisinchallengesaltered_the_worlds_greatest_military_spies_and_secret_service_agentstxt"><pre><code>wget https://raw.githubusercontent.com/jboyce1/ppsCTF/main/workrole/msdisin/challenges/Altered_The_Worlds_Greatest_Military_Spies_and_Secret_Service_Agents.txt</code></pre></div>

<span id="wget-httpsrawgithubusercontentcomjboyce1ppsctfmainclassesmsdisintrainingreplaced_wordstxt"></span>

<div class="terminal lesson-command" id="wget-httpsrawgithubusercontentcomjboyce1ppsctfmainworkrolemsdisinchallengesreplaced_wordstxt"><pre><code>wget https://raw.githubusercontent.com/jboyce1/ppsCTF/main/workrole/msdisin/challenges/replaced_words.txt</code></pre></div>

Count only the terms from the downloaded list. `-F` treats each entry as literal text, `-w` matches whole words, and `-o` prints just the match. A multiword term stays on one line.

<div class="terminal lesson-command"><pre><code>grep -o -w -F -f replaced_words.txt Altered_The_Worlds_Greatest_Military_Spies_and_Secret_Service_Agents.txt &gt; matches.txt</code></pre></div>

<div class="terminal lesson-command"><pre><code>sort matches.txt &gt; sorted-matches.txt</code></pre></div>

<div class="terminal lesson-command"><pre><code>uniq -c sorted-matches.txt &gt; term-counts.txt</code></pre></div>

<div class="terminal lesson-command"><pre><code>LC_ALL=C sort -k1,1nr -k2 term-counts.txt</code></pre></div>

Read the six terms from highest count to lowest, then take the first letter of each term. In this practice file, `189 agent` and `49 Lower Canada` give you `a` and `L`. The final sort uses the spelling of the term to break ties.

### Situation 3: find the most visited site in the mrboyce_traffic_history.db    
<span id="wget-httpsrawgithubusercontentcomjboyce1ppsctfmainclassesmsdisintrainingmrboyce_traffic_historydb"></span>

<div class="terminal lesson-command" id="wget-httpsrawgithubusercontentcomjboyce1ppsctfmainworkrolemsdisinchallengesmrboyce_traffic_historydb"><pre><code>wget https://raw.githubusercontent.com/jboyce1/ppsCTF/main/workrole/msdisin/challenges/mrboyce_traffic_history.db</code></pre></div>

    
### Situation 4: find the a spike in the traffic to a site in spykid_traffic_history.db
<span id="wget-httpsrawgithubusercontentcomjboyce1ppsctfmainclassesmsdisintrainingspykid_traffic_historydb-1"></span>

<div class="terminal lesson-command" id="wget-httpsrawgithubusercontentcomjboyce1ppsctfmainworkrolemsdisinchallengesspykid_traffic_historydb-1"><pre><code>wget https://raw.githubusercontent.com/jboyce1/ppsCTF/main/workrole/msdisin/challenges/spykid_traffic_history.db</code></pre></div>

<div style="text-align: center;">
  <img src="{{ 'workrole/msdisin/images/Ms_Disin Banner.jpg' | relative_url }}" alt="Ms_Disin Banner2" style="max-width: 80%; height: auto;">
</div>    
