import openai
import os
from dotenv import load_dotenv

class OpenAIClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            load_dotenv()
            api_key = os.getenv('OPENAI_API_KEY')

            cls._instance = super(OpenAIClient, cls).__new__(cls)
            cls.client = openai.OpenAI(api_key=api_key)

        return cls._instance

    def ai_processor(self, prompt):
        system_prompt = "You'll answer all questions well."

        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content.strip()

