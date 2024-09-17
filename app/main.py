import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from real_time.custom_search import CustomSearchClient

def main():
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

if __name__ == '__main__':
    main()
