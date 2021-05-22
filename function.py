import re
import nepali_roman as nr
from web_scrape import Web_scrape
import pandas as pd
import spacy
from entity_finder import Entities
import schedule
import time

cron = True


def excel_reader():
    xls = pd.ExcelFile('phone-number-2077-09-15.xlsx')
    all_df = None

    for i in range(7):
        new_df = None
        value = i + 1
        name = f'{value} No. State'

        new_df = pd.read_excel(xls, value)
        filt_df = new_df[['name', 'phone']]

        if i == 0:
            all_df = filt_df

        else:
            all_df = pd.concat([filt_df, all_df], ignore_index=True)
    return all_df


def nepali_word_filter(word):
    ret_word = re.sub(r'[^a-z0-9 ]+', '', word)
    return_word = re.sub("\s\s*", " ", ret_word)
    return_word = return_word.strip()

    return return_word


def word_filter(word):
    new_word = None
    return_word = None
    asd = ['०', '१', '२', '३', '४', '५', '६', '७', '८', '९']
    try:
        word = word.replace('.kaa ', 'karyalayaa ')
        word = word.replace('pra.', 'prahari ')
        word = word.replace('kaa.', 'karyalayaa ')
        word = word.replace('ji.', 'jilla ')
        word = word.replace('chau.', 'chauki ')
        word = word.replace('su.', 'suraksa ')
        word = word.replace('po.', 'posta ')
        word = word.replace('i.', 'ilakka ')
        word = word.replace('a.', 'asthaai ')

    except:
        pass
    if 'prahari' in word:

        new_word = re.sub(r'[a-z]*\.', '', word)
        if "(" in new_word:
            new_word = new_word.replace("(", "")
        elif ")" in new_word:
            new_word = new_word.replace(")", "")

        return_word = nepali_word_filter(new_word)
    else:
        return_word = False

    return return_word


def int_pair(arr):
    j = 0
    new_arr = []

    if len(arr) != 0:
        for i in range(int(len(arr)/2)):
            tr = (arr[j], arr[j+1], 'Jilla Prahari Karyalaya')
            new_arr.append(tr)

            j += 2
    return new_arr


def word_indent(arr):
    a = arr
    b = []
    c = []

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


def text_finder(link):
    num_array = []
    gh = link
    new_text = nr.romanize_text(link)
    new_text = nepali_word_filter(new_text)
    top = new_text.split(" ")
    threshold = 0.80

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

    for i in new_text.split(" "):
        if i in new_arr:
            res = [[ele.start(), ele.end() - 1]
                   for ele in re.finditer(rf"{i}", new_text)]
            blo = [txt for txt in re.finditer(rf"{i}", new_text)]
            if num_array == None:
                num_array = res

            else:
                for j in res:
                    if j not in num_array:
                        num_array.append(j)

    m = sorted(num_array)

    word_value = word_indent(m)

    if word_value != []:
        app_arr = [new_text, word_value]
        global_arr.append(app_arr)
    return word_value


def resources_executer():
    cities = Web_scrape(
        'https://en.wikipedia.org/wiki/List_of_cities_in_Nepal').city_scraper()
    hospitals = Web_scrape(
        'https://ne.wikipedia.org/wiki/नेपालका_अस्पतालहरू').hospital_finder()
    bank = Web_scrape(
        'https://ne.wikipedia.org/wiki/नेपालका_बैङ्कहरूको_सूची').hospital_finder()


def spacy_zip(arr):
    train_text = []
    train_ent = []

    for i in range(len(new_arr)):

        train_text.append(new_arr[i][0])
        train_ent.append({'entities': new_arr[i][1]})

    train_data = list(zip(train_text, train_ent))

    return train_data


def spacy_trainer(train_data, filename):
    nlp = spacy.blank('en')
    db = DocBin()
    i = 0
    for text, annot in tqdm(train_data):  # data in previous format
        doc = nlp.make_doc(text)  # create doc object from text
        ents = []

        for start, end, label in annot["entities"]:  # add character indexes

            new_end = end+1
            span = doc.char_span(start, new_end, label=label,
                                 alignment_mode="contract")
            if span is None:
                print("Skipping entity")
            else:

                #             if len(span) >= 1:
                #                 second_ents.append(span)

                if " " in str(span):

                    ents.append(span)

        i += 1
        if ents != []:

            doc.ents = ents
            db.add(doc)

    db.to_disk(f"./data/{filename}")
    return True


def new_entity(text, entity):
    ent_array = None

    if entity == 'city':
        ent_array = Entities.city_entity_finder(text)
    elif entity == 'hospital':
        ent_array = Entities.hospital_entity_finder(text)
    elif entity == 'municipality':
        ent_array = Entities.municipality_entity_finder(text)
    else:
        ent_array = Entities.jilla_prahari_karyala(text)

    zip_arr = spacy_zip(ent_array)
    return_array = spacy_trainer(zip_arr, 'train')
    return return_array


def spacy_predicter(text):
    return_arr = []
    nlp = spacy.load(R".\output\model-best")
    new_inp = text
    new_data = nr.romanize_text(new_inp)
    new_data = new_data.strip(" ")
    filt_data = nepali_word_filter(new_data)
    doc = nlp(filt_data)
    entitities = doc.ents
    for ent in doc.ents:
        ent_dict = {'text': ent.text, 'start_index': ent.start_char,
                    'end_index': ent.end_char, 'entity': ent.label_}
        return_arr.append(ent_dict)


def cron_job(status):
    cron = status
    if cron:
        resources_executer()
    else:
        pass


schedule.every().minutes.do(cron_job)
schedule.every(23).hour.do(cron_job)
schedule.every().day.at("10:30").do(cron_job)

while 1:
    schedule.run_pending()
    time.sleep(1)
