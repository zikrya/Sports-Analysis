import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from real_time.upstash_client import RedisClient
from processing.nlp_cleaning import clean_news_content
import json

def pull_and_clean_data(team):
    """
    Pulls news articles from Redis based on the team and cleans the content.
    """
    redis_client = RedisClient().setup_redis()

    team_key = team.replace(" ", "_").lower()
    redis_key = f'news_{team_key}'

    raw_articles = redis_client.get(redis_key)
    if raw_articles:
        articles = json.loads(raw_articles)

        cleaned_articles = []
        for article in articles:
            cleaned_content = clean_news_content(article['content'])
            article['cleaned_content'] = cleaned_content
            cleaned_articles.append(article)

        return cleaned_articles
    else:
        print(f"No articles found for {team}")
        return None

def main():
    teams = ['Atlanta Falcons', 'Philadelphia Eagles']

    for team in teams:
        print(f"Pulling and cleaning articles for {team}...\n")
        cleaned_articles = pull_and_clean_data(team)

        if cleaned_articles:
            for article in cleaned_articles:
                print(f"Title: {article['title']}")
                print(f"Cleaned Content: {article['cleaned_content']}\n")

if __name__ == '__main__':
    main()
