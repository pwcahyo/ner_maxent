#!/usr/bin/python	

from __future__ import with_statement
from urlparse import urlparse

class TLDRemoval:
	def check_tld(self, word):
		# load tlds, ignore comments and empty lines:
		with open("effective_tld_names.dat") as tld_file:
			tlds = [line.strip() for line in tld_file if line[0] not in "/\n"]

		binary_check_url = 0
		#apabila kata tidak ada label maka lakukan statement berikut
		if "/LOC" not in word:
			slice_split = word.split("/")
			for slice_word in slice_split:
				dot_split = slice_word.split(".")
				for word_clean in dot_split:
					if word_clean in tlds:
						binary_check_url = 1

		if binary_check_url == 1:
			#apabila merupakan url
			clean_word = ""
		else:
			#apabila bukan url
			clean_word = word

		return clean_word