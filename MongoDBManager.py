from configHeroku import dbConnection


def MongoDB(userTweets, sentiment, userID, keyword):
    # Connecting to database
    client = dbConnection()
    print(client)

    # get database
    db = client.get_database('TweetFeel')
    tweetCollection = db.Raw_Tweets

    tweetData = []
    print("here")
    i = 0
    for tweet in userTweets:
        t = {"userid": userID,
             "name": tweet.user.name,
             "created at": tweet.created_at,
             "text": tweet.text,
             "keyword": keyword,
             "sentiment": str(sentiment[i])}
        tweetData.append(t)

        print("name:", tweet.user.name)
        print("created at: ", tweet.created_at)
        print("text: ", tweet.text)
        print("keyword: ", keyword)
        print(sentiment[i])
        print("")

        i = i + 1

    # for tw in tweetData:
    #     print(tw)

    tweetCollection.insert_many(tweetData)
