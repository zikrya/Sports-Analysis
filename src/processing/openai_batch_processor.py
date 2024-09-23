import openai
import os
from dotenv import load_dotenv
import asyncio
import time
class OpenAIClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            load_dotenv()
            api_key = os.getenv('OPENAI_API_KEY')

            cls._instance = super(OpenAIClient, cls).__new__(cls)
            cls.client = openai

        return cls._instance

    # Function to process prompts with retry logic and exponential backoff
    async def ai_processor(self, prompt, retries=3, backoff_factor=2):
        system_prompt = (
            "You are an assistant. Summarize the following content in a concise manner, retaining only the key points and omitting unnecessary details."
        )

        for attempt in range(retries):
            try:
                response = self.client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt}
                    ]
                )
                print(response)
                print( response.choices[0].message.content)
                return response.choices[0].message.content.strip()
            except openai.RateLimitError as e:
                if attempt < retries - 1:
                    sleep_time = backoff_factor ** attempt
                    print(f"Rate limit hit. Retrying in {sleep_time} seconds...")
                    time.sleep(sleep_time)
                else:
                    print(f"RateLimitError: {e}. Max retries reached. Exiting...")
                    return None
            except openai.APIError as e:
                print(f"OpenAI API error: {e}")
                return None
            except openai.APIConnectionError as e:
                print(f"Failed to connect to OpenAI API: {e}")
                return None
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                return None

# Batch data into smaller chunks
def batch_data(preprocessed_data, batch_size=5):
    batched_data = {"injury": [], "weather": [], "performance": [], "general": []}

    for article in preprocessed_data:
        if "injury" in article['tags']:
            batched_data["injury"].append(article)
        elif "weather" in article['tags']:
            batched_data["weather"].append(article)
        elif "performance" in article['tags']:
            batched_data["performance"].append(article)
        else:
            batched_data["general"].append(article)

    # Break data into chunks
    for category in batched_data:
        batched_data[category] = [
            batched_data[category][i:i + batch_size]
            for i in range(0, len(batched_data[category]), batch_size)
        ]

    return batched_data

# Asynchronously  batches with chunking and retry logic
async def process_batches(client, batched_data):
    results = {"injury": [], "weather": [], "performance": [], "general": []}

    for category, articles in batched_data.items():
        for batch in articles:
            tasks = []
            for article in batch:
                tasks.append(client.ai_processor(article['content']))

            responses = await asyncio.gather(*tasks)
            results[category].extend(responses)

    return results

async def process_team_data(preprocessed_data, team_name):
    client = OpenAIClient()

    # Batch the data
    batched_data = batch_data(preprocessed_data)

    # Process batches asynchronously
    ai_responses = await process_batches(client, batched_data)

    print(f"Processed data for team {team_name}")
    return ai_responses
