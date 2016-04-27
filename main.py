#!/usr/bin/python

import maxent as m
import gazetter as g
import func as f
import regexp as regx
from nltk.tokenize import sent_tokenize
from nltk import word_tokenize
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

#call class maxent
classify = m.maxent()

#call class function
func = f.Func()

#call class steming
factory = StemmerFactory()
stemmer = factory.create_stemmer()

# pelatihan iis
#==========================================================================
paragraph = []
paragraph.append("di tegal/LOC empat puluh lima/NUM orang menderita/CON dbd empat puluh satu/NUM meninggal/CON tiga puluh/NUM orang dirawat")
paragraph.append("di malang/LOC 4/NUM orang menderita/CON dbd")
paragraph.append("10/NUM orang mati/CON karena dbd di bantul/LOC")
paragraph.append("di sleman/LOC 4/NUM orang menderita/CON dbd")
paragraph.append("cirebon/LOC meninggal/CON karena dbd")
paragraph.append("jakarta/LOC meninggal/CON karena dbd")
paragraph.append("empat/NUM warga bandung/LOC meninggal/CON karena dbd")
paragraph.append("3/NUM warga grobogan/LOC meninggal/CON karena dbd")
paragraph.append("kota/ORG tarakan/LOC 5/NUM orang mati/CON karena dbd")
paragraph.append("pemerintah/ORG tarakan/LOC 5/NUM orang mati/CON karena dbd")
paragraph.append("dinas/ORG kesehatan/ORG sleman/LOC 5/NUM orang mati/CON karena dbd")
paragraph.append("warga klaten/LOC 5/NUM orang mati/CON karena dbd")

train = []
w = regx.w
lbl = regx.lbl

for index, data in enumerate(paragraph):
	sentence = sent_tokenize(data)
# 1. Pemecahan paragraf kedalam kalimat
	for index, data in enumerate(sentence):	
# 2. Convert sentence to lower
		sent_lower = data.lower()
# 3. Convert terbilang ke angka
		sent_conv = func.terbilang_to_number(sent_lower)
# 4. Stemming
		tokenize = word_tokenize(sent_conv)

		div_sentence = []
		for data in tokenize:
			if "/" not in data:
				sent_stem = stemmer.stem(data)
				data = sent_stem
			elif "/con" in data:
				sent_stem = stemmer.stem(w.search(data).group(1))
				data = sent_stem+"/CON"
			elif "/" in data:
				word = w.search(data).group(1)
				label = lbl.search(data).group(1)
				data = word+"/"+label.upper()
			div_sentence.append(data)
		train.append(" ".join(div_sentence))
# 5. Pembobotan
classification = classify.training_weight_iis(paragraph)

#==========================================================================

# pelatihan NER
# 1. Mengubah huruf besar menjadi huruf kecil
sentence = "di padang lima orang mati gara - gara dbd tujuh kritis. warga bantul tiga puluh orang meninggal karena dbd"
sentence = sentence.lower()

# 2. Tokenisasi sentence
sentence = sent_tokenize(sentence)
print sentence
for index, data in enumerate(sentence):
# 3. Convert terbilang ke angka
	sent_conv = func.terbilang_to_number(data)
# 4. Stemming
	sent_stem = stemmer.stem(sent_conv)
	print classify.training_ner(sent_stem, classification)