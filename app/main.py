import sys
import os
import asyncio

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ai_handler import generate_search_queries
from search_handler import perform_search_and_store
from api_handler import fetch_team_stats


async def fetch_data_for_team(team_name):
    # Fetch both  data in parallel
    api_task = asyncio.create_task(fetch_team_stats(team_name))
    search_task = asyncio.create_task(generate_and_store_search_data(team_name))

    # complete both tasks
    await asyncio.gather(api_task, search_task)


async def generate_and_store_search_data(question):
    search_queries = generate_search_queries(question)
    await perform_search_and_store(search_queries)


async def main():
    team1 = input("Enter the first team (e.g., 'Philadelphia Eagles'): ").strip()
    team2 = input("Enter the second team (e.g., 'Atlanta Falcons'): ").strip()

    question = f"Which team is likely to win, {team1} or {team2}?"
    print(f"User question: {question}\n")

    await asyncio.gather(
        fetch_data_for_team(team1),
        fetch_data_for_team(team2)
    )


if __name__ == '__main__':
    asyncio.run(main())
