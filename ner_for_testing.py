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
# classifier.show_most_informative_features()
# print classifier

month = "mar"

# define month clean
month_data_preprocessor = "%s_clean"%month

# define month ner
month_data_ner = "%s_ner_for_testing"%month

# sentences = "semoga bantuan fogging kejadian berkurang gt terlambat ditolong 3 penderita dbd meninggal"
# # sentences = "sebulan penderita dbd di kabupaten subang 200 orang"
# ner = classify.training_ner(sentences.encode("utf8"), classifier)
# print ner

# --------------------------------------------------------------------------
# NER
# --------------------------------------------------------------------------
for date_day in range(1,32):
	day = ""
	day_str = str(date_day)
	if len(day_str) == 1:
		day = "0"+day_str
	else:
		day = day_str

	cursor_get_data_preprocessor = dbmodel.get_data_preprocessor(month_data_preprocessor,day)
	#documents = cursor_get_data_preprocessor["result"]
	for document in cursor_get_data_preprocessor:
		data = document["data"]
		#print data
		for sentences in data :
			sentence = sentences["text_tweet"]
			if sentence :
				#print sentences["id"]
				ner = classify.training_ner(sentence.encode("utf8"), classifier)
				print sentences["id"]
				ner["id"] = sentences["id"]
				ner["url"] = sentences["url"]
				ner["username"] = sentences["username"]
				ner["text_tweet"] = ner["text_tweet"]
				ner["time"] = sentences["time"]

				cursor_insert_data = dbmodel.insert_ner_to_db(month_data_ner, day, ner)
				print cursor_insert_data