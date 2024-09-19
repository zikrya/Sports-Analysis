import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from data.api_sports import (
    get_team_games_by_season,
    get_team_games_by_multiple_seasons,
    get_injuries,
    get_odds,
    get_player_statistics,
)
from src.data.team_data_manager import load_team_data, get_team_id_by_name


def fetch_team_stats(team_name):
    team_id = get_team_id_by_name(team_name)
    if team_id is None:
        print(f"Team '{team_name}' not found.")
        return

    # Define the seasons
    seasons = list(range(2013, 2022))

    # Fetch stats
    print(f"\nFetching statistics for {team_name} for multiple seasons...")
    multi_season_stats = get_team_games_by_multiple_seasons(team_id, seasons)

    # statis for verification
    print("\nMulti-season statistics fetched:")
    print(multi_season_stats)

    return multi_season_stats

