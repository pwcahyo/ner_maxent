#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

from pymongo import MongoClient

class DBModel:

	client = MongoClient()

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
		"""

		#coba get satu DATA
		res = []
		ok = []
		data = {}
		hasil = {}
		tweet = {}
		coba = {}
		tweet["text_tweet"] = u"G Dana U Demam Berdarah Bupati JOMBANG AKAN BELI 918 Sepeda Motor U Pejabat 10 MILYAR"
		tweet["text_tweet"] = u"portalsurya kasus dbd di jember naik dua kali lipat belum klb"
		ok.append(tweet)
		data["data"] = ok
		res.append(data)
		hasil["result"] = res
		
		return hasil
		"""

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

		

	def get_data(self, database, collection):
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

	def bulk_insert(self, database, collection, documents):
		db = self.client[database]
		results = db[collection].insert(documents)

		return results

	def insert_sentence_clean(self, database, collection, document):
		result = {}
		db = self.client[database]
		if not document['text_tweet']:
			result = "data %s error, tidak masuk" %document["id"]
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
			result = "data %s error, tidak masuk" %document["id"]
		else:
			db[collection].insert(document)
			keterangan = "data %s (inserted into database %s collection %s)"%(document["id"],database,collection)
			sentence = document["text_tweet"]
			result["keterangan"] = keterangan
			result["document"] = sentence
			
		return result