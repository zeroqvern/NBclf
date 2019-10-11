# from boto.s3.connection import S3Connection
import os
import tweepy

# initialize api instance
CONSUMER_KEY = os.environ.get("CONSUMER_KEY")
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
ACCESS_KEY = os.environ.get('ACCESS_KEY')
ACCESS_SECRET = os.environ.get('ACCESS_SECRET')
auth = tweepy.OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)


def authentication():
    try:
        api = tweepy.API(auth)
        print("Authentication OK")
        return api
    except:
        print("Error during authenticatoin")
        return None


# test authentication
# print(twitter_api.VerifyCredentials())


