README - Level 1: Using Diff to Find Flags

Overview:
In this challenge, you will use the 'diff' command to identify changes between two versions of a text file. Your goal is to locate flags hidden within the differences. These flags are formatted as 'pps{value_x_value_dif&cmp-code}', where 'code' is a string you will uncover.

The Challenge:
Two text files will be provided to you: an original and a modified version. The modified version contains exactly four alterations where each change includes a part of the flag. Your task is to use the 'diff' command to compare these files and find the differences that contain the flag components.

Understanding 'diff':
The 'diff' utility is used to compare files line by line. As you progress through this challenge, you will need to experiment with different flags that 'diff' offers to better view and understand these changes.

Key Flags for 'diff':
- '-u': Shows differences in a unified format, giving a few lines of context, which can be helpful for understanding where and how changes occur.
- '-c': Offers context for the changes, similar to '-u' but provides more lines around the changes.
- '--side-by-side': Displays the files next to each other for easier comparison of changes.
- '--ignore-case': Useful if changes might include variations in capitalization.
- '--ignore-all-space': Helps if changes involve spaces that you need to ignore to see more substantive text changes.

Your Task:
1. Analyze the text files using the 'diff' command with appropriate flags to highlight differences.
2. Identify the lines that have been changed and look for any patterns or strings that match the flag format.
3. Compile the parts of the flag from the changes you identify.

Tips for Success:
- Experiment with different 'diff' flags to see which presentations of the data help you spot changes most clearly.
- Be meticulous. Pay attention to small changes, as every character can be part of the flag.
- Remember, the flags are embedded in the text changes. Look for anything that resembles the flag format.

Do not rush through this process. Understanding how to effectively use 'diff' and its various flags will be crucial not only for finding the flags but also for your growth in handling file comparison tasks in many computing environments.

Support:
If you encounter difficulties, review this README again for hints on using the 'diff' command effectively or consider discussing strategies with peers or instructors. This challenge is designed to develop your analytical skills and command-line proficiency.

Remember, the goal is to learn and become proficient in these tools, so take your time and approach the challenge methodically.
