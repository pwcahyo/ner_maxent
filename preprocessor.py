#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

from pymongo import MongoClient
from nltk.tokenize import sent_tokenize
from nltk import word_tokenize
import maxent as m
import stopwordremoval as s
import removetag as r
import dbmodel as d
import func as f


#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Bedakan data yang digunakan untuk training iis dan proses ner, karena prosesnya juga berbeda
# misal pada training IIS Yogyakarta/LOC masih tetap di pertahankan, 
# akan tetapi pada NER menjadi Yogyakarta LOC (atau dihilangkan simbol /)
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#create object class maxent
classify = m.Maxent()

#create object class stopword removal
stopword = s.StopwordRemoval()

#create object class remove tag
tag = r.RemoveTag()

#create object class independent function
func = f.Func()

#create object class database model
dbmodel = d.DBModel()

#--------------------------------------------------------------------------
# open hasil training iis
#--------------------------------------------------------------------------
classifier = func.open_file('iis.pickle')
#print classifier

# define month
month = "april"

# define month clean
month_data_tweet = month

# define month ner
month_data_clean = "%s_clean_unique"%month

# define date
#date = "03"


# --------------------------------------------------------------------------
# PREPROCESSING
# --------------------------------------------------------------------------
for date in range(1,32):
	if len(str(date)) == 1 :
		date = "0%s"%(str(date))
	cursor_get_data_tweet_without_label = dbmodel.get_data_without_label(month_data_tweet,str(date))
	print cursor_get_data_tweet_without_label
	#documents = cursor_get_data_tweet_without_label["result"]
	#print cursor_get_data_tweet_without_label


	for index, document in enumerate(cursor_get_data_tweet_without_label):
		datas = document["data"]
		#print datas
		#angka+=1
		#print angka
		for data in datas:
			#	print data["id"]
			#print data["text_tweet"]
			token_sentences = sent_tokenize(data["text_tweet"])
			for sentence in token_sentences:
				#clean tag. example : #, @, link internet
				sentence_clean_tag = tag.tag_removal(sentence.encode("utf8"), "ner")
				#clean stopword. example : yah, hlo 
				sentence_clean_stopword = stopword.stopword_removal(sentence_clean_tag, "ner")
				#finalisasi clean sentence
				sentence_clean = sentence_clean_stopword

				sentence_to_db = {}
				sentence_to_db["id"] = data["id"]
				sentence_to_db["url"] = data["url"]
				sentence_to_db["username"] = data["username"]
				sentence_to_db["text_tweet"] = sentence_clean
				sentence_to_db["time"] = data["time"]


				insert_sentence_clean = dbmodel.insert_sentence_clean(month_data_clean, str(date), sentence_to_db)
				print insert_sentence_clean


