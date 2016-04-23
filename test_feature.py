from nltk import word_tokenize
from pymongo import MongoClient
from nltk import MaxentClassifier, classify
import re
import numpy as np

#gazzeter
gaz_sp = ["jiwa","orang","warga","pasien","kasus"]
gaz_o = ["demam", "berdarah", "dengue", "dbd", "sakit", "db"]
gaz_knd = ["meninggal", "dirawat", "korban", "penderita", "tewas", "keritis", "mati"]
gaz_org = ["pemkot", "dinkes", "warga", "pemda", "pemkab", "dinas", "pemerintah", "kabupaten", "rs"]

#mongodb connection
client = MongoClient()
db = client.bigcities

#regex find word (w) and label (lbl), especially in data train
w = re.compile(r"(.*)/") 
lbl = re.compile(r"/(.*)") 

#method sett binary features
def template_feature(token, label, index):
	# apabila other maka return None
	if label[index] == "O": 
		return 
	# else other maka continue
	"""ORG = f1,f2,f3 | LOC = f4,f5,f6 | NUM = f7,f8 | CON = f9,f10"""
	f1 = token[index] in gaz_org
	f2 = token[index-1] == "di"
	f3 = token[index] in gaz_org
	f4 = len(list(db.cities.find({"kota":re.compile("^"+token[index]+"$", re.IGNORECASE)})))>=1
	f5 = token[index-1] == "di"
	f6 = label[index-1] == "ORG"
	try:
	    data = token[index+1]
	except IndexError:
	    data = "null"
	f7 = data in gaz_knd or data in gaz_sp
	f8 = token[index].isdigit()
	f9 = token[index] in gaz_knd
	f10 = token[index-1] in gaz_sp
	"""
	feature entitas O / Other 
	f11 = token[index] in gaz_o or token[index] in gaz_sp
	f12 = np.sum([f1, f2, f3, f4, f5, f6, f7, f8, f9, f10]) == 0
	"""
#	lst = np.array([f1, f2, f3, f4, f5, f6, f7, f8, f9, f10, f11, f12])
	lst = np.array([f1, f2, f3, f4, f5, f6, f7, f8, f9, f10])
	b_ft = lst*1

#	result = (dict(f1=b_ft[0], f2=b_ft[1], f3=b_ft[2], f4=b_ft[3], f5=b_ft[4], f6=b_ft[5], f7=b_ft[6], f8=b_ft[7], f9=b_ft[8], f10=b_ft[9], f11=b_ft[10], f12=b_ft[11]), label[index])
	result = (dict(f1=b_ft[0], f2=b_ft[1], f3=b_ft[2], f4=b_ft[3], f5=b_ft[4], f6=b_ft[5], f7=b_ft[6], f8=b_ft[7], f9=b_ft[8], f10=b_ft[9]), label[index])
	return result


sentence = []
sentence.append("3/NUM warga/ORG situbondo/LOC meninggal/CON karena/O dbd/O")
sentence.append("di/O tegal/LOC 4/NUM orang/O menderita/CON dbd/O")
sentence.append("jombang/LOC 5/NUM warga/O terkena/CON dbd/O")
sentence.append("10/NUM orang/O mati/CON karena/O dbd/O di/O bantul/LOC")


label = []
train = []

"""
# single word test
sentence = "di/O tegal/LOC 4/NUM orang/O menderita/CON dbd/O"
token = word_tokenize(sentence)
for index, data in enumerate(token):
	label.append(lbl.search(token[index]).group(1))
	token[index] = w.search(token[index]).group(1)
result = template_feature(token, label, 5)
print result
"""

# loop sentence training data
for index, data in enumerate(sentence):
	token = word_tokenize(data)
	for index, data in enumerate(token):
		#add label to array
		label.append(lbl.search(token[index]).group(1))
		#add word to array
		token[index] = w.search(token[index]).group(1)
	for index, data in enumerate(token):
		#feature processing
		result = template_feature(token, label, index)
		train.append(result) 
# filter array empty/none karena Other atau entitas O tidak diproses
train_set = filter(None, train)
#print train_set

me_classifier = MaxentClassifier.train(train_set, 'iis', trace=10, max_iter=100, min_lldelta=0.8)
test = [(dict(f1=0, f2=0, f3=0, f4=0, f5=0, f6=0, f7=0, f8=1, f9=0, f10=0))]
print
print ' '*11+''.join(['      test[%s]  ' % i for i in range(len(test))])
print ' '*4+'p(ORG)    p(LOC)    p(NUM)    p(CON)'*len(test)
print '-'*(24+18*len(test))
for featureset in test:
	pdist = me_classifier.prob_classify(featureset)
	print '%10.4f%10.4f%10.4f%10.4f' % (pdist.prob('ORG'), pdist.prob('LOC'), pdist.prob('NUM'), pdist.prob('CON')),
print
