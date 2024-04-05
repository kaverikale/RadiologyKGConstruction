import re
import nltk.data


output_file = open("./in_data/CleanData0.txt",'w')

with open("./CleanData.txt",'r') as file: 
    words = []
    # reading each line 
    i = 0  
    char_count = 0  
    for line in file: 
        print(len(line))	
        char_count = char_count + len(line)
        if (char_count <= 5000):
            output_file.write(line+" ")
        else : 
            char_count = len(line) 
            i = i+1
            output_file.close()
            file_name = str("./in_data/CleanData" +str(i)+".txt")
            output_file = open(file_name,'w')
            output_file.write(line+" ")

output_file.close()


