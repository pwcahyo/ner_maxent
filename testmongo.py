from pymongo import MongoClient
import re

client = MongoClient()
db = client.bigcities
data = "Bangkalan"
key = re.compile("^"+data+"$", re.IGNORECASE)
#print list(db.cities.find({"kota":{"$regex": u''+data}}))
print len(list(db.cities.find({"kota":re.compile("^"+data+"$", re.IGNORECASE)})))