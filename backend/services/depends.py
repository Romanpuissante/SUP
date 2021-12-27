
from fastapi_jwt_auth import AuthJWT
from fastapi import Depends
from conf.jwt import APIAuth
from orm.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession

class AD():

    def __init__(self, service=None) -> None:
        self.service = service

    async def serv(self, db: AsyncSession = Depends(get_db)):
        return self.service(db)

    async def protect(self, Authorize: AuthJWT = Depends(), apikey = Depends(APIAuth().set)):
        """
            Требует авторизацию и возвращает текущего пользователя.
            вызов - в аргументы функции передать user_id = Depends(cls.protect)
        """

        Authorize.jwt_required()
        current_user = Authorize.get_jwt_subject()

        return current_user

