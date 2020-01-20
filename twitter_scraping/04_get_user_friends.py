import pandas as pd
import tweepy
import json
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

# Change to change save folder and filename.
folder_path = r'.\data'
in_file = '#michellewilliams_users'
start = 46
end = 47

# Connect to twitter api.
with open(r'.\twitter_scraping\keys.json') as f:
    keys = json.load(f)

auth = tweepy.OAuthHandler(keys['consumer_key'], keys['consumer_secret'])
auth.set_access_token(keys['access_token'], keys['access_token_secret'])
# wait_on_rate_limit=True avoids error 429 for hitting twitter api limits.
api = tweepy.API(auth, wait_on_rate_limit=True)

import_path = folder_path + '\\' + in_file + '.csv'
data = pd.read_csv(import_path)
user_ids = data['user.id_str'][start:end]

print(f'scraping {start} to {end} out of {data.shape[0]} ids.')

users_friends = {}
for i, id in enumerate(user_ids):
    friends = []
    print(f'{i+1}. getting friends for user {id}.')
    tweepy_object = tweepy.Cursor(api.friends_ids, user_id=id).items()
    for friend in tweepy_object:
        friends.append(friend)
    print(f'user {id} has {len(friends)} friends.')
    users_friends[str(id)] = friends

    # The data is saved into two files to prevent file corruption when the
    # program is terminated early.
    out_file = in_file + '_friends.json'
    export_path = f'{folder_path}\\{out_file}'
    try:
        with open(export_path) as f:
            users_friends = dict(list(dict(json.load(f)).items()) + list(users_friends.items()))
            print('users in file: ', len(users_friends))
    except FileNotFoundError:
        with open(export_path, 'w') as f:
            print('users in file: ', len(users_friends))

    with open(export_path, 'w') as outfile:
        json.dump(users_friends, outfile)

print('all done.')
