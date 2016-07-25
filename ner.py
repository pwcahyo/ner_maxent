#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

from pymongo import MongoClient
from nltk.tokenize import sent_tokenize
import pickle
import maxent as m
import stopwordremoval as s
import removetag as r
import regexp as regx


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

#==========================================================================
# NER
#==========================================================================
# Preprocessing NER
#--------------------------------------------------------------------------
#sentence = "#kicauHealth di Yogyakarta tiga puluh orang penderita dbd meninggal. Penelitian RSPAD Buka Peluang 'Kalahkan' dbd bit.ly/1KuKsxO"
#sentence = "2 minggu jatuh sakit kena dbd,minggu ke 3 ﺍَﻟْﺤَﻤْﺪُﻟِﻠّﻪِ sembuh,giliran mamah yang sakit,udah satu minggu blm... fb.me/3Wnh4xm5e"
"""
sentences = "Selamat hari brozolnya @IniDentha semoga makin segalagalanya,e&;nya gak ilang y,panjang buntut ongkoh pokona HBD DBD XTC BRZ UGD TOD GBS★!!!"
token_sentences = sent_tokenize(sentences)
for sentence in token_sentences:
	#print sentence
	#clean tag. example : #, @, link internet
	sentence_clean_tag = tag.tag_removal(sentence, "ner")
	#clean stopword. example : yah, hlo 
	sentence_clean_stopword = stopword.stopword_removal(sentence_clean_tag, "ner")
	#finalisasi clean sentence
	sentence_clean = sentence_clean_stopword
	#print sentence_clean_tag

	print sentence_clean
	#--------------------------------------------------------------------------
	# Proses NER
	#--------------------------------------------------------------------------

	#--------------------------------------------------------------------------
	# open hasil training iis
	#--------------------------------------------------------------------------
	f = open('iis.pickle', 'rb')
	classifier = pickle.load(f)
	f.close()


	ner = classify.training_ner(sentence_clean, classifier)
	print ner
"""


#--------------------------------------------------------------------------
# PROSES LOAD DATA FROM MONGODB
#--------------------------------------------------------------------------

client = MongoClient()
db = client.maret


#--------------------------------------------------------------------------
# open hasil training iis
#--------------------------------------------------------------------------
f = open('iis.pickle', 'rb')
classifier = pickle.load(f)
f.close()

cursor = db["02"].aggregate(
    [
        {"$group": 
        	{"_id": "$url", 
		        "data": {
		        	"$push":{
			                "id":"$url", 
			                "url":"$data_id", 
			                "username":"$username", 
			                "text_tweet":"$text_tweet",
			                "time":"$time_tweet"
		                	}
		            	}	
	    		}
        } 
    ]
)

documents = cursor["result"]

angka = 0

for index, document in enumerate(documents):
	datas = document["data"]
	angka+=1
	print angka
	for data in datas:
		print data["id"]
		token_sentences = sent_tokenize(data["text_tweet"])
		for sentence in token_sentences:
			#print sentence
			#clean tag. example : #, @, link internet
			sentence_clean_tag = tag.tag_removal(sentence.encode("utf8"), "ner")
			#clean stopword. example : yah, hlo 
			sentence_clean_stopword = stopword.stopword_removal(sentence_clean_tag, "ner")
			#finalisasi clean sentence
			sentence_clean = sentence_clean_stopword

			#print sentence_clean
			#--------------------------------------------------------------------------
			# Proses NER
			#--------------------------------------------------------------------------

			ner = classify.training_ner(sentence_clean, classifier)
			print ner