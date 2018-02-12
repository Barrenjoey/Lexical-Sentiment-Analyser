# Lexical-Sentiment-Analyser
Analyses the sentiment of a body of text.

This script either extracts data from a database to be analysed, or from a chosen text file. 
It then extracts sentiment based on keywords which are determined by the user. Or it can simply
be used to determine the overall sentiment of a body of text without assigning the sentiment to
a keyword. Lastly, it returns the analysed data to a new database, which records instances of 
mentioned sentiment for that keyword, and displays the overall text sentiment within the console.
The script may be modified easily, such as changing between text files and database importation,
setting whether first and full-names will be added to flagged keywords, and also determining
whether keywords are automatically found by selecting the proper noun switch.

To use this script:
1. Have your body of text ready in either a .txt file or within a database.
2. Choose whether you are importing from .txt or database in the sentinal.p script.
3. If it's by text file, set the text file import location.
4. If it's database, configure to your own database needs.
5. Select whether you want names to be flagged in the keywords.
6. Select whether you want for proper nouns to automatically be flagged in keywords. ie locations, businesses, names etc.
7. Create your own line delimitted keyword list in a .txt file to search for the keywords you want.
8. Set the keyword list's location for importation.
9. Run the script.
10. Retrieve results from either the console or in a chosen database.

