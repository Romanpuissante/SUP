from fastapi import (
    APIRouter,
    status,
    Depends,   
)

from fastapi_jwt_auth import AuthJWT
from orm.schema import UserRegister, UserLogin, User
from services.depends import AD
from services.auth import AuthService

router = APIRouter()

# *Auth

@router.post("/auth/register", status_code=status.HTTP_201_CREATED, tags=['Авторизация'])
async def get_my_projects(user_data: UserRegister, auth_service: AuthService = Depends(AuthService)):
    """ Регистрация пользователя """

    return await auth_service.create(user_data)

@router.post('/auth/login', tags=['Авторизация'])
async def login(user_data: UserLogin, auth_service: AuthService =  Depends(AuthService), Authorize: AuthJWT = Depends()):
    """ Вход на сайт """

    return await auth_service.auth(user_data, Authorize)


@router.post('/auth/refresh', tags=['Авторизация'])
async def refresh(Authorize: AuthJWT = Depends()):
    """ Обновление токена """

    Authorize.jwt_refresh_token_required()
    current_user = Authorize.get_jwt_subject()

    user= await User.objects.select_related(["otdel", "rank"]).filter(username=current_user).get()
    new_access_token = AuthService.create_access(Authorize, user)

    return {"access_token": new_access_token}

@router.get('/auth/logout', tags=['Авторизация'])
async def logout(Authorize: AuthJWT = Depends()):

    Authorize.jwt_required()
    Authorize.unset_jwt_cookies()
    return {"msg":"Successfully logout"}

# # *User

@router.get("/user/{id_user}", tags=['Пользователь'])
async def get_user(id_user: int, username:str = Depends(AD.protect)):
    user = await User.objects.get(id=id_user)
    return user.dict(exclude={"password", })

@router.get("/users", tags=['Пользователь'])
async def get_users( username:str = Depends(AD.protect)):
    users = await User.objects.all()
    return [user.dict(exclude={"password", }) for user in users]

@router.delete("/user/del/{id_user}", tags=['Пользователь'])
async def del_user(id_user: int, username:str = Depends(AD.protect)):
    return await User.objects.delete(id=id_user)