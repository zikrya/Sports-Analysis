import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

import json
import re
from real_time.openai_processor import OpenAIClient

def generate_search_queries(question):
    openai_client = OpenAIClient()

    prompt = f"Generate 3-5 search queries for external factors that could affect the outcome of this question: {question}. Return the response as a JSON array of strings."

    response = openai_client.ai_processor(prompt)

    try:
        clean_response = re.sub(r'```json\s*|\s*```', '', response).strip()

        queries = json.loads(clean_response)

        if not isinstance(queries, list):
            raise ValueError("Expected a list of queries")

        print("OpenAI generated the following search queries:")
        for i, query in enumerate(queries, 1):
            print(f"{i}. {query}")

        return queries
    except (json.JSONDecodeError, ValueError) as e:
        print(f"Error: {str(e)}")
        print("Raw response:", response)
        return []
