from nltk.tokenize import RegexpTokenizer
from nltk import tokenize
import nltk

import re
import pkg_resources
from symspellpy.symspellpy import SymSpell, Verbosity
import collections
import csv
nltk.download('punkt')



#-----------------------------Create Dictionary

sym_spell = SymSpell()
corpus_path = "./RemovedSpacesLine.txt"
sym_spell.create_dictionary(corpus_path)

words = list(sym_spell.words)
print(len(sym_spell.words))
with open("Dictionary.csv", 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=' ')    
    writer.writerows(sym_spell.words.items())
    
#-----------------------------Create Dictionary
