#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

from pymongo import MongoClient

class DBModel:

	client = MongoClient()

	def check_like_loc(self, database, collection, search_loc):
		db = self.client[database]
		return (db[collection].find({"$text": {"$search": search_loc}}).count())>=1

	def check_real_loc(self, database, collection, search_loc):
		db = self.client[database]
		return (db[collection].find({"kabupaten":search_loc}).count())>=1 or (db[collection].find({"kecamatan":search_loc}).count())>=1 or (db[collection].find({"desa":search_loc}).count())>=1

	def check_loc_and_date(self, database, collection, location, time):
		db = self.client[database]
		return db[collection].find({"$and":[{"LOC":location},{"time" :time}]}).count() >= 1

	def check_num_in_loc_and_date(self, database, collection, location, incident, time):
		db = self.client[database]
		return db[collection].find({"$and":[{"LOC":location},{"NUM":int(incident)},{"time":time}]}).count() >= 1
			
	def update_data_fwc_push_url_duplicate(self, database, collection, location, incident, time, url):
		db = self.client[database]
		result = db[collection].update(
		   	{"$and":[{"LOC":location},{"NUM":int(incident)},{"time" :time}]},
		    {"$push": {"url_duplicate": url}}
		)

		return result

	def district_check(self, database, collection, location):
		db = self.client[database]
		if db[collection].find({"kabupaten":location}).count() >= 1:
			district = "kabupaten"
		elif db[collection].find({"kecamatan":location}).count() >= 1:
			district = "kecamatan"
		elif db[collection].find({"desa":location}).count() >= 1:
			district = "desa"
		elif db[collection].find({"provinsi":location}).count() >= 1:
			district = "provinsi"
		else:
			district = "other"
		return district

	def top_location_of_month(self, database, collection):
		db = self.client[database]
		cursor = db[collection].aggregate(
				[
		            {"$group":{
		                "_id":{"LOC":"$LOC", 
		                        "NUM":{"$max":'$NUM'}, 
		                        "date":"$time", 
		                        "text_tweet":"$text_tweet", 
		                        "url_duplicate":"$url_duplicate",
		                        "ORG":"$ORG",
		                        "CON":"$CON"
		                        }}},
			      	{"$sort": {"_id.NUM":-1 }}
				])

	def get_data_without_label(self, database, collection):
		db = self.client[database]
		cursor = db[collection].aggregate(
		    [
		        {"$group": 
		        	{"_id": "$text_tweet", 
				        "data": {
				        	"$push":{
					                "id":"$url", 
					                "url":"$data_id", 
					                "username":"$username", 
					                "text_tweet":"$text_tweet",
					                "time":"$time_tweet"
				                	}
				            	}	
			    		}
		        },
		        { "$sort": { "_id":-1 } } 
		    ]
		)
		# group : aggregate
		# push : fill list array
		# $sort -1 : descending, ascending 1

		return cursor

	def get_data_with_label(self, database, collection):
		db = self.client[database]
		if len(str(collection)) == 1:
			collection="0%s"%(str(collection))
		check_collection = str(collection) in db.collection_names()
		if check_collection:
			cursor = db[collection].aggregate(
		    [
		        {"$group": 
		        	{"_id": "$text_tweet", 
				        "data": {
				        	"$push":{
					                "id":"$id", 
					                "url":"$url", 
					                "username":"$username", 
					                "text_tweet":"$text_tweet",
					                "time":"$time"
				                	}
				            	}	
			    		}
		        },
		        { "$sort": { "_id":-1 } } 
		    ]
		)
		else:
			cursor = ""

		return cursor


	def get_data_preprocessor(self, database, collection):
		db = self.client[database]
		cursor = db[collection].aggregate(
		    [
		        {"$group": 
		        	{"_id": "$text_tweet", 
				        "data": {
				        	"$push":{
					                "id":"$id", 
					                "url":"$url", 
					                "username":"$username", 
					                "text_tweet":"$text_tweet",
					                "time":"$time"
				                	}
				            	}	
			    		}
		        },
		        { "$sort": { "_id":-1 } } 
		    ]
		)
		# group : aggregate
		# push : fill list array
		# $sort -1 : descending, ascending 1

		return cursor	

		"""
		#coba get satu DATA
		res = []
		ok = []
		data = {}
		hasil = {}
		tweet = {}
		coba = {}
		#tweet["text_tweet"] = u"G Dana U Demam Berdarah Bupati JOMBANG AKAN BELI 918 Sepeda Motor U Pejabat 10 MILYAR"
		tweet["text_tweet"] = u"portalsurya kasus dbd di jember naik dua kali lipat belum klb"
		ok.append(tweet)
		data["data"] = ok
		res.append(data)
		hasil["result"] = res
		
		return hasil
		"""

		

	def get_data_unique_ner(self, database, collection):
		db = self.client[database]
		cursor = db[collection].aggregate(
		    [
		        {"$group": 
		        	{"_id": "$text_tweet", 
				        "data": {
				        	"$push":{
					                "id":"$id", 
					                "url":"$url", 
					                "username":"$username", 
					                "text_tweet":"$text_tweet",
					                "entity":"$entity",
					                "entity_position":"$entity_position",
					                "time":"$time"
				                	}
				            	}	
			    		}
		        },
		        { "$sort": { "_id":-1 } } 
		    ]
		)
		# group : aggregate
		# push : fill list array
		# $sort -1 : descending, ascending 1

		return cursor	

	def get_data_from_db_ner(self, database, collection):
		db = self.client[database]
		cursor = db[collection].aggregate(
		    [
		        {"$group": 
		        	{"_id": {"LOC":"$entity.LOC", "NUM":"$entity.NUM"},
				        "data": {
				        	"$push":{
					                "id":"$id", 
					                "url":"$url", 
					                "username":"$username", 
					                "text_tweet":"$text_tweet",
					                "url_duplicate":"$url_duplicate",
					                "entity":"$entity",
					                "entity_position":"$entity_position",
					                "time":"$time"
				                	}
				            	}	
			    		}
		        },
		        { "$sort": { "_id":-1 } } 
		    ]
		)
		# group : aggregate berdasarkan LOC (Lokasi) dan NUM (Jumlah Penderita)
		# push : fill list array
		# $sort -1 : descending, ascending 1

		return cursor

	def get_data_all(self, database, collection):
		db = self.client[database]
		cursor = db[collection].find({})

		return cursor

	def get_data_one_from_id(self, database, collection, id):
		db = self.client[database]
		if db[collection].find({"id":id}) >= 1:
			cursor = db[collection].find({"id":id})
		else:
			cursor = ""

		return cursor

	def bulk_insert(self, database, collection, documents):
		db = self.client[database]
		results = db[collection].insert(documents)

		return results

	def many_insert(self, database, collection, documents):
		db = self.client[database]
		results = db[collection].insert_many(documents)

		return results.inserted_ids

	def insert_sentence_clean(self, database, collection, document):
		result = {}
		db = self.client[database]
		if not document['text_tweet']:
			result = "bukan data %s (warn), tidak masuk" %document["id"]
		else:
			db[collection].insert(document)
			keterangan = "data %s (inserted sentence clean into database %s collection %s)"%(document["id"],database,collection)
			sentence = document["text_tweet"]
			result["keterangan"] = keterangan
			result["document"] = sentence
			
		return result

	def insert_ner_to_db(self, database, collection, document):
		result = {}
		db = self.client[database]
		if not document['text_tweet']:
			result = "bukan data %s (warn), tidak masuk" %document["id"]
		else:
			db[collection].insert(document)
			keterangan = "data %s (inserted into database %s collection %s)"%(document["id"],database,collection)
			sentence = document["text_tweet"]
			result["keterangan"] = keterangan
			result["document"] = sentence
			
		return result