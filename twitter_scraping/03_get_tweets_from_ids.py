import pandas as pd
import tweepy
import tweepy_functions as tf
import sys
import io
import json
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

# Connect to twitter api.
with open(r'.\twitter_scraping\keys.json') as f:
    keys = json.load(f)

auth = tweepy.OAuthHandler(keys['consumer_key'], keys['consumer_secret'])
auth.set_access_token(keys['access_token'], keys['access_token_secret'])
# wait_on_rate_limit=True avoids error 429 for hitting twitter api limits.
api = tweepy.API(auth, wait_on_rate_limit=True)

with open(r'all_tweet_ids.json') as f:
    ids = json.load(f)

stats = []
for id in ids:
    try:
        status = api.get_status(id, tweet_mode='extended')
        stat = tf.jsonify_tweepy(status)
        stats.append(stat)
    except tweepy.error.TweepError:
        continue

with open(r'.\data\#cancelnetflix.json', 'w') as outfile:
    json.dump(stats, outfile)

# retweeted_status_author = status.retweeted_status.author
# quoted_status_author = status.quoted_status.author


# df = pd.io.json.json_normalize(stats)
#
#
# export_path = r'.\data\replies_to_jk.csv'
# df.to_csv(export_path)

# print(zip(authors, ids))
# print({k: v for k, v in zip(authors, ids)})
#
# with open(r'replies.json', 'w') as outfile:
#     json.dump({k: v for k, v in zip(authors, ids)}, outfile)
