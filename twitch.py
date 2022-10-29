import click
import urllib.parse
import requests
import json
from flask import Flask

app = Flask(__name__)

@app.route("/redirect")
def hello_world():
    return "<p>Hello, World!</p>"

@click.command()
# @click.option('--name', prompt='Your name',
#               help='The person to greet.')
def login():
    """
    Open browser for user to authorize our app
    """
    url = "https://id.twitch.tv/oauth2/authorize?"
    params = {
        "client_id": "dp0t996p82u064cj7dneccwa2n7auv", 
        "response_type": "token",
        "scope": "user:read:follows",
        "redirect_uri": "http://localhost:7001/redirect"}

    auth_url = "{}{}".format(url, urllib.parse.urlencode(params))
    print(auth_url)

@click.command()
@click.option('--name', prompt='twitch username',
              help='Twitch username.')
def get_streams(name):
    #get userid
    headers = {
        "Client-Id": "dp0t996p82u064cj7dneccwa2n7auv",
        "Authorization": "Bearer 8usvb9c1z4vntva0zew4ca3p10ayti"
        }
    r = requests.get(f"https://api.twitch.tv/helix/users?login={name}", headers=headers)
    data = json.loads(r.text)
    user_id = data['data'][0]['id']

    #get followed streams
    r = requests.get(f"https://api.twitch.tv/helix/streams/followed?user_id={user_id}", headers=headers)
    data = json.loads(r.text)

    for i in data['data']:
        print(f"{i['user_login']}: {i['game_name']} {i['viewer_count']}")

if __name__ == '__main__':
    get_streams()
