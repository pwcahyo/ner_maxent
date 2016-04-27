#!/usr/bin/python

import maxent as m
import func as f
from nltk.tokenize import sent_tokenize

classify = m.maxent()

# pelatihan iis
#==========================================================================
sentence = []
sentence.append("3/NUM warga situbondo/LOC meninggal/CON karena dbd")
sentence.append("di tegal/LOC 4/NUM orang menderita/CON dbd")
sentence.append("di malang/LOC 4/NUM orang menderita/CON dbd")
sentence.append("10/NUM orang mati/CON karena dbd di bantul/LOC")
sentence.append("di sleman/LOC 4/NUM orang menderita/CON dbd")
sentence.append("cirebon/LOC meninggal/CON karena dbd")
sentence.append("jakarta/LOC meninggal/CON karena dbd")
sentence.append("3/NUM warga bandung/LOC meninggal/CON karena dbd")
sentence.append("3/NUM warga grobogan/LOC meninggal/CON karena dbd")
sentence.append("kota tarakan/LOC 5/NUM orang mati/CON karena dbd")
sentence.append("pemerintah/ORG tarakan/LOC 5/NUM orang mati/CON karena dbd")
sentence.append("dinas/ORG kesehatan/ORG sleman/LOC 5/NUM orang mati/CON karena dbd")

classification = classify.training_weight_iis(sentence)
#==========================================================================

# pelatihan NER
# 1. Mengubah huruf besar menjadi huruf kecil
kalimat = "di padang 5 orang mati gara - gara dbd tujuh kritis. sleman lima warga meninggal akibat dbd. delapan warga bandung terkena dbd"
kalimat = kalimat.lower()

# 2. Tokenisasi kalimat
kalimat = sent_tokenize(kalimat)

# 3. Convert terbilang ke angka
func = f.Func()

for index, data in enumerate(kalimat):
	sent_conv = func.convert_terbilang_to_number(data)
	print classify.training_ner(sent_conv, classification)
