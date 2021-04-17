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
