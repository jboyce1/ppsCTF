CTF Challenge: Operation Iron Curtain - The Frequency Puzzle

A misinformation group has manipulated a historical document by replacing words with propaganda terms.
To uncover the truth, **you must find the most frequently repeated altered words**.

### What You Need to Do:
1. **Find which words appear most frequently in the altered document.**
2. **Extract the first letter of each of the top 6 words.**
3. **Rearrange them in order of frequency to form the missing part of the flag.**

### Two Ways to Solve It:

#Step by Step:
tr -cs 'A-Za-z' '
' < input.txt > step1.txt      # Step 1: Extract words, replace non-alphabet chars with newlines
tr 'A-Z' 'a-z' < step1.txt > step2.txt             # Step 2: Convert all letters to lowercase
sort < step2.txt > step2_sorted.txt                # Step 3: Sort words (needed before counting)
uniq -c step2_sorted.txt > step3.txt               # Step 4: Count occurrences
sort -nr step3.txt > step4.txt                     # Step 5: Sort by frequency in descending order


#### **Using Code Analysis:**
Run the following command to extract the top altered words:
```
grep -o -w -f replaced_words.txt document_to_search.txt > step1.txt      # Step 1: Search for specific strings in the document and save the matches
sort step1.txt > step2_sorted.txt                                          # Step 2: Sort the matched strings alphabetically
uniq -c step2_sorted.txt > step3.txt                                       # Step 3: Count occurrences of each unique match
sort -nr step3.txt > step4_sorted.txt                                      # Step 4: Sort by frequency in descending order
awk '{print $2}' step4_sorted.txt > step5_strings.txt                      # Step 5: Extract the strings without the counts
head -6 step5_strings.txt > step6_top6.txt                                 # Step 6: Extract the top 6 most frequent strings
cut -c1 step6_top6.txt > step7_first_chars.txt                             # Step 7: Extract the first character of each string
tr -d '\n' < step7_first_chars.txt                                         # Step 8: Remove newlines to create a single string

grep -o -w -E "string_one|string_two|string_three" document_to_search.txt | sort | uniq -c | sort -nr | awk '{print $2}' | head -6 | cut -c1 | tr -d '
'
```


#### **Using `replaced_words.txt`:**
```
grep -o -w -f replaced_words.txt document_to_search.txt | sort | uniq -c | sort -nr | awk '{print $2}' | head -6 | cut -c1 | tr -d '
'
```


### Example Steps:
1. Run the appropriate command.
2. Take the first letter of each of the top 6 most frequent altered words.
3. Construct the missing flag part.


