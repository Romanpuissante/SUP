# from typing import Type
from passlib.hash import bcrypt

from fastapi_jwt_auth import AuthJWT
from asyncpg.exceptions import UniqueViolationError

from conf.exeptions import UnauthError, UsernameError
from conf.log import logger
from orm.models import User, Otdel, Rank, Position, Model
from orm.schema import UserRegister



fkAuth: dict = {"otdel": Otdel, "position": Position, "rank": Rank}


class AuthService:
    
    @classmethod
    def hash_password(cls, password: str) -> str:
        return bcrypt.hash(password)

    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.verify(plain_password, hashed_password)

    @classmethod
    def create_access(cls, Authorize: AuthJWT, user: dict) -> str:
        return 'Bearer ' + Authorize.create_access_token(subject=user.username, user_claims= {"user": {k:v for k,v in user.dict().items() if k != 'password'}})

    async def create(self, into_schema: UserRegister) -> User:

        if await User.objects.filter(username=into_schema.username).exists():
            return UsernameError()
        
        into_schema.password = self.hash_password(into_schema.password)
            
        return await User.objects.create(**(await self.create_fk(into_schema, fkAuth)).dict())
      

    

    async def create_fk(self, into_schema, dict_fk: dict) -> dict:
        """
        Создает форины

        Args:
            into_schema ([type]): Ожидаемая схема для создания
            dict_fk (dict): Словарь по типу {колонка:таблица}

        Returns:
            [dict]: Словарь для создания объекта
        """
        
        for key, model in dict_fk.items():
            res = await model.objects.get_or_create(**(getattr(into_schema,key).dict()))
            setattr(into_schema, key, res)

        return into_schema


# class AuthService(BaseServices[UserRegister, UserFull, User]):



#     async def auth_user(self, user_data: UserLogin, Authorize: AuthJWT): 

#         user: UserAuth = await self.get_with_filter({"username": user_data.username}, UserAuth)

#         if not user:
#             raise unauthError

#         if not self.verify_password(user_data.password, user.password):
#             raise unauthError

#         access_token = self.create_access(Authorize, user)
#         refresh_token = Authorize.create_refresh_token(subject=user.username)
  
#         Authorize.set_refresh_cookies(refresh_token)

#         return { "access_token": access_token }