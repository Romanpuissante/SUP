from fastapi import (
    APIRouter,
    status,
    Depends,   
)

from fastapi_jwt_auth import AuthJWT
from services.depends import AD
from orm.schema import UserFull, UserRegister, UserLogin
from services.auth import AuthService

router = APIRouter()

AS = AD(AuthService)

# *Auth

@router.post('/auth/register', status_code=status.HTTP_201_CREATED, response_model=UserFull, tags=['Авторизация'])
async def register(user_data: UserRegister, auth_service: AuthService = Depends(AS.serv)):
    """ Регистрация пользователя """
 
    return await auth_service.create(user_data)

@router.post('/auth/login', tags=['Авторизация'])
async def login(user_data: UserLogin, auth_service: AuthService = Depends(AS.serv), Authorize: AuthJWT = Depends()):
    """ Вход на сайт """

    return await auth_service.auth_user(user_data, Authorize)

@router.post('/auth/refresh', tags=['Авторизация'])
async def refresh(Authorize: AuthJWT = Depends(), auth_service: AuthService = Depends(AS.serv)):
    """ Обновление токена """

    Authorize.jwt_refresh_token_required()
    current_user = Authorize.get_jwt_subject()

    user= await auth_service.get_with_filter({"username": current_user})

    new_access_token = AuthService.create_access(Authorize, user)
    return {"access_token": new_access_token}

@router.get('/auth/logout', tags=['Авторизация'])
async def logout(Authorize: AuthJWT = Depends()):

    Authorize.jwt_required()
    
    Authorize.unset_jwt_cookies()
    return {"msg":"Successfully logout"}

# *User

@router.get("/user/{id_user}", response_model=UserFull, tags=['Пользователь'])
async def get_user(id_user: int, auth_service: AuthService = Depends(AS.serv), username:str = Depends(AS.protect)):
    user = await auth_service.get(id_user)
    return UserFull(**user.dict())

@router.get("/users", response_model=list[UserFull], tags=['Пользователь'])
async def get_users(auth_service: AuthService = Depends(AS.serv), username:str = Depends(AS.protect)):

    users = await auth_service.all()
    return users

@router.put("/user/update/{id_user}", tags=['Пользователь'])
async def update_user(id_user: int, in_schema: UserFull ,auth_service: AuthService = Depends(AS.serv), username:str = Depends(AS.protect)):
    return await auth_service.update(id_user, in_schema)

# @router.patch("")

@router.delete("/user/del/{id_user}", tags=['Пользователь'])
async def del_user(id_user: int, auth_service: AuthService = Depends(AS.serv), username:str = Depends(AS.protect)):
    return await auth_service.delete(id_user)

@router.delete("user/del", tags=['Пользователь'])
async def del_all_user(auth_service: AuthService = Depends(AS.serv), username:str = Depends(AS.protect)):
    return await auth_service.delete_all()