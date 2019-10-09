from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import re
from nltk.tokenize import word_tokenize
from string import punctuation
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

class PreProcessTweets:
    def __init__(self):
        self._stopwords = set(stopwords.words('english') + list(punctuation) + ['AT_USER', 'URL'])

    def cleanTweetSet(self, rawData):
        cleanedSet = []
        print("cleaning...")
        for tweet in rawData:
            tweet = self.cleanTweet(tweet)
            cleanedSet.append(tweet)

        print("clean complete.")
        return cleanedSet

    def cleanTweet(self, text):

        text = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', 'URL', text)
        text = re.sub('@[^\s]+', 'USER', text)
        text = text.lower().replace("ё", "е")
        text = re.sub('[^a-zA-Zа-яА-Я1-9]+', ' ', text)
        text = re.sub(' +', ' ', text)
        tweet = word_tokenize(text)

        cleanedWords = []
        lem = WordNetLemmatizer()
        for w in tweet:
            w = lem.lemmatize(w)
            if w not in self._stopwords:
                cleanedWords.append(w)

        joinedWords = ' '.join(cleanedWords)

        return joinedWords

    def featureExtraction(self, cleanedSet):
        # create bag of words

        # convert words to numbers using bag of words approach
        # as the data could contain tens thousands of unique words
        # max_features is set to 1500 to collect most occurring words as features
        # min_df is set to 5 = include words that occur in at least 5 tweets
        # max_df is set to 0.7 = include words that occur in a max of 70% of all tweets
        vectorizer = CountVectorizer(max_df=0.7)

        # converts text into corresponding numeric features
        X = vectorizer.fit_transform(cleanedSet)

        tfidfconverter = TfidfVectorizer(max_df=0.7)
        X = tfidfconverter.fit_transform(cleanedSet)
