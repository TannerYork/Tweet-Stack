import os
import tweepy

# Imports for tweet processing
from tensorflow import keras
import tensorflow_hub as hub
import nltk
from nltk.corpus import stopwords
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

def analyze_query(query):
    """
    A function for taking in users search query and returning sentiment data based on the query
        Args: 
            query (string): a string representing the users serach
        Returns:
            Data: An object that contains the overall sentiment score, 10 of the 
                tweets recived form the query, and those 10 tweets sentiment score
    """
    pass

def preprocess_tweets(tweets):
    """
    A function for preparing tweets to be put into the sentiment analysis model
        Args:
            tweets (array): list of tweets' text form using the users query in the twitter api
        Returns:
            processed_tweets: a list of tweets' text that is lowercased, tokenized, 
                            and has all the special characters removed
    """
    pass