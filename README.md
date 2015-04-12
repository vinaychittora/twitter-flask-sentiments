
### Requirements

* Python 2.7.x
* Virtualenv
* PIP
* Heroku Toolbelt / Foreman
* Twitter Account
* textblob (Based on NLTK)


## How to run locally

### git clone

## Set up virtual environment


* Create and activate virtual environment for directory.

		mkvirtualenv <env-name>
		. <env-name>/bin/activate

* Install requirements for app

		pip install -r requirements.txt


## Create Twitter Application/Account

* Create new app here, <https://dev.twitter.com/>.
* Set application as **Read and Write** capable

From app settings generate OAUTH Key and Secret for yourself to use.

### Set up Twitter Credentials

In your Application settings, find the tokens and keys, you will need these to use the Twitter API.

Create **.env** file with the following


	OAUTH_TOKEN=YOUROAUTHTOKENHERE
	OAUTH_SECRET=YOUROAUTHSECRETHERE
	CONSUMER_KEY=YOURCONSUMERKEYHERE
	CONSUMER_SECRET=YOURCONSUMERSECRETHERE

Save as **.env** in your code directory.


## Start the server

To start server you must have Foreman / [Heroku toolbelt](http://toolbelt.heroku.com) installed. Foreman will read your .env files to get your credentials.

Start your engines

	foreman start


### There there man

Open browser, <http://localhost:5000>


