import os
import requests
import pandas as pd
from dotenv import load_dotenv
from real_time.web_scraper import WebScraper

class CustomSearchClient:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv('GOOGLE_API_KEY')
        self.cse_id = os.getenv('GOOGLE_CSE_ID')
        self.base_url = 'https://www.googleapis.com/customsearch/v1'
        self.scraper = WebScraper()

        if not self.api_key or not self.cse_id:
            raise ValueError('API key and CSE ID must be set in the .env file.')

    def search(self, query):
        params = {
            'key': self.api_key,
            'cx': self.cse_id,
            'q': query
        }
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()

            if 'error' in data:
                print("Error:", data['error']['message'])
                return None
            elif 'items' not in data:
                print("No search results found.")
                return None
            else:
                search_results = data['items']

                results_data = []
                for result in search_results:
                    title = result.get('title')
                    link = result.get('link')
                    snippet = result.get('snippet')

                    # Pull the raw content from the page
                    full_content = self.scraper.scrape_page_content(link)

                    results_data.append({
                        'Title': title,
                        'Link': link,
                        'Snippet': snippet,
                        'FullContent': full_content
                    })

                # Convert dictionaries into a DataFrame
                df = pd.DataFrame(results_data)
                return df
        except requests.exceptions.HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'An error occurred: {err}')
        return None
