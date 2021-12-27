import os
from pathlib import Path
from dotenv import load_dotenv

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

import aioredis
from broadcaster import Broadcast


BASE_DIR = Path(__file__).parent.parent.parent
load_dotenv(BASE_DIR.joinpath(".env"))

engine = create_async_engine(
    os.environ["DATABASE_URL"].replace("postgresql://", "postgresql+asyncpg://"),
    echo=False,
)

async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


redis = aioredis.from_url("redis://redis", decode_responses=True)
broadcast = Broadcast("redis://redis")