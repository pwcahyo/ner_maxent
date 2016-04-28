#!/usr/bin/python

import maxent as m

#call class maxent
classify = m.maxent()

# pelatihan iis
#==========================================================================
paragraph = []
paragraph.append("di tegal/LOC empat puluh lima/NUM orang menderita/CON dbd. empat puluh satu/NUM meninggal/CON tiga puluh/NUM orang dirawat")
paragraph.append("di malang/LOC 4/NUM orang menderita/CON dbd")
paragraph.append("10/NUM orang mati/CON karena dbd di bantul/LOC")
paragraph.append("warga sleman/LOC 4/NUM orang menderita/CON dbd")
paragraph.append("cirebon/LOC meninggal/CON karena dbd")
paragraph.append("jakarta/LOC meninggal/CON karena dbd")
paragraph.append("empat/NUM warga bandung/LOC meninggal/CON karena dbd")
paragraph.append("lima/NUM warga grobogan/LOC meninggal/CON karena dbd")
paragraph.append("kota/ORG tarakan/LOC 5/NUM orang mati/CON karena dbd")
paragraph.append("pemerintah/ORG tarakan/LOC 5/NUM orang mati/CON karena dbd")
paragraph.append("dinas/ORG kesehatan/ORG sleman/LOC 5/NUM orang mati/CON karena dbd")
paragraph.append("sepuluh/NUM warga klaten/LOC 5/NUM orang mati/CON karena dbd")
paragraph.append("empat/NUM warga solo/LOC tewas/CON terkena/CON dbd")
paragraph.append("empat/NUM warga bantul/LOC tewas/CON terkena/CON dbd")
paragraph.append("enam/NUM warga lumajang/LOC tewas/CON terkena/CON dbd")
paragraph.append("delapan/NUM warga bekasi/LOC tewas/CON terkena/CON dbd")
paragraph.append("enam/NUM warga klaten/LOC tewas/CON terkena/CON dbd")
paragraph.append("satu/NUM warga klaten/LOC tewas/CON terkena/CON dbd")

classification = classify.training_weight_iis(paragraph)

#==========================================================================

# pelatihan NER
sentence = "padang terkena dbd meninggal lima. tujuh orang mati karena dbd di wates"
print classify.training_ner(sentence, classification)
#print len(ner)