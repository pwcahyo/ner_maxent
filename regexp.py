#!/usr/bin/python

#kumpulang fungsi reguler expression
import re

# get word
w = re.compile(r"(.*)/") 
# get label
lbl = re.compile(r"/(.*)") 
# get number
#get symbol no slice / dan juga # @ &text
symbol_train = re.compile(r"(#\S+)|(@\S+)|(&\S+)|(')|[^A-Za-z!/]")
#get symbol dan juga # @ &text
symbol_ner = re.compile(r"(#\S+)|(@\S+)|(')|[^A-Za-z!^0-9!.]")
#tag = re.compile(r"(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)")
# get url
url = re.compile(r"^https?:\/\/.*[\r\n]*", flags=re.MULTILINE)