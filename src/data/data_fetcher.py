import sys
import os
import json
import re

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'real_time'))

from upstash_client import RedisClient

# Function to clean unnecessary content from the articles
def clean_article(content):
    # Remove typical fluff patterns
    fluff_patterns = [
        r"Download for free[\s\S]*",  # Remove "Download for free" ads
        r"Register now[\s\S]*",  # Remove "Register now" ads
        r"\s*\d+\s*USD yearly",  # Remove subscription pricing
        r"https?://\S+",  # Remove URLs
        r"Log in[\s\S]*",  # Remove login prompts
    ]

    for pattern in fluff_patterns:
        content = re.sub(pattern, '', content)

    # Additional cleaning: Remove excessive whitespace and footnotes
    content = re.sub(r'\s+', ' ', content).strip()

    # Further clean based on keywords: Keep sentences with stats or key phrases
    keywords = ['attendance', 'performance', 'revenue', 'fans', 'injury', 'game', 'franchise']
    sentences = content.split('.')
    important_sentences = [sentence for sentence in sentences if any(kw in sentence.lower() for kw in keywords)]

    return '. '.join(important_sentences)

# fetch data based on tags
def fetch_data_by_tags(team_name, tags):
    # Initialize Redis client
    redis_client = RedisClient().setup_redis()

    # Fetch all stored content for the given team from Redis
    raw_content = redis_client.get(f"team:{team_name}:web_content")

    if not raw_content:
        print(f"No web content found for team {team_name}")
        return []

    try:
        # Deserialize JSON
        team_content = json.loads(raw_content)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return []

    # Filter the content based on the tags and clean it
    filtered_data = [
        {"content": clean_article(article['content']), "tags": article['tags']}
        for article in team_content
        if any(tag in article['tags'] for tag in tags)
    ]

    return filtered_data
