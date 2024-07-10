import spacy
from preprocessing import *
nlp = spacy.load("en_core_web_sm")
#nlp.add_pipe("merge_entities")

#-------------------------------------
# Read cleaned text data
#------------------------------------ 

df = open('Data.txt','r') 
lines = df.readlines()

debugFile = open('Debug.txt', 'w')

#-------------------------------------
# Open file to write triplets
#------------------------------------ 

csvfile = open('NewKG.csv', 'w', newline='\n')
fieldnames = ['ent1', 'rel', 'ent2']
writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
writer.writeheader()

#-------------------------------------
# For each line find chunk dependencies
#------------------------------------ 

error_cnt = 0
for line in lines:
  if line.find('/') != -1:
    continue
  print(line)
  sentence_matadata_df = pd.DataFrame(columns=['chunk_token','chunk_POS','chunk_dep','token_list','index_list','ss_list','root_list'])
  ent1 = line.replace('\n','')
  ent1 = ent1.lower()
  
  #-------------------------------------
  #get supersenses
  #-------------------------------------
  try:
    value1 = supersense_dictionary[ent1]
  except KeyError:
    error_cnt = error_cnt + 1
    #print(error_cnt)
    continue
  ent1_val = pd.DataFrame(value1).T
  ent1_val.columns = ['token', 'pos', 'supersense']  
  supersense = ent1_val['supersense'].tolist()
  pos_list = ent1_val['pos'].tolist()
  #print(supersense)
  doc = nlp(ent1)
  root_list = []
  for chunk in doc.noun_chunks:
    if (len(chunk)>1):
      root_list.append(chunk.root.lemma_)
  
  nlp.add_pipe(nlp.create_pipe('merge_noun_chunks'))
  doc = nlp(ent1)
  
  #for token in doc:
  #    print(token.text, token.pos_, token.dep_)
  sentences = list(doc.sents)
  sent = sentences[0]

  leaf_nodes = []

  root_token = sent.root
  #get all leaf nodes
  final_root_list = []
  cnt = 0
  i = 0
  token_SS_dict = dict()

  for token in sent:   

    if (token.n_lefts + token.n_rights) == 0 :
      leaf_nodes.append(token)

    tokens= token.lemma_.split(' ')
    if (len(tokens)>1):
      root = root_list[cnt]
      cnt = cnt + 1
    else:
      root = token.lemma_
    index = [item for item in range(i, i + len(tokens))]

    ss_list = supersense[i:i + len(tokens)]
    pos_lst = pos_list[i:i + len(tokens)]
    df2 = {'token_list':tokens, 'index_list':index, 'pos_list':pos_lst, 'ss_list':ss_list, 'root_list':root}
    
    token_SS_dict[token] = df2

    i = i + len(tokens)

  #print('token_SS_dict',token_SS_dict)
  #print(sent, leaf_nodes)
  print(leaf_nodes)
  
  object_to_process = []
  verb_to_process = []
  adp_to_process = []
  subj_list = []
  path_aux = []

  #foreach leaf node find path upto root

  for leaf_token in leaf_nodes:
    path_obj = []
    path_adp = []
    path_subj = []
    temp_path_subj = []
    token = leaf_token
    #print('leaf', leaf_token)
    while True:
      #find ancestor
      #print('token',token)
      print(token)
      if token.dep_ == 'attr' and token.pos_ == 'NOUN' or token.pos_ == 'PROPN':
        path_obj.append(token)
      if token.dep_ == 'appos' and token.pos_ == 'NOUN' or token.pos_ == 'PROPN':
        if len(path_obj) != 0:
          prev_obj = path_obj.pop()
          if len(path_adp)!=0:
            prev_adp = path_adp.pop()
            rel, seq = get_relation( prev_obj, prev_adp, token,token_SS_dict)

      if token.dep_ == 'xcomp':
        verb_to_process.append(token)

      if token.pos_ == 'AUX':
        path_aux.append(token)

      if token.dep_ == 'prep':
        path_adp.append(token)

      if token.dep_ == 'nsubj' or token.dep_ == 'nsubjpass':        
        subj_list.append(token)
        subj_list = subj_list + temp_path_subj
        #remove from obj
        #print('before obj', object_to_process,temp_path_subj)
        object_to_process = [i for i in object_to_process if i not in temp_path_subj]
        #print('after obj', object_to_process)
        if len(path_obj) != 0:
          prev_obj = path_obj.pop()
          if len(path_adp)!=0:
            prev_adp = path_adp.pop()
            rel, seq = get_relation( prev_obj, prev_adp, token,token_SS_dict)

     
      #-----------------------process conj
      
      if token.dep_ == 'conj':

        if token.pos_ == 'NOUN' or token.pos_ == 'PROPN':
          if len(path_obj) != 0:
            prev_obj = path_obj.pop()
            if len(path_adp)!=0:
              prev_adp = path_adp.pop()
              rel, seq = get_relation( prev_obj, prev_adp, token,token_SS_dict)
        else:
          verb_processed = False
          right_childeren = token.rights
          child = None
          for r_child in right_childeren:
            child = r_child
            break
          if child != None:
            if child.dep_ == 'pobj' or child.dep_ == 'dobj':
              verb_processed = True
              rel, seq = get_relation( token, None, child, token_SS_dict)
              #print('token',token)

          if token.pos_ == 'VERB' and not verb_processed:
            verb_to_process.append(token)
          elif not verb_processed:
            object_to_process.append(token)
            temp_path_subj.append(token)
            #print('temp_path_subj',token,temp_path_subj)

      


      if token.dep_ == 'pobj' or token.dep_ == 'dobj':

        if len(path_obj) != 0:
          prev_obj = path_obj.pop()
          if len(path_adp)!=0:
            prev_adp = path_adp.pop()
            rel, seq = get_relation( token, prev_adp, prev_obj,token_SS_dict)

        path_obj.append(token)

      if token.pos_ == 'ADJ':
        #print('ADJ', token, len(path_obj), len(path_adp))
        if len(path_obj) != 0:
          prev_obj = path_obj[0]
          if len(path_adp)!=0:
            prev_adp = path_adp.pop()
            rel, seq = get_relation( token, prev_adp, prev_obj,token_SS_dict)

      #print('token',token)
      
      for ancestor in token.ancestors:
        ans = ancestor
        #print('ans',ans)
        break

      if token.pos_ == 'AUX' and ans.pos_ == 'VERB':
        verb_to_process.append(ans)

      if (ans == root_token):
        if token.pos_ == 'VERB':
          print(token)
          verb_to_process.append(token)
          
        if ans.dep_ == 'ROOT' and (ans.pos_ == 'NOUN' or ans.pos_ == 'PROPN'):
          #print("In root")
          if len(path_obj) != 0:
            prev_obj = path_obj.pop()
            if len(path_adp)!=0:
              prev_adp = path_adp.pop()
              rel, seq = get_relation( ans, prev_adp, prev_obj,token_SS_dict)
              #print('ent1:', ans.text, 'rel:', prev_adp.text, 'ent2:', prev_obj.text)
        object_to_process = object_to_process + path_obj
        adp_to_process = adp_to_process + path_adp
        
        break
       # if is_last_obj_processed:
        #  break
        #else:
          # find subject of root
         # object_to_process.append()
          #findSubject()
      else:
        #print('ans',ans)
        token = ans

  #print(subj_list,object_to_process, verb_to_process)

  subj_list = set(subj_list)
  object_to_process = set(object_to_process)
  verb_to_process = set(verb_to_process)

  #if len(subj_list)!=0 and len(object_to_process)==0 and len(verb_to_process)==0:



  if len(subj_list)!=0 and len(object_to_process)!=0:
    for sub in subj_list:
      for obj in object_to_process:
        if len(adp_to_process) != 0:
          rel = adp_to_process.pop()
        else:
          rel = root_token
        rel, seq = get_relation( sub, rel, obj,token_SS_dict)

  if len(subj_list) and len(verb_to_process)!=0:
    for sub in subj_list:
      for obj in verb_to_process:
        rel, seq = get_relation( obj, None, sub,token_SS_dict)

  nlp.remove_pipe('merge_noun_chunks')