from pymongo import MongoClient
import re

client = MongoClient()

db = client.maret
#print list(db["01"].find({"time_tweet":"1 Mar 15"}))

#select all data in collection
"""
cursor = db["01"].group(
    {
        "key":{"text_tweet":1},
        "reduce": function(curr,result){
           result.id = curr.url 
           result.username = curr.username
           result.time = curr.time_tweet
        },
        initial: {}
     }
)"""

cursor = db["01"].aggregate(
    [
        {"$group": 
        	{"_id": "$url", 
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
        } 
    ]
)


documents = cursor["result"]

for index, document in enumerate(documents):
	#print data
	datas = document["data"]
	for data in datas:
		print data["text_tweet"]

#SELECT SEMUA DATA PADA OBJECT RESULT
#print cursor["result"]

#print data


"""
# CHECK DB MONGO EXIST
dbnames = client.database_names()
if 'juni' in dbnames:
    print "It's there!"
else:
	print "no there"
"""

"""
# SELECT ALL COLLECTION IN DB
db = client.maret
collections = db.collection_names()
#print len(db.collection_names())

for collection in collections:
	print collection
"""

"""
# REGEX FIND KOTA
db = client.bigcities
data = "Bangkalan"
key = re.compile("^"+data+"$", re.IGNORECASE)
#print list(db.cities.find({"kota":{"$regex": u''+data}}))
print len(list(db.cities.find({"kota":re.compile("^"+data+"$", re.IGNORECASE)})))
"""