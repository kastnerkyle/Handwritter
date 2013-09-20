#!/usr/bin/env python

#Heavily adapted from a post by Clayton Davis @
#https://www.wakari.io/sharing/bundle/wakari_demo/realtime_twitter_analysis

import json
import time
import dateutil.parser
import numpy as np
import multiprocessing as mp
import redis
import string
import collections
from Queue import Empty
import itertools
import twitter

#Read oAuth credentials from symlinked twitter_creds.txt file
"""
Expected file structure for twitter_creds.txt is:

consumer_key:XXXX
consumer_secret:XXXX
token:XXXX
token_secret:XXXX
"""

with open("twitter_creds.txt") as f:
    twitter_creds = {line.split(":")[0]:line.split(":")[1].strip() for line in f}

twitter_stream = twitter.TwitterStream(auth=twitter.OAuth(
            token=twitter_creds["token"],
            token_secret=twitter_creds["token_secret"],
            consumer_key=twitter_creds["consumer_key"],
            consumer_secret=twitter_creds["consumer_secret"]))

stream = twitter_stream.statuses.sample(block=True)
tweet = stream.next()
print json.dumps(tweet, indent=2, sort_keys=True)
