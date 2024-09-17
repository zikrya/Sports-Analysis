import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')
BASE_URL = "https://v1.american-football.api-sports.io"

# Headers with API Key
HEADERS = {
    'x-rapidapi-key': API_KEY,
    'x-rapidapi-host': 'v1.american-football.api-sports.io'
}

# Fetch team statistics for a game
def get_team_statistics(game_id, team_id):
    url = f"{BASE_URL}/games/statistics/teams?id={game_id}&team={team_id}"
    response = requests.get(url, headers=HEADERS)
    data = response.json()
    print(f"Team Game Statistics: {data}")
    return data

# Fetch player statistics for a game
def get_player_statistics(game_id):
    url = f"{BASE_URL}/games/statistics/players?id={game_id}"
    response = requests.get(url, headers=HEADERS)
    data = response.json()
    print(f"Player Game Statistics: {data}")
    return data

# current injuries for a team (outdated since it's on free tier for now)
def get_injuries(team_id):
    url = f"{BASE_URL}/injuries?team={team_id}"
    response = requests.get(url, headers=HEADERS)
    data = response.json()
    print(f"Current Injuries: {data}")
    return data

#  odds for a game
def get_odds(game_id):
    url = f"{BASE_URL}/odds?game={game_id}"
    response = requests.get(url, headers=HEADERS)
    data = response.json()
    print(f"Game Odds: {data}")
    return data

# placeholder since we can't get live events on free tier
def get_live_events(game_id):
    url = f"{BASE_URL}/games/events?id={game_id}"
    response = requests.get(url, headers=HEADERS)
    data = response.json()
    print(f"Live Game Events: {data}")
    return data

def main():
    # Example game and team IDs
    game_id = 1985
    team_id = 12   # eagles

    print("Fetching team stats: ")
    team_stats = get_team_statistics(game_id, team_id)

    print("\nFetching player stats: ")
    player_stats = get_player_statistics(game_id)

    print("\nFetching injuries: ")
    injuries = get_injuries(team_id)

    print("\nFetching odds: ")
    odds = get_odds(game_id)

    print("\nFetching live events: ")
    live_events = get_live_events(game_id)

if __name__ == "__main__":
    main()
