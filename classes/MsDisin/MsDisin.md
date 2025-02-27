---
layout: default
title: Ms. Disin
---

# Ms. Disin   

**Focus**: Text manipulation  
**Skill**: Use grep, sed, awk, diff, xxd and sort to extract and manipulate text and data  
**Activity**: Extract and manipulate files that are text based   

<div style="text-align: center;">
  <img src="{{ 'classes/MsDisin/Ms_Disin Banner2.jpg' | relative_url }}" alt="Ms_Disin Banner2" style="max-width: 80%; height: auto;">
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
## Use cat to combine multiple text files and display their contents quickly
### “cat” the cat and “grep” the dog (because who names a cat?)

<div style="text-align: center;">
  <img src="{{ 'classes/MsDisin/msdisins_dog.webp' | relative_url }}" alt="Hash Hound Logo" style="max-width: 80%; height: auto;">
</div>

Start a Kali machine    
**Step 1:**      
Download the cat observations     
#### `wget https://github.com/jboyce1/ppsCTF/raw/main/classes/MsDisin/cat_observations.zip`    
Unzip the contents of the folder.    
Open a terminal inside the cat_observations folder    
use the cat command to read each passage    
cat cat_1    
(hint: use the up arrow key and backspace to quickly advance in the journal)    
    
**Step 2:**    
From  inside the cat_observations folder, open a terminal    
To display all of the text in the files:    
#### `find . -type f -exec cat {} +`    
To display all of the text in the files with their file names in order and get really fancy?:    
#### `find . -type f -name "*" | sort | xargs cat`    
Explaination of flags:    
 -  `find . -type f -name "*."`  Search for all files with an extension in the current directory (.) and its subdirectories.    
 - `| sort` pipes the output to sort in order to list of filenames alphabetically.    
 - `| xargs cat`  Pass the sorted list of filenames to the cat command to display their contents in order.   

<div style="text-align: center;">
  <img src="{{ 'classes/MsDisin/msdisins_cat.webp' | relative_url }}" alt="Hash Hound Logo" style="max-width: 80%; height: auto;">
</div>    

### Try it now    
use the dog_oberservations.zip to do the same thing  
#### `wget https://github.com/jboyce1/ppsCTF/raw/main/classes/MsDisin/dog_observations.zip`    
Write a synopsis of what you think is happening <a href="https://forms.office.com/Pages/ResponsePage.aspx?id=mhxxjxzsu023kLsMdxsdzM6J33C5yQRJgc1SHWy_64dUOFYxN1JKSUExN09WVzY3VzE0WFU1VU1IUC4u" target="_blank">here</a>  

<div style="text-align: center;">
<iframe width="560" height="315" src="https://www.youtube.com/embed/jmTVwNt24Sk?si=6UXLuTWlRTuxneLB" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</div>
--- 

## Part 2: 

### Use grep to find specific instances of strings    
### Use grep and awk to find locations of strings within a text    
### Use sed to change all instances of a string to another string    
### Combine awk and sed to identify instances of a string and change them    
### Use grep and wc to count how many instances of a string are in a text    
### Use diff to determine the differences between two files    
### Use diff to determine the differences between two directories    


<div style="text-align: center;">
  <img src="{{ 'classes/MsDisin/worldsgreatestspies_cover.jpg' | relative_url }}" alt="worldsgreatestspies_cover" style="max-width: 80%; height: auto;">
</div>  

get the file:
#### `wget https://github.com/jboyce1/ppsCTF/raw/main/classes/MsDisin/The_Worlds_Greatest_Military_Spies_and_Secret_Service_Agents.txt`

### grep overview:     
grep searches for items and returns the entire line that contains the item    

To search non-case sensitive:    
#### `grep -i  "napoleon" file.txt`      
    
To search recursively (all files) in directories:    
#### `grep -r "Napoleon" /path/to/directory/    
    
To get the file names that contain an item:    
#### `grep -l "Napoleon" *.txt`    
    
To include the file names that contain an item:    
#### `grep -H "Napoleon" *.txt`     
    
To invert the search and search of lines that do not contain the item:        
#### `grep -v "Napoleon" file.txt`    
    
To count the matches:    
#### `grep -c "Napoleon" file.txt`    
    
To see the lines before and after, use -B and -A      
#### `grep -B 2 "Napoleon" file.txt`    
#### `grep -A 2 "Napoleon" file.txt`    
    
To highlight matches in the text    
#### `grep --color=auto "Napoleon" file.txt`    


### awk overview:
General pattern: awk 'pattern {action}' file    
 - pattern: The condition you want to match (optional).    
 - action: The operation to perform on the matched lines (optional).    
- file: The file you're processing.    

Use similar to grep
#### `awk '/Prince of Spies/' The_Worlds_Greatest_Military_Spies_and_Secret_Service_Agents.txt`    
 - similar to grep

Add conditional logical controls    
#### `awk '/Belle Boyd/ && /1917/' The_Worlds_Greatest_Military_Spies_and_Secret_Service_Agents.txt`    
 - find lines containing "Belle Boyd" and  "1917"

The an example of more powerful application of awk 
#### `awk '/The Battle of/,/Confederate/ { if (index($0, "Belle Boyd") > 0) print $0 }' The_Worlds_Greatest_Military_Spies_and_Secret_Service_Agents.txt`
 - `/The Battle of/,/Confederate/` is an awk range pattern. It tells awk to start processing lines when it encounters a line containing "The Battle of", and stop processing once it encounters a line containing "Confederate".
So, awk will process all lines in between these two patterns.    
 - `{ if (index($0, "Belle Boyd") > 0) print $0 }:`
 - `$0`: This refers to the entire current line in awk.
`index($0, "Belle Boyd")`: The `index()` function returns the position of the first occurrence of "Belle Boyd" in the current line. If "Belle Boyd" is found, it returns a position (a number greater than 0), otherwise it returns 0.
 - `if (index($0, "Belle Boyd") > 0)`: This checks if "Belle Boyd" exists in the line (i.e., the position is greater than 0).
print $0: If "Belle Boyd" is found, the entire line is printed.


Find out who:
Use grep to find the name of the person who was called the "Prince of Spies".    
**`grep -i "Prince of Spies" The_Worlds_Greatest_Military_Spies_and_Secret_Service_Agents.txt`**    
    
When did:    
Use grep to discover when the book "The World's Greatest Military Spies and Secret Service Agents" was first published.    
**`grep -i "first impression" The_Worlds_Greatest_Military_Spies_and_Secret_Service_Agents.txt`**    
    
Where did:    
Use grep and awk to find the location where "Belle Boyd" saved Stonewall Jackson.    
**`grep -i "Belle Boyd" The_Worlds_Greatest_Military_Spies_and_Secret_Service_Agents.txt | awk '{print $0}'`**    
    
What event:    
Use grep to identify the event described as "the capture of Major André".    
**`grep -i "Major André" The_Worlds_Greatest_Military_Spies_and_Secret_Service_Agents.txt`**    
    
Manipulate names:        
Use sed to change all instances of "Napoleon" to "Roger Rabbit"      
**`sed -i 's/Napoleon/Roger Rabbit/g' The_Worlds_Greatest_Military_Spies_and_Secret_Service_Agents.txt`**   
    
Alter dates:    
Use sed to change all instances of the year "1917" to "1947".    
**`sed -i 's/1917/1947/g' The_Worlds_Greatest_Military_Spies_and_Secret_Service_Agents.txt`**    
    
Combine awk and sed:    
Use awk to find lines containing "King Philip" and then sed to change "King Philip" to "King Roger".    
**`awk '/King Philip/' The_Worlds_Greatest_Military_Spies_and_Secret_Service_Agents.txt | sed 's/King Philip/King Roger/g'`**   
    
 Extracting sentences:    
Use grep to extract sentences that mention "Confederate spy"    
**`grep -i "Confederate spy" The_Worlds_Greatest_Military_Spies_and_Secret_Service_Agents.txt`**    
    
Count occurrences:    
Use grep and wc to count how many times the word "secret" appears in the text.    
**`grep -o -i "secret" The_Worlds_Greatest_Military_Spies_and_Secret_Service_Agents.txt | wc -l`**    
    
Spot the Differences:    
Use diff to extract what has changed in the two files line by line    
**`diff -y original_file.txt modified_file.txt`**     
or    
**`diff -u original_file.txt modified_file.txt`**    
or for directories:    
**`diff -r original_directory modified_directory`**    
    
Finally, display the top 100 most common words.    
Here's how you can get the 100 most common words in a text file directly in the terminal:    
#### `tr -cs 'A-Za-z' '\n' < input.txt | tr 'A-Z' 'a-z' | sort | uniq -c | sort -nr | head -100`    
    
Explanation of Each Command:    
 - **`tr -cs 'A-Za-z' '\n'`**: This translates all sequences of characters that are not alphabets into newlines, effectively putting each word on a new line.      
 - **`tr 'A-Z' 'a-z'`**: This converts all uppercase letters to lowercase.    
 - **`sort`**: This sorts the words alphabetically, which is necessary for uniq to count all occurrences properly.    
 - **`uniq -c`**: This counts the number of occurrences of each word. The words need to be sorted as uniq only matches consecutive duplicate lines.    
 - **`sort -nr`**: This sorts the list numerically in reverse order, placing the most frequent words at the top.    
 - **`head -100`**: This displays only the top 100 results.    
    
Or add in awk capabilities to filter out small words    
#### `tr -cs 'A-Za-z' '\n' < input.txt | tr 'A-Z' 'a-z' | awk 'length($0) > 3' | sort | uniq -c | sort -nr | head -100`    
    
--- 
### Use xxd to compare the hexidecimal difference between files    
    
#### `xxd original.txt > original.hex`    
#### `xxd modified.txt > modified.hex`    
#### `diff -u original.hex modified.hex`    

<div style="text-align: center;">
  <img src="{{ 'classes/MsDisin/xxd_screenshot.png' | relative_url }}" alt="worldsgreatestspies_cover" style="max-width: 80%; height: auto;">
</div>  

---
## Part 3
### Use sqlite to query web browser history
    
### Determine the visited sites in the database
Navigate the the directory with the .db file in it

In terminal, open sqlite
#### `sqlite3 whatever_the_traffic_database_is_called.db`

Verify database is open and you are able to access the tables    
#### `.tables`    
 - you should see something like browsing_history
Inspect the stucture of the tables    
#### `PRAGMA table_info(browsing_history);`
  - commands will execute once they end with a semi-colon `;`

Test a basic query from the browsing_history table    
#### `SELECT * FROM browsing_history LIMIT 10;`    

Quit out of the sqlite3    
#### `.quit`

Query the most visited sites:
```
sqlite> select url, COUNT(*) as visit_count
   ...> FROM browsing_history
   ...> GROUP BY url
   ...> ORDER BY visit_count DESC
   ...> LIMIT 100;
```

### Identify and determine spikes in web traffic

Download the sample database
#### `wget https://raw.githubusercontent.com/jboyce1/ppsCTF/main/classes/MsDisin/training/spy_traffic_history.db`

Open the database
#### `sqlite3 spy_traffic_history.db`

Look for spikes in activity that seem excessively high or low on a weekly basis
```
SELECT strftime('%Y-%W', timestamp) AS week, COUNT(*) AS visit_count
FROM browsing_history
GROUP BY week
ORDER BY week ASC;
```
Here the number 94 stands out
<div style="text-align: center;">
  <img src="{{ 'classes/MsDisin/high_activity_in_method1.png' | relative_url }}" alt="worldsgreatestspies_cover" style="max-width: 80%; height: auto;">
</div>  


Look find the average web traffic and the highest web traffic
```
SELECT AVG(visit_count) AS avg_visits, MAX(visit_count) AS max_visits
FROM (
    SELECT strftime('%Y-%W', timestamp) AS week, COUNT(*) AS visit_count
    FROM browsing_history
    GROUP BY week
);
```
Here we see the average of 37.03 with a max of 94
<div style="text-align: center;">
  <img src="{{ 'classes/MsDisin/screenshot-avg-visit-most-visit.png' | relative_url }}" alt="worldsgreatestspies_cover" style="max-width: 80%; height: auto;">
</div>  

Find traffic that is above or below the average visits by a certain threshold
```
WITH weekly_traffic AS (
    SELECT strftime('%Y-%W', timestamp) AS week, COUNT(*) AS visit_count
    FROM browsing_history
    GROUP BY week
),
stats AS (
    SELECT AVG(visit_count) AS avg_visits FROM weekly_traffic
)
SELECT wt.week, wt.visit_count
FROM weekly_traffic wt, stats s
WHERE wt.visit_count > s.avg_visits * 1.5
ORDER BY wt.visit_count DESC;
```
You can ajust the `WHERE wt.visit_count > s.avg_visits * 1.5` to define your own thresholds
Here we see the week of high activity was 2025-00
<div style="text-align: center;">
  <img src="{{ 'classes/MsDisin/above_average_browser_activity.png' | relative_url }}" alt="worldsgreatestspies_cover" style="max-width: 80%; height: auto;">
</div>  

Investigate specific weeks by getting a count of the sites visited during that week
```
SELECT url, COUNT(*) AS visit_count
FROM browsing_history
WHERE strftime('%Y-%W', timestamp) = '2025-00'
GROUP BY url
ORDER BY visit_count DESC
LIMIT 5;
```
Here we can see the url that was suspicous
<div style="text-align: center;">
  <img src="{{ 'classes/MsDisin/investigate_week_by_traffic.png' | relative_url }}" alt="worldsgreatestspies_cover" style="max-width: 80%; height: auto;">
</div>  
---
## Training links:

#### `wget https://raw.githubusercontent.com/jboyce1/ppsCTF/main/classes/MsDisin/training/Altered_The_Worlds_Greatest_Military_Spies_and_Secret_Service_Agents.txt`

#### `wget https://raw.githubusercontent.com/jboyce1/ppsCTF/main/classes/MsDisin/training/The_Worlds_Greatest_Military_Spies_and_Secret_Service_Agents_modified.txt`

#### `wget https://raw.githubusercontent.com/jboyce1/ppsCTF/main/classes/MsDisin/training/replaced_words.txt`

#### `wget https://raw.githubusercontent.com/jboyce1/ppsCTF/main/classes/MsDisin/training/mrboyce_traffic_history.db`

<div style="text-align: center;">
  <img src="{{ 'classes/MsDisin/Ms_Disin Banner.jpg' | relative_url }}" alt="Ms_Disin Banner2" style="max-width: 80%; height: auto;">
</div>    
