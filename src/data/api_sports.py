import sys
import os
import requests
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.config.config import BASE_URL, HEADERS
from src.data.team_data_manager import load_team_data, get_team_id_by_name

# Fetch team statsfor a game
def get_team_statistics(game_id, team_id):
    url = f"{BASE_URL}/games/statistics/teams?id={game_id}&team={team_id}"
    response = requests.get(url, headers=HEADERS)
    data = response.json()
    print(f"Team Game Statistics: {data}")
    return data

# Fetch player stats for a game
def get_player_statistics(game_id):
    url = f"{BASE_URL}/games/statistics/players?id={game_id}"
    response = requests.get(url, headers=HEADERS)
    data = response.json()
    print(f"Player Game Statistics: {data}")
    return data

# Fetch current injuries
def get_injuries(team_id):
    url = f"{BASE_URL}/injuries?team={team_id}"
    response = requests.get(url, headers=HEADERS)
    data = response.json()
    print(f"Current Injuries: {data}")
    return data

# Fetch odds for a game
def get_odds(game_id):
    url = f"{BASE_URL}/odds?game={game_id}"
    response = requests.get(url, headers=HEADERS)
    data = response.json()
    print(f"Game Odds: {data}")
    return data

# Fetch live events for a game (placeholder for now)
def get_live_events(game_id):
    url = f"{BASE_URL}/games/events?id={game_id}"
    response = requests.get(url, headers=HEADERS)
    data = response.json()
    print(f"Live Game Events: {data}")
    return data

# Main function to run the program
def main():
    # Load team data from the local JSON file
    team_data = load_team_data()

    if not team_data:
        print("Team data not available. Exiting.")
        return

    # Ask user for team name
    team_name = input("Enter the name of the team (e.g., 'Philadelphia Eagles'): ").strip()

    # Get the team ID using the team name
    team_id = get_team_id_by_name(team_name)
    if team_id is None:
        print(f"Team '{team_name}' not found.")
        return

    # Example game ID (you could modify this to ask for a specific game ID)
    game_id = 1985

    # Fetch and display team and player statistics
    print(f"\nFetching statistics for {team_name}...")
    team_stats = get_team_statistics(game_id, team_id)
    player_stats = get_player_statistics(game_id)

    # Fetch additional data (optional)
    print("\nFetching injuries...")
    injuries = get_injuries(team_id)

    print("\nFetching odds...")
    odds = get_odds(game_id)

    print("\nFetching live events (placeholder)...")
    live_events = get_live_events(game_id)

if __name__ == "__main__":
    main()
