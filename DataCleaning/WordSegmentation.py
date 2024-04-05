import pkg_resources
from symspellpy.symspellpy import SymSpell
import re

import nltk.data

sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
dictionary_path = "./Dictionary.csv"

loaded = sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1)
print(loaded)

#sym_spell.load_bigram_dictionary(bigram_path, term_index=0, count_index=2)

output_file = open("./CleanData.txt",'w')

with open("./RemovedSpacesLine.txt",'r') as fl: 
    words = []
    # reading each line     
    for line in fl: 	
        print(line)
        result = sym_spell.word_segmentation(line, ignore_token= r'\d+|\,')
        print(result)
        output_file.write(result.corrected_string + ".\n")

output_file.close()


