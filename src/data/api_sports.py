import sys
import os
import requests
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.config.config import BASE_URL, HEADERS
from src.data.team_data_manager import load_team_data, get_team_id_by_name

# Scrub and display  game data
def scrub_game_data(games, season):
    scrubbed_games = []
    for game in games:
        game_info = {
            "season": season,
            "home_team": game.get('teams', {}).get('home', {}).get('name', 'N/A'),
            "away_team": game.get('teams', {}).get('away', {}).get('name', 'N/A'),
            "home_score": game.get('scores', {}).get('home', {}).get('total', 'N/A'),
            "away_score": game.get('scores', {}).get('away', {}).get('total', 'N/A'),
            "possession_home": game.get('statistics', [{}])[0].get('statistics', {}).get('Ball Possession', 'N/A') if game.get('statistics') else 'N/A',
            "possession_away": game.get('statistics', [{}])[1].get('statistics', {}).get('Ball Possession', 'N/A') if game.get('statistics') else 'N/A',
            "shots_home": game.get('statistics', [{}])[0].get('statistics', {}).get('Total Shots', 'N/A') if game.get('statistics') else 'N/A',
            "shots_away": game.get('statistics', [{}])[1].get('statistics', {}).get('Total Shots', 'N/A') if game.get('statistics') else 'N/A',
            "passes_home": game.get('statistics', [{}])[0].get('statistics', {}).get('Passes', 'N/A') if game.get('statistics') else 'N/A',
            "passes_away": game.get('statistics', [{}])[1].get('statistics', {}).get('Passes', 'N/A') if game.get('statistics') else 'N/A',
            "fouls_home": game.get('statistics', [{}])[0].get('statistics', {}).get('Fouls', 'N/A') if game.get('statistics') else 'N/A',
            "fouls_away": game.get('statistics', [{}])[1].get('statistics', {}).get('Fouls', 'N/A') if game.get('statistics') else 'N/A',
            "status": game.get('status', {}).get('short', 'N/A')
        }

        # Remove key-value pairs with "N/A" values
        scrubbed_game_info = {k: v for k, v in game_info.items() if v != 'N/A'}

        scrubbed_games.append(scrubbed_game_info)

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


