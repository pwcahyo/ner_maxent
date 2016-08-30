#!/usr/bin/python

import re
import numpy as np
import gazetter as g
from pymongo import MongoClient
import dbmodel as d

class Feature:
	#mongodb connection
	client = MongoClient()
	db = client.indo_db
	gaz_sp = g.gaz_sp
	gaz_o = g.gaz_o
	gaz_org = g.gaz_org
	gaz_knd = g.gaz_knd

	def template_feature(self, token, label, index):
		# apabila other maka return None
		if label and (label[index] == ("O" or "o")): 
			return 
		elif (token[index] in self.gaz_sp) or (token[index] in self.gaz_o):
			if label:
				#apabila data sekarang ada didalam gazetter other dan satuan penderita
				return (dict(f1=0, f2=0, f3=0, f4=0, f5=0, f6=0, f7=0, f8=0, f9=0, f10=0), label[index])
			else:
				return (dict(f1=0, f2=0, f3=0, f4=0, f5=0, f6=0, f7=0, f8=0, f9=0, f10=0))
		else:
			# else other maka continue
			"""ORG = f1,f2,f3 | LOC = f4,f2,f3 | NUM = f5| CON = f6,f7"""
			try:
			    data = token[index+1]
			except IndexError:
			    data = "null"
			f1 = token[index] in self.gaz_org
			f2 = token[index-1] == "di"
			f3 = token[index-1] in self.gaz_org
			search_loc = token[index]
			if token[index] == "kabupaten":
				f4 = False
			else:
				f4 = (self.db.location.find({"$text": {"$search": search_loc}}).count())>=1
			isdigit = token[index].isdigit()
			num_to_occur = data in self.gaz_knd or data in self.gaz_sp

			if isdigit and num_to_occur:
				f5 = True
			else:
				f5 = False

			f6 = token[index] in self.gaz_knd
			f7 = token[index-1] in self.gaz_sp
			lst = np.array([f1, f2, f3, f4, f5, f6, f7])
			b_ft = lst*1

			if label:
				#apabila label ada, saat data train teranotasi
				result = (dict(f1=b_ft[0], f2=b_ft[1], f3=b_ft[2], f4=b_ft[3], f5=b_ft[4], f6=b_ft[5], f7=b_ft[6]), label[index])
			else:
				#apabila label tidak ada, saat data train tidak teranotasi
				result = (dict(f1=b_ft[0], f2=b_ft[1], f3=b_ft[2], f4=b_ft[3], f5=b_ft[4], f6=b_ft[5], f7=b_ft[6]))

			return result