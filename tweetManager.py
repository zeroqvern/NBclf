import twitter
import tweepy
from configHeroku import authentication
from preProcessTweets import PreProcessTweets


def begin(keyword):
    result = getTweets(keyword)

    for tweet in result:
        print(tweet)

    return result


def getTweets(keyword):
    api = authentication()

    keyword = keyword + " -filter:retweets"

    # tweets_fetched = twitter_api.GetSearch(search_keyword, count=10)
    tweets = tweepy.Cursor(api.search, q=keyword, result_type="recent", lang="en").items(5)
    return [tweet.text for tweet in tweets]
