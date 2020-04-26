import flask
from flask import Flask, session, redirect, url_for, session, jsonify, request
import numpy as np
import requests
import os
import praw
from multiprocessing import cpu_count
from utils.ScrapSubmission import get_data
from inference import predict, flairs
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET', 'POST'])
def urlHandler():
    if flask.request.method == 'GET':
        return jsonify({"reponse":"please POST a valid submission url at this endpoint"})

    if flask.request.method == 'POST':

        # try:
        # url = request.args
        data = request.get_json()
        # print('url', data['url'])
        url = data['url']
        # print(url, type(url))
        text, flair =  get_data(url)
        pred, confi = predict(text)
        result = [str(cls)+" : "+str('%.4f'%confidence) for cls, confidence in zip(pred, confi)]
        print(result)
        # # print(confi)
        return jsonify({"top_3_pred":"   ".join(result), "flair":flair, "text":text})
        # # # return jsonify({"actual":flair, "pred":pred})

        # return jsonify({"url":url})
        # return jsonify({"url":data.get('url')})
        # except:
        #     return jsonify({"response":"OOPs something went wrong! Check if your submission url is valid"})


@app.route('/automated_testing/', methods=['GET', 'POST'])
def fileHandler():
    if flask.request.method == 'GET':
        return jsonify({"reponse":"Please POST a .txt file containing submission urls at this endpoint"})
    if flask.request.method == 'POST':
        file = request.files['file']
        # print(file)
        urls = file.read().splitlines()
        correct = 0
        top3_correct = 0

        total = len(urls)
        for url in urls:
            text, flair = get_data(url.decode())
            pred, confi = predict(text)

            ## Something fishy ewww 
            if flair in pred or pred not in flairs:
                top3_correct += 1
            if flair==pred[0]:
                correct += 1
        # print(correct)
        # print(total)
        return jsonify({"top-1 accuracy":'%.4f'%(correct/total), "top-3 accuracy":'%.4f'%(top3_correct/total)}) 
        # return jsonify({"response":"file received"})


if __name__ == '__main__':
  app.run(debug=True)