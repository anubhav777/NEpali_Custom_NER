import numpy as np
import pandas as pd
import spacy
import nepali_roman as nr
from tqdm import tqdm
from spacy.tokens import DocBin
from googletrans import Translator
import itertools
from itertools import permutations 
import collections
from collections import OrderedDict
import openpyxl
import Levenshtein
import re
from function import *


nlp = spacy.load("en_core_web_sm")

#all excel file reader
xls = pd.ExcelFile('phone-number-2077-09-15.xlsx')
all_df=None

for i in range(7):
    new_df=None
    value = i +1
    name= f'{value} No. State'
    
    new_df = pd.read_excel(xls, value)
    filt_df=new_df[['name', 'phone']]
    
    if i == 0: 
        all_df = filt_df
        
    else:
        all_df = pd.concat([filt_df,all_df],ignore_index=True)

for i in range(len(all_df)):
    new_inp=all_df.iloc[i]['name']
    new_value = nr.romanize_text(new_inp)
    new_text=new_value.strip()
    all_df.iloc[i]['name'] = new_text
    all_df.iloc[i]['phone'] = 'Jilla Prahari Karyalaya'

new_df= all_df.copy()

new_df.to_csv(r'./new_data.csv')   

global_arr=[]
def new_text_finder(link):
    num_array=[]
    gh = link
    new_text = nr.romanize_text(link)
    new_text = nepali_number(new_text)
    top=new_text.split(" ")
    threshold = 0.90 
    
#     new_l= list(set(top) & set(newarr))
  
            # if needed
    for key in new_arr:
        for word in top:

            try:
              

                res = cosdis(word2vec(word), word2vec(key))
                if res != False:
  
                    if res > threshold:

                        pattern = re.compile(rf'{key}[a-z]+')
                        if pattern.match(word):
                            new_text = re.sub(pattern, key, new_text)
            except IndexError:
                pass
#     print(new_text)
#     print(gh)

    
    

    for i in new_text.split(" "):
        if i in new_arr:
            res = [[ele.start(), ele.end() - 1] for ele in re.finditer(rf"{i}", new_text)]
            blo=[txt for txt in re.finditer(rf"{i}", new_text)]
            if num_array == None:
                num_array = res
               
            else:
                for j in res:
                    if j not in num_array:
                        num_array.append(j)

    m=sorted(num_array)

    word_value=word_indent(m)
    
    if word_value != []:
        app_arr=[new_text,word_value]
        global_arr.append(app_arr)
    return word_value
