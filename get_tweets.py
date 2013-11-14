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

class Tweet(dict):
    def __init__(self, tweet_json):
        super(Tweet, self).__init__(self)
        if tweet_json and 'delete' not in tweet_json:
            self['timestamp'] = dateutil.parser.parse(tweet_json[u'created_at']).replace(tzinfo=None).isoformat()
            self['text'] = tweet_json['text']
            self['hashtags'] = [x['text'] for x in tweet_json['entities']['hashtags']]
            self['geo'] = tweet_json['geo']['coordinates'] if tweet_json['geo'] else None
            self['id'] = tweet_json['id']
            self['screen_name'] = tweet_json['user']['screen_name']
            self['user_id'] = tweet_json['user']['id']

    def __str__(self):
       return json.dumps(self, indent=2, sort_keys=True)


#Read oAuth credentials from symlinked twitter_creds.txt file
"""
Expected file structure for twitter_creds.txt is:

consumer_key:XXXX
consumer_secret:XXXX
token:XXXX
token_secret:XXXX
"""

with open("twitter_creds.txt") as f:
     twitter_creds = {}
     for line in f:
         k,v = line.strip().split(":")
         twitter_creds[k] = v

twitter_stream = twitter.TwitterStream(auth=twitter.OAuth(
            token=twitter_creds["token"],
            token_secret=twitter_creds["token_secret"],
            consumer_key=twitter_creds["consumer_key"],
            consumer_secret=twitter_creds["consumer_secret"]))

stream = twitter_stream.statuses.sample(block=True)
print Tweet(stream.next())
#json.dumps(tweet, indent=2, sort_keys=True)
