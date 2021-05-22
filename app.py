from routes import *
import spacy
from tqdm import tqdm
from spacy.tokens import DocBin
import json
import re
from flask import Flask


app = Flask(__name__)


app.config.from_object('config.Development')


if __name__ == "__main__":
    app.run(debug=True)
