from passlib.hash import bcrypt

from fastapi import (
    HTTPException,
    status,
    Depends
)

from fastapi_jwt_auth import AuthJWT
from .otdels import OtdelService
from .positions import PositionsService
from .ranks import RanksService
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

    async def register_new_user(self,
                user_data: UserFull):

        user_data.password = self.hash_password(user_data.password)

        dicter = {"otdel": OtdelService,
                  "position":PositionsService,
                  "rank":RanksService
        }
        user_data=user_data.dict()
        newdict={}
        for key,val in dicter.items():
            newdict[key]= await val.checkForeign(user_data[key].lower().title())        
        user_data = user_data | newdict
        
        query = user.insert().values(**user_data)
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

        access_token = Authorize.create_access_token(subject=user_db["username"])
        refresh_token = Authorize.create_refresh_token(subject=user_db["username"])
        
        Authorize.set_access_cookies(access_token)
        Authorize.set_refresh_cookies(refresh_token)

        return {"access_token": access_token, "refresh_token": refresh_token}

        
        # query = cls.model.select().where(cls.model.c.id == id)
        # result = await db.fetch_one(query)
        # return cls.schema(**result).dict()
