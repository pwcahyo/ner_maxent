#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

import dbmodel as d
import gazetter as g
import func as f
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

dbmodel = d.DBModel()

#call class steming
factory = StemmerFactory()
stemmer = factory.create_stemmer()
func = f.Func()


db_of_data = "ner_coba_lagi"
collection_of_data = "mar"

documents = list(dbmodel.get_data_from_db_ner(db_of_data, collection_of_data))


result = {}
bulk = []
for document in documents :
	data = document["data"]
	doc = document["data"]
	if data:
		#get Lokasi dan Jumlah penderita
		entitas_lokasi = data[0]["entity"]["LOC"]
		entitas_num = data[0]["entity"]["NUM"]

		if "ORG" in data[0]["entity"]:
			# jika entitas organisasi ada, maka lakukan statement berikut
			entitas_org = list(set(data[0]["entity"]["ORG"]))
		else:
			entitas_org = []

		#get position entitas
		entity_position_from_db = data[0]["entity_position"]

		#get url dupplicate
		url_duplicate = data[0]["url_duplicate"]

		#get time
		time= data[0]["time"]

		# print data[0]["id"]

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

		temp_arr_kota = {}
		for kota in arr_unique_kota:
			#membuat array kota yang duplicate menjadi unique
			check_kota = dbmodel.check_like_kota(kota)
			if check_kota>=1:
				temp_arr_kota[kota] = entity_position_from_db[kota]
		data_lokasi = func.grouping_data_lokasi(temp_arr_kota)
		loc_clear = []
		for location in data_lokasi:
			#join kata lokasi yang berdekatan. contoh ("jakarta","selatan") menjadi ("jakarta selatan")
			loc = " ".join(location)
			if dbmodel.check_real_kota(loc):
				loc_clear.append(loc)

		res_unique_num = []
		for num in entitas_num:
			#check num adalah number
			if num.isdigit():
				res_unique_num.append(num)

		

		if loc_clear:
			# apabila lokasi benar ada
			# print loc_clear
			for real_loc in loc_clear:
				entity = {}
				loc_data = {}
				# loop ada berapa lokasi dalam satu kali tweet
				if real_loc not in result:
					loc_data["LOC"] = real_loc

					# =============== pencarian kedekatan kata lokasi dengan kata angka insiden ==================
					# #ambil kata pertama pada lokasi
					split_loc = real_loc.split(" ")
					if len(res_unique_num) > 1:
						# apabila kejadian lebih dari satu
						arr_num = []
						arr_index_num = {}
						temp_num = {}
						for num in res_unique_num:
							#split lokasi apabila berupa frase, dan ambil paling depan
							temp_loc = entity_position_from_db[split_loc[0]]
							#mencari jarak antara lokasi dengan angka kejadian
							dist_num_to_loc = abs(entity_position_from_db[num]-temp_loc)
							#jarak yang didapat dimasukan kedalam array
							arr_index_num[num] = dist_num_to_loc
							# print "~ iter kota :%s: kejadian :%s: jarak :%s:"%(real_loc,num,arr_index_num[num])

						# cari minimal jarak antara kota dengan angka kejadian 
						num_min = min(arr_index_num.items(), key=lambda x: x[1])
						loc_data["NUM"] = num_min[0]
					else:
						loc_data["NUM"] = res_unique_num[0]
					# ========================================= end pencarian kedekatan ===========================

					loc_data["CON"] = res_unique_con
					loc_data["ORG"] = entitas_org
					loc_data["entity_position"] = entity_position_from_db
					loc_data["url_duplicate"] = url_duplicate
					loc_data["time"] = time
					result[real_loc] = loc_data
				else:
					result[real_loc]["url_duplicate"].append(url_duplicate[0])

for counter, index in enumerate(result):
	ins = dbmodel.bulk_insert("data_fwc",collection_of_data,result[index])
	print ins