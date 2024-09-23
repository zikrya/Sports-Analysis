import sys
import os
import json

# Add the parent directory of 'real_time' to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'real_time'))

from upstash_client import RedisClient
# fetch data based on tags
def fetch_data_by_tags(team_name, tags):
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


if __name__ == "__main__":
    team_name = "Atlanta Falcons"
    tags = ["general"]

    fetched_data = fetch_data_by_tags(team_name, tags)

    if fetched_data:
        print(f"Fetched data for tags {tags} under team {team_name}:")
        for article in fetched_data:
            print(f"Article: {article['content']}, Tags: {article['tags']}")
    else:
        print(f"No data found for tags {tags} under team {team_name}.")