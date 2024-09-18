import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ai_handler import generate_search_queries
from search_handler import perform_search_and_store

def main():
    question = "Which team is likely to win, Eagles or Falcons?"
    print(f"User question: {question}\n")

    # search queries using OpenAI
    search_queries = generate_search_queries(question)
    print()

    perform_search_and_store(search_queries)

if __name__ == '__main__':
    main()
