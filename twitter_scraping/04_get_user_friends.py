import json
import tweepy
import pandas as pd
import math
import shutil
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

# Change to change save folder and filename.
folder_path = r'.\data'
in_file = '#michellewilliams_users'
start = 329
batch_size = 20

# Connect to twitter api.
with open(r'.\twitter_scraping\keys.json') as f:
    keys = json.load(f)

auth = tweepy.OAuthHandler(keys['consumer_key'], keys['consumer_secret'])
auth.set_access_token(keys['access_token'], keys['access_token_secret'])
# wait_on_rate_limit=True avoids error 429 for hitting twitter api limits.
api = tweepy.API(auth, wait_on_rate_limit=True)

import_path = folder_path + '\\' + in_file + '.csv'
data = pd.read_csv(import_path)

# Divide users into batches.
batches = math.ceil((data.shape[0] - start) / batch_size)

for i in range(batches):

    # Check for last batch.
    if i == batches - 1:
        user_ids = data['user.id_str'][start:]
        print(
            f'scraping {start} to {data.shape[0]} out of {data.shape[0]} ids.')
    else:
        user_ids = data['user.id_str'][start:(start + batch_size)]
        print(
            f'scraping {start} to {(start + batch_size)} out of {data.shape[0]} ids.')
        start += batch_size

    users_friends = {}
    for i, id in enumerate(user_ids):
        try:
            # Gets all a user's friends.
            friends = []
            tweepy_object = tweepy.Cursor(api.friends_ids, user_id=id).items()
            for friend in tweepy_object:
                friends.append(friend)
            print(f'{i+1}. getting user {id}\'s {len(friends)} friends.')
            users_friends[str(id)] = friends

            # Loads old file to continue where it left off and saves it back.
            out_file = in_file + '_friends.json'
            export_path = f'{folder_path}\\{out_file}'
            try:
                with open(export_path) as f:
                    users_friends = dict(
                        list(dict(json.load(f)).items()) + list(users_friends.items()))
                    print('users in file: ', len(users_friends))
            except FileNotFoundError:
                with open(export_path, 'w') as f:
                    print('users in file: ', len(users_friends))
            with open(export_path, 'w') as outfile:
                json.dump(users_friends, outfile)

        # Continue if not authorized to scrape user.
        except tweepy.error.TweepError as err:
            print(f'TweepError encountered: {err}')
            print('continuing...')
            continue

    # Create batch backup.
    shutil.copyfile(
        export_path, f'{folder_path}\\{in_file}' + '_friends.batch')

print('all done.')
