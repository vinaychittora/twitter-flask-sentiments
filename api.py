"""
This tool works by examining individual words and short sequences of words (n-grams)
and comparing them with a probability model. The probability model is built on a
prelabeled test set of IMDb movie reviews. It can also detect negations in phrases,
i.e, the phrase "not bad" will be classified as positive despite having two individual
words with a negative sentiment.


Endpoint Definition

POST - https://community-sentiment.p.mashape.com/text/

"""
import unirest
import os
import threading
import time
import csv
import os
from textblob import TextBlob


def get_sentiments_by_api(tweet):
	return unirest.post("https://community-sentiment.p.mashape.com/text/",
			  headers={
			    "X-Mashape-Key": os.environ.get('X_MASHUP_KEY'),
			    "Content-Type": "application/x-www-form-urlencoded",
			    "Accept": "application/json"
			  },
			  params={
			    "txt": tweet
			  }
			)

def get_sentiments(tweet):
	result = TextBlob(tweet)
	return result