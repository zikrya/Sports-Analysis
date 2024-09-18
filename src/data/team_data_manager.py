import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import json
import requests
from src.config.config import BASE_URL, HEADERS, TEAM_DATA_FILE


def load_team_data():
    if not os.path.exists(TEAM_DATA_FILE):
        print(f"Team data file {TEAM_DATA_FILE} not found.")
        return {}

    with open(TEAM_DATA_FILE, 'r') as file:
        return json.load(file)

# save team data to local JSON data
def save_team_data(data):
    with open(TEAM_DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)
    print(f"Team data saved to {TEAM_DATA_FILE}.")

# update team data with API
def update_team_data():
    url = f"{BASE_URL}/teams?league=1&season=2022"
    response = requests.get(url, headers=HEADERS)
    api_data = response.json()

    if 'response' in api_data:
        team_data = {team['name']: team['id'] for team in api_data['response']}
        save_team_data(team_data)
        print(f"Populated team data:\n{json.dumps(team_data, indent=4)}")
    else:
        print("Failed to fetch data from API.")

# retrieve team ID by team name from JSON
def get_team_id_by_name(team_name):
    team_data = load_team_data()

    # Check if 'teams' key exists and iterate through the list
    if 'teams' in team_data:
        for team in team_data['teams']:
            if team['name'].lower() == team_name.lower():
                return team['id']

    print(f"Team '{team_name}' not found in local data.")
    return None
