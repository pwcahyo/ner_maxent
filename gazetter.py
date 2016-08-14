#!/usr/bin/python

#gazzeter
gaz_sp = ["jiwa", "anak", "orang","warga","pasien","kasus"]
gaz_o = ["demam", "berdarah", "dengue", "dbd", "sakit", "db"]
gaz_knd = ["derita", "kena", "rawat", "korban", "derita", "tewas", "keritis", "mati", "kritis", "tinggal"]
#apabila di stemming maka kondisi diubah menjadi kata dasar. (penderita = derita)
gaz_org = ["pemkot", "dinkes", "pemda", "pemkab", "dinas", "pemerintah", "kabupaten", "rs"]
#gaz_org delete warga

array_kon_mati = ["tewas","mati","tinggal"]
array_kon_penderita = ["derita", "kena", "rawat", "korban", "derita", "keritis", "kritis"]