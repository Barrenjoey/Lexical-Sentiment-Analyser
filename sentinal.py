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

c.close()
conn.close()

