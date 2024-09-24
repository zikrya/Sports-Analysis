import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from config.db import engine, Base

from models.team import Team
from models.player import Player
from models.game import Game
from models.performance import Performance
from models.weather import Weather
from models.injury import Injury

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    asyncio.run(create_tables())
