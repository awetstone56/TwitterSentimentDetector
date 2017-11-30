import json
import re
import operator
import configparser
from collections import Counter
import nltk
#nltk.download('punkt')
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk import bigrams
import string
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

punctuation = list(string.punctuation)
stop = stopwords.words('english') + punctuation + ['rt', 'via']
 
def tokenize(s):
    return tokens_re.findall(s)
 
def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens

fname = config['DEFAULT']['tweet_file']
with open(fname, 'r') as f:
    count_all = Counter()
    for line in f:
        tweet = json.loads(line) # load it as Python dict
        # Create a list with all the terms
        terms_all = [term for term in preprocess(tweet['text'])]
        # Count terms only once, equivalent to Document Frequency
        terms_single = set(terms_all)
        # Count hashtags only
        terms_hash = [term for term in preprocess(tweet['text']) 
              if term.startswith('#')]
        # Count terms only (no hashtags, no mentions)
        terms_only = [term for term in preprocess(tweet['text']) 
              if term not in stop and
              not term.startswith(('#', '@'))] 
              # mind the ((double brackets))
              # startswith() takes a tuple (not a list) if 
              # we pass a list of inputs
        terms_stop = [term for term in preprocess(tweet['text']) if term not in stop]
        # Update the Counter
        count_all.update(terms_stop)
        # The bigrams() function from NLTK will take a list of tokens 
        # and produce a list of tuples using adjacent tokens
        terms_bigram = bigrams(terms_stop) # have to cast bigram as a list
        print(list(terms_bigram)) 
    print(count_all.most_common(5))


