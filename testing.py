#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
from nltk import word_tokenize
import dbmodel as d
from decimal import Decimal

#create object class database model
dbmodel = d.DBModel()
db_testing = "mar_ner_for_testing";
db_source = "mar_label";


tp = 0
fp = 0
fn = 0
tn = 0
sentences = 0
labels = 0
for date_day in range(1,32):
	day = ""
	day_str = str(date_day)
	if len(day_str) == 1:
		day = "0"+day_str
	else:
		day = day_str

	cursor = dbmodel.get_data_all(db_source,day);
	for doc in cursor :
		if "/" in doc["text_tweet"]:
			sentences+=1
			cur = dbmodel.get_data_one_from_id(db_testing, day, doc["id"])
			for doc2 in cur:
				data_label = doc["text_tweet"]
				data_test = doc2["text_tweet"]
				token_label = word_tokenize(data_label)
				token_test = word_tokenize(data_test)
				if(len(token_label) == len(token_test)):
					for index, label in enumerate(token_label):
						if ("/" in token_label[index]):
							labels+=1
							arr_lab = token_label[index].split("/")
							token_label[index] = arr_lab[0].lower()+"/"+arr_lab[1]

							arr_test = token_test[index].split("/")
							if (token_label[index] == token_test[index]):
								# terpilih benar
								tp+=1
							elif ("/" in token_label[index]) and ("/" not in token_test[index]):
								# tidak terpilih padahal benar
								fn+=1
							elif ("/" in token_test[index]) and (arr_test[1] != arr_lab[1]):
								# terpilih tetapi tidak benar
								fp+=1
							else:
								# tidak terpilih dan tidak benar (TIDAK DIPAKAI)
								tn+=1

								# print "%s : %s"%(token_label[index],token_test[index])
								

print "==========================================="
print "Sentences : %d"%sentences
print "Labels : %d"%labels
print "==========================================="
print "TP : %d"%tp
print "FP : %d"%fp
print "FN : %d"%fn
print "==========================================="
p = Decimal(tp/Decimal((tp+fp)))
r = Decimal(tp/Decimal((tp+fn)))
fm = Decimal(2*(p*r/Decimal(tp+fn)))
print "PRECISION : %.8f"%(Decimal(p).normalize())
print "RECALL : %.8f"%(Decimal(r).normalize())
print "F-Measure : %.8f"%(Decimal(fm).normalize())
print "==========================================="
