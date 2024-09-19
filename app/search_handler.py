import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from real_time.custom_search import CustomSearchClient
from real_time.upstash_client import RedisClient

# Tagging based on query content
def tag_query(query):
    if 'injuries' in query.lower():
        return ['injury']
    elif 'weather' in query.lower():
        return ['weather']
    elif 'performance' in query.lower():
        return ['performance']
    else:
        return ['general']

async def perform_search_and_store(search_queries, team_name):
    # Initialize Redis client
    redis_client = RedisClient().setup_redis()

    # Custom search
    client = CustomSearchClient()

    for query in search_queries:
        print(f"Searching for: {query}")
        df = client.search(query, count=3)

        if df is not None and not df.empty:
            web_content = []
            tags = tag_query(query)
            for index, row in df.iterrows():
                link = row['Link']
                full_content = row['FullContent']

                if full_content:
                    web_content.append({'link': link, 'content': full_content, 'tags': tags})

            # Store the web content in Redis under the team-specific key
            redis_client.set(f"team:{team_name}:web_content", web_content)
            print(f"Stored web content for {team_name} and query '{query}' in Redis with tags {tags}.")

        else:
            print(f'No results found or an error occurred for query: {query}')
