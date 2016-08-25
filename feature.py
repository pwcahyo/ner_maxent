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
	gaz_kt_sambung = g.gaz_kt_sambung

	def template_feature(self, token, label, index):
		# apabila other maka return None
		# print "isi : %s"%token[index]
		# print "label : %s"%label
		if label and (label[index] == ("O" or "o")): 
			return 
		elif (token[index] in self.gaz_sp) or (token[index] in self.gaz_o) or (token[index] in self.gaz_kt_sambung):
			if label:
				#apabila data sekarang ada didalam gazetter other dan satuan penderita
				return (dict(f1=0, f2=0, f3=0, f4=0, f5=0, f6=0, f7=0, f8=0, f9=0, f10=0), label[index])
			else:
				return (dict(f1=0, f2=0, f3=0, f4=0, f5=0, f6=0, f7=0, f8=0, f9=0, f10=0))
		else:
			# else other maka continue
			"""ORG = f1,f2,f3 | LOC = f4,f5,f6 | NUM = f7,f8 | CON = f9,f10"""
			try:
			    data = token[index+1]
			except IndexError:
			    data = "null"
			f1 = token[index] in self.gaz_org
			f2 = token[index-1] == "di"
			f3 = token[index-1] in self.gaz_org
			#print token[index]
			#self.db.location.createIndex({"kabupaten":"text","kecamatan":"text","desa":"text"})
			# f4 = len(list(self.db.location.find(
			#     {"$text": {"$search": "string"}},
			#     "fields"=({"kabupaten": token[index], "kecamatan": token[index], "desa": token[index]})
			# )))
			#CREATE INDEX MONGODB:
			#self.db.location.create_index([('kabupaten','text'), ('kecamatan','text'), ('desa','text')])
			search_loc = token[index]
			if token[index] == "kabupaten":
				f4 = False
			else:
				f4 = (self.db.location.find({"$text": {"$search": search_loc}}).count())>=1
			#f4 = len(list(self.db.location.find({"$text":{"$search":"sihatubang"}})))>=1
			#f4 = len(list(self.db.location.find({"desa":{"$regex":token[index]}})))>=1 or len(list(self.db.location.find({"kecamatan":{"$regex":token[index]}})))>=1 or len(list(self.db.location.find({"kabupaten":{"$regex":token[index]}})))>=1
			#f4 = len(list(self.db.cities.find({"kota":re.compile("^"+token[index]+"$", re.IGNORECASE)})))>=1
			#f4 = len(list(self.db.location.find_one({"kota":token[index]})))>=1
			#f4 = len(list(self.db.cities.find({"kota":{"$regex": u""+token[index], "$options": "-i"}})))>=1
			f5 = token[index-1] == "di"
			#f6 = label[index-1] == "ORG"
			#f6 = token[index-1] in self.gaz_org or token[index-1] in self.gaz_sp
			f6 = token[index-1] in self.gaz_org
			# f7 = token[index].isdigit()
			# if f7: 
			# 	f8 = data in self.gaz_knd or data in self.gaz_sp
			# else:
			# 	f8 = False
			isdigit = token[index].isdigit()
			num_to_occur = data in self.gaz_knd or data in self.gaz_sp

			if isdigit and num_to_occur:
				f7 = True
			else:
				f7 = False

			f8 = token[index] in self.gaz_knd
			f9 = token[index-1] in self.gaz_sp
			lst = np.array([f1, f2, f3, f4, f5, f6, f7, f8, f9])
			b_ft = lst*1

			if label:
				#apabila label ada, saat data train teranotasi
				result = (dict(f1=b_ft[0], f2=b_ft[1], f3=b_ft[2], f4=b_ft[3], f5=b_ft[4], f6=b_ft[5], f7=b_ft[6], f8=b_ft[7], f9=b_ft[8]), label[index])
			else:
				#apabila label tidak ada, saat data train tidak teranotasi
				result = (dict(f1=b_ft[0], f2=b_ft[1], f3=b_ft[2], f4=b_ft[3], f5=b_ft[4], f6=b_ft[5], f7=b_ft[6], f8=b_ft[7], f9=b_ft[8]))

			# print "masuk"
			# print result
			return result

			# if label:
			# 	#apabila label ada, saat data train teranotasi
			# 	result = (dict(f1=b_ft[0], f2=b_ft[1], f3=b_ft[2], f4=b_ft[3], f5=b_ft[4], f6=b_ft[5], f7=b_ft[6], f8=b_ft[7], f9=b_ft[8], f10=b_ft[9]), label[index])
			# else:
			# 	#apabila label tidak ada, saat data train tidak teranotasi
			# 	result = (dict(f1=b_ft[0], f2=b_ft[1], f3=b_ft[2], f4=b_ft[3], f5=b_ft[4], f6=b_ft[5], f7=b_ft[6], f8=b_ft[7], f9=b_ft[8], f10=b_ft[9]))
			# #print token[index]
			# #print result