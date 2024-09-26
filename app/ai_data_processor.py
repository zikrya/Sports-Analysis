import sys
import asyncio
import os
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import sqlalchemy.exc

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

# Correct imports
from data.data_fetcher import fetch_data_for_all_tags
from processing.openai_batch_processor import process_team_data
from config.db import get_db
from models.team import Team

async def get_or_create_team(team_name, db_session: AsyncSession):
    result = await db_session.execute(select(Team).where(Team.name == team_name))
    try:
        team = result.scalar_one()
    except sqlalchemy.exc.NoResultFound:
        # Correctly convert the established year string to a datetime object
        established_year = datetime.strptime('2024-09-24', '%Y-%m-%d')  # Convert string to datetime
        new_team = Team(
            name=team_name,
            city="Atlanta",
            coach="Coach Name",
            established_year=established_year  # Pass the datetime object here
        )
        db_session.add(new_team)
        await db_session.commit()
        return new_team.id

    return team.id

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
            team_id = await get_or_create_team(team_name, db_session)  # Get or create team
            await process_team_data(preprocessed_data, team_name, team_id, db_session)  # Use the team_id
    else:
        print(f"No data found for team {team_name}.")

if __name__ == "__main__":
    asyncio.run(main())
