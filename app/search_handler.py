import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from real_time.custom_search import CustomSearchClient
from real_time.upstash_client import RedisClient


async def perform_search_and_store(search_queries):
    # Initialize Redis client
    redis_client = RedisClient().setup_redis()

    # Custom search
    client = CustomSearchClient()

    for query in search_queries:
        print(f"Searching for: {query}")
        df = client.search(query, count=3)

        if df is not None and not df.empty:
            web_content = []
            for index, row in df.iterrows():
                link = row['Link']
                full_content = row['FullContent']

                if full_content:
                    web_content.append({'link': link, 'content': full_content})

            # web content in Redis under web_content key
            redis_client.set(f"team:{query}:web_content", web_content)
            print(f"Stored web content for query '{query}' in Redis.")

        else:
            print(f'No results found or an error occurred for query: {query}')