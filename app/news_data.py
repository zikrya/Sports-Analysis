from datetime import datetime
import json
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from real_time.upstash_client import RedisClient
from data.news_api import fetch_articles


def main():
    teams = ['Atlanta Falcons', 'Philadelphia Eagles']
    optional_keywords = ['NFL', 'injury', 'performance', 'stats', 'game highlights']
    start_date = '2024-09-01'
    end_date = '2024-09-30'
    max_results = 3

    redis_client = RedisClient().setup_redis()

    for team in teams:
        print(f"Fetching articles for {team} with optional keywords {optional_keywords} from {start_date} to {end_date}...\n")
        articles = fetch_articles(team, optional_keywords, start_date, end_date, max_results)

        # Create or update a single key for each team
        match_id = team.replace(" ", "_").lower()
        key = f'news_{match_id}'

        # Check if there's already data for this team
        existing_data = redis_client.get(key)
        if existing_data:
            existing_articles = json.loads(existing_data)
        else:
            existing_articles = []

        # Append the new articles
        existing_articles.extend(articles)

        # Save the updated articles back to Redis
        redis_client.set(key, json.dumps(existing_articles))
        print(f"Saved/Updated articles under key: {key}")

if __name__ == '__main__':
    main()