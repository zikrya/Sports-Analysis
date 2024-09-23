import sys
import asyncio
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

# Correct import
from data.data_fetcher import fetch_data_for_all_tags
from processing.openai_batch_processor import process_team_data

if __name__ == "__main__":
    team_name = "Atlanta Falcons"

    # Fetch data for all tags
    preprocessed_data = fetch_data_for_all_tags(team_name)

    if preprocessed_data:
        print(f"Fetched data for all tags under team {team_name}:")
        for tag, articles in preprocessed_data.items():
            print(f"Tag: {tag}")
            for article in articles:
                print(f"Article: {article['content']}, Tags: {article['tags']}")

        # Ensure you pass both `preprocessed_data` and `team_name` to process_team_data
        asyncio.run(process_team_data(preprocessed_data, team_name))
    else:
        print(f"No data found for team {team_name}.")
