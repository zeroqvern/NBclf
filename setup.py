from __future__ import division
from flask import Flask, jsonify, request
from flask_restful import reqparse, abort, Api, Resource
import pickle
import numpy as np
import json
import pandas as pd



#app
app = Flask(__name__)
api = Api(app)

#load NBModel
# model = MultinomialNB()
with open('model.pkl', 'rb') as training_model:
    model = pickle.load(training_model)



# # argument parsing
# parser = reqparse.RequestParser()
# parser.add_argument('query')

#routes
@app.route('/', methods=['POST'])

def begin():
    # get data (in list, dict, str format)
    req = request.get_json(force=True)
    # print("type: {}".format(type(data)))
    tweetList = []
    data = req
    if (isinstance(req, list)):
        print("list")
        req = str(req[0])
        data = req.replace("'", "\"")
    elif (isinstance(req, dict)):
        data = json.dumps(req)
        print (data)

    p = json.loads(data)
    for i in p['tweet']:
        tweetList.append(i)

    #prediction
    output = prediction(tweetList)

    print(output)
    # output =  {'Overall Sentiment': str(1), 'Positive': 1, 'Negative': 1}
    return jsonify(output)

def prediction (tweetList):

    pos = 0
    neg = 0

    # predictions
    result = model.predict(tweetList)
    print(result)

    for i in result:
        if (i == 0): neg = neg + 1
        else: pos = pos + 1

    avg = avgSentiment(result)

    #json output
    output = {'Overall Sentiment': str(avg), 'Positive': pos, 'Negative': neg}
    return  output

def avgSentiment (allSentiment):

    sumSentiment = sum(allSentiment)
    tweetNum = len(allSentiment)

    avg = sumSentiment/tweetNum
    avg = round(avg, 2)

    return avg

if __name__ == '__main__':
    app.run(debug=True)


