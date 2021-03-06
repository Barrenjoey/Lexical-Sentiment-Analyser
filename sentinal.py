'''
### Lexical Sentiment Analyser ###
This script either extracts data from a database to be analysed, or from a chosen text file. 
It then extracts sentiment based on keywords which are determined by the user. Or it can simply
be used to determine the overall sentiment of a body of text without assigning the sentiment to
a keyword. Lastly, it returns the analysed data to a new database, which records instances of 
mentioned sentiment for that keyword, and displays the overall text sentiment within the console.
The script may be modified easily, such as changing between text files and database importation,
setting whether first and full-names will be added to flagged keywords, and also determining
whether keywords are automatically found by selecting the proper noun switch.
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

# Negation words - Negation reverses the polarity of a positive or negative word. ie: not good.
NEGATION = r"""
    (
       never|no\s|nothing|nowhere|noone|none|not\s|
       havent|hasnt|hadnt|cant|couldnt|shouldnt|
       wont|wouldnt|dont|doesnt|didnt|isnt|arent|aint|n't
	)"""
NEGATION_RE = re.compile(NEGATION, re.VERBOSE)

# Declaring variables
keywords = []
keyword_linger = []
positives = []
negatives = []
key_sides = ""
key_sides3 = ""
key_sides4 = ""
key_sides5 = ""
score = 0
total_score = 0
scoreDict = {}
nouns = []
full_name = []
fuller_name = []
nameDict = {}
single_name = ""
single_names = []
negate_counter = 0
frase_counter = 0
counter = 0

# Main loop of data entries
for link in data[0:]:
	counter += 1
	# Extracting wanted data from crawled DB. Modify to suit your own database.
	if text_file:
		sentiment_text = data[0]
	else:
		url = link[0]
		article_date = link[1]
		source = link[2]
		location = link[3]
		date_scraped = link[6]
		sentiment_text = link[5]

	# Converting to lower case	
	sentiment_text = sentiment_text.lower()
	# Adding spaces after full stops to filter sentences correctly.
	sentiment_text = re.sub(r'\.', '. ', sentiment_text)
	
	# Tokenizing
	word_text = word_tokenize(sentiment_text)		#Word Tokenize
	sent_text = sent_tokenize(sentiment_text)		#Sentence Tokenize

	# Looping through sentences to analyse each sentence.
	for sent in sent_text:	
		print(sent)
		# Word tokenize for 1 sentence
		single_sent = word_tokenize(sent)
		# Part of Speech tags		
		tagged = nltk.pos_tag(single_sent)	
		# Compiling re negation
		negate = re.findall(NEGATION_RE, sent) 	

		# Looping through each word in sentence
		for key in single_sent:	
		# Flagging whether keyword is encountered and adding to list.
			if key in keyword_list:
				keywords.append(key)
		# This allows for multiword keywords, up to 5 words in length.
			key_sides += " " + key		#2 word keywords
			key_sides3 += " " + key		#3 
			key_sides4 += " " + key		#4
			key_sides5 += " " + key		#5 
		# Appening to list if multiword keyword in sentence.	
			if key_sides in keyword_list:
				keywords.append(key_sides)
			elif key_sides3 in keyword_list:
				keywords.append(key_sides3)
			elif key_sides4 in keyword_list:
				keywords.append(key_sides4)
			elif key_sides5 in keyword_list:
				keywords.append(key_sides5)
		# Shifting words to the right for next loop.				
			key_sides5 = key_sides4
			key_sides4 = key_sides3
			key_sides3 = key_sides	
			key_sides = key
	
	# Searching for Noun phrases to add to keywords list	
		for word,pos in tagged:
			if proper_noun:
				if (pos == 'NNP' and word != 'My' and word not in keywords):
					keywords.append(word)
			
	# People Names - Adding firstname to keywords. Also adds name and last name together then adds to keywords if successful.
			if names:
				if word in name_list:
					full_name.append(word)
					keywords.append(word)	
			if full_names:		
				if len(full_name) > 0:
					if pos == 'NN':
						full_name.append(word)
						if len(full_name) == 2:
							single_name = full_name[1]
							full_name = full_name[0] + " " + full_name[1]
							keywords.append(full_name)
							nameDict[single_name] = full_name
							fuller_name = full_name
							full_name = []
					else:
						full_name = []
		
	# Searching for positive words
		for pos in single_sent:
			if pos in positive_list:
				positives.append(pos)
				score += 1
	# Searching for negative words
		for neg in single_sent:
			if neg in negative_list:
				negatives.append(neg)
				score += -1	
				
	# like negation		
		for wrd,ps in tagged:
			if (ps == 'IN' and wrd == 'like'):
				print('like NEGATION!!!!')
				score += -1			

	# Adding space to no and not to match negation list			
			if wrd == "not" or wrd == "no":
				wrd = wrd + " "	

	# Searching for negating words and turning their polarity by score. Positional counting system for assigning negation.		
			if wrd in negate or negate_counter >= 1:
				negate_counter += 1
				if wrd in positives:
					score += -2
					negate_counter = 0
				elif wrd in negatives:
					score += 2
					negate_counter = 0
				elif negate_counter >= 6 or wrd == '.':
					negate_counter = 0	
					
	# Phrase scoring. Searching for phrase and then scoring by assigned value. ie. 'expected more' -1 
		for phrases in phrase_list:
			find_phrase = re.findall(phrases[0],sent)
			if len(find_phrase) >= 1:
				score += int(phrases[1])

	# Phrase negation. Negating phrases and turning polarity. ie. 'could have' been better -1 		
		for frase in frase_list:		
			find_frase = re.findall(frase,sent)	
			if len(find_frase) >= 1:
				find_frase = word_tokenize(find_frase[0])
				for werd in single_sent:
					if werd in find_frase:
						frase_counter += 1
					if frase_counter == len(find_frase):
						if werd in positives:
							print('Phrase_negative: ',frase)
							score += -2
							frase_counter = 0
						elif wrd in negatives:
							print('Phrase_positive: ',find_phrase)
							score += 2
							frase_counter = 0
						elif frase_counter >= 3 or werd == '.':
							frase_counter = 0
								
	# Adding the keyword and score to a dictionary. Checking if keyword in dict, if so it adds the scores, else it creates new entry.		
		for k in keywords:
			if k in scoreDict:
				y = scoreDict.get(k)
				scoreDict[k] = y + score
			else:	
				scoreDict[k] = score
			
	# Scoring single word names to match with full name. Only does this if full name is not in sentence as well.				
		if names and full_names:
			for word in single_sent:		
				if word in nameDict:
					if len(fuller_name) == 0:
						single_names.append(word)
						z = nameDict.get(word)
						try:
							s = scoreDict.get(z)
							scoreDict[z] = s + score
						except Exception as e:	
							print("Error updating score from single name with full name" + str(e))	
						
	# Assigning pos/neg words to previous sentence keyword		
		if score != 0 and len(keywords) == 0 and len(scoreDict) != 0:
			for l in keyword_linger:
				x = scoreDict.get(l)
				scoreDict[l] = score + x
				
	# Printing desired sentence info for console viewing
		print("Sentence score: ",score)
		print ("Positive Words: ",positives)
		print ("Negative Words: ",negatives)
		print("Keywords: ",keywords)
		print()
		
	# Resetting active variables for next sentence.	
		keyword_linger = keywords
		keywords = []
		total_score = total_score + score
		score = 0
		positives = []
		negatives = []
		negate = []
		single_names = []
		fuller_name = []
		
	# Printing desired combined info for the whole of the text.
	print(scoreDict)
	print("Total Score: ",total_score)
	print(counter)

	# Data entry - Uploading analysed data to a database table if desired.
	if not text_file:
		date_analysed()
		select_existing_url()
		for topic in scoreDict:
			upload_score = scoreDict[topic]
			data_entry()
			
	# Resetting text wide variables for next text.		
	scoreDict = {}
	total_score = 0	
	nameDict = {}
	print("#" * 40)
	print("\n")

# Closing database connection.
c.close()
conn.close()

