#!/usr/bin/python

import os 
from pymongo import MongoClient

client = MongoClient()

def export_data(db):
	database = client[db]
	for collection in range(1,32):
		if len(str(collection)) == 1:
			collection="0%s"%(str(collection))
		check_collection = str(collection) in database.collection_names()
		if check_collection:
			os.system("mongoexport --db %s --collection %s --out db/april/new/%s.csv"%(db,collection,collection))
			message = "exported collection %s success"%(collection)
			print message

def import_data(db, path):
	for collection in range(1,32):
		if len(str(collection)) == 1:
			collection="0%s"%(str(collection))
		check_file = os.path.exists("%s/%s.csv"%(path,collection))
		if check_file:
			os.system("mongoimport --db %s --collection %s --file %s/%s.csv"%(db,collection,path,collection))
			message = "imported collection %s to %s success"%(collection, db)
			print message