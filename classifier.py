import sys
import nltk
import time
import tweepy
import string
import SocketServer
import nltk.classify
import BaseHTTPServer
from nltk import bigrams
from nltk.corpus import stopwords
from sklearn.svm import LinearSVC
from nltk.stem.lancaster import LancasterStemmer

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    
	def do_HEAD(s):
		s.send_response(200)
		s.send_header("Content-type", "text/html")
		self.send_header("Access-Control-Allow-Origin", "*");
		self.send_header("Access-Control-Expose-Headers", "Access-Control-Allow-Origin");
		self.send_header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
		s.end_headers()

	def do_GET(s):
		s.send_response(200)
		path = s.path.split("=")
		user = path[-1]
		result = analyze_account(user, 100)
		s.send_header("Content-type", "text/html")
		s.end_headers()
		s.wfile.write("<html><body>")
		s.wfile.write("<p>" + str(user) + "</p>")
		s.wfile.write("<p>" + str(result) + "</p>")
		s.wfile.write("</body></html>")

def get_tweets(file):
	tweets = []
	for line in open(file, "r"):
		params = line.split(",\"")
		tweet = params[-1].strip("\n")[:len(params[-1])-2]
		tweet = clean_tweet(tweet)
		label = params[0]
		tweets.append((tweet, label))
	return tweets

def get_words(tweets):
	words = []
	for tweet, label in tweets:
		words.extend(tweet)
		# for t in bigrams(tweet):
		# 	words.extend([" ".join(t)])
	return words

def get_features(words):
	words = nltk.FreqDist(words)
	features = words.keys()
	return features

def analize_tweet(tweet):
	tweet_words = set(tweet)
	tweet_features = {}
	for word in features:
		tweet_features[word] = (word in tweet_words)
	return tweet_features

def clean_tweet(tweet):
	st = LancasterStemmer()
	tweet_stem = tweet
	tweet_stem = tweet_stem.replace(".", "")
	clean_tweet = ""
	for token in tweet_stem.split():
		if not token.startswith(("@", "http", "www")):
			clean_tweet += st.stem(token) + " "
	clean_tweet = [w.lower() for w in clean_tweet.split() if not w in stopwords.words('english') and len(w) >= 3]
	return clean_tweet

def get_accuracy(filename, samples):
	c = 0
	for line in open(filename, "r"):
		params = line.split(",\"")
		tweet = params[-1].strip("\n")[:len(params[-1])-2]
		tweet = clean_tweet(tweet)
		label = params[0]
		if label == classifier.classify(analize_tweet(tweet)):
			c += 1
	return (c/samples) * 100

def analyze_account(user, num):
	tweets = twitter_fetch(user, num)
	positive = 0
	negative = 0
	for tweet in tweets:
		tweet = clean_tweet(tweet)
		sentiment = classifier.classify(analize_tweet(tweet))
		if sentiment == "\"0\"":
			negative += 1
		else:
			positive += 1
	return (positive, negative)

def twitter_fetch(screen_name, num_tweets):
	ckey = "peTdiI7qoZGme5vHlJyh0OKd7"
	csecret = "WEK2ARMZtWxYyccNk22qdEDXZWf9mRZSXasoKJ1lWclkCDKDIo"
	atoken = "81963120-4u3rLdZHoTehxMUfuSG57bvOjpkKpUxLyrOhZ9Jba"
	asecret = "sSW2HRPQE2Q2o7eJLbcrt6CVaiQstqnuFRAT3ZeSfXNbl"
	auth = tweepy.OAuthHandler(ckey, csecret)
	auth.set_access_token(atoken,asecret)    
	api  = tweepy.API(auth)
	tweets = []
	for status in tweepy.Cursor(api.user_timeline, id=screen_name).items(num_tweets): 
		tweet = status.text
		clean_tweet = ""
		for c in tweet:
			if c in string.printable:
				clean_tweet += c
		tweets.append(clean_tweet)
	return tweets

# MAIN
print "Reading tweets...\n"
tweets = get_tweets("dataset/training.txt")

print "Getting words...\n"
words = get_words(tweets)

print "Getting features...\n"
features = get_features(words)

print "Training...\n"
training_set = nltk.classify.apply_features(analize_tweet, tweets)

print "Getting classifier...\n"
# classifier = nltk.classify.SklearnClassifier(LinearSVC())
# classifier.train(training_set)
classifier = nltk.NaiveBayesClassifier.train(training_set)
# print classifier.show_most_informative_features(30)

# print analyze_account("oprah", 100)
# print analyze_account("billgates", 100)
# print analyze_account("emwatson", 100)
# print analyze_account("google", 100)

HOST_NAME = "127.0.0.1"
PORT_NUMBER = 9000

server_class = BaseHTTPServer.HTTPServer
httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
try:
	httpd.serve_forever()
except KeyboardInterrupt:
	pass
httpd.server_close()
print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)
