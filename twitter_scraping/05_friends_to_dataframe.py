import pandas as pd
import tweepy
import tweepy_functions as tf
import json
import zipfile
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')
#
# df = pd.read_json(
#     r'.\data\#michellewilliams_users_friends - Copy.json', columns=['id', 'friends'])
# print(df.shape)

with open(r'.\data\#michellewilliams_users_friends - Copy.json') as f:
    ids = json.load(f)

user_ids = [k for k, v in ids.items()]
friends = [v for k, v in ids.items()]
print(len(user_ids))

dic = {'ids': user_ids, 'friends': friends}
# dic2 = {'friends': [] for k, v in ids.items()}

print(len(dic))

# dic.update(dic2)
df = pd.DataFrame.from_dict(dic)
print(len(df['friends'][339]))

#
# print(len(ids))
# print(ids)
