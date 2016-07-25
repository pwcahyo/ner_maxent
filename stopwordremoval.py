#!/usr/bin/python

import stopword
from nltk import word_tokenize

class StopwordRemoval:
	data_stopword = stopword.data_stopword

	def remove_word(self, sentence):
		sentence_clean = []
		#kalimat di tokenisasi kedalam kata
		word_token = word_tokenize(sentence)
		for word in word_token:
			check = word in self.data_stopword
			#apabila kata tidak masuk dalam stopword maka jalankan statement berikut
			if not check :
				sentence_clean.append(word)
		#return dengan join array, example  ["saya","makan","nasi"] menjadi "saya makan nasi"
		return " ".join(sentence_clean)

	def stopword_removal(self, paragraph, type):
		if type=="train":
			#Apabila saat train IIS, maka jalankan statement stopword berikut
			#karena saat training, menggunakan array dengan banyaknya susunan kalimat
			temp_array = []
			for data in paragraph:				
				temp_array.append(self.remove_word(data))
			return temp_array
		else:
			#Apabila saat proses NER, maka jalankan statement berikut
			#karena pengecekan entitas pada proses NER hanya dalam satu kalimat
			return self.remove_word(paragraph)


#kata = "waduh ini kenapa ya kok tidak selesai. padahal saya baru makan"
#data = StopwordRemoval()
#print data.removal(kata)

