import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ai_handler import generate_search_queries
from search_handler import perform_search_and_store
from api_handler import fetch_team_stats

def main():
    team1 = input("Enter the first team (e.g., 'Philadelphia Eagles'): ").strip()
    team2 = input("Enter the second team (e.g., 'Atlanta Falcons'): ").strip()

    question = f"Which team is likely to win, {team1} or {team2}?"
    print(f"User question: {question}\n")

    # Generate search queries using OpenAI for web scraping
    search_queries = generate_search_queries(question)
    print()

    perform_search_and_store(search_queries)

    print(f"Fetching statistics for {team1} and {team2}...\n")

    fetch_team_stats(team1)
    fetch_team_stats(team2)

if __name__ == '__main__':
    main()