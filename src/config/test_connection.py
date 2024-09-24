import asyncio
from db import connect_db

async def test_connection():
    try:
        conn = await connect_db()

        version = await conn.fetchval("SELECT version();")
        print(f"PostgreSQL version: {version}")

        # Close connection
        await conn.close()

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(test_connection())
