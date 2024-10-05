import os
import requests
from dotenv import load_dotenv

# Load API key
load_dotenv()
API_KEY = os.getenv('RAPIDAPI_KEY')

headers = {
    'X-RapidAPI-Key': API_KEY,
    'X-RapidAPI-Host': 'nfl-api-data.p.rapidapi.com'
}

urls = {
    "team_stats": "https://nfl-api-data.p.rapidapi.com/nfl-team-statistics?year=2023&id=15",
    "team_records": "https://nfl-api-data.p.rapidapi.com/nfl-team-record?id=15&year=2023",
    "team_injuries": "https://nfl-api-data.p.rapidapi.com/nfl-team-injuries?id=15",
    "team_odds": "https://nfl-api-data.p.rapidapi.com/nfl-team-oddsrecords?id=15&year=2023",
    "team_leaders": "https://nfl-api-data.p.rapidapi.com/nfl-team-leaders?id=15&year=2023",
    "game_summary": "https://nfl-api-data.p.rapidapi.com/nfl-gamesummary?id=401437954",
    "game_boxscore": "https://nfl-api-data.p.rapidapi.com/nfl-boxscore?id=401437954",
    "player_stats": "https://nfl-api-data.p.rapidapi.com/nfl-ath-statistics?id=15035&year=2023"
}

def fetch_data(url):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data from {url}: {response.status_code}")
        return None

team_stats = fetch_data(urls["team_stats"])
team_records = fetch_data(urls["team_records"])
team_injuries = fetch_data(urls["team_injuries"])
team_odds = fetch_data(urls["team_odds"])
team_leaders = fetch_data(urls["team_leaders"])
game_summary = fetch_data(urls["game_summary"])
game_boxscore = fetch_data(urls["game_boxscore"])
player_stats = fetch_data(urls["player_stats"])

print("Team Stats:", team_stats)
print("Team Records:", team_records)
print("Team Injuries:", team_injuries)
print("Team Odds:", team_odds)
print("Team Leaders:", team_leaders)
print("Game Summary:", game_summary)
print("Game Boxscore:", game_boxscore)
print("Player Stats:", player_stats)
