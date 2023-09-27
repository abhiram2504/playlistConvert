from dotenv import load_dotenv
import os
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import base64
import json

load_dotenv()

# Spotify Authentication
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
redirect_uri = "http://localhost:3000"

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

def user_authorization():
    # Make a request to the /authorize endpoint to get an authorization code
    auth_code = requests.get('https://accounts.spotify.com/authorize', {
        'client_id': client_id,
        'response_type': 'code',
        'redirect_uri': 'https://open.spotify.com/collection/playlists',
        'scope': 'playlist-modify-private',
    })
    return auth_code

# get header
def get_auth_header(token):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    return headers

# different header for different endpoint
def get_auth_header_new():
    headers = {
        
    }
    return headers

def search_artist_id(token, artist):
    url = f"https://api.spotify.com/v1/search?q={artist}&type=artist&limit=1"
    req = requests.get(url, headers=get_auth_header(token))
    res = json.loads(req.content)["artists"]["items"]
    if res.__len__() == 0:
        print ("Artist not found with this name!")
        return None

    return res[0]["id"]

def get_artist_top_tracks(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?market=US"
    req = requests.get(url, headers=get_auth_header(token))
    res = json.loads(req.content)["tracks"]
    return res

def tracks_formatter(token_api, artist_id):
    songs_list = [[]]
    tracks = get_artist_top_tracks(token_api, artist_id)
    for track in tracks:
        songs_list.append([track["name"], track["external_urls"]["spotify"]])
    return songs_list

def get_track_id(token, track_name):
    url = f"https://api.spotify.com/v1/search?q={track_name}&type=track&limit=1"
    req = requests.get(url, headers=get_auth_header(token))
    res = json.loads(req.content)["tracks"]["items"]
    if res.__len__() == 0:
        print ("Track not found with this name!")
        return None

    return res[0]["id"]

def tracks_ids_formatter(token_api, artist_id):
    songs_list = []
    tracks = get_artist_top_tracks(token_api, artist_id)
    for track in tracks:
        songs_list.append(track["id"])
    return songs_list

def get_track_info(token, track_id):
    url = f"https://api.spotify.com/v1/tracks/{track_id}"
    req = requests.get(url, headers=get_auth_header(token))
    res = json.loads(req.content)
    return res

def play_track(token, track_id):
    url = f"https://api.spotify.com/v1/me/player/play"
    data = {
        "uris": [f"spotify:track:{track_id}"]
    }
    trackInfo = get_track_info(token, track_id)
    print(trackInfo["name"]  + " " + trackInfo["external_urls"]["spotify"])
    req = requests.put(url, headers=get_auth_header(token), data=json.dumps(data))
    res = json.loads(req.content)
    print(res)


# get user id (not working)
# This was no working because the authrization scope was not appropriate.
# TODO: fix this
def get_user_id(token):
    return "da3xyrtvbvjhqwb3lc4rmqw60"
    url = "https://api.spotify.com/v1/me"
    req = requests.get(url, headers=get_auth_header(token))

    res = json.loads(req.content)
    print(res)
    if(res["error"]):
        print("Error")
        return None
    return res["id"]
    
def get_user_profile(token):
    url = f"https://api.spotify.com/v1/users/{get_user_id(token)}"
    req = requests.get(url, headers=get_auth_header(token))
    res = json.loads(req.content)
    return res
    
def create_playlist(username, playlist_name, track_uris, public=False):
    # Initialize the Spotify API client
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                   client_secret=client_secret,
                                                   redirect_uri=redirect_uri,
                                                   scope='playlist-modify-private'))

    # Create a new playlist
    playlist = sp.user_playlist_create(username, playlist_name, public=public)

    # Add tracks to the playlist (You can add tracks by their URIs)
    
    #sp.playlist_add_items(playlist['id'], track_uris)

    return playlist



if __name__ == "__main__":
    token = get_access_token()  
    print(token)
    print(get_user_profile(token))
    artistName = input("Enter artist name: ")
    artist_id = search_artist_id(token, artistName)
    print("Do you want artist top tracks? (y/n) /n Do you want to play artist top tracks? (p)")
    choice = input()
    if choice == "y":
        print(tracks_formatter(token, artist_id))
    elif choice == "p":
        print("Playing artist top tracks")
        arr = tracks_ids_formatter(token, artist_id)
        for track in arr:
            play_track(token, track)
    else:
        print("Wrong input")




