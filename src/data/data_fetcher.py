import sys
import os
import json

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'real_time'))

from upstash_client import RedisClient
# fetch data based on tags
def fetch_data_by_tags(team_name, tags):
    # Initialize Redis client
    redis_client = RedisClient().setup_redis()

    # Fetch all stored content for the given team from Redis
    raw_content = redis_client.get(f"team:{team_name}:web_content")

    if not raw_content:
        print(f"No web content found for team {team_name}")
        return []

    try:
        # Deserialize JSON
        team_content = json.loads(raw_content)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return []

    # Filter the content based on the tags
    filtered_data = [article for article in team_content if any(tag in article['tags'] for tag in tags)]

    return filtered_data