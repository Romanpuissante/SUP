from pydantic import BaseModel

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException

from .jwt import give_secret



app = FastAPI(title="Async SUP", version="alfa 1.0.0", description="Схема")


# !JWT section
class Settings(BaseModel):
    authjwt_secret_key: str = give_secret()
    authjwt_token_location: set = {'headers', 'cookies'}
    authjwt_cookie_csrf_protect: bool = False
    authjwt_cookie_secure: bool = False
    authjwt_cookie_samesite: str = 'lax'

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
# @app.on_event("startup")
# async def startup():

    

# @app.on_event("shutdown")
# async def shutdown():
