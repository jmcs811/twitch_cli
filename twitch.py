import click
import urllib.parse
from utils.twitch_utils import get_userid, get_followed_streams
from dotenv import load_dotenv
import socket
import os

load_dotenv()

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

    # listeon on port 7001
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("localhost", 7001))
    s.listen()
    while True:
        csock, caddr = s.accept()
        print("Connection from: " + repr(caddr))
        req = csock.recv(1024)
        print(req)
    

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
