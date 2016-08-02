#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

from pymongo import MongoClient
from nltk.tokenize import sent_tokenize
from nltk import word_tokenize
import maxent as m
import stopwordremoval as s
import removetag as r
import regexp as regx
import dbmodel as d
import func as f


#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Bedakan data yang digunakan untuk training iis dan proses ner, karena prosesnya juga berbeda
# misal pada training IIS Yogyakarta/LOC masih tetap di pertahankan, 
# akan tetapi pada NER menjadi Yogyakarta LOC (atau dihilangkan simbol /)
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#create object class maxent
classify = m.Maxent()

#create object class independent function
func = f.Func()

#create object class database model
dbmodel = d.DBModel()

#--------------------------------------------------------------------------
# open hasil training iis
#--------------------------------------------------------------------------
classifier = func.open_file('iis.pickle')
#print classifier

month = "maret"

# define month clean
month_data_preprocessor = "%s_clean"%month

# define month ner
month_data_ner = "%s_ner"%month


# define date
date = "04"

# --------------------------------------------------------------------------
# NER
# --------------------------------------------------------------------------
cursor_get_data_preprocessor = dbmodel.get_data_preprocessor(month_data_preprocessor,date)
documents = cursor_get_data_preprocessor["result"]
for document in documents:
	data = document["data"]
	for sentences in data :
		sentence = sentences["text_tweet"]
		if sentence :
			ner = classify.training_ner(sentence.encode("utf8"), classifier)
			# apabila array ner tidak kosong dan berisikan entitas NUM dan LOC maka jalankan statement berikut
			if ner and ("NUM" in ner["entity"] and "LOC" in ner["entity"]):
				#print sentences["id"]
				ner["id"] = sentences["id"]
				ner["url"] = sentences["url"]
				ner["username"] = sentences["username"]
				ner["time"] = sentences["time"]

				cursor_insert_data = dbmodel.insert_ner_to_db(month_data_ner, date, ner)
				print cursor_insert_data