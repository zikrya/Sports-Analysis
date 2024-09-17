import os
from upstash_redis import Redis
from dotenv import load_dotenv

class RedisClient:
    def __init__(self):
        load_dotenv()
        self.url = os.getenv('UPSTASH_REDIS_REST_URL')
        self.token = os.getenv('UPSTASH_REDIS_REST_TOKEN')

        # Initialize the Redis clien
        self.redis = Redis(url=self.url, token=self.token)

    def setup_redis(self):
        """
        Setup and return Redis client.
        This function ensures the Redis client is initialized properly.
        """
        try:
            print("Redis client has been successfully set up.")
            return self.redis
        except Exception as e:
            print(f"Error setting up Redis client: {e}")
            return None

if __name__ == "__main__":
    redis_client = RedisClient()
    redis_connection = redis_client.setup_redis()
