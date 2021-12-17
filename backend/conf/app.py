from pydantic import BaseModel

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException

from .db import db, redis
from .jwt import give_secret

app = FastAPI()


# !JWT section
class Settings(BaseModel):
    authjwt_secret_key: str = give_secret()
    authjwt_token_location: set = {"cookies"}
    authjwt_cookie_csrf_protect: bool = False

@AuthJWT.load_config
def get_config():
    return Settings()

@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )

# !Event app
@app.on_event("startup")
async def startup():
    await db.connect()
    

@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()
    await redis.close()