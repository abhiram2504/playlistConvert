import requests
import json
import base64
from dotenv import load_dotenv
import os

def get_user_id(headers):
    url = "https://api.spotify.com/v1/me"
    req = requests.get(url, headers=headers)
    res = json.loads(req.content)
    user_id = res["id"]
    return user_id


if __name__ == "main":
    print("hello world")

    
    