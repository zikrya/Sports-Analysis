import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')
BASE_URL = "https://v1.american-football.api-sports.io"
HEADERS = {
    'x-rapidapi-key': API_KEY,
    'x-rapidapi-host': 'v1.american-football.api-sports.io'
}

# Corrected path to point to the JSON file within the `src/data/` directory
TEAM_DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'team_data.json')
