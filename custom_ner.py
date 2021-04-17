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