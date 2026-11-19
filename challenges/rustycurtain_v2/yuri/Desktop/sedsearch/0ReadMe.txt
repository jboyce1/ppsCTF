OPERATION IRON CURTAIN

OBJECTIVE  
You have captured a sed key and a set of historical texts suspected to contain altered information. The adversary is attempting to rewrite history by embedding misinformation into existing literature.

Your goal is to:  
1. Use sed to process the altered document and extract a hint.  
2. Identify the historical event that the hint refers to.  
3. Use the year of the event as the password to unlock a note to my comrades.zip.  
4. Extract the flag inside the zip file.

FILES PROVIDED  
- various books → The altered document containing the hidden hint.  
- sed-key → The key to reveal the hidden hint using sed.  
- a note to my comrades.zip → A locked file containing the final flag.

STEPS TO SOLVE  

Step 1: Use sed to Extract the Hidden Hint  
Run the following command to apply the sed transformations to the altered document:  

sed -n -f "string 1|string 2| more strings" text-to-be-changed.txt
OR
sed -n -f sedfile.txt text-to-be-changed.txt

This will print a phrase that hints at a historical event.  

Step 2: Identify the Historical Event  
- Research the phrase extracted from the text.  
- Determine the year when the event happened.  
- The year will be the password for the locked zip file.  

Step 3: Unlock a note to my comrades.zip  
Once you have identified the correct year, use it to unlock the zip file:  

7z x "a note to my comrades.zip"  

When prompted for a password, enter the 4-digit year.  

If the password is correct, the final flag will be inside.  

Everything you need is in the provided files. Start investigating.  
