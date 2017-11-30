import json
import re
import operator
import configparser
from collections import Counter
#import nltk
#nltk.download('punkt')
#from nltk.tokenize import word_tokenize

config = configparser.ConfigParser()
config.read('TwitterSentimentDetector.ini')

emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""
 
regex_str = [
    emoticons_str,
    r'<[^>]+>', # HTML tags
    r'(?:@[\w_]+)', # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
 
    r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
]
    
tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)
 
def tokenize(s):
    return tokens_re.findall(s)
 
def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens

fname = config['DEFAULT']['tweet_file']
with open(fname, 'r') as f:
    for line in f:
        tweet = json.loads(line) # load it as Python dict
        #print(json.dumps(tweet, indent=4)) # pretty-print
        tokens = preprocess(tweet['text'])
        print(tokens)
        #do_something_else(tokens)
 
#tweet = 'RT @marcobonzanini: just an example! :D http://example.com #NLP'
#print(preprocess(tweet))

