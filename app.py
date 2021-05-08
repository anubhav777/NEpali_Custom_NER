import spacy
from tqdm import tqdm
from spacy.tokens import DocBin
import json
import re

new_arr=[]

with open('all_filtered.json') as json_file:
        filt_data = json.load(json_file)
    
for i in filt_data:
  if len(i[1]) != 0 :
    new_arr.append(i)