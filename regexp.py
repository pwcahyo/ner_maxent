#!/usr/bin/python

#kumpulang fungsi reguler expression
import re

w = re.compile(r"(.*)/") 
lbl = re.compile(r"/(.*)") 
num = re.compile(r"(.*)/int") 
tag = re.compile(r"(#\S+)|(@\S+)|(&\S+)|(')")
symbol_train = re.compile(r"[^A-Za-z!/]")
symbol_ner = re.compile(r"[^A-Za-z!]")
#tag = re.compile(r"(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)")
url = re.compile(r"^https?:\/\/.*[\r\n]*", flags=re.MULTILINE)