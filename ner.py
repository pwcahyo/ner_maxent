#!/usr/bin/python

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
sentence = "#kicauHealth di Yogyakarta tiga puluh orang penderita dbd meninggal. Penelitian RSPAD Buka Peluang 'Kalahkan' dbd bit.ly/1KuKsxO"
#sentence = "di yogyakarta lima orang terkena dbd"
#clean tag. example : #, @, link internet
sentence_clean_tag = tag.tag_removal(sentence, "ner")
#clean stopword. example : yah, hlo 
sentence_clean_stopword = stopword.stopword_removal(sentence_clean_tag, "ner")
#finalisasi clean sentence
sentence_clean = sentence_clean_stopword
#print sentence_clean
#--------------------------------------------------------------------------
# Proses NER
#--------------------------------------------------------------------------
f = open('iis.pickle', 'rb')
classifier = pickle.load(f)
f.close()
print classify.training_ner(sentence_clean, classifier)
#--------------------------------------------------------------------------