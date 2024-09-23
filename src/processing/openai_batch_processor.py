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
            "You are an intelligent assistant that specializes in analyzing complex datasets. Your task is to identify trends and key insights across various aspects of sports data, such as player injuries, performance metrics, weather impact, and external factors. "
            "Provide a comprehensive analysis that highlights patterns, correlations, and actionable insights for each of these categories."
        )

        user_prompt = (
            f"Analyze the following data and generate trends for the team. Break the analysis into the following categories:\n\n"
            "1. **Injuries**: Identify patterns or trends related to player injuries, including frequency, severity, and their impact on the team’s overall performance. Highlight whether certain positions or players are more prone to injuries and examine any correlation between injuries and game outcomes.\n"
            "2. **Performance Metrics**: Analyze the team’s key performance metrics, including passing accuracy, defense efficiency, scoring trends, and individual player statistics. Identify any trends in performance across multiple games, particularly under conditions such as injuries, substitutions, or changes in player roles.\n"
            "3. **Weather Impact**: Evaluate how weather conditions (rain, wind, temperature) affected the team's gameplay. Identify patterns where specific weather conditions correlate with better or worse performance, including potential impacts on passing, rushing, and defense.\n"
            "4. **External Factors**: Examine external factors such as player morale, public sentiment, and off-field events (e.g., contract disputes, personal life issues). Identify recurring themes and trends that influenced individual and team performance, as well as game outcomes.\n\n"
            f"Data: {prompt}\n"
            "Provide a well-structured, coherent analysis that considers all available information."
        )

        for attempt in range(retries):
            try:
                response = self.client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
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
def batch_data_by_tags(data_by_tag, batch_size=5):
    batched_data = {}

    # Create batches for each tag category
    for tag, articles in data_by_tag.items():
        batched_data[tag] = [
            articles[i:i + batch_size]
            for i in range(0, len(articles), batch_size)
        ]

    return batched_data

# Asynchronously process batches with chunking and retry logic
async def process_batches(client, batched_data):
    results = {}

    for tag, batches in batched_data.items():
        results[tag] = []

        for batch in batches:
            tasks = []
            for article in batch:
                tasks.append(client.ai_processor(article))

            # Await and collect all responses for the current batch
            responses = await asyncio.gather(*tasks)
            results[tag].extend(responses)

    return results

async def process_team_data(data_by_tag, team_name):
    client = OpenAIClient()

    # Batch the data by tags
    batched_data = batch_data_by_tags(data_by_tag)

    # Process batches asynchronously
    ai_responses = await process_batches(client, batched_data)

    print(f"Processed data for team {team_name}")
    return ai_responses
