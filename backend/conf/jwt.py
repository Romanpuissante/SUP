from fastapi import (
    Security,
)

from fastapi.security.api_key import APIKeyHeader

def give_secret():

    from dotenv import load_dotenv
    import os
    from pathlib import Path

    BASE_DIR = Path(__file__).parent.parent.parent
    load_dotenv(BASE_DIR.joinpath(".env"))
    return os.environ["SECRET_KEY"]


api_key_header = APIKeyHeader(name="Authorization", auto_error=True)

class APIAuth:
    async def set(self, api_key_header: str = Security(api_key_header)):
        return api_key_header
    

