import sys
import os
import requests
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.config.config import BASE_URL, HEADERS
from src.data.team_data_manager import load_team_data, get_team_id_by_name

# Scrub game data with season/year
def scrub_game_data(games, season):
    scrubbed_games = []
    for game in games:
        game_info = {
            "season": season,
            "home_team": game.get('teams', {}).get('home', {}).get('name', 'N/A'),
            "away_team": game.get('teams', {}).get('away', {}).get('name', 'N/A'),
            "home_score": game.get('scores', {}).get('home', {}).get('total', 'N/A'),
            "away_score": game.get('scores', {}).get('away', {}).get('total', 'N/A'),
            "status": game.get('status', {}).get('short', 'N/A')
        }
        scrubbed_games.append(game_info)
    return scrubbed_games

# Fetch team games for a specific season
def get_team_games_by_season(team_id, season):
    url = f"{BASE_URL}/games?team={team_id}&season={season}"
    response = requests.get(url, headers=HEADERS)
    data = response.json()

    if 'response' in data and data['response']:
        games = data['response']
        scrubbed_data = scrub_game_data(games, season)
        print(f"Scrubbed games for {season}: {scrubbed_data}")
        return scrubbed_data
    else:
        print(f"No games data found for the {season} season.")
        return {}

# Fetch player statistics for a game
def get_player_statistics(game_id):
    url = f"{BASE_URL}/games/statistics/players?id={game_id}"
    response = requests.get(url, headers=HEADERS)
    data = response.json()
    print(f"Player Game Statistics: {data}")
    return data

# Fetch stats for multiple seasons
def get_team_games_by_multiple_seasons(team_id, seasons):
    all_season_data = {}
    for season in seasons:
        print(f"\nFetching games for the {season} season...")
        season_data = get_team_games_by_season(team_id, season)
        all_season_data[season] = season_data
    return all_season_data

# Fetch current injuries for a team
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

    # Seasons to fetch (e.g., last 10 years)
    seasons = list(range(2013, 2024))

    # Fetch statistics for multiple seasons
    print(f"\nFetching statistics for {team_name} for multiple seasons...")
    multi_season_stats = get_team_games_by_multiple_seasons(team_id, seasons)

    # Print out the statistics for verification
    print("\nMulti-season statistics fetched:")
    print(multi_season_stats)

if __name__ == "__main__":
    main()
