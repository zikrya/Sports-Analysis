import asyncpg
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

async def connect_db():
    conn = await asyncpg.connect(os.getenv('DB_CONNECTION_STRING'))
    return conn
