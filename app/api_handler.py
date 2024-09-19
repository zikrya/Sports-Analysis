import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from data.api_sports import (
    get_team_games_by_multiple_seasons
)
from src.data.team_data_manager import get_team_id_by_name

from real_time.upstash_client import RedisClient


async def fetch_team_stats(team_name):
    redis_client = RedisClient().setup_redis()

    # data from JSON file
    team_id = get_team_id_by_name(team_name)
    if team_id is None:
        print(f"Team '{team_name}' not found.")
        return


    seasons = list(range(2013, 2022))

    # Fetch stats
    print(f"\nFetching statistics for {team_name} for multiple seasons...")
    multi_season_stats = get_team_games_by_multiple_seasons(team_id, seasons)

    # Store the API data in Redis
    redis_client.set(f"team:{team_name}:api_data", multi_season_stats)
    print(f"Stored API data for {team_name} in Redis.")

    return multi_season_stats
