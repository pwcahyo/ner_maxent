#!/usr/bin/python

#gazzeter
gaz_sp = ["jiwa", "anak", "orang","warga","pasien","kasus","nyawa"]
gaz_kt_sambung = ["di", "dan", "jadi", "kejadian","harian", "minta"]
gaz_o = ["demam", "berdarah", "dengue", "dbd", "db", "nyamuk"]
gaz_knd = ["sakit", "derita", "kena", "rawat", "korban", "derita", "tewas", "keritis", "mati", "kritis", "tinggal", "layang", "bunuh", "serang", "tular", "terjangkit", "jangkit", "idap", "pengidap", "bahaya", "mengalami", "alami", "nyerang", "renggut","telan", "makan"]
#apabila di stemming maka kondisi diubah menjadi kata dasar. (penderita = derita)
gaz_org = ["warga","pemkot", "dinkes", "pemda", "pemkab", "dinas", "pemerintah", "rs", "dprd", "kecamatan", "kabupaten", "kota", "desa", "pemdes", "kab","who", "puskesmas","korpri","kelurahan", "provinsi", "menkes","pmi","kab", "klinik"]
#"kabupaten", 
#gaz_org delete warga

array_kon_mati = ["tewas","mati","tinggal","layang"]
array_kon_penderita = ["derita", "kena", "rawat", "korban", "derita", "keritis", "kritis"]