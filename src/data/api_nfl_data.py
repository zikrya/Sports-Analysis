import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('RAPIDAPI_KEY')

headers = {
    'X-RapidAPI-Key': API_KEY,
    'X-RapidAPI-Host': 'nfl-api-data.p.rapidapi.com'
}
url = "https://nfl-api-data.p.rapidapi.com/nfl-team-listing/v1/data"

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print(f"Error: {response.status_code}")
