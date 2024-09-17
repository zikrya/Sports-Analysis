import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')
BASE_URL = "https://v3.football.api-sports.io"


# Calling an api to render data
def get_live_scores():
    headers = {
        'x-rapidapi-key': API_KEY,
        'x-rapidapi-host': "v3.football.api-sports.io"
    }
    url = f"{BASE_URL}/fixtures?live=all"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None
