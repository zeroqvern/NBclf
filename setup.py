from flask import Flask, jsonify, request
from flask_restful import reqparse, abort, Api, Resource
import pickle
import json
from preProcessTweets import PreProcessTweets
from tweetManager import begin
from MongoDBManager import MongoDB
from bson.objectid import ObjectId

app = Flask(__name__)
api = Api(app)

# load NBModel
with open('model.pkl', 'rb') as training_model:
    model = pickle.load(training_model)


# routes
@app.route('/predict', methods=['POST'])
@app.route('/analysis', methods=['GET'])
def start():
    if request.method == "POST":
        print("post method called")

        # get data (in list, dict, str format)
        req = request.get_json(force=True)
        output = postRequest(req)

        # print output and return to requester
        print(output)
        return jsonify(output)

    elif request.method == "GET":
        keyword = request.args.get('keyword')
        userid = ObjectId(request.args.get('userid'))
        output = getRequest(keyword, userid)

        return jsonify(output)

    else:
        output = {'error': 'Invalid method'}
        print(output)
        return jsonify(output)


def postRequest(req):
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
    return output


def getRequest(keyword, userid):
    userTweets = begin(keyword)

    # prediction and write database
    output = prediction(userTweets, userid)

    return output


def prediction(userTweets, userid):
    tweetList = []
    tweetData = []
    for tweet in userTweets:
        tweetList.append(tweet.text)
        tweetData.append(tweet)

    pos = 0
    neg = 0

    # clean tweet texts in list
    proc = PreProcessTweets()
    cleanListSet = proc.cleanTweetSet(tweetList)

    # predictions
    result = model.predict(cleanListSet)

    # write to database
    MongoDB(tweetData, result, userid)


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
