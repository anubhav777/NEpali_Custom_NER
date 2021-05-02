import re
import nepali_roman as nr
global_arr=[]
hospital_common=['अस्पताल','केन्द्र','गृह','औषधालय','आयुर्वेद','स्वास्थ्यकेन्द्र']
all_hospitals=[]

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
    

def new_text_finder(link):
    num_array=[]
    gh = link
    new_text = nr.romanize_text(link)
    new_text = nepali_number(new_text)
    top=new_text.split(" ")
    threshold = 0.80 
    
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

def web_scrap(src):
    
    source=requests.get(src).text
    soup= BeautifulSoup(source,"html.parser")
    parent= soup.find_all('table',class_='wikitable sortable')
    
    for j in range(len(parent)):
        child = parent[j].find_all('tr')
        for i in range(len(child)):
            if i != 0:
                all_td = child[i].find_all('td')[2].text
                new_txt = re.sub(r'\n','',all_td)
                if new_txt not in cities:
                    
                    cities.append(new_txt)
                else:
                    print('found')
def comm_check(string):
    words = string.split(" ")
    for w in words:
        if w in hospital_common:
            if words[-1] in cities:
                
                new_text=string.rsplit(' ', 1)[0]
                all_hospitals.append(new_text)
                
            else:               
                all_hospitals.append(string)
            break;


def hospital_finder():
    source=requests.get(f'https://ne.wikipedia.org/wiki/नेपालका_अस्पतालहरू').text
    soup= BeautifulSoup(source,"html.parser")
    parent= soup.find('div',{'class':'mw-parser-output'})
    child= parent.find_all('p')
    for i in child:
        poss = i.find_all('a')

        if poss == None:
             comm_check(i.text)
             
        
        else:
            if len(poss) == 1:
                
                comm_check(poss[0].text)
            elif len(poss) > 1:
                
                  for j in poss:
                        if ',' in j.text:
                            old_text = j.text.split(",")
                            new_text = old_text[0]
                            comm_check(new_text)
                        else:
                            comm_check(j.text)
