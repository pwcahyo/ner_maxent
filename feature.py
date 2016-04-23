import re
import numpy as np
import gazetter as g
from pymongo import MongoClient

class Feature:
	#mongodb connection
	client = MongoClient()
	db = client.bigcities

	def template_feature(self, token, label, index):
		# apabila other maka return None
		if label and label[index] == "O": 
			return 
		# else other maka continue
		"""ORG = f1,f2,f3 | LOC = f4,f5,f6 | NUM = f7,f8 | CON = f9,f10"""
		f1 = token[index] in g.gaz_org
		f2 = token[index-1] == "di"
		f3 = token[index] in g.gaz_org
		f4 = len(list(self.db.cities.find({"kota":re.compile("^"+token[index]+"$", re.IGNORECASE)})))>=1
		f5 = token[index-1] == "di"
		#f6 = label[index-1] == "ORG"
		f6 = token[index-1] in g.gaz_org
		try:
		    data = token[index+1]
		except IndexError:
		    data = "null"
		f7 = data in g.gaz_knd or data in g.gaz_sp
		f8 = token[index].isdigit()
		f9 = token[index] in g.gaz_knd
		f10 = token[index-1] in g.gaz_sp
		lst = np.array([f1, f2, f3, f4, f5, f6, f7, f8, f9, f10])
		b_ft = lst*1

		if label:
			#apabila label ada, saat data train teranotasi
			result = (dict(f1=b_ft[0], f2=b_ft[1], f3=b_ft[2], f4=b_ft[3], f5=b_ft[4], f6=b_ft[5], f7=b_ft[6], f8=b_ft[7], f9=b_ft[8], f10=b_ft[9]), label[index])
		else:
			#apabila label tidak ada, saat data train tidak teranotasi
			result = (dict(f1=b_ft[0], f2=b_ft[1], f3=b_ft[2], f4=b_ft[3], f5=b_ft[4], f6=b_ft[5], f7=b_ft[6], f8=b_ft[7], f9=b_ft[8], f10=b_ft[9]))

		return result

