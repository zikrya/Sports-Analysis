import asyncio
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from config.db import engine, Base

# Import all your models
from models.team import Team
from models.player import Player
from models.game import Game
from models.performance import Performance
from models.weather import Weather
from models.injury import Injury
from models.ai_response import AIResponse
from models.external_factor import ExternalFactor

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    asyncio.run(create_tables())

