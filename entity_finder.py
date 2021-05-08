import json
import re
import spacy
from web_scrape import Web_scrape
from tqdm import tqdm
from spacy.tokens import DocBin

class Entities:
    def __init__(self,array=None):
        self.array = array
        self.entity_arr = Web_scrape.json_to_array('all_filtered.json')
    
    def entity_filt(num1,num2,arr,endarr,no):
        bol = True
        
        if len(arr) != 0:
            for i in range(len(arr)):
                if arr[i] <= num1 <= endarr[i] or arr[i] <= num2 <= endarr[i]:
                    print(arr[i],endarr[i],num1,num2,no)
                    return False
        return True
        
    



    def hospital_entity_finder(self):
        for i in range(len(self.entity_arr)):
            for j in hospital:
                if j in self.entity_arr[i][0]:
                    res = [[ele.start(), ele.end() - 1] for ele in re.finditer(rf"{j}", self.entity_arr[i][0])]
                    new_val=[res[0][0],res[0][1],"Nepal Hospital"]
                    if new_val not in self.entity_arr[i][1]:
                        self.entity_arr[i][1].append(new_val)
    
    def municipality_entity_finder(self):
        for i in range(len(self.entity_arr)):
            new_text = self.entity_arr[i][0]
            top = new_text.split(" ")
            for j in range(len(top)):
                if top[j] == 'gaaunpaalikaa'or top[j] == 'nagrapaalika' or top[j] == 'mahaanagarapaalikaa':
                    if j > 0:
                        res = [[ele.start(), ele.end() - 1] for ele in re.finditer(rf"{top[j-1]} {top[j]}", self.entity_arr[i][0])]
                        if len(res) == 1:        
                            new_val=[res[0][0],res[0][1],"gaaunpaalikaa/nagrapaalika/mahaanagarapaalikaa"]
                            if new_val not in self.entity_arr[i][1]:
                                self.entity_arr[i][1].append(new_val)
                                gaaun_count.append(top[j])
                        else:
                            for k in range(len(res)):                 
                                new_val=[res[k][0],res[k][1],"gaaunpaalikaa/nagrapaalika/mahaanagarapaalikaa"]
                                if new_val not in self.entity_arr[i][1]:
                                    self.entity_arr[i][1].append(new_val)

    def jilla_prahari_karyala(self):
        
        filt_arr=[]
        nlp=spacy.blank('en')
        db = DocBin()
        i=0
        excel_arr=[]
        for text, annot in tqdm(self.array): # data in previous format
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
            
        return filt_arr
    
    def city_entity_finder(self):
        for i in range(len(self.enity_arr)):
            new_text = self.enity_arr[i][0]
            top = new_text.split(" ")
            
            for j in range(len(top)):
                
                if top[j] in rom_cities:
                    if j != (len(top)-1):
                        if top[j+1] != 'gaaunpaalikaa' and top[j+1] != 'nagrapaalika' and top[j+1] != 'mahaanagarapaalikaa':
                            res = [[ele.start(), ele.end() - 1] for ele in re.finditer(rf"{top[j]}", self.enity_arr[i][0])] 
                            if len(res) == 1:
                                start = []
                                end = []
                                if len(self.enity_arr[i][1]) != 0:
                                    for l in range(len(self.enity_arr[i][1])):
                                        if self.enity_arr[i][1][l][2] != 'Nepal cities':
                                            start.append(self.enity_arr[i][1][l][0])
                                            end.append(self.enity_arr[i][1][l][1])
                                
                                new_val=[res[0][0],res[0][1],"Nepal cities"]
                                ent_f=entity_filt(res[0][0],res[0][1],start,end,i)
                                if ent_f != False:
                                    if new_val not in self.enity_arr[i][1]:
                                        self.enity_arr[i][1].append(new_val)
                                        
                                        
                            else:
                                start = []
                                end = []
                                if len(self.enity_arr[i][1]) != 0:
                                    for l in range(len(self.enity_arr[i][1])):
                                        if self.enity_arr[i][1][l][2] != 'Nepal cities':
                                            start.append(self.enity_arr[i][1][l][0])
                                            end.append(self.enity_arr[i][1][l][1])
                                
                                for k in range(len(res)):                 
                                    new_val=[res[k][0],res[k][1],"Nepal cities"]
                                    ent_f=entity_filt(res[k][0],res[k][1],start,end,i)
                                    if ent_f != False:
                                    
                                    
                                        if new_val not in self.enity_arr[i][1]:
                                            self.enity_arr[i][1].append(new_val)

    def all_enties(self):
        self.hospital_entity_finder()
        self.jilla_prahari_karyala()
        self.municipality_entity_finder()
        return self.entity_arr

                                        
                                        
                            

