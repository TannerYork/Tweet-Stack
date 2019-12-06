import os
import tweepy

# Imports for tweet processing
from tensorflow import keras
import tensorflow_hub as hub
import nltk
from nltk.tokenize import word_tokenize 
import preprocessor as p
import re

# Load Twitter API keys
CONSUMER_KEY = os.getenv('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

# Setup tweepy api
AUTH = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
AUTH.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
API = tweepy.API(AUTH)

class TwitterAnalysis():
    def __init__(self):
        """A class for recieving and processing user queries"""
        self.model = keras.models.load_model('sentiment_analysis/tweet-sentiment.h5', custom_objects={'KerasLayer': hub.KerasLayer})
        self.api = API

    def analyze_query(self, query):
        """
        A function for taking in users search query and returning sentiment data based on the query
            Args: 
                query (string): a string representing the users serach
            Returns:
                Data: An object that contains the overall sentiment score, 10 of the 
                    tweets recived form the query, and those 10 tweets sentiment score
        """
        tweets = tweepy.Cursor(self.api.search,q="#" + query + " -filter:retweets", rpp=5, lang="en").items(100)
        tweets = [tweet.text for tweet in tweets]
        if len(tweets) < 6:
            return
        processed_tweets = self.preprocess_tweets(tweets)
        sentiment = sum(self.model.predict([tweet]) for tweet in processed_tweets)/len(processed_tweets)
        preview_tweets = []
        for index in range(0, 6):
            tweet = tweets[index]
            tweet_sentiment = self.model.predict([processed_tweets[index]])
            preview_tweets.append((tweet, tweet_sentiment))
        return {'sentiment': sentiment, 'preview_tweets': preview_tweets}

    def preprocess_tweets(self, tweets):
        """
        A helper function for preparing tweets to be put into the sentiment analysis model
            Args:
                tweets (array): list of tweets' text form using the users query in the twitter api
            Returns:
                processed_tweets: a list of tweets' text that is lowercased, tokenized, 
                                and has all the special characters removed
        """
        proccessed_tweets = []
        for text in tweets:
            new_text = p.clean(text)
            new_text = re.sub(r'@\S+|https?:\S+|http?:\S|[^A-Za-z0-9]+', ' ', new_text.lower()).strip()
            proccessed_tweets.append(' '.join(new_text))
        return proccessed_tweets