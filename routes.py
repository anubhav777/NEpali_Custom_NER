from app import app
from function import spacy_predicter, new_entity, cron_job
from flask import request


@app.route('/predict', methods=['POST'])
def pred_text():
    text = request.json['text']
    spacy_predicter(text)
    return {'data': spacy_predicter}


@app.route('/inputs', methods=['POST'])
def inp_text():
    text = request.json['text']
    ent_name = request.json['entity']
    ret_arr = new_entity(text, ent_name)
    if ret_arr:
        return {'status': 'sucessfully added entity on train set'}
    else:
        return {'status': 'unsucessfull the enity could not be added'}


@app.route('/cron', methods=['POST'])
def cron_text():
    status = request.json['status']
    cron_job(status)
    return {'status': 'updated cronjob'}
