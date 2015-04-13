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
	overall_polarity = 0.0
	overall_subjectivity = 0.0
	THUMB_CONF = {'Positive':"thumbs-o-up", "Negative":"thumbs-o-down", "Neutral":"meh-o"}
	# get search term from querystring 'q' or default search for "Whiplash"
	query = request.args.get('q') or "#whiplash"


	# search with query term and return 50
	results = twitter.search.tweets(q='"%s" -RT' %(query), lang="en", result_type="mixed", count=100)
	tweets_obj = results.get('statuses')

	if len(tweets_obj):
		factor = len(tweets_obj)
	else:
	 	factor = 1.0

	for tweet in tweets_obj:
		#print tweet.get("text").replace(str(request.args.get("q")), " ")
		result = get_sentiments(tweet.get("text"))#.replace(str(request.args.get("q")), " "))
		
		tweet['sentiment'] = float(result.sentiment.polarity)
		overall_polarity += float(result.sentiment.polarity)
		
		tweet['subjectivity'] = float(result.sentiment.subjectivity)
		overall_subjectivity += float(result.sentiment.subjectivity)

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
		'THUMB_CONF':THUMB_CONF,
		'overall_polarity':overall_polarity / factor,
		'overall_subjectivity':overall_subjectivity / factor,
		'result_count':factor,
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

@app.template_filter('polarity_icon')
def _jinja2_filter_datetime(date, polarity):
	if polarity>0.0:
		icon = "thumbs-o-up"
	elif polarity<0.0:
		icon = "thumbs-o-down"
	else :
		icon = "meh-o"
	return icon

    
    
# --------- Server On ----------
# start the webserver
if __name__ == "__main__":
	app.debug = True
	
	port = int(os.environ.get('PORT', 5000)) # locally PORT 5000, Heroku will assign its own port
	app.run(host='0.0.0.0', port=port)


