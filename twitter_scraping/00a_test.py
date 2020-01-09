import pandas as pd
import tweepy
import tweepy_functions as tf
import sys
import io
import json
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

with open(r'.\twitter_scraping\keys.json') as f:
    keys = json.load(f)
auth = tweepy.OAuthHandler(keys['consumer_key'], keys['consumer_secret'])
auth.set_access_token(keys['access_token'], keys['access_token_secret'])
api = tweepy.API(auth)

with open(r'.\data\replies_to_jk_rowling.json') as f:
    data = json.load(f)

df = pd.DataFrame(data)

print(df.iloc[1])
