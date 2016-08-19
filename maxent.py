#!/usr/bin/python
from nltk import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk import MaxentClassifier, classify
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from pymongo import MongoClient
import numpy as np
import feature as f
import func
import regexp as regx
import string
import re

class Maxent:
	#regex find word (w) and label (lbl), especially in data train
	w = regx.w
	lbl = regx.lbl

	#call class function
	func = func.Func()

	#call class steming
	factory = StemmerFactory()
	stemmer = factory.create_stemmer()

	#mongodb connection
	client = MongoClient()
	db = client.bigcities

	def binary_feature(self, sentence, type_feature):
		self.sentence = sentence

		#define unclean temporary array data train and label
		train = []

		#jika training iis maka lakukan pencarian binary feature dengan label
		#contoh : (dict(f1=0, f2=0, f3=0, f4=0, f5=0, f6=0, f7=1, f8=1, f9=0, f12=0, f10=0, f11=0}, "NUM"))
		if type_feature == "train_iis":
			for index, data in enumerate(sentence): 
				label = []
				token = word_tokenize(data)
				for index, data in enumerate(token):
					if "/" in data :
						#add label to array
						label.append(self.lbl.search(token[index]).group(1))
						#add word to array
						token[index] = self.w.search(token[index]).group(1)
					else:
						label.append("O")
				for index, data in enumerate(token):
					#feature processing panggil class feature
					featuretrain = f.Feature()
					result = featuretrain.template_feature(token, label, index)
					#result = template_feature(token, label, index)
					train.append(result) 
		else:
			#jika training ner atau selain iis maka hanya melakukan pencarian binary feature, tidak dengan label
			#contoh : (dict(f1=0, f2=0, f3=0, f4=0, f5=0, f6=0, f7=1, f8=1, f9=0, f12=0, f10=0, f11=0}))
			token = word_tokenize(sentence)
			label = []
			for index, data in enumerate(token):
				#feature processing panggil class feature
				featuretrain = f.Feature()
				result = featuretrain.template_feature(token, label, index)
				#result = template_feature(token, label, index)
				train.append(result) 

		# filter array empty/none karena Other atau entitas O tidak diproses
		train_set = filter(None, train)
		#print train_set
		return train_set

	def training_weight_iis(self, paragraph):
		train = []
		for index, data in enumerate(paragraph):
			sentence = sent_tokenize(data)
		# 1. Pemecahan paragraf kedalam kalimat
			for index, data in enumerate(sentence):	
		# 2. Convert sentence to lower
				sent_lower = data.lower()
		# 3. Convert terbilang ke angka
				sent_conv = self.func.terbilang_to_number(sent_lower)
				print "training kata [%s]"%sent_conv
		# 4. Stemming
				tokenize = word_tokenize(sent_conv)

				div_sentence = []
				for data in tokenize:
					if "/" not in data:
						# ubah menjadi kata dasar
						sent_stem = self.stemmer.stem(data)
						data = sent_stem
					elif "/con" in data:
						# ubah menjadi kata dasar kemudian dicocokan kedalam gazeter kondisi
						sent_stem = self.stemmer.stem(self.w.search(data).group(1))
						data = sent_stem+"/CON"
					elif "/" in data:
						word = self.w.search(data).group(1)
						label = self.lbl.search(data).group(1)
						data = word+"/"+label.upper()
					div_sentence.append(data)
				train.append(" ".join(div_sentence))

		#print train
		#melakukan training dengan sentence yang sudah diubah kedalam kata dasar
		me_classifier = MaxentClassifier.train(self.binary_feature(train, "train_iis"), 'iis', trace=100, max_iter=2000, min_lldelta=0.5)
		#print me_classifier.show_most_informative_features()
		return me_classifier

	def training_ner(self, paragraph, classification):
		sentence = sent_tokenize(paragraph)
		#print paragraph
		
		#result = []
		train = []
		sentence_ne = ""
		# 1. Pemecahan paragraf kedalam kalimat
		for index, data in enumerate(sentence):	
			tokenize = word_tokenize(data)
			div_sentence = []
			for word in tokenize:
				check_kota = len(list(self.db.cities.find({"kota":re.compile("^"+word+"$", re.IGNORECASE)})))>=1
				if not check_kota:
					#apabila kata bukan kota maka dibuat kata dasar
					sent_stem = self.stemmer.stem(word)
					word = sent_stem
				div_sentence.append(word)
			train.append(" ".join(div_sentence))
			#ket parameter : self.div_sentence_ner(kalimat_dengan_kata_dasar, kalimat_asli, jenis_klasifikasi) 
			sentence_ne = self.div_sentence_ner("".join(train), " ".join(tokenize), classification)
			#result.append(sentence_ne)
			#reset array train agar tidak diikutkan training ner
			train = []

		return sentence_ne

	def div_sentence_ner(self, sentence_stem, sentence_unstem, classification):
		#kalimat sudah dicari kata dasar
		sentence_stem = sentence_stem.lower()
		sent_stem_conv = self.func.terbilang_to_number(sentence_stem)

		#kalimat asli (tidak di jadikan kata dasar)
		sentence_unstem = sentence_unstem.lower()
		sent_unstem_conv = self.func.terbilang_to_number(sentence_unstem)

		featureset = self.binary_feature(sent_stem_conv, "train_ner")
		self.classification = classification
		token = word_tokenize(sent_unstem_conv)

		entity = ["ORG", "LOC", "NUM", "CON"]
		temp_sentence = []

		# create array object result untuk penampung array balikan
		result = {} 

		result_entity = {}
		result_index_entity = {}
		
		temp_entity = []
		for index, feature in enumerate(featureset):
			#print token[index]
			#print index
			if sum(feature.values()) != 0:
				#print feature
				print ' '*20+'%s' %token[index]
				#jika bukan other atau sum feature tidak sama dengan 0
				print ' '*4+'p(ORG)      p(LOC)      p(NUM)      p(CON)'
				print '-'*(28+24)
				pdist = classification.prob_classify(feature)
				en = np.array([pdist.prob('ORG'), pdist.prob('LOC'), pdist.prob('NUM'), pdist.prob('CON')])
				en_index = np.argmax(en)
				print en
				print

				if "/" not in token[index]:
					#replace word original with word label
					temp_replace = token[index].replace(token[index], token[index]+"/"+entity[en_index])
					#apabila entitas maka append
					temp_sentence.append(temp_replace)
					result_index_entity[token[index]] = index

					if entity[en_index] in result_entity:
						#apabila index array entitas didalam result entitas, maka ambil array entitas tersebut, kemudian tambahkan data baru
						data = result_entity[entity[en_index]]
						data.append(token[index])
					else:
						#apabila ada entitas baru maka kosongkan array dan buat index array baru
						temp_entity = []
						temp_entity.append(token[index])
						result_entity[entity[en_index]] = temp_entity
			else:
				#apabila bukan entitas maka append
				temp_sentence.append(token[index])

			#print " ".join(temp_sentence)
			sentence = " ".join(temp_sentence)

		result["text_tweet"] = sentence
		result["entity"] = result_entity
		result["entity_position"] = result_index_entity
		
		#print result
		return result


# #create object class maxent
# classify = Maxent()
# #create object class independent function
# func = func.Func()

# classifier = func.open_file('iis.pickle')
# sentence = "dbd tewaskan 4 anak di kabupaten cirebon dan tangerang"
# ner = classify.training_ner(sentence, classifier)
# print ner
