import os
from eventregistry import *
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('NEWS_API_KEY')

er = EventRegistry(apiKey=API_KEY)

def fetch_articles(team_name, optional_keywords, start_date, end_date, max_results=3):
    usa_location_uri = er.getLocationUri("United States")

    q = QueryArticlesIter(
        keywords=QueryItems.AND([team_name]),
        dateStart=start_date,
        dateEnd=end_date,
        sourceLocationUri=usa_location_uri
    )

    for art in q.execQuery(er, returnInfo=ReturnInfo(articleInfo=ArticleInfoFlags(body=True)), maxItems=max_results):
        if any(keyword in art.get('title', '') or keyword in art.get('body', '') for keyword in optional_keywords):
            print(f"Title: {art.get('title', 'No title')}")
            print(f"Author: {art.get('author', 'No author')}")
            print(f"Source: {art.get('source', {}).get('title', 'No source')}")
            print(f"Published At: {art.get('date', 'No date')}")
            print(f"Content: {art.get('body', 'No content')}\n")

def main():
    teams = ['Atlanta Falcons', 'Philadelphia Eagles']
    optional_keywords = ['NFL', 'injury', 'performance', 'stats', 'game highlights']
    start_date = '2024-09-01'
    end_date = '2024-09-30'
    max_results = 3

    for team in teams:
        print(f"Fetching articles for {team} with optional keywords {optional_keywords} from {start_date} to {end_date}...\n")
        fetch_articles(team, optional_keywords, start_date, end_date, max_results)

if __name__ == '__main__':
    main()
