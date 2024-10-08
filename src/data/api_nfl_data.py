import os
import requests
from dotenv import load_dotenv

# Load API key
load_dotenv()
API_KEY = os.getenv('RAPIDAPI_KEY')

headers = {
    'X-RapidAPI-Key': API_KEY,
    'X-RapidAPI-Host': 'nfl-api-data.p.rapidapi.com'
}

# Function to fetch data for a team by team_id
def fetch_team_data(team_id):
    urls = {
        "team_stats": f"https://nfl-api-data.p.rapidapi.com/nfl-team-statistics?year=2023&id={team_id}",
        "team_records": f"https://nfl-api-data.p.rapidapi.com/nfl-team-record?id={team_id}&year=2023",
        "team_injuries": f"https://nfl-api-data.p.rapidapi.com/nfl-team-injuries?id={team_id}",
        "team_odds": f"https://nfl-api-data.p.rapidapi.com/nfl-team-oddsrecords?id={team_id}&year=2023",
        "team_leaders": f"https://nfl-api-data.p.rapidapi.com/nfl-team-leaders?id={team_id}&year=2023"
    }

    # Fetch data from each endpoint
    data = {}
    for key, url in urls.items():
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data[key] = response.json()
        else:
            print(f"Error fetching {key} data for team {team_id}: {response.status_code}")

    return data

# Test fetching data for two teams
if __name__ == "__main__":
    team_1_id = input("Enter Team 1 ID: ")
    team_2_id = input("Enter Team 2 ID: ")

    team_1_data = fetch_team_data(team_1_id)
    team_2_data = fetch_team_data(team_2_id)

    print(f"Team 1 Data: {team_1_data}")
    print(f"Team 2 Data: {team_2_data}")
