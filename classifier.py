import nltk
import numpy as np

def read_tweets(file):
	tweets = np.load(file)
	return tweets

def save_tweets(file):
	tweets = []
	for line in open(file, "r"):
		params = line.split(",")
		tweet = params[-1]
		s_tweet = tweet[1:len(tweet)-2].strip('\n')
		label = [False,True][params[0] == '"4"']
		tweets.append([label, s_tweet])
	np.save("dataset/training", np.array(tweets))
