import os
from eventregistry import *
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('NEWS_API_KEY')

er = EventRegistry(apiKey=API_KEY)

def fetch_articles(keyword, max_results=10):
    q = QueryArticlesIter(keywords=keyword)
    for art in q.execQuery(er, returnInfo=ReturnInfo(articleInfo=ArticleInfoFlags(body=True)), maxItems=max_results):
        print(f"Title: {art.get('title', 'No title')}")
        print(f"Author: {art.get('author', 'No author')}")
        print(f"Source: {art.get('source', {}).get('title', 'No source')}")
        print(f"Published At: {art.get('date', 'No date')}")
        print(f"Content: {art.get('body', 'No content')}\n")
def main():
    keyword = 'Bitcoin'
    max_results = 5
    print(f"Fetching articles about {keyword}...\n")
    fetch_articles(keyword, max_results)

if __name__ == '__main__':
    main()
