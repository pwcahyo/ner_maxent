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

class maxent:
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
		# 4. Stemming
				tokenize = word_tokenize(sent_conv)

				div_sentence = []
				for data in tokenize:
					if "/" not in data:
						sent_stem = self.stemmer.stem(data)
						data = sent_stem
					elif "/con" in data:
						sent_stem = self.stemmer.stem(self.w.search(data).group(1))
						data = sent_stem+"/CON"
					elif "/" in data:
						word = self.w.search(data).group(1)
						label = self.lbl.search(data).group(1)
						data = word+"/"+label.upper()
					div_sentence.append(data)
				train.append(" ".join(div_sentence))

		me_classifier = MaxentClassifier.train(self.binary_feature(train, "train_iis"), 'iis', trace=10, max_iter=100, min_lldelta=0.5)
		return me_classifier

	def training_ner(self, paragraph, classification):
		sentence = sent_tokenize(paragraph)
		#print paragraph
		
		arr_sentence = []
		train = []
		# 1. Pemecahan paragraf kedalam kalimat
		for index, data in enumerate(sentence):	
			tokenize = word_tokenize(data)
			div_sentence = []
			for word in tokenize:
				check_kota = len(list(self.db.cities.find({"kota":re.compile("^"+word+"$", re.IGNORECASE)})))>=1
				if not check_kota:
					sent_stem = self.stemmer.stem(word)
					word = sent_stem
				div_sentence.append(word)
			train.append(" ".join(div_sentence))
			sentence_ne = self.per_sentence_ner("".join(train), " ".join(tokenize), classification)
			arr_sentence.append(sentence_ne)
			#reset array train agar tidak diikutkan training ner
			train = []

		return arr_sentence

	def per_sentence_ner(self, sentence_stem, sentence_unstem, classification):
		sentence_stem = sentence_stem.lower()
		sentence_unstem = sentence_unstem.lower()
		sent_stem_conv = self.func.terbilang_to_number(sentence_stem)
		sent_unstem_conv = self.func.terbilang_to_number(sentence_unstem)
		#print sent_stem_conv
		
		#print train
		featureset = self.binary_feature(sent_stem_conv, "train_ner")
		#print featureset
		self.classification = classification
		#print token
		token = word_tokenize(sent_unstem_conv)
		print token

		entity = ["ORG", "LOC", "NUM", "CON"]
		temp_sentence = []
		
		for index, feature in enumerate(featureset):
			#print feature
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
					temp_replace = token[index].replace(token[index], token[index]+"/"+entity[en_index])
						#apabila entitas maka append
					temp_sentence.append(temp_replace)
			else:
				#apabila bukan entitas maka append
				temp_sentence.append(token[index])

			#print " ".join(temp_sentence)
			sentence = " ".join(temp_sentence)
		return sentence
