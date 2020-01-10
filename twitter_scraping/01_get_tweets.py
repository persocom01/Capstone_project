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

api = tweepy.API(auth, wait_on_rate_limit=True)

# u = api.get_user(783214)


# tweet_attribs = ['id_str', 'text']
# user_attribs = ['id_str', 'name', 'screen_name', 'description', 'friends_count']

search_term = '#MichelleWilliams'
search_term = search_term.lower()

# Get tweet from hastag.
# max_tweets = 2500
search = tweepy.Cursor(api.search, q=search_term, rpp=100).items()

tweets = [tf.jsonify_tweepy(tweet) for tweet in search]
df = pd.io.json.json_normalize(tweets)
export_path = '.\\data\\' + search_term + '.csv'
df.to_csv(export_path, index=None)

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
