

def jsonify_tweepy(tweepy_object):
    import json
    json_str = json.dumps(tweepy_object._json)
    return json.loads(json_str)
