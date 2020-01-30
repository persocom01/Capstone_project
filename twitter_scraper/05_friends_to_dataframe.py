import pandas as pd
import tweepy
import tweepy_functions as tf
import json
import zipfile
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

with open(r'.\data\#michellewilliams_users_friends.json') as f:
    ids = json.load(f)

# with open(r'.\data\#michellewilliams_users_friends2.json', 'w') as outfile:
#     json.dump(ids, outfile)

user_ids = [k for k, v in ids.items()]
friends = [v for k, v in ids.items()]
print(len(user_ids))

dic = {'ids': user_ids, 'friends': friends}

print(len(dic))

df = pd.DataFrame.from_dict(dic)
print(df['ids'][474])
print(len(df['friends'][474]))
print(df['friends'][474])
