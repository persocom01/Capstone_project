import pandas as pd
import tweepy
import tweepy_functions as tf
import json
import zipfile
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

# Change to change save folder and filename.
folder_path = r'.\data'
out_file = ''

# Connect to twitter api.
with open(r'.\twitter_scraping\keys.json') as f:
    keys = json.load(f)

auth = tweepy.OAuthHandler(keys['consumer_key'], keys['consumer_secret'])
auth.set_access_token(keys['access_token'], keys['access_token_secret'])
# wait_on_rate_limit=True avoids error 429 for hitting twitter api limits.
api = tweepy.API(auth, wait_on_rate_limit=True)
compression = zipfile.ZIP_DEFLATED

with open(r'all_tweet_ids.json') as f:
    ids = json.load(f)

print('total ids:', len(ids))

all_data = []
for id in ids:
    try:
        data = api.get_status(id, tweet_mode='extended')
        data_json = tf.jsonify_tweepy(data)
        all_data.append(data_json)
    # Continue if a banned id is encountered.
    except tweepy.error.TweepError:
        continue

# Create zipped master json file.
print('creating zipped master json file.')
export_path = f'{folder_path}\\{out_file}.csv'
zf = zipfile.ZipFile(export_path, mode='w')
output_file = f'{out_file}.json'
zf.write(output_file, compress_type=compression)
zf.close()

# Create excel readable csv file.
print('creating flattened csv file.')
df = pd.io.json.json_normalize(all_data)  # Flattens the json file.
export_path = f'{folder_path}\\{out_file}.csv'
df.to_csv(export_path, index=None)
