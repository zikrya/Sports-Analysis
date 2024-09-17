import requests
from bs4 import BeautifulSoup

class WebScraper:
    def scrape_page_content(self, url):
        """Scrape the text content from the given URL with headers."""
        # Trying to mimic real users when going through pages
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Remove uneccesary content
            for tag in soup(['footer', 'nav', 'header', 'aside']):
                tag.decompose()

            # Get all the text from the page and clean up the tags
            page_text = soup.get_text(separator=' ', strip=True)
            return page_text
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred while scraping {url}: {http_err}")
            return None
        except Exception as e:
            print(f"Failed to scrape {url}: {e}")
            return None
