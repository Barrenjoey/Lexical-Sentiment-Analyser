'''
### Lexical Sentiment Analyser ###
'''
from nltk.tokenize import sent_tokenize, word_tokenize
import nltk
import re 
import csv
import sqlite3
import datetime

# SET to True if you prefer importing a text doccument rather than from a database.
text_file = True
text_location = "D:/Desktop/ExampleText.txt"

# SET to True if you want to flag for persons names from name list.
names = True
full_names = True

# SET proper nouns to True if you want the analyser to automatically add names/places/things to keyword list.
proper_noun = False

# Date
date = datetime.date.today()

# Sqlite database stuff
conn = sqlite3.connect('Sentiment_Analysis.db')
c = conn.cursor()

# Creating Main_DB table if it doesnt exist
def create_table():
	c.execute("CREATE TABLE IF NOT EXISTS Main_DB (id INTEGER PRIMARY KEY, topic TEXT, score INTEGER, article_date TEXT, translated_score TEXT, category TEXT, location TEXT, string_snippet TEXT, source TEXT, url TEXT, date_scraped TEXT, date_analysed TEXT)")
	
# Main data entry function to add topics to Main_DB
def data_entry():
	c.execute("INSERT INTO Main_DB (topic, score, article_date, translated_score, category, location, string_snippet, source, url, date_scraped, date_analysed) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (topic,upload_score,article_date,'translated','category',location,'string',source,url,date_scraped,date))
	conn.commit()
	
# Function to add analysed date to crawled_Data to show what has been analysed for future processing.
def date_analysed():
	c.execute("UPDATE Crawled_Data SET date_analysed=? WHERE url=?", (date,url))
	conn.commit()
	
# Selecting the data to be analysed from the Scraped/Crawled DB
def select_crawled_data():
	c.execute("SELECT * FROM Crawled_Data WHERE date_analysed IS NULL")
	data = c.fetchall()
	return data
	
# Looks to see if the url exists in the main DB, then deletes if a match.
def select_existing_url():
	c.execute("SELECT url FROM Crawled_Data")
	existing_url = c.fetchall()
	for cell in existing_url:
		cell = cell[0]
		if cell == url:
			delete_existing_url()
		else:
			pass

# Deletes matching url from database.			
def delete_existing_url():
	c.execute("SELECT * FROM Main_DB")
	dat = c.fetchall()
	c.execute("DELETE FROM Main_DB WHERE url=?", (url,))
	conn.commit()

# Creates database table if it doesn't exist.
create_table()

# Importing data for analysing. Default setting for database is date_analysed is null from crawled_Data.
if text_file:
	with open(text_location) as f:
		data = f.read()
		data = [data]
	print(data)
else:
	data = select_crawled_data()
	
# Importing list of keywords you want to scan. ie companys/names/products
with open("D:/Desktop/Code/Web Crawler/Keywords.txt") as k:
	keyword_list = k.readlines()
# Converting to lower case.	
keyword_list = [x.lower() for x in keyword_list]
# Stripping newline and whitespace	
keyword_list = [x.strip() for x in keyword_list]

# Importing list of peoples names
with open("D:/Desktop/Code/Web Crawler/All_names.txt") as name:
	name_list = name.readlines()
name_list = [x.lower() for x in name_list]	
name_list = [x.strip() for x in name_list]	

# Importing positive word list
with open("D:/Desktop/Code/Web Crawler/positive-words.txt") as p:
	positive_list = p.readlines()	
positive_list = [x.strip() for x in positive_list]

# Importing negative word list
with open("D:/Desktop/Code/Web Crawler/negative-words.txt") as n:
	negative_list = n.readlines()
negative_list = [x.strip() for x in negative_list] 

# Importing phrase list and values for scoring, convert to csv for delimiter, create list and make lower case.
with open("D:/Desktop/Code/Web Crawler/Phrase_scoring.txt") as phr:
	phrase_list = csv.reader(phr, delimiter = ",")
	phrase_list = list(phrase_list)
phrase_list = [[j.lower() for j in i] for i in phrase_list]

# Importing negation phrases.
with open("D:/Desktop/Code/Web Crawler/Phrase_negation.txt") as frase:
	frase_list = frase.readlines()
frase_list = [x.lower() for x in frase_list]	
frase_list = [x.strip() for x in frase_list]	

c.close()
conn.close()

