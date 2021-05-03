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

cities=[]
rom_cities=[]

web_scrap('https://en.wikipedia.org/wiki/List_of_cities_in_Nepal')
web_scrap('https://en.wikipedia.org/wiki/List_of_gaunpalikas_of_Nepal')


with open('cities.json','w',encoding='utf-8') as outfile:
    json.dump(cities,outfile,ensure_ascii=False)

with open('data.json') as json_file:
    data = json.load(json_file) 

for i in cities:
    new_txt=nr.romanize_text(i)
    rom_cities.append(new_txt)
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
with open('filtered.json') as json_file:
    ol_data = json.load(json_file)

 train_text=[]
train_ent=[]

for i in range(len(data)):

    train_text.append(data[i][0])
    train_ent.append({'entities':data[i][1]})

train_data=list(zip(train_text,train_ent))
   
for i in range(len(all_df)):
    new_inp=all_df.iloc[i]['name']
    new_value = nr.romanize_text(new_inp)
    new_text=new_value.strip()
    all_df.iloc[i]['name'] = new_text
    all_df.iloc[i]['phone'] = 'Jilla Prahari Karyalaya'

    new_df= all_df.copy()

    new_df.to_csv(r'./new_data.csv')   

        
    filt_arr=[]
    nlp=spacy.blank('en')
    db = DocBin()
    i=0
    excel_arr=[]
    for text, annot in tqdm(train_data): # data in previous format
        doc = nlp.make_doc(text) # create doc object from text
        ents = []
        clean_txt = []
        for start, end, label in annot["entities"]: # add character indexes
            new_end= end+1
            span = doc.char_span(start, new_end, label=label, alignment_mode="contract")
            if span is None:
                print("Skipping entity")
            else:
                
    #             if len(span) >= 1:
    #                 second_ents.append(span)
                    
                
                if " " in str(span):
                    txt = str(span)
                    # ents.append(span)
                    if any(word in txt for word in common_words):
                    pattern = re.compile(r'[a-z]+\s[a-z]+\s[a-z]{3}')
                    if pattern.match(txt):
                        if txt not in rem_words:
                        if 'prahari' in txt:
                            if len(clean_txt) == 0:
                            new_ent=({'entities': [[start, end, 'Jilla Prahari Karyalaya']]})
                            arr=[text,new_ent]
                            clean_txt = arr
                            excel_arr.append(txt)
                            print(txt)
                            else:
                            add_ent=[start, end, 'Jilla Prahari Karyalaya']
                            clean_txt[1]['entities'].append(add_ent)
                            excel_arr.append(txt)
                            
                            
                            
        if len(clean_txt) != 0:
            filt_arr.append(clean_txt)
        
        i+=1
    #     if ents!= []:
        
    #         doc.ents = ents # label the text with the ents
    #         db.add(doc)
    #     i+=1
    # db.to_disk("./data/train.spacy")
rom_cities=[]
for i in cities:
    new_txt=nr.romanize_text(i)
    rom_cities.append(new_txt)

with open('rom_cities.json','w',encoding='utf-8') as outfile:
    json.dump(rom_cities,outfile,ensure_ascii=False)

with open('hospital.json',encoding="utf8") as json_file:
    hospital = json.load(json_file)

new_arr=[]
for i in result:
    ins_arr=[i,[]]
    new_arr.append(ins_arr)

#hospital entity
for i in range(len(new_arr)):
    for j in hospital:
        if j in new_arr[i][0]:
             res = [[ele.start(), ele.end() - 1] for ele in re.finditer(rf"{j}", new_arr[i][0])]
             new_val=[res[0][0],res[0][1],"Nepal Hospital"]
             if new_val not in new_arr[i]:
                 new_arr[i][1].append(new_val)
                 
            

            
#              print(res[0])

#gaaunpalika nagarpaalika mahaanagarapalika entry
for i in range(len(new_arr)):
    new_text = new_arr[i][0]
    top = new_text.split(" ")
    for j in range(len(top)):
        if top[j] == 'gaaunpaalikaa'or top[j] == 'nagrapaalika' or top[j] == 'mahaanagarapaalikaa':
            if j > 0:
                res = [[ele.start(), ele.end() - 1] for ele in re.finditer(rf"{top[j-1]} {top[j]}", new_arr[i][0])]
                if len(res) == 1:        
                    new_val=[res[0][0],res[0][1],"gaaunpaalikaa/nagrapaalika/mahaanagarapaalikaa"]
                    if new_val not in new_arr[i]:
                         new_arr[i][1].append(new_val)
                else:
                    for k in range(len(res)):                 
                        new_val=[res[k][0],res[k][1],"gaaunpaalikaa/nagrapaalika/mahaanagarapaalikaa"]
                        if new_val not in new_arr[i]:
                             new_arr[i][1].append(new_val)
                    print(i)

#cities entity
try_ar=[]
for i in range(len(new_arr)):
    new_text = new_arr[i][0]
    top = new_text.split(" ")
    
    for j in range(len(top)):
        
        if top[j] in rom_cities:
            if j != (len(top)-1):
                if top[j+1] != 'gaaunpaalikaa' and top[j+1] != 'nagrapaalika' and top[j+1] != 'mahaanagarapaalikaa':
                     res = [[ele.start(), ele.end() - 1] for ele in re.finditer(rf"{top[j]}", new_arr[i][0])] 
                     if len(res) == 1:        
                        new_val=[res[0][0],res[0][1],"Nepal cities"]
                        if new_val not in new_arr[i]:
                             new_arr[i][1].append(new_val)
                     else:
                        start = []
                        end = []
                        for l in range(len(new_arr[i][1])):
                            start.append(new_arr[i][1][l][0])
                            end.append(new_arr[i][1][l][1])
                        print(start,end,i)  
                        for k in range(len(res)):                 
                            new_val=[res[k][0],res[k][1],"Nepal cities"]
                            if res[k][0] not in start and res[k][1] not in end:
                                if new_val not in new_arr[i]:
                                     new_arr[i][1].append(new_val)
                                            