import os
from newsapi import NewsApiClient
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('NEWS_API_KEY')

# Initialize the NewsApiClient
newsapi = NewsApiClient(api_key=API_KEY)

def fetch_top_headlines():
    """Fetches top headlines based on specific criteria."""
    top_headlines = newsapi.get_top_headlines(
        q='bitcoin',
        category='business',
        language='en',
        country='us'
    )
    return top_headlines

def fetch_all_articles():
    """Fetches all articles based on a keyword and other filters within the past month."""
    all_articles = newsapi.get_everything(
        q='bitcoin',
        sources='bbc-news,the-verge',
        domains='bbc.co.uk,techcrunch.com',
        from_param='2024-09-01',
        to='2024-09-30',
        language='en',
        sort_by='relevancy',
        page=2
    )
    return all_articles

def main():
    """Main function to run the fetch methods."""
    print("Fetching Top Headlines...")
    headlines = fetch_top_headlines()
    print(headlines)

    print("\nFetching All Articles...")
    articles = fetch_all_articles()
    print(articles)

if __name__ == '__main__':
    main()
