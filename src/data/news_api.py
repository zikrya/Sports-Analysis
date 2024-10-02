import os
from eventregistry import *
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('NEWS_API_KEY')

er = EventRegistry(apiKey=API_KEY)

def fetch_articles(team_name, optional_keywords, start_date, end_date, max_results=4):
    usa_location_uri = er.getLocationUri("United States")

    q = QueryArticlesIter(
        keywords=QueryItems.AND([team_name]),
        dateStart=start_date,
        dateEnd=end_date,
        sourceLocationUri=usa_location_uri
    )

    articles = []

    for art in q.execQuery(er, returnInfo=ReturnInfo(articleInfo=ArticleInfoFlags(body=True)), maxItems=max_results):
        if any(keyword in art.get('title', '') or keyword in art.get('body', '') for keyword in optional_keywords):
            article_data = {
                'title': art.get('title', 'No title'),
                'author': art.get('author', 'No author'),
                'source': art.get('source', {}).get('title', 'No source'),
                'published_at': art.get('date', 'No date'),
                'content': art.get('body', 'No content')
            }
            articles.append(article_data)

    return articles
