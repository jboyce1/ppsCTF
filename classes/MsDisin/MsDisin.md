---
layout: default
title: Ms. Disin
---

# Ms. Disin   

**Focus**: Text manipulation  
**Skill**: Use grep, sed, awk, diff, and sort to extract and manipulate text  
**Activity**: Discover the most   

<div style="text-align: center;">
  <img src="{{ 'classes/MsDisin/Ms_Disin Banner2.jpg' | relative_url }}" alt="Ms_Disin Banner2" style="max-width: 80%; height: auto;">
</div>    

## Sometimes the world can be a web of lies
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


### Things to experiment with on the range:     
Regex with grep: Mastering regular expressions to refine search criteria and pinpoint exact data sets.    
Stream editing with sed: Practice on-the-fly file content manipulations during competitive scenarios.    
Data manipulation with awk: Leverage awk's programming capabilities to analyze and report on data extracted during competitions.    

 
### How this skill can be used:  
Offensive Operations:
 - Data Extraction Tactics: Utilize combinations of grep, awk, and sed to extract sensitive information from opponent’s files, which could range from passwords to strategic plans.
 - Script Manipulation: Through direct file editing using sed and cat, alter scripts or configurations in the enemy's network to disrupt their operations or misdirect their strategies.

Defensive Operations:
 - File Integrity Checks: Use grep and awk to monitor files for unauthorized changes that could indicate infiltration attempts.
 - Rapid Response Editing: Employ sed to quickly revert any unauthorized changes or to patch vulnerabilities in script configurations during live competitions.

 


---
## Use cat to combine multiple text files and display their contents quickly
### “cat” the cat and “grep” the dog (because who names a cat?)

<div style="text-align: center;">
  <img src="{{ 'classes/MsDisin/msdisins_dog.webp' | relative_url }}" alt="Hash Hound Logo" style="max-width: 80%; height: auto;">
</div>

Start a Kali machine    
Level 1:    
On Kali    
Download the cat observations   
Unzip the contents of the folder.    
Open a terminal inside the cat_observations folder    
use the cat command to read each passage    
cat cat_1    
(hint: use the up arrow key and backspace to quickly advance in the journal  

Level 2:    
On Kali

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
Write a synopsis of what you think is happening here    

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
