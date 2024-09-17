import os
import requests
import pandas as pd
from dotenv import load_dotenv
from real_time.web_scraper import WebScraper

class CustomSearchClient:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv('BING_API_KEY')
        self.base_url = 'https://api.bing.microsoft.com/v7.0/search'
        self.scraper = WebScraper()

        if not self.api_key:
            raise ValueError('API key must be set in the .env file.')
# set up search parameters to only go for 5 url linkes
    def search(self, query, count=5):
        """Search Bing API for the query and scrape page content."""
        params = {
            'q': query,
            'count': count,
            'textDecorations': True,
            'textFormat': 'HTML'
        }
        headers = {
            'Ocp-Apim-Subscription-Key': self.api_key
        }

        try:
            response = requests.get(self.base_url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()

            if 'webPages' not in data or 'value' not in data['webPages']:
                print("No search results found.")
                return None

            search_results = data['webPages']['value']

            results_data = []
            for result in search_results:
                title = result.get('name')
                link = result.get('url')
                snippet = result.get('snippet')

                # Scrape the raw content from the page
                full_content = self.scraper.scrape_page_content(link)

                results_data.append({
                    'Title': title,
                    'Link': link,
                    'Snippet': snippet,
                    'FullContent': full_content
                })

            # Convert the dictionaries into a DataFrame for easy handling
            df = pd.DataFrame(results_data)
            return df

        except requests.exceptions.HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'An error occurred: {err}')
        return None

