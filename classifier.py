import sys
import nltk
import tweepy
import string
import nltk.classify
from nltk import bigrams
from nltk.corpus import stopwords
from sklearn.svm import LinearSVC
from nltk.stem.lancaster import LancasterStemmer

def read_file(file):
	data = np.load(file)
	return data

def get_tweets(file):
	tweets = []
	for line in open(file, "r"):
		params = line.split(",\"")
		tweet = params[-1].strip("\n")[:len(params[-1])-2]
		tweet = clean_tweet(tweet)
		label = params[0]
		tweets.append((tweet, label))
	return tweets
	# np.save("dataset/training", np.array(tweets, dtype=object))

def get_words(tweets):
	words = []
	for tweet, label in tweets:
		words.extend(tweet)
		# for t in bigrams(tweet):
		# 	words.extend([" ".join(t)])
	return words
	# np.save("dataset/words", np.array(words))

def get_features(words):
	words = nltk.FreqDist(words)
	features = words.keys()
	return features
	# np.save("dataset/features", np.array(features))

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
# get_tweets("dataset/training.txt")
# tweets = read_file("dataset/training.npy")
tweets = get_tweets("dataset/training.txt")

print "Getting words...\n"
# get_words(tweets.tolist())
# words = read_file("dataset/words.npy")
words = get_words(tweets)

print "Getting features...\n"
# get_features(words.tolist())
# features = read_file("dataset/features.npy")
features = get_features(words)

print "Training...\n"
training_set = nltk.classify.apply_features(analize_tweet, tweets)

print "Getting classifier...\n"
# classifier = nltk.classify.SklearnClassifier(LinearSVC())
# classifier.train(training_set)

classifier = nltk.NaiveBayesClassifier.train(training_set)
print classifier.show_most_informative_features(30)

# Twitter
while True:
	user = raw_input("Enter a user: ")
	tweets = twitter_fetch(user, 10)
	positive = 0
	negative = 0
	for tweet in tweets:
		tweet = clean_tweet(tweet)
		sentiment = classifier.classify(analize_tweet(tweet))
		if sentiment == "\"0\"":
			negative += 1
		else:
			positive += 1
	print "Positive: " + str(positive) + "%"
	print "Negative: " + str(negative) + "%"

# Validation
# c = 0
# for line in open("dataset/test.csv", "r"):
# 	params = line.split(",\"")
# 	tweet = params[-1].strip("\n")[:len(params[-1])-2]
# 	tweet = clean_tweet(tweet)
# 	label = params[0]
# 	if label == classifier.classify(analize_tweet(tweet)):
# 		c += 1
# print "Accuracy: " + str((c/359.0) * 100)

# User input
# while True:
# 	tweet = raw_input("Enter a tweet: ")
# 	if tweet == "exit()":
# 		sys.exit()
# 	st = LancasterStemmer()
# 	tweet_stem = ""
# 	for token in tweet.split():
# 		tweet_stem += st.stem(token) + " "
# 	filtered_tweet = [w for w in tweet_stem.split() if not w in stopwords.words('english')]
# 	print classifier.classify(analize_tweet(tweet_stem))