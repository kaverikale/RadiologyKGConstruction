from information_extraction import IE
#--------------------------------demo
def remove_measurement(lines):
  ###print(lines)
  measure_unit = re.compile(r'(\d+ x \d+ x \d+ (mm|cm|cc))|(\d+.\d+ x \d+.\d+ x \d+.\d+ (mm|cm|cc))|(\d+ x \d+.\d+ x \d+.\d+ (mm|cm|cc))|(\d+ x \d+.\d+ x \d+ (mm|cm|cc))|(\d+ x \d+.\d+ (mm|cm|cc))|(\d+.\d+ x \d+ (mm|cm|cc))|(\d+.\d+ x \d+.\d+ (mm|cm|cc))|(\d+ x \d+ (mm|cm|cc))|(\d+ (cm|mm|cc))|(\d+.\d+ (cm|mm|cc))')
  newlines = []
  for line in lines:
    temp = re.sub(' measuring | measures | measure | vol | volume ', ' ', line)
    temp = re.sub(measure_unit, '', temp)
    temp = re.sub('\s+',' ', temp)
    newlines.append(temp)

  return newlines
    

def get_path_desc(lines):
  #-------------------remove all created files
  !rm FindingTriplets.csv
  !rm SuggestiveTriplets.csv
  !rm Triplets.csv
  !rm TripletsKG.csv
  !rm edges.txt
  organ = 'kidney'


  #-------------------Information Extraction

  lines_without_measure = remove_measurement(lines)
  #data_fl = open('Data_without_measure.txt','a')
  #data_fl.write(lines_without_measure[0] +'\n')
  #return
  print('size remove', lines_without_measure)
  #lines_without_measure = lines

  ie = IE(lines_without_measure)
  is_suggestive = ie.extract_information(lines_without_measure, lines)

  
  size_list = ie.extract_measurement(lines[0])

  df = pd.read_csv('TripletsKG.csv', delimiter=',')
  str_final = ''
  for index, row in df.iterrows():
    str_final = str_final + ", (" + row["ent1"] +','+ row["rel"] + ',' + row["ent2"] + ')'

  
  #--------------------------find missing entities from static KG and dynamic KG
  return str_final

#out = get_path_desc(['uterus is anteverted and normal in size shape contour with uniform echotexture'])
#print(path_desc)


lines = pd.read_csv('IE_input.csv', delimiter = '\t')
fl = open('IE.txt','w')

for index, row in lines.iterrows():
  line = row['path_desc']
  input = row['Input']
  #target = row['target1']
  print(line)
  ie = get_path_desc([line])
  try:
    fl.write(input + '\t' + line + '\t' + ie + '\n')
  except TypeError:
    continue
