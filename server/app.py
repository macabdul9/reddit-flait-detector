import flask
from flask import Flask, render_template, session, redirect, url_for, session, jsonify, request
import numpy as np
import joblib
import re
import requests
import os
import pickle as pkl
import praw
import torch
from multiprocessing import cpu_count
# import simpletransformers
from simpletransformers.classification import ClassificationModel

model_path = str(os.path.dirname(__file__)) + 'models/pytorch_model.bin'

app = flask.Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def main():
    if flask.request.method == 'GET':
        print("GET REQUEST RECEIVED")
        # url = flask.request.form['url']
        url = request.args.get('url', '')
        print("hello", url)
        return {"get reponse":"model loaded"}

    if flask.request.method == 'POST':
        print("POST REQUEST RECEIVED")
        url = request.args.get('url', '')
        print("url", url)
        actual, pred = return_out(url)
        return {"pred":pred, "actual":actual}


@app.route('/automated_testing', methods=['POST'])
def automated_testing():
    print(request.files)
    attachment = request.files['upload_file']
    urls = attachment.read()
    if urls == "":
      if 'url' not in request.args:
        return {"error":400}
      
      else:
        url = request.args['url']
        actual, pred = return_out(url)

        final_result = {
          url: pred
        }

        return jsonify(final_result)

    elif 'upload_file' in request.files:
        urls = urls.decode("utf-8")

        print(urls)
        print("\n")

        urls_list = str(urls).split('\n')

        print(urls_list)

        lists = []

        for url in urls_list:
          if(url != ''):
            actual, pred = return_out(url)

            element = {
              str(url): pred
            }

            lists.append(element)
          
        return jsonify(lists)

def return_out(url, justLoad = False):
    global loaded
    global model_
    if(not loaded):
      model_ = ClassificationModel('distilbert', str(os.path.dirname(__file__)) + 'models/', use_cuda=False, num_labels=11, args = args)
      checkpoint = torch.load(model_path, map_location='cpu')
      model_.model.load_state_dict(checkpoint)
      model_.model.eval()
      loaded = True
      print("\n\nModel Loaded\n\n")
      if(justLoad):
        return -1

    reddit = praw.Reddit(
        client_id='pw8WCM92ySUjsQ', 
        client_secret='y0MJFMWBtHXMLW2-3B2upsU2jYQ', 
        user_agent='reddit-scrap', 
        username='macabdul9', 
        password='Sudo$0#1'
    )
    print(1)
    sub = reddit.submission(url=url)
    data = [sub.title, sub.url, sub.selftext, sub.link_flair_text]
    print("\n", data[0], "\n")

    data[1] = processURL(data[1])
    
    print("\n", data[1], "\n")

    preds = np.argmax(model_.predict([data[0] + ' ' + data[1]])[1])

    print("\n Preds Loaded \n")
    
    preds = enc[preds+1]
    actual = data[3]

    return actual, preds

def processURL(words):
  words = words.split('://')
  if(len(words) > 1):
    words = words[1]
  else:
    words = words[0]
  words = words.split('/')
  seq = ' '.join(words)
  seq = re.sub("[^a-zA-Z]", " ", seq)
  seq = re.sub(" +", " ", seq).strip()
  return seq

enc = {
 1: 'Politics',
 2: 'Science/Technology',
 3: 'AskIndia',
 4: 'Non-Political',
 5: '[R]eddiquette',
 6: 'Business/Finance',
 7: 'Policy/Economy',
 8: 'Sports',
 9: 'Photography',
 10: 'Entertainment',
 11: 'Not in English.',
 12: 'Coronavirus'
}

args = {
    "output_dir": "../tmp/",
    "cache_dir": "../tmp/",
    "best_model_dir": "../tmp/",

    "fp16": False,
    "fp16_opt_level": "O1",
    "max_seq_length": 128,
    "train_batch_size": 128,
    "eval_batch_size": 128,
    "gradient_accumulation_steps": 1,
    "num_train_epochs": 1,
    "weight_decay": 0,
    "learning_rate": 1e-4,
    "adam_epsilon": 1e-8,
    "warmup_ratio": 0.06,
    "warmup_steps": 0,
    "max_grad_norm": 1.0,
    "do_lower_case": False,

    "logging_steps": 50,
    "evaluate_during_training": False,
    "evaluate_during_training_steps": 2000,
    "evaluate_during_training_verbose": False,
    "use_cached_eval_features": False,
    "save_eval_checkpoints": False,
    "no_cache": True,
    "save_model_every_epoch": False,
    "tensorboard_dir": None,

    "overwrite_output_dir": False,
    "reprocess_input_data": False,

    "process_count": cpu_count() - 2 if cpu_count() > 2 else 1,
    "n_gpu": 0,
    "silent": False,
    "use_multiprocessing": True,

    "wandb_project": None,
    "wandb_kwargs": {},

    "use_early_stopping": True,
    "early_stopping_patience": 3,
    "early_stopping_delta": 0,
    "early_stopping_metric": "eval_loss",
    "early_stopping_metric_minimize": True,

    "manual_seed": 0,
    "encoding": None,
    "config": {},
}

loaded = False
model_ = -1
return_out(None, justLoad = True)

if __name__ == '__main__':
    app.run(debug=False)