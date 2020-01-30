

def jsonify_tweepy(tweepy_object):
    import json

    json_str = json.dumps(tweepy_object._json)
    return json.loads(json_str)


def get_latest_tweet_id(filepath):
    import pandas as pd

    import_path = filepath
    data = pd.read_csv(import_path, low_memory=False, index_col=0)
    return data['id_str'][0]
