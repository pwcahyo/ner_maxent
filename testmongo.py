from pymongo import MongoClient
import re

client = MongoClient()
db = client.bigcities
data = "padang"
key = re.compile("^"+data+"$", re.IGNORECASE)
#print list(db.cities.find({"kota":{"$regex": u''+data}}))
print list(db.cities.find({"kota":{"$regex": u""+data, "$options": "-i"}}))