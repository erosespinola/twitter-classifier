import nltk
import numpy as np
import cPickle as pickle
import sys

def read_file(file):
	data = np.load(file)
	return data

def get_tweets(file):
	tweets = []
	for line in open(file, "r"):
		params = line.split(",")
		tweet = params[-1].strip("\n")[1:len(params[-1])-2]
		tweet = [w.lower() for w in tweet.split() if len(w) >= 3]
		label = ["negative", "possitive"][params[0] == '"4"']
		tweets.append((tweet, label))
	np.save("dataset/training", np.array(tweets, dtype=object))

def get_words(tweets):
	words = []
	for t in tweets:
		words.extend(t[0])
	np.save("dataset/words", np.array(words))

def get_features(words):
	words = nltk.FreqDist(words)
	features = words.keys()
	np.save("dataset/features", np.array(features))

def analize_tweet(tweet):
	tweet_words = set(tweet)
	tweet_features = {}
	for word in features:
		tweet_features[word] = (word in tweet_words)
	return tweet_features

# MAIN

# get_tweets("dataset/training_reduced.csv")
tweets = read_file("dataset/training.npy")
# print tweets

# get_words(tweets.tolist())
# words = read_file("dataset/words_reduced.npy")
# print words

# get_features(words.tolist())
features = read_file("dataset/features.npy")
# print features

training_set = nltk.classify.apply_features(analize_tweet, tweets.tolist())
classifier = nltk.NaiveBayesClassifier.train(training_set)

print classifier.show_most_informative_features(10)

while True:
	tweet = raw_input("Enter a tweet: ")
	if tweet == "exit()":
		sys.exit()
	print classifier.classify(analize_tweet(tweet.split()))