#!/usr/bin/python
from nltk import word_tokenize
from nltk import MaxentClassifier, classify
import numpy as np
import feature as f
import regexp as regx
import string

class maxent:
	def binary_feature(self, sentence, type_feature):
		self.sentence = sentence

		#regex find word (w) and label (lbl), especially in data train
		w = regx.w
		lbl = regx.lbl

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
						label.append(lbl.search(token[index]).group(1))
						#add word to array
						token[index] = w.search(token[index]).group(1)
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

	def training_weight_iis(self, sentence):
		me_classifier = MaxentClassifier.train(self.binary_feature(sentence, "train_iis"), 'iis', trace=10, max_iter=100, min_lldelta=0.5)
		return me_classifier

	def training_ner(self, sentence, classification):
		featureset = self.binary_feature(sentence, "train_ner")
		#print featureset
		self.classification = classification
		token = word_tokenize(sentence)
		entity = ["ORG", "LOC", "NUM", "CON"]
		temp_sentence = []
		for index, feature in enumerate(featureset):
			#print
			#print ' '*20+'%s' %token[index]
			if sum(feature.values()) != 0:
				#jika bukan other atau sum feature tidak sama dengan 0
				print ' '*4+'p(ORG)      p(LOC)      p(NUM)      p(CON)'
				print '-'*(28+24)
				pdist = classification.prob_classify(feature)
				en = np.array([pdist.prob('ORG'), pdist.prob('LOC'), pdist.prob('NUM'), pdist.prob('CON')])
				en_index = np.argmax(en)
				print en
				if "/" not in token[index]:
					temp_replace = token[index].replace(token[index], token[index]+"/"+entity[en_index])
					#apabila entitas maka append
					temp_sentence.append(temp_replace)
			else:
				#apabila bukan entitas maka append
				temp_sentence.append(token[index])

		#sentence = " ".join(str(temp_sentence))
		sentence = " ".join(temp_sentence)
		return sentence
