import re

def nepali_number(word):
    ret_word=re.sub(r'[^a-z0-9 ]+','',word)
    return_word=re.sub("\s\s*" , " ", ret_word)
    return_word=return_word.strip()

    return return_word

def word_filter(word):
    new_word=None
    return_word=None
    asd=['०','१','२','३','४','५','६','७','८','९']
    try:
        word=word.replace('.kaa ','karyalayaa ')
        word=word.replace('pra.','prahari ')
        word=word.replace('kaa.','karyalayaa ')
        word=word.replace('ji.','jilla ')
        word=word.replace('chau.','chauki ')
        word=word.replace('su.','suraksa ')
        word=word.replace('po.','posta ')
        word=word.replace('i.','ilakka ')
        word=word.replace('a.','asthaai ')
        
    except:
            pass
    if 'prahari' in word:

        new_word=re.sub(r'[a-z]*\.','',word)
        if "(" in new_word:
            new_word=new_word.replace("(","")
        elif ")" in new_word:
            new_word=new_word.replace(")","")
            
        
        return_word = nepali_number(new_word)
    else:
        return_word = False

    return return_word

def int_pair(arr):
    j=0
    cunt=[]
    
    if len(arr) != 0:
        for i in range(int(len(arr)/2)):
            tr=(arr[j],arr[j+1],'Jilla Prahari Karyalaya')
            cunt.append(tr)
            
            j+=2
    return cunt

def word_indent(arr):
    a = arr
    b = []          
    c =[]
    
    for i in a:
            for j in a:
                if i[1] - j[0] == -2:
                    if i[1] not in b:
                        b.append(i[1])

                    if j[0] not in b:
                        b.append(j[0])

                    if i[0] not in c:
                        c.append(i[0])

                    if j[1] not in c:
                        c.append(j[1])
    db = int_pair(sorted(list(set(c) - set(b))))
    return db

def word2vec(word):
    from collections import Counter
    from math import sqrt

    # count the characters in word
    cw = Counter(word)
    # precomputes a set of the different characters
    sw = set(cw)
    # precomputes the "length" of the word vector
    lw = sqrt(sum(c*c for c in cw.values()))

    # return a tuple
    return cw, sw, lw

def cosdis(v1, v2):
    # which characters are common to the two words?
    common = v1[1].intersection(v2[1])
    if v1[2] != 0 and v2[2] != 0:
        
        # by definition of cosine distance we have
        return sum(v1[0][ch]*v2[0][ch] for ch in common)/v1[2]/v2[2]
    else:
        return False