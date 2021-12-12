import os
from pathlib import Path
from databases import Database
from dotenv import load_dotenv
import sqlalchemy


BASE_DIR = Path(__file__).parent.parent
load_dotenv(BASE_DIR.joinpath(".env"))

db = Database(os.environ["DATABASE_URL"])

metadata = sqlalchemy.MetaData()