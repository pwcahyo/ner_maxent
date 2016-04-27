#!/usr/bin/python
import regexp as regx
import kamus_angka as ka

class Func:
	def check_terbilang(self, terbilang):
		arr_terbilang = terbilang.split(" ")
		arr_angka = []
		result = {}
		check = False
		for index, data in enumerate(arr_terbilang):
			try:
				check = data in ka.check_angka
			except IndexError:
			    check = False
			
			if check:
				#apabila check adalah true maka lakukan penambahan array terbilang
				arr_angka.append(data)

		#join list arr_angka agar ada penambahan space, contoh : ['dua', 'puluh', 'lima'] menjadi "dua puluh lima"
		result["angka"] = " ".join(arr_angka)
		result["sentence"] = terbilang
		return result

	def idx_exist(self, array, idx):
		#print array[idx]
		try:
			array[idx]
		except IndexError:
			return False
		return array[idx]

	def convert_terbilang_to_number(self, sentence):
		data = self.check_terbilang(sentence)
		#instance data terbilang
		terbilang = data["angka"]
		# pecah data terbilang
		angka = terbilang.split(" ")
		# instance data kalimat
		kalimat = data["sentence"]
		if not terbilang:
			return kalimat

		angka_str = ""

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
				print "angka_str : %s, temp_int : %i" %(angka_str,temp_int)

		return kalimat.replace(terbilang, angka_str)


#main process
#data = Func()
#print data.convert_terbilang_to_number(kalimat.lower())
