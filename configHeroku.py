import os
import tweepy
from pymongo import MongoClient

# initialize api instance
CONSUMER_KEY = os.environ.get("CONSUMER_KEY")
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
ACCESS_KEY = os.environ.get('ACCESS_KEY')
ACCESS_SECRET = os.environ.get('ACCESS_SECRET')
MONGODB = os.environ.get('MONGODB')
auth = tweepy.OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

# twitter authentication
def authentication():
    try:
        api = tweepy.API(auth)
        print("Authentication OK")
        return api
    except:
        print("Error during authentication")
        return None

# MongoDB authentication
def dbConnection():
    try:
        client = MongoClient(MONGODB)
        print("Connected to database")
        return client

    except:
        print("Error connecting to database")



