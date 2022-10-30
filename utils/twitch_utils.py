import requests
import json

def get_followed_streams(user_id, headers):
    r = requests.get(f"https://api.twitch.tv/helix/streams/followed?user_id={user_id}", headers=headers)
    return json.loads(r.text)

def get_userid(name, headers):
    r = requests.get(f"https://api.twitch.tv/helix/users?login={name}", headers=headers)
    data = json.loads(r.text)
    return data['data'][0]['id']