Step Pengerjakan Tranining Data :
1. Tentukan entitas/kata yang akan kita labeli
	ada 4 entitas yang dipake, diantaranya :
	* LOC adalah entitas Lokasi
	* NUM adalah entitas Jumlah Penderita
	* ORG adalah entitas Organisasi
	* CON adalah entitas Kondisi

2. Apabila ada kata terbilang di ubah dulu menjadi angka
	ex : empat puluh menjadi 40, tiga menjadi 3

3. Untuk Lokasi :
	Lakukan labelisasi pada kata yang diprediksi kota/tempat apabila bukan, maka jangan dilabeli
	ex : di yogyakarta, jombang, warga jombang,

4. Untuk Jumlah penderita :
	Lakukan labelisasi pada kata yang diprediksi Jumlah penderita 
	ex : 10 warga, 30 penderita, 3 meninggal, 4 kritis

5. Untuk Kondisi :
	lakukan labelisasi pada kata yang diprediksi Kondisi
	ex : meninggal, mati, penderita, sakit, terkena

6. Untuk Organisasi :
	lakukan labelisasi pada kata yang diprediksi Organisasi
	ex : RS, pemkab, dinkes, pemkot, dinas

Contoh labelisasi :
1. Bantul/LOC 2015 332/NUM warga terkena DBD
2. Waspada Penderita/CON DBD di Bantul/LOC Capai 295/NUM Orang
3. DBD Tewaskan Empat Anak di Kabupaten Cirebon --konversi--> DBD Tewaskan 4/NUM Anak di Kabupaten Cirebon/LOC 
