import tweepy # pip install tweepy==3.5.0
import django # pip install Django
import json
import configparser
from django.utils.encoding import smart_str, smart_unicode
from tweepy import OAuthHandler

config = configparser.ConfigParser()
config.read('TwitterSentimentDetector.ini')

fname = config['DEFAULT']['tweet_file']
file = open(fname, "w") # call file what ever you need to
# this method writes a tweet to a file
def process_or_store(tweet):
    file.write(json.dumps(tweet) + "\n")

consumer_key = config['twitter.com']['consumer_key']
consumer_secret = config['twitter.com']['consumer_secret']
access_token = config['twitter.com']['access_token']
access_secret = config['twitter.com']['access_secret']

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
# api is what you use to access anything from twitter
api = tweepy.API(auth)
tweets = tweepy.Cursor(api.search, q='#Christmas').items(100)

# change the number of tweets it grabs by changing the number '25'
#for tweet in tweepy.Cursor(api.home_timeline).items(25):
for tweet in tweets:
    # Process a single status
    # if you're going to print any text use smart_str from django
    # print smart_str(status._json)
    #print smart_str(tweet._json)
    process_or_store(tweet._json)

file.close()