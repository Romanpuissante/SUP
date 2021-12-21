from passlib.hash import bcrypt

from fastapi import (
    HTTPException,
    status,
)

from fastapi_jwt_auth import AuthJWT

from orm.models import user
from orm.schema import UserFull, UserLogin
from conf.db import db


class AuthService:
    
    @classmethod
    def hash_password(cls, password: str) -> str:
        return bcrypt.hash(password)

    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.verify(plain_password, hashed_password)

    async def register_new_user(self, user_data: UserFull):
        user_data.password = self.hash_password(user_data.password)
        query = user.insert().values(**user_data.dict())
        id_db = await db.execute(query)
        return { "id": id_db}

    async def authenticate_user(self, user_data: UserLogin, Authorize: AuthJWT):

        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Некоректные имя пользователя или пароль',
            headers={'WWW-Authenticate': 'Bearer'},
        )
        
        query = user.select().where(user.c.username == user_data.username)
        user_db = await db.fetch_one(query)

        if not user_db:
            raise exception

        user_db = dict(user_db)

        if not self.verify_password(user_data.password, user_db["password"]):
            raise exception

        access_token = 'Bearer ' + Authorize.create_access_token(subject=user_db["username"])
        refresh_token = Authorize.create_refresh_token(subject=user_db["username"])
  
        Authorize.set_refresh_cookies(refresh_token)

        return { "access_token": access_token, "user": {k:v for k,v in user_db.items() if k != 'password'} }