import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from real_time.custom_search import CustomSearchClient
from data.api_sports import get_live_scores

def main():
    # Custom search example
    client = CustomSearchClient()
    query = 'batman'
    df = client.search(query)

    # Test case to see if it can pull the raw content from a page
    if df is not None and not df.empty:
        first_result_full_content = df.iloc[0]['FullContent']
        print("Full content of the first search result (text only):")
        print(first_result_full_content)
    else:
        print('No results found or an error occurred.')

    # Rendering the api values
    live_scores = get_live_scores()
    if live_scores:
        print("Live football scores:")
        print(live_scores)
    else:
        print("Failed to retrieve live scores")

if __name__ == '__main__':
    main()
