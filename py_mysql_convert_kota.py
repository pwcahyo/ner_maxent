import mysql.connector
import dbmodel as d

dbmodel = d.DBModel()

cnx = mysql.connector.connect(user='root', database='indo_location')
cursor = cnx.cursor()

query = ("SELECT v.name AS desa, d.name AS kecamatan, r.name AS kabupaten, p.name AS provinsi FROM villages as v"
	" LEFT JOIN districts as d ON d.id = v.district_id"
	" LEFT JOIN regencies as r ON r.id = d.regency_id"
	" LEFT JOIN provinces as p ON p.id = r.province_id")

cursor.execute(query)



for (desa, kecamatan, kabupaten, provinsi) in cursor:
	documents = []
	document = {}
	document["desa"] = desa.lower()
	document["kecamatan"] = kecamatan.lower()
	kab = kabupaten.lower()
	str_kab = (kab).replace("kota ","").replace("kabupaten ","")
	if "kabupaten" in kab:
		tipe = "kabupaten"
	else:
		tipe = "kota"
	document["regency_tipe"] = tipe 
	document["kabupaten"] = str_kab
	document["provinsi"] = provinsi.lower()
	documents.append(document)

	# print documents
	dbmodel.bulk_insert("indo_db","location",documents)

cursor.close()
cnx.close()