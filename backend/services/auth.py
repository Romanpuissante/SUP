# from typing import Type
from passlib.hash import bcrypt

from fastapi_jwt_auth import AuthJWT

from conf.exeptions import UnauthError, UsernameError
from conf.log import logger
from orm.models import User
from orm.schema import UserRegister, UserLogin, create_user
from .base import BaseService


class AuthService(BaseService):
    
    @classmethod
    def hash_password(cls, password: str) -> str:
        return bcrypt.hash(password)

    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.verify(plain_password, hashed_password)

    @classmethod
    def create_access(cls, Authorize: AuthJWT, user: User) -> str:
        print(user.dict(include=create_user, exclude={"password"}))
        return 'Bearer ' + Authorize.create_access_token(subject=user.username, user_claims= {"user": user.dict(include=create_user, exclude={"password"})})

    async def create(self, into_schema: UserRegister) -> dict:

        if await User.objects.filter(username=into_schema.username).exists():
            raise UsernameError()
        
        into_schema.password = self.hash_password(into_schema.password)
            
        await User.objects.create(**await self.create_fk(into_schema.dict(), ("otdel", "rank", "position")))
        return {"mess": "Пользователь успешно создан"}

    async def auth(self, user_data: UserLogin, Authorize: AuthJWT):

        user: User = await User.objects.filter(username=user_data.username).get_or_none()

        if not user or not self.verify_password(user_data.password, user.password):
            raise UnauthError()

        access_token = self.create_access(Authorize, user)
        refresh_token = Authorize.create_refresh_token(subject=user.username)

        Authorize.set_refresh_cookies(refresh_token)

        return { "access_token": access_token }