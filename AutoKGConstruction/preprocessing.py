import pandas as pd
import csv

import json

#-------------------------------------
# Read supersense dictionary
#------------------------------------ 

supersense_dictionary = {}
with open('SS_dictionary.json') as json_file:
    supersense_dictionary = json.load(json_file)
#print(supersense_dictionary)

#-------------------------------------
# Read ultrasound term dictionary
#------------------------------------ 

rad_csv = pd.read_csv('radiology_dictionary.csv',names=['entity','category']) 
rad_dict = dict(zip(rad_csv.entity, rad_csv.category))


#-------------------------------------
# Read supersence-relations mapping
#------------------------------------ 

rel_ss_df = pd.read_csv("SS_rel_mapping.csv", names=['SS','rel'])

dict_from_csv = dict(zip(rel_ss_df.SS, rel_ss_df.rel))

#-------------------------------------
# Read ultrasound term dictionary
#------------------------------------ 

#dict_df = pd.read_csv('UltrasoundDictionary.csv',names=['entity']) 
dict_list = rad_csv['entity'].tolist()

#dict_list = [_ for i in range(len(dict_list)) for _ in dict_list[i]]

#print(dict_list[0:20])
#--------------------------------------------------------------
#  find max substring
#--------------------------------------------------------------       
def substringSieve(string_list):
  out = []
  for s in string_list:
    if not any([s in entity for entity in string_list if s != entity]):
      out.append(s)
  return out

def get_pos(word, tokens,pos_list):
  try :
    index = tokens.index(word)
  except ValueError :
    index  = 0
  
  return pos_list[index]


def get_property_relation(ent_1,ent_2, single_entity):
  
  seq = 1
  rel = 'PropertyOf'
  try:
    cat1 = rad_dict[ent_1]
  except KeyError as e:
    cat1 = 'property'
  try:
    cat2 = rad_dict[ent_2]
  except KeyError as e:
    cat2 = 'property'
  if cat1 == 'anatomy' and cat2 == 'anatomy':
    rel = 'PartOf'
    #depend on adp : todo
    if single_entity:
      seq = 2
    else:
      seq = 1

  elif cat1 == 'finding' and cat2 == 'anatomy':
    rel = 'FoundIn'
    seq = 1
  elif cat1 == 'descriptor' and cat2 == 'anatomy':
    rel = 'PropertyOf'
    seq = 1
  elif cat1 == 'property' and cat2 == 'finding':
    rel = 'PropertyOf'
    seq = 1
  elif cat1 == 'property' and cat2 == 'anatomy':
    rel = 'PropertyOf'
    seq = 1
  elif cat1 == 'descriptor' and cat2 == 'finding':
    rel = 'PropertyOf'
    seq = 1

  elif cat2 == 'descriptor' and cat1 == 'anatomy':
    rel = 'DescriptorOf'
    seq = 2
  elif cat2 == 'property' and cat1 == 'finding':
    rel = 'PropertyOf'
    seq = 2
  elif cat2 == 'property' and cat1 == 'anatomy':
    rel = 'PropertyOf'
    seq = 2
  elif cat2 == 'descriptor' and cat1 == 'finding':
    rel = 'PropertyOf'
    seq = 2



  return rel, seq

def process_noun_chunk(ent_1, token_SS_dict):
  token1 = token_SS_dict[ent_1]
  token_list = token1['token_list']
  root_list = token1['root_list']
  pos_list = token1['pos_list']
  #print(token_list, root_list,pos_list )
  #get root of element


  dictinary_match_list  = [s for s in dict_list if (" " + s.strip() + " ") in " " + ent_1.lemma_.strip() + " "]
  dictinary_match_list = substringSieve(dictinary_match_list)   
  #print("dictinary_match_list",dictinary_match_list)

    #find unmatched entities
  unmatched_entities = []
  if (len(dictinary_match_list)!=0):
    matched_sent = ' '.join(dictinary_match_list)
    unmatched_entities = set(token_list).difference(set(matched_sent.split()))

      #unmatched_entities = unmatched_entities +  [item for item in token_list if item not in dict_item]
  else:
    unmatched_entities = token_list

  #print('unmatched',unmatched_entities)
  if (len(dictinary_match_list)!=0):
    root_element_list = [s for s in dictinary_match_list if str(root_list) in s]
    if (len(root_element_list) != 0):
      root_element = root_element_list[0]
    else:
      root_element = str(root_list)        
  else:
    root_element = str(root_list)


  for s in dictinary_match_list:
      #print('s ',s)
    if s != root_element:
      s_pos = get_pos(s,token_list, pos_list )
      if s_pos in (['PNOUN','NOUN','ADJ']):

        rel, seq = get_property_relation(s, root_element, True)
          
        if seq == 1:
          #writer.writerow({'ent1': s , 'rel' : rel ,'ent2': root_element })
          print('ent1: ', s  , 'rel: ', rel ,'ent2: ',  root_element)
        else:
          #writer.writerow({'ent1': root_element , 'rel' : rel ,'ent2': s })
          print('ent1: ', root_element  , 'rel: ', rel ,'ent2: ',  s)
  
  for word in unmatched_entities:
    #print('word', word)
    s_pos = get_pos(word,token_list, pos_list)
    #print(type(word), type(root_element))
    if word != root_element:
      if s_pos in (['PNOUN','NOUN','ADJ']):
        writer.writerow({'ent1': word , 'rel' : 'PropertyOf' ,'ent2': root_element })
        print('ent1: ', word , 'rel: PropertyOf' ,'ent2: ',  root_element)

  return root_element


def get_relation(ent_1, verb, ent_2, token_SS_dict):
  print('Input : ',ent_1, verb, ent_2)

  #---------------------process entity 1

  root_element1 = process_noun_chunk(ent_1, token_SS_dict)
  root_element2 = process_noun_chunk(ent_2, token_SS_dict)

  #----------------------------------

  token1 = token_SS_dict[ent_1]
  token1_list = token1['token_list']
  root1_list = token1['root_list']
  pos1_list = token1['pos_list']

  token2 = token_SS_dict[ent_2]
  token2_list = token2['token_list']
  root2_list = token2['root_list']
  pos2_list = token2['pos_list']
  seq = 1
  rel = 'PropertyOf'
  if verb == None:
    rel, seq = get_property_relation(root_element1, root_element2, False)
    if seq == 1:
      #writer.writerow({'ent1': s , 'rel' : rel ,'ent2': root_element })
      print('ent1: ', root_element1  , 'rel: ', rel ,'ent2: ',  root_element2)
    else:
      #writer.writerow({'ent1': root_element , 'rel' : rel ,'ent2': s })
      print('ent1: ', root_element2  , 'rel: ', rel ,'ent2: ',  root_element1)
  
 
  else:

    try:
      cat1 = rad_dict[root_element1]
    except KeyError as e:
      cat1 = 'NotFound'
    try:
      cat2 = rad_dict[root_element2]
    except KeyError as e:
      cat2 = 'NotFound'

    if cat1 == 'NotFound' or cat2 == 'NotFound':
      varb_token = token_SS_dict[verb]
      verb_SS_list = varb_token['ss_list']
      ss = verb_SS_list[0]
      rel = dict_from_csv[ss]
      print('ent1:', root_element1, 'rel:', rel, 'ent2:', root_element2)

    else:

      if cat1 == 'anatomy' and cat2 == 'anatomy':
        rel = 'PartOf'
        #depend on adp : todo
        seq = 1
      elif cat1 == 'finding' and cat2 == 'anatomy':
        rel = 'FoundIn'
        seq = 1
      elif cat1 == 'descriptor' and cat2 == 'anatomy':
        rel = 'PropertyOf'
        seq = 1
      elif cat1 == 'property' and cat2 == 'finding':
        rel = 'PropertyOf'
        seq = 1
      elif cat1 == 'property' and cat2 == 'anatomy':
        rel = 'PropertyOf'
        seq = 1

      elif cat2 == 'descriptor' and cat1 == 'anatomy':
        rel = 'DescriptorOf'
        seq = 2
      elif cat2 == 'property' and cat1 == 'finding':
        rel = 'FoundIn'
        seq = 1
      elif cat2 == 'property' and cat1 == 'anatomy':
        rel = 'PropertyOf'
        seq = 2
      
      if seq == 1:
        print('ent1:', root_element1, 'rel:', rel, 'ent2:', root_element2)
      else:
        print('ent1:', root_element2, 'rel:', rel, 'ent2:', root_element1)

  return rel, seq