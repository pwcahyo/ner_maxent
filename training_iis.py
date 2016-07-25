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
# PELATIHAN IIS
#==========================================================================
paragraph = []
paragraph.append("di tegal/LOC empat puluh lima/NUM orang menderita/CON dbd. empat puluh satu/NUM meninggal/CON tiga puluh/NUM orang dirawat")
paragraph.append("di malang/LOC 4/NUM orang menderita/CON dbd")
paragraph.append("10/NUM orang mati/CON karena dbd di bantul/LOC @macanbantul")
paragraph.append("warga sleman/LOC 4/NUM orang menderita/CON dbd")
paragraph.append("cirebon/LOC meninggal/CON karena dbd")
paragraph.append("jakarta/LOC meninggal/CON karena dbd")
paragraph.append("empat/NUM warga bandung/LOC meninggal/CON karena dbd")
paragraph.append("lima/NUM warga grobogan/LOC meninggal/CON karena dbd")
paragraph.append("kota/ORG tarakan/LOC 5/NUM orang mati/CON karena dbd")
paragraph.append("pemerintah/ORG tarakan/LOC 5/NUM orang mati/CON karena dbd")
paragraph.append("dinas/ORG kesehatan/ORG sleman/LOC 5/NUM orang mati/CON karena dbd")
paragraph.append("sepuluh/NUM warga klaten/LOC 5/NUM orang mati/CON karena dbd")
paragraph.append("empat/NUM warga solo/LOC tewas/CON terkena/CON dbd")
paragraph.append("empat/NUM warga bantul/LOC tewas/CON terkena/CON dbd")
paragraph.append("enam/NUM warga lumajang/LOC tewas/CON terkena/CON dbd")
paragraph.append("delapan/NUM warga bekasi/LOC tewas/CON terkena/CON dbd")
paragraph.append("#info @janggal dua/NUM puluh/NUM warga klaten/LOC tewas/CON terkena/CON dbd bit.ly/1KuKsxO")
#paragraph.append("meninggal/CON dunia, tiga/NUM orang di klaten/LOC karena dbd")

#==========================================================================
# TRAIN IIS
#==========================================================================
# Preprocessing Train
#--------------------------------------------------------------------------
#clean tag. example : #, @, link internet 
paragraph_clean_tag = tag.tag_removal(paragraph, "train")
#clean stopword. example : yah, hlo 
paragraph_clean_stopword = stopword.stopword_removal(paragraph_clean_tag, "train")
#finalisasi clean sentence
paragraph_clean = paragraph_clean_stopword
#--------------------------------------------------------------------------
# Proses Training IIS
#--------------------------------------------------------------------------
classifier = classify.training_weight_iis(paragraph_clean)
#--------------------------------------------------------------------------

f = open('iis.pickle', 'wb')
pickle.dump(classifier, f)
f.close()