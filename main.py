from dotenv import load_dotenv
import os
import requests
import youtube_dl
from spotipy.oauth2 import SpotifyOAuth
import base64
import json
import playlistConvert.user as user

load_dotenv()

# Spotify Authentication
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
redirect_uri = "http://localhost:8000/"

'''
We first to request an access token using client id and client secret then usign that tocken we can access the Spotify API.
We get back a JSON object. The tocken expiry is 3600 seconds or 10 minutes. 
we send it to /api/token endpoint and we get back a JSON object with the access token and refresh token.
'''

def get_access_token():
    # Initialize Spotify API
    #we have to send a post request to the endpoint
    auth_str = f"{client_id}:{client_secret}"
    auth_bytes = auth_str.encode("UTF-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": f"Basic {auth_base64}",
        "Content-type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "client_credentials"
    }
    req = requests.post(url, headers=headers, data=data)
    res = json.loads(req.content)
    token = res["access_token"]
    return token
    # we will need to use this token to use this token to access the Spotify API in the header

# get header
def get_header(token):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    return headers

# get user id
def get_user_id(headers):
    url = "https://api.spotify.com/v1/me"
    req = requests.get(url, headers=headers)
    res = json.loads(req.content)
    user_id = res["id"]
    return user_id

# create a playlist
def create_playlist(headers, id, name):
    url = f"https://api.spotify.com/v1/users/{id}/playlists"
    data = {
        "name": name
    }
    req = requests.post(url, headers=headers, data=data)
    res = json.loads(req.content)
    playlist_id = res["id"]
    return playlist_id


if __name__ == "__main__":
    token = get_access_token()
    header = get_header(token)
    create_playlist(header, "Test Playlist")

    

