#!/usr/bin/python
import regexp as regx
import kamus_angka as ka
import pickle
import operator

class Func:
	w = regx.w
	def check_terbilang(self, terbilang):
		arr_terbilang = terbilang.split(" ")
		arr_angka = []
		result = {}
		check = False
		lbl = False
		arr_data = {}
		count = 0
		for index, data in enumerate(arr_terbilang):
			try:
				if "/" in data :
					#conditional bila label ada, contoh empat puluh/num [label num]
					data = self.w.search(data).group(1)
					if data in ka.check_angka :
						lbl = True

				# check apakah data termasuk dalam kamus angka	
				check = data in ka.check_angka

				# isikan array angka berdasarkan banyaknya karakter huruf angka pada teks,
				# contoh lima orang meninggal sedangkan tiga orang mati, maka 5 orang meninggal sedangkan 3 orang mati
				try:
					#check apakah ada arr_terbilang[index+1]
					end_num = arr_terbilang[index+1]
					if "/" in end_num:
						karakter = self.w.search(arr_terbilang[index+1]).group(1)
					else:
						karakter = arr_terbilang[index+1]
				except:
					#apabila arr_terbilang[index+1] tidak ada
					end_num = False
					karakter = False
			except IndexError:
			    check = False

			#print check

			if check:
				#apabila check adalah true maka lakukan penambahan array terbilang
				arr_angka.append(data)

				if karakter not in ka.check_angka:
					# apabila karakter dibelakang terbilang maka lakukan pemenggalan terbilang
					arr_data[count] = (" ".join(arr_angka))
					count+=1
					arr_angka = []

		#join list arr_angka agar ada penambahan space, contoh : ['dua', 'puluh', 'lima'] menjadi "dua puluh lima"
		#result["angka"] = " ".join(arr_angka)
		result["angka"] = arr_data
		result["label"] = lbl
		result["sentence"] = terbilang
		return result

	def idx_exist(self, array, idx):
		#print array[idx]
		try:
			array[idx]
		except IndexError:
			return False
		return array[idx]

	def replace_string(self, sentence):
		data = self.check_terbilang(sentence)
		label = data["label"]
		arr_terbilang = data["angka"]
		data_terbilang = data["sentence"]
		for index, terbilang in enumerate(arr_terbilang):
			if label :
				# jika label ada, atau pada saat proses pelatihan iis
				words = data["sentence"].split()
				imbuhan =arr_terbilang[index]
				idx_imbuhan = words.index(imbuhan)
				idx_str_or_numeric = idx_imbuhan-1
				temp_str = words[idx_str_or_numeric]+" "+imbuhan
				if imbuhan in ka.angka and words[idx_str_or_numeric].isdigit():
					#apabila ada kombinasi angka dengan terbilang, exmple : 10 milyar, 10 juta,
					result = int(words[idx_str_or_numeric]) * ka.angka[imbuhan]
					data_terbilang = data_terbilang.replace(temp_str+"/num", str(result)+"/num")
				else:
					temp_num = self.convert(arr_terbilang[index])
					data_terbilang = data_terbilang.replace(arr_terbilang[index]+"/num", temp_num+"/num")
			else:
				# jika  label tidak ada, atau pada saat proses ner
				words = data["sentence"].split()
				imbuhan =arr_terbilang[index]
				idx_imbuhan = words.index(imbuhan)
				idx_str_or_numeric = idx_imbuhan-1
				temp_str = words[idx_str_or_numeric]+" "+imbuhan
				if imbuhan in ka.angka and words[idx_str_or_numeric].isdigit():
					#apabila ada kombinasi angka dengan terbilang, exmple : 10 milyar, 10 juta,
					result = int(words[idx_str_or_numeric]) * ka.angka[imbuhan]
					data_terbilang = data_terbilang.replace(temp_str, str(result))
				else:
					temp_num = self.convert(arr_terbilang[index])
					data_terbilang = data_terbilang.replace(arr_terbilang[index], temp_num)

		return data_terbilang

	def convert(self, terbilang):
		angka_str = ""
		angka = terbilang.split(" ")
		if len(angka)==1 and angka[0] in ka.imbuhan:
			#untuk menangani belas, contoh belas kasihan, kata belas tersebut ada berada array imbuhan
			angka_str = angka[0]
		else:
			#diambil dari kamus data
			ka_angka = ka.angka
			ka_im = ka.imbuhan

			index = 0
			while index < len(angka):
				#instance data angka
				idx_one = self.idx_exist(angka, index)
				idx_two = self.idx_exist(angka, index+1)
				idx_three = self.idx_exist(angka, index+2)
				#print "loop ke %s = {one : %s},{two : %s},{three : %s}" %(index,idx_one,idx_two,idx_three)

				#catch agar angka_str tidak error maka penambahan string 0
				if angka_str == "":
					angka_int = 0
				#check apakah index ada didalam array ka.angka
				if (idx_one in ka_angka) and (idx_two in ka_im):
					#print "masuk atas : %s, %s" %(idx_one, idx_two)
					if idx_two == "belas":
						# contoh lima belas ribu [ada angka dan 2 imbuhan dengan belas]
						temp_str = str(ka_im[idx_two])+str(ka_angka[idx_one])
						if (idx_three in ka_im):
							temp_int = int(temp_str) * ka_im[idx_three]
							index+=3
						else:
							temp_int = int(temp_str)
							index+=2

					else:
						# contoh lima puluh ribu [ada angka dan 2 imbuhan selain belas]
						if (idx_three in ka_im):
							# ~ apabila element idx_three ada di kamus data imbuhan, contoh : tiga puluh juta
							temp_int = (ka_angka[idx_one] * ka_im[idx_two]) * ka_im[idx_three]
							index+=3
						else:
							# ~ apabila hanya ada angka dan 1 imbuhan, contoh : tiga puluh
							temp_int = ka_angka[idx_one] * ka_im[idx_two]
							index+=2
				else:
					if idx_one in ka_angka:
						# ~ apabila hanya ada 1 angka tanpa imbuhan, contoh : satu
						temp_int = ka_angka[idx_one]
						index+=1
					else:
						# ~ apabila hanya ada 1 imbuhan tanpa angka, contoh : ratus
						temp_int = int(angka_str) * ka_im[idx_one]
						index+=1

				if (angka_int > temp_int) or angka_str =="":
					# ~ apabila angka int global lebih besar dari temporary interger sekarang atau angka string global kosong
					angka_int = angka_int + temp_int
					angka_str = str(angka_int)
				else:
					# ~ apabila angka int global lebih kecil dari temporary interger sekarang atau angka string global tidak kosong
					temp_str = angka_str.replace('0','')
					temp_str += str(temp_int)
					angka_str = temp_str
					#print "angka_str : %s, temp_int : %i" %(angka_str,temp_int)

		return angka_str

	#fungsi konversi terbilang ke angka
	def terbilang_to_number(self, sentence):
		number = self.replace_string(sentence)

		return number

	#fungsi open file
	def open_file(self, name_file):
		f = open(name_file, 'rb')
		classifier = pickle.load(f)
		f.close()

		return classifier

	def grouping_data_lokasi(self, data):
		#parameter data = array dictionary

		#sorting dictionary ascending berdasarkan value
		sort_loc = sorted(data.items(), key=operator.itemgetter(1))

		dist_loc = 0
		arr_temp_loc = []
		arr_loc = []
		for loc_in_search in sort_loc:
			dist_loc = abs(dist_loc) - loc_in_search[1]
			abs_dist_loc = abs(dist_loc)
			if (not arr_loc) or abs_dist_loc==1:
				#apabila arr_loc kosong atau jarak indek kata lokasi = 1
				#maka arr_loc append index
			 	arr_loc.append(loc_in_search[0])
			 	#reset dist_location
			 	dist_loc = loc_in_search[1]
			 	if abs_dist_loc != 1:
			 		#apabila jarak != 1
			 		#append grup arr lokasi
			 		arr_temp_loc.append(arr_loc)
			 		#reset dist_location
			 		dist_loc = loc_in_search[1]
			else:
				#reset dist_location
				dist_loc = loc_in_search[1]
				#reset arr location
				arr_loc = []
				arr_loc.append(loc_in_search[0])
				arr_temp_loc.append(arr_loc)

		return arr_temp_loc



#main process
#data = Func()
#print data.convert_terbilang_to_number(kalimat.lower())
