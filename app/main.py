import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from real_time.custom_search import CustomSearchClient
from real_time.upstash_client import RedisClient

def main():
    # Initialize Redis client
    redis_client = RedisClient().setup_redis()

    # Custom search
    client = CustomSearchClient()
    query = 'Latest football sports news'
    df = client.search(query, count=3)

    # Check if DataFrame has valid data
    if df is not None and not df.empty:
        for index, row in df.iterrows():
            link = row['Link']
            full_content = row['FullContent']

            # Store each page's content in Redis with the link as the key
            if full_content:
                redis_client.set(link, full_content)
                print(f"Stored content from {link} into Redis.")

        # retrieve the content  from Redis
        first_result_link = df.iloc[0]['Link']
        redis_content = redis_client.get(first_result_link)
        if redis_content:
            print(f"Retrieved content from Redis for {first_result_link}:")
            print(redis_content[:500])
    else:
        print('No results found or an error occurred.')

if __name__ == '__main__':
    main()
