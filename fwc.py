#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

import dbmodel as d
import gazetter as g
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

dbmodel = d.DBModel()

#call class steming
factory = StemmerFactory()
stemmer = factory.create_stemmer()


db_of_data = "ner_coba"
collection_of_data = "mar"

documents = dbmodel.get_data_from_db_ner(db_of_data, collection_of_data)

#print documents
for document in documents :
	data = document["data"]
	print data

	if data:
		#get Lokasi dan Jumlah penderita
		entitas_lokasi = data[0]["entity"]["LOC"]
		entitas_num = data[0]["entity"]["NUM"]

		#get position entitas
		entity_position_from_db = data[0]["entity_position"]

		print data[0]["id"]

		#get value unique
		arr_unique_kota = list(set(entitas_lokasi))
		arr_unique_num = list(set(entitas_num))

		res_unique_con = []
		#check apakah index array CON ada didalam array data[0]["entity"]
		if "CON" not in data[0]["entity"] :
			#apabila kondisi tidak ada, maka statement ini dijalankan
			res_unique_con = []
		else:
			#apabila kondisi ada, maka jalankan statement berikut
			entitas_con = data[0]["entity"]["CON"]
			#setting unique identitas
			arr_unique_con = list(set(entitas_con))
			check_jumlah_kondisi_mati = 0
			check_jumlah_kondisi_penderita = 0
			for kondisi in arr_unique_con:
				#pencarian kata dasar kondisi
				kondisi_stem = stemmer.stem(kondisi.encode("utf8"))
				#check duplicate array kondisi kematian, apabila ada dua atau lebih kategori kematian dalam satu kota. ex : mati dan tewas
				if len(arr_unique_kota) == 1 and kondisi_stem in g.array_kon_mati:
					check_jumlah_kondisi_mati+=1
				#check duplicate array kondisi penderita, apabila ada dua atau lebih kategori penderita dalam satu kota
				if len(arr_unique_kota) == 1 and kondisi_stem in g.array_kon_penderita:
					check_jumlah_kondisi_penderita+=1
				
				#jika kondisi memang benar2 kondisi dan dipastikan tidak ada duplicate kondisi kematian atau penderita, ex : terkena, penderita
				#maka masukan kedalam array
				if kondisi_stem in g.gaz_knd and (check_jumlah_kondisi_mati <= 1 and check_jumlah_kondisi_penderita	 <= 1):
					#print "kondisi %s jumlah kondisi %s"%(kondisi_stem,check_jumlah_kondisi_penderita)
					res_unique_con.append(kondisi)

			print "kondisi : %s"%res_unique_con

		# for kota in arr_unique_kota:
		# 	print kota
		res_unique_num = []
		for num in entitas_num:
			if num.isdigit():
				res_unique_num.append(num)

		print "kota : %s"%arr_unique_kota
		print "jumlah : %s"%res_unique_num

		print "id %s : %s"%(data[0]["id"],arr_unique_kota)
		for index, kota in enumerate(arr_unique_kota):	
			print arr_unique_kota[index]
			print index
			# reset array
			#data[index]["entity"]["LOC"] = []
			#data[index]["entity"]["LOC"] = arr_unique_kota[index]
			#data[index]["entity"]["NUM"] = []
			#data[index]["entity"]["NUM"] = arr_unique_num[index]

		#print data
		"""
		for lokasi in entitas_lokasi:
			print lokasi
		for num in entitas_num:
			print num
		"""