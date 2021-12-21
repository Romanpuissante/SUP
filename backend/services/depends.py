
from fastapi_jwt_auth import AuthJWT
from fastapi import Depends
from conf.jwt import APIAuth

async def currentuserID(Authorize: AuthJWT = Depends(), apikey = Depends(APIAuth().set)):
    """
    Требует авторизацию и возвращает текущего пользователя.
    вызов - в аргументы функции передать user_id = Depends(currentuserID)
    """
    
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    return current_user