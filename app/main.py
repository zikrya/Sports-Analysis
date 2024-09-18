import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from real_time.custom_search import CustomSearchClient
from real_time.upstash_client import RedisClient
from real_time.openai_processor import OpenAIClient

import json
import re


# btw I used cursor to make the openai function calling for queries, and it worked!

def generate_search_queries(question):
    openai_client = OpenAIClient()

    prompt = f"Generate 3-5 search queries for external factors that could affect the outcome of this question: {question}. Return the response as a JSON array of strings."

    response = openai_client.ai_processor(prompt)

    try:
        # Remove code block markers if present
        clean_response = re.sub(r'```json\s*|\s*```', '', response).strip()

        # Parse the JSON response
        queries = json.loads(clean_response)

        # Ensure queries is a list
        if not isinstance(queries, list):
            raise ValueError("Expected a list of queries")

        # Print the generated queries
        print("OpenAI generated the following search queries:")
        for i, query in enumerate(queries, 1):
            print(f"{i}. {query}")

        return queries
    except (json.JSONDecodeError, ValueError) as e:
        print(f"Error: {str(e)}")
        print("Raw response:", response)
        return []

def main():
    # Initialize Redis client
    redis_client = RedisClient().setup_redis()

    # Custom search
    client = CustomSearchClient()

    # User's question
    question = "Which team is likely to win, Eagles or Falcons?"
    print(f"User question: {question}\n")

    # Generate search queries using OpenAI
    search_queries = generate_search_queries(question)
    print()  # Add a blank line for better readability

    # Perform searches and store results
    for query in search_queries:
        print(f"Searching for: {query}")
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

            # Retrieve the content from Redis for the first result
            first_result_link = df.iloc[0]['Link']
            redis_content = redis_client.get(first_result_link)
            if redis_content:
                print(f"Retrieved content from Redis for {first_result_link}:")
                print(redis_content[:500])
        else:
            print(f'No results found or an error occurred for query: {query}')

if __name__ == '__main__':
    main()
