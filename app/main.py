import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from real_time.custom_search import CustomSearchClient
from data.api_sports import get_live_scores
from real_time.upstash_client import RedisClient  # Import the Redis client

def main():
    # Initialize Redis client
    redis_client = RedisClient().setup_redis()

    # Custom search example
    client = CustomSearchClient()
    query = 'batman'
    df = client.search(query)

    # Test case to see if it can pull the raw content from a page
    if df is not None and not df.empty:
        for index, row in df.iterrows():
            link = row['Link']
            full_content = row['FullContent']

            # Store each page's content in Redis with the link as the key
            if full_content:
                redis_client.set(link, full_content)
                print(f"Stored content from {link} into Redis.")

        # Example to retrieve the content back from Redis
        first_result_link = df.iloc[0]['Link']
        redis_content = redis_client.get(first_result_link)
        if redis_content:
            print(f"Retrieved content from Redis for {first_result_link}:")
            print(redis_content)
    else:
        print('No results found or an error occurred.')

    # Rendering the API values
    live_scores = get_live_scores()
    if live_scores:
        print("Live football scores:")
        # print(live_scores)
    else:
        print("Failed to retrieve live scores")

if __name__ == '__main__':
    main()
