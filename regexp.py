#!/usr/bin/python

#kumpulang fungsi reguler expression
import re

# get word
w = re.compile(r"(.*)/") 
# get label
lbl = re.compile(r"/(.*)") 
# get number
num = re.compile(r"(.*)/int") 
# get tag # @ &text
tag = re.compile(r"(#\S+)|(@\S+)|(&\S+)|(')")
#get symbol no slice /
symbol_train = re.compile(r"[^A-Za-z!/]")
#get symbol
symbol_ner = re.compile(r"[^A-Za-z]")
#tag = re.compile(r"(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)")
# get url
url = re.compile(r"^https?:\/\/.*[\r\n]*", flags=re.MULTILINE)