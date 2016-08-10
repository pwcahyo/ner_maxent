#!/usr/bin/python

import dbmodel as d

dbmodel = d.DBModel()


db_of_data = "ner"
mount_of_data = "mar"

documents = dbmodel.get_data_from_db_ner(db_of_data, mount_of_data)

#print documents
for document in documents :
	if document:
		print document["data"]