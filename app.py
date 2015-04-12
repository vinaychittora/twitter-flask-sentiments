import os
import time
from twitter import *
from flask import Flask, request, render_template, redirect, abort, flash, jsonify
from api import *

app = Flask(__name__)   # create our flask app

# configure Twitter API
twitter = Twitter(
            auth=OAuth(os.environ.get('OAUTH_TOKEN'), os.environ.get('OAUTH_SECRET'),
                       os.environ.get('CONSUMER_KEY'), os.environ.get('CONSUMER_SECRET'))           

           )


@app.route('/')
def main():


	# fetch latest tweets from vinaychittora
	MyTweets = twitter.statuses.user_timeline(screen_name="vinaychittora", limit=20)
	
	templateData = {
		'title' : 'On my twitter timeline',
		'MyTweets' : MyTweets
	}

	return render_template('index.html', **templateData)


@app.route('/search')
def search():
	with_sentiments = []
	THUMB_CONF = {'Positive':"thumbs-o-up", "Negative":"thumbs-o-down", "Neutral":"meh-o"}
	# get search term from querystring 'q' or default search for "Whiplash"
	query = request.args.get('q') or "#whiplash"

	# search with query term and return 50
	results = twitter.search.tweets(q=query, count=50)
	tweets_obj = results.get('statuses')

	for tweet in tweets_obj:
		result = get_sentiments(tweet.get("text"))
		tweet['sentiment'] = float(result.sentiment.polarity)
		tweet['subjectivity'] = float(result.sentiment.subjectivity)
		if tweet['sentiment']>0.0:
			tweet['icon'] = THUMB_CONF['Positive']
		elif tweet['sentiment']<0.0:
			tweet['icon'] = THUMB_CONF['Negative']
		else:
			tweet['icon'] = THUMB_CONF['Neutral']
		with_sentiments.append(tweet)

	templateData = {
		'query' : query,
		'tweets' : with_sentiments,
		'THUMB_CONF':THUMB_CONF

	}
	app.logger.debug(tweets_obj)	

	return render_template('search.html', **templateData)



	
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


# This is a jinja custom filter
@app.template_filter('strftime')
def _jinja2_filter_datetime(date, fmt=None):
    pyDate = time.strptime(date,'%a %b %d %H:%M:%S +0000 %Y') # convert twitter date string into python date/time
    return time.strftime('%Y-%m-%d %H:%M:%S', pyDate) # return the formatted date.
    
# --------- Server On ----------
# start the webserver
if __name__ == "__main__":
	app.debug = True
	
	port = int(os.environ.get('PORT', 5000)) # locally PORT 5000, Heroku will assign its own port
	app.run(host='0.0.0.0', port=port)


