import csv
import os
from textblob import TextBlob

PATH = os.path.dirname(os.path.abspath(__file__))
test_file = open(os.path.join(PATH, 'data/testdata.csv'),'r')
test_csv = csv.reader(test_file)
for row in test_csv:
	tweet = TextBlob(row[5])
	if tweet.sentiment.polarity > 0.0:
		print tweet," - pos"
	else:
		print tweet," - neg"