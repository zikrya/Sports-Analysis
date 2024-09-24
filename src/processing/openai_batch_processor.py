import openai
import os
from dotenv import load_dotenv
import asyncio
import time
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert
from models.ai_response import AIResponse
from models.external_factor import ExternalFactor
from config.db import get_db
from datetime import datetime

class OpenAIClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            load_dotenv()
            openai.api_key = os.getenv('OPENAI_API_KEY')

            cls._instance = super(OpenAIClient, cls).__new__(cls)
            cls.client = openai

        return cls._instance

    # Function to process prompts with retry logic and exponential backoff
    async def ai_processor(self, prompt, retries=3, backoff_factor=2):
        system_prompt = (
            "You are an intelligent assistant that specializes in analyzing sports data. "
            "Your task is to analyze trends in player injuries, performance metrics, weather impact, and external factors. "
            "Provide a comprehensive analysis that includes actionable insights and correlations."
        )

        user_prompt = (
            f"Analyze the following data and generate trends for the team. Break the analysis into the following categories:\n\n"
            "1. **Injuries**: Trends related to injuries (frequency, severity, and their impact).\n"
            "2. **Performance Metrics**: Key performance trends such as passing accuracy, defense efficiency, and player stats.\n"
            "3. **Weather Impact**: How weather conditions (rain, wind, temperature) affected gameplay.\n"
            "4. **External Factors**: Impact of off-field events, morale, public sentiment, etc.\n\n"
            f"Data: {prompt}\n"
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
                print( response.choices[0].message.content)
                return response.choices[0].message.content.strip()
            except openai.error.RateLimitError as e:
                if attempt < retries - 1:
                    sleep_time = backoff_factor ** attempt
                    print(f"Rate limit hit. Retrying in {sleep_time} seconds...")
                    time.sleep(sleep_time)
                else:
                    print(f"RateLimitError: {e}. Max retries reached. Exiting...")
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

# Asynchronously process batches with chunking and save raw AI responses to DB
async def process_batches(client, batched_data, team_id, db_session: AsyncSession):
    results = {}

    for tag, batches in batched_data.items():
        results[tag] = []

        for batch in batches:
            tasks = [client.ai_processor(article) for article in batch]
            responses = await asyncio.gather(*tasks)

            # Save raw AI responses to the DB
            await save_ai_results_to_db(responses, tag, team_id, db_session)

            results[tag].extend(responses)

    return results

# Save AI response to the database in the AIResponses table
async def save_ai_results_to_db(ai_responses, category, team_id, db_session: AsyncSession):
    for response in ai_responses:
        if not response:
            continue

        # Store raw AI response in the AIResponses table
        new_ai_response = AIResponse(
            team_id=team_id,
            response_text=response,
            category=category,
            generated_at=datetime.utcnow()
        )
        db_session.add(new_ai_response)
    await db_session.commit()

# Process team data, batching and saving results
async def process_team_data(data_by_tag, team_name, team_id, db_session: AsyncSession):
    client = OpenAIClient()

    # Batch data by tags
    batched_data = batch_data_by_tags(data_by_tag)

    # Process batches and save AI responses to DB
    ai_responses = await process_batches(client, batched_data, team_id, db_session)

    print(f"Processed data for team {team_name}")
    return ai_responses
