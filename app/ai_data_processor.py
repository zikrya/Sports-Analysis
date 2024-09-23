import sys
import asyncio
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))


from data.data_fetcher import fetch_data_by_tags
from processing.openai_batch_processor import process_team_data


if __name__ == "__main__":
    team_name = "Atlanta Falcons"
    tags = ["general"]

    # Fetch the data
    preprocessed_data = fetch_data_by_tags(team_name, tags)

    if preprocessed_data:
        print(f"Fetched data for tags {tags} under team {team_name}:")
        for article in preprocessed_data:
            print(f"Article: {article['content']}, Tags: {article['tags']}")

        # Ensure you pass both `preprocessed_data` and `team_name` to process_team_data
        asyncio.run(process_team_data(preprocessed_data, team_name))
    else:
        print(f"No data found for tags {tags} under team {team_name}.")
