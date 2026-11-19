Spacerace Challenge README

Overview:
Your objective is to unlock password-protected files. The password for each file is derived from counting words in a specific text file and using those counts to form a phrase. Use command-line tools to analyze text files and derive passwords based on word frequencies.

Challenge Goal:
You must obtain a word count and determine the most frequently used words to assemble the password for each locked file. The password format is words connected by hyphens, like this: word1-word2-word3.

Hint for the Challenge:
Your hint for this challenge is: 50-85-84-111-339-75. Each number represents the word count of a specific word that will help form the password. Use the tools provided to identify the most common words corresponding to these counts. This only works with one of the files in the directory so it will take some guess and check. 

Tools and Commands:
1. Convert non-alphabet characters to new lines and change case:
   tr -cs 'A-Za-z' '\n' < input.txt | tr 'A-Z' 'a-z'
   This command replaces all non-alphabet characters with new lines and converts all uppercase letters to lowercase.

2. Sort words alphabetically:
   sort
   This sorts all the words alphabetically, necessary before counting unique words.

3. Count occurrences of each word:
   uniq -c
   After sorting, this counts each unique word's occurrences.

4. Sort words by frequency:
   sort -nr
   This sorts the words by their frequency in descending order.

5. Display the most common words:
   head -100
   This displays the top 100 most frequent words, aiding in identifying potential password components.

How to Proceed:
1. Analyze the Text: Run the commands in sequence on your text file to produce a list of the most common words.
2. Identify Key Words: Use the hint provided (50-85-84-111-339-75) to pick out the key words from your list.
3. Form the Password: Combine the identified words into a phrase with hyphens separating each word to unlock the file.

Tips for Success:
- Practice Command Line: Get comfortable with the command line, as it is crucial for accurately executing the given commands.

