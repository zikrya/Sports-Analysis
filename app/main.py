import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from real_time.custom_search import CustomSearchClient

def main():
    client = CustomSearchClient()
    query = 'latest sports news'
    df = client.search(query)
    if df is not None and not df.empty:
        print(df)
    else:
        print('No results found or an error occurred.')

if __name__ == '__main__':
    main()
