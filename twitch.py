import click
import urllib.parse
import requests
import json
from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

def get_userid(name, headers):
    r = requests.get(f"https://api.twitch.tv/helix/users?login={name}", headers=headers)
    data = json.loads(r.text)
    return data['data'][0]['id']

def get_followed_streams(user_id, headers):
    r = requests.get(f"https://api.twitch.tv/helix/streams/followed?user_id={user_id}", headers=headers)
    return json.loads(r.text)

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
        "client_id": os.environ['client'], 
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
        "Client-Id": os.environ['client'],
        "Authorization": "Bearer evkg1u50ujqvjtr5kbyvieccnmnoqi"
        }
    user_id = get_userid(name, headers)

    #get followed streams
    data = get_followed_streams(user_id, headers)

    for i in data['data']:
        print(f"{i['user_login']:<15} {i['game_name'][:20]:<20} {i['viewer_count']}")

if __name__ == '__main__':
    get_streams()
