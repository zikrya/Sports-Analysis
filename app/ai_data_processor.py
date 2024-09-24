import sys
import asyncio
import os
from sqlalchemy.ext.asyncio import AsyncSession

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

# Correct imports
from data.data_fetcher import fetch_data_for_all_tags
from processing.openai_batch_processor import process_team_data
from config.db import get_db

async def main():
    team_name = "Atlanta Falcons"

    # Fetch data for all tags
    preprocessed_data = fetch_data_for_all_tags(team_name)

    if preprocessed_data:
        print(f"Fetched data for all tags under team {team_name}:")
        for tag, articles in preprocessed_data.items():
            print(f"Tag: {tag}")
            for article in articles:
                print(f"Article: {article['content']}, Tags: {article['tags']}")

        # Establish a DB session and process the team data
        async for db_session in get_db():  # Use async for to get db_session from async generator
            await process_team_data(preprocessed_data, team_name, 1, db_session)  # Assuming team_id = 1
    else:
        print(f"No data found for team {team_name}.")

if __name__ == "__main__":
    asyncio.run(main())
