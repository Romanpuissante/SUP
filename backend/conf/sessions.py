import os
from pathlib import Path
from dotenv import load_dotenv

import sqlalchemy
import databases

import aioredis

BASE_DIR = Path(__file__).parent.parent.parent
load_dotenv(BASE_DIR.joinpath(".env"))

database = databases.Database(os.environ["DATABASE_URL"].replace("postgresql://", "postgresql+asyncpg://"))
metadata = sqlalchemy.MetaData()


async def get_redis_pool():
    return await aioredis.from_url("redis://redis", encoding="utf-8", decode_responses=True)


