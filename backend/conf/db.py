import os
from pathlib import Path
from databases import Database
from dotenv import load_dotenv
import sqlalchemy
import aioredis


BASE_DIR = Path(__file__).parent.parent.parent
load_dotenv(BASE_DIR.joinpath(".env"))

db = Database(os.environ["DATABASE_URL"])
redis = aioredis.from_url("redis://redis", decode_responses=True)

metadata = sqlalchemy.MetaData()