import tweepy
from configHeroku import authentication
from preProcessTweets import PreProcessTweets


def begin(keyword):
    api = authentication()
    keyword = keyword + " -filter:retweets"
    tweets = tweepy.Cursor(api.search, q=keyword, result_type="recent", lang="en").items(100)

    return tweets
