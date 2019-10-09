from flask import Flask, jsonify, request
from flask_restful import reqparse, abort, Api, Resource
import pickle
import numpy as np
import json

app = Flask(__name__)
api = Api(app)

# load NBModel
with open('model.pkl', 'rb') as training_model:
    model = pickle.load(training_model)


# routes
@app.route('/', methods=['POST'])
def begin():
    # get data (in list, dict, str format)
    req = request.get_json(force=True)

    tweetList = []
    data = req

    # convert request data to string
    if isinstance(req, list):
        print("list")
        req = str(req[0])
        data = req.replace("'", "\"")
    elif isinstance(req, dict):
        data = json.dumps(req)
        print(data)

    # store strings to list
    p = json.loads(data)
    for i in p['tweet']:
        tweetList.append(i)

    # prediction
    output = prediction(tweetList)

    # print output and return to requester
    print(output)
    return jsonify(output)


def prediction(tweetList):
    pos = 0
    neg = 0

    # clean tweet texts in list
    proc = PreProcessTweets()
    cleanListSet = proc.cleanTweetSet(tweetList)

    # predictions
    result = model.predict(cleanListSet)

    # count number of negative and positive tweets
    for i in result:
        if i == 0:
            neg = neg + 1
        else:
            pos = pos + 1

    # calculate average overall sentiment
    avg = avgSentiment(result)

    # json output
    output = {'Overall Sentiment': str(avg), 'Positive': pos, 'Negative': neg}
    return output


def avgSentiment(allSentiment):
    sumSentiment = sum(allSentiment)
    tweetNum = len(allSentiment)

    avg = sumSentiment / tweetNum
    avg = round(avg, 2)

    return avg


if __name__ == '__main__':
    app.run(debug=True)
