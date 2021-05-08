import spacy
from web_scrape import Web_scrape
from entity_finder import Entity
from function import spacy_zip,spacy_trainer


nlp = spacy.load("en_core_web_sm")

array = Entity.all_enties()

sapcy_data = spacy_zip(array)

train_length = Math.floor(len(sapcy_data) * 0.8)


spacy_train = spacy_trainer(spacy_data[:train_length],'train.spacy')

spacy_valid = spacy.trainer(spacy_data[train_length:],'valid.spacy')




