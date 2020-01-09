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

# u = api.get_user(783214)


# tweet_attribs = ['id_str', 'text']
# user_attribs = ['id_str', 'name', 'screen_name', 'description', 'friends_count']

# Get tweet from hastag.
max_tweets = 1000
search = tweepy.Cursor(api.search, q='the first temptation of christ', rpp=100).items(max_tweets)

tweets = [tf.jsonify_tweepy(tweet) for tweet in search]
df = pd.io.json.json_normalize(tweets)
export_path = r'.\data\the_first_temptation_of_christ.csv'
df.to_csv(export_path)

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
