from fastapi import (
    APIRouter,
    status,
    Depends,
)
from fastapi_jwt_auth import AuthJWT

from orm.schema import UserFull, UserLogin
from services.auth import AuthService

router = APIRouter(
    prefix='/auth',
    tags=['Auth'],
)


@router.post('/register', status_code=status.HTTP_201_CREATED)
async def register(user_data: UserFull, auth_service: AuthService = Depends()):
    """ Регистрация пользователя """
    return await auth_service.register_new_user(user_data)

@router.post('/login')
async def login(user_data: UserLogin, auth_service: AuthService = Depends(), Authorize: AuthJWT = Depends()):
    """ Вход на сайт """
    return await auth_service.authenticate_user(user_data, Authorize)

@router.post('/refresh')
def refresh(Authorize: AuthJWT = Depends()):
    """ Обновление токена """
  
    Authorize.jwt_refresh_token_required()

    current_user = Authorize.get_jwt_subject()
    new_access_token = 'Bearer ' + Authorize.create_access_token(subject=current_user, fresh=True)

    return {"access_token": new_access_token}

@router.get('/logout')
async def logout(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    Authorize.unset_jwt_cookies()
    return {"msg":"Successfully logout"}