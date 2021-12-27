from typing import Type

from passlib.hash import bcrypt
from fastapi_jwt_auth import AuthJWT

from orm.models import User
from orm.schema import UserRegister, UserFull, UserLogin, UserSimple, UserAuth
from .base import BaseServices
from services.dicts import OtdelService, PositionService, RankService
from conf.exeptions import unauthError, usernameError


class tableFK(object):
    def __init__(self, db):
        self.fk = {
            "otdel": OtdelService(db),
            "position": PositionService(db),
            "rank": RankService(db)
        }

class AuthService(BaseServices[UserRegister, UserFull, User]):

    @property
    def _in_schema(self) -> Type[UserFull]:
        return UserRegister

    @property
    def _schema(self) -> Type[UserFull]:
        return UserFull

    @property
    def _table(self) -> Type[User]:
        return User

    @property
    def _tableFK(self) -> tableFK:
        return tableFK(self._db_session)

    @classmethod
    def hash_password(cls, password: str) -> str:
        return bcrypt.hash(password)

    @classmethod
    def create_access(cls, Authorize: AuthJWT, user: dict) -> str:
        return 'Bearer ' + Authorize.create_access_token(subject=user.username, user_claims= {"user": {k:v for k,v in user.dict().items() if k != 'password'}})

    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.verify(plain_password, hashed_password)

    async def create(self, in_schema: UserRegister) -> UserFull:
        
        in_schema.password = self.hash_password(in_schema.password)
        user: UserSimple = await self.get_with_filter({"username": in_schema.username}, UserSimple)
        if user:
            raise usernameError

        in_schema = await self.check_foreign_key(in_schema)
        entry = self._table(**in_schema)
        self._db_session.add(entry)
        
        await self._db_session.commit()
      
        return self._schema.from_orm(entry)


    async def auth_user(self, user_data: UserLogin, Authorize: AuthJWT): 

        user: UserAuth = await self.get_with_filter({"username": user_data.username}, UserAuth)

        if not user:
            raise unauthError

        if not self.verify_password(user_data.password, user.password):
            raise unauthError

        access_token = self.create_access(Authorize, user)
        refresh_token = Authorize.create_refresh_token(subject=user.username)
  
        Authorize.set_refresh_cookies(refresh_token)

        return { "access_token": access_token }