from nltk.tokenize import RegexpTokenizer
from nltk import tokenize
import nltk

import re
import pkg_resources
from symspellpy.symspellpy import SymSpell, Verbosity
import collections
import csv
nltk.download('punkt')

#-----------------------------Unwanted character removal


fp = open("./Corpus.txt", encoding = "utf-8")

data = fp.read().replace("\n", " ")
fp.close()

#add necessary spaces

p = re.compile(r'(?P<bracket>\()')
s = p.sub(r' \g<bracket> ',data)

p = re.compile(r'(?P<bracket>\))')
s = p.sub(r' \g<bracket> ',s)

p = re.compile(r'(?P<data>\d+\s*)(?P<mm>mm)')
s = p.sub(r'\g<data> \g<mm> ',s)

p = re.compile(r'(?P<data>\d+\s*)(?P<cm>cm)')
s = p.sub(r'\g<data> \g<cm> ',s)

p = re.compile(r'(?P<and>&)')
s = p.sub(r' \g<and> ',s)

p = re.compile(r'(?P<comma>\,)')
s = p.sub(r' \g<comma> ',s)

p = re.compile(r':')
s = p.sub(r'',s)

p = re.compile(r':-')
s = p.sub(r'',s)

p = re.compile(r': -')
s = p.sub(r'',s)

#remove all unwanted spaces
p = re.compile(r'(?P<space>\s+)')
s = p.sub(r' ',s)

p = re.compile(r'(?P<space>\d+\.)\s+(?P<space1>\d+)')
s = p.sub(r'\g<space>\g<space1>',s)

p = re.compile(r'(?P<space>[a-z]\.)(?P<space1>[A-Z])')
s = p.sub(r'\g<space> \g<space1>',s)



print(s)
fp = open("spaceremoved_data.txt",'w')
fp.write(s)
fp.close()

#-----------------------------Unwanted character removal


#-----------------------------Sentence segmentation


fp = open("./spaceremoved_data.txt")
data = fp.read().replace("\n", " ")
fp.close()
result = tokenize.sent_tokenize(data)

outF = open("RemovedSpacesLine.txt", "w")
for line in result:
  # write line to output file
  outF.write(line)
  outF.write("\n")
outF.close()

#-----------------------------Sentence segmentation


