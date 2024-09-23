import openai
import os
from dotenv import load_dotenv
import asyncio

class OpenAIClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            load_dotenv()
            api_key = os.getenv('OPENAI_API_KEY')

            cls._instance = super(OpenAIClient, cls).__new__(cls)
            cls.client = openai.OpenAI(api_key=api_key)

        return cls._instance

    async def ai_processor(self, prompt):
        system_prompt = (
            "you're a good assistant"
        )

        #  request to OpenAI asynchronously
        response = await self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content.strip()


# batch data based on the tags
def batch_data(preprocessed_data):
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

    return batched_data


# Asynchronously process each batch using OpenAI
async def process_batches(client, batched_data):
    results = {"injury": [], "weather": [], "performance": [], "general": []}

    for category, articles in batched_data.items():
        tasks = []
        for article in articles:
            # Create async tasks to process each article's content using OpenAI
            tasks.append(client.ai_processor(article['content']))

        # Asynchronously gather results for each category
        responses = await asyncio.gather(*tasks)
        results[category] = responses

    return results


async def process_team_data(preprocessed_data, team_name):
    # Initialize OpenAI client
    client = OpenAIClient()

    batched_data = batch_data(preprocessed_data)

    # Process batches asynchronously
    ai_responses = await process_batches(client, batched_data)

    return ai_responses
