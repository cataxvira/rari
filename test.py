import random

tweets = open('tweets.txt', 'r')
Lines = tweets.readlines()
random_tweet = random.choice(Lines)
