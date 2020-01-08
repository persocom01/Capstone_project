import pandas as pd
import tweepy
from keys import *
import tweepy_functions
import sys
import io
from pandas.io.json import json_normalize
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# u = api.get_user(783214)


tweet_attribs = ['id_str', 'text']
user_attribs = ['id_str', 'name', 'screen_name', 'description', 'friends_count']

# Get tweet from hastag.
max_tweets = 20
tweets = tweepy.Cursor(api.search, q='the first temptation of christ', rpp=100).items(max_tweets)

l = [jsonify_tweepy(tweet) for tweet in tweets]
df = json_normalize(l)
export_path = r'.\data\tweets.xlsx'
df.to_excel(export_path)

# tweet_dict = {}
# for tweet in tweets:
#     tweet_json = jsonify_tweepy(tweet)
#     print(tweet_json)
#     for attrib in tweet_attribs:
#         if attrib in tweet_dict:
#             tweet_dict[attrib].append(tweet_json[attrib])
#         else:
#             tweet_dict[attrib] = [tweet_json[attrib]]
#     for attrib in user_attribs:
#         prefixed_attrib = 'user_' + attrib
#         if prefixed_attrib in tweet_dict:
#             tweet_dict[prefixed_attrib].append(tweet_json['user'][attrib])
#         else:
#             tweet_dict[prefixed_attrib] = [tweet_json['user'][attrib]]

# df = pd.DataFrame(tweet_dict)
# print(df)
#
# export_path = r'.\data\tweets.xlsx'
# df.to_excel(export_path)


# print(public_tweets[0].user)
# print(dict['name'])
# needed features: id,


# for tweet in public_tweets:
#     print(tweet.user)
# print(tweet.user.name + ': ' + tweet.text)
