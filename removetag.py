#!/usr/bin/python
# -*- coding: utf-8 -*-

#load sentence tokenize
from nltk.tokenize import sent_tokenize
#load word tokenize
from nltk import word_tokenize
#load format regex
import regexp as regx
#import fungsi tld (top level domain) removal
import tldremoval as tld

class RemoveTag:
	remove_url = tld.TLDRemoval()
	def punctuation_remove(self, sentence, type):
		# remove hashtag, tag, code html with start &
		#sentences = " ".join(regx.coba.sub(" ",sentence).split())
		if type=="train":
			sentence_clean = " ".join(regx.symbol_train.sub(" ",sentence).split())
		else:
			sentence_clean = " ".join(regx.symbol_ner.sub(" ",sentence).split())

		return sentence_clean

	def tld_remove(self, sentence):
		#remove url
		sentence_clean = []
		arr_word = sentence.split()
		for word in arr_word:
			#check url dengan top level domain (tld)
			if self.remove_url.check_tld(word) != "":
				sentence_clean.append(word)
		return " ".join(sentence_clean)

	def clean_sentence(self, sentence, type):
		#membersihkan perkalimat
		temp_sentence = self.tld_remove(sentence)
		sentence_clean = self.punctuation_remove(temp_sentence, type) 
		return sentence_clean

	def tag_removal(self, paragraph, type):
		if type == "train":
			paragraph_clean =[]
			#memecahkan array kalimat
			for sentence in paragraph:
				#proses clean
				#menambahkan kalimat bersih kedalam array kalimat
				paragraph_clean.append(self.clean_sentence(sentence, type))
			return paragraph_clean
		else:
			#proses clean
			return self.clean_sentence(paragraph, type)


#sentence = "#kicauHealth Masuk Jurnal Internasional, Penelitian RSPAD Buka Peluang 'Kalahkan' DBD bit.ly/1KuKsxO"
#func = RemoveTag()
#print func.tag_removal(sentence, "ner")

