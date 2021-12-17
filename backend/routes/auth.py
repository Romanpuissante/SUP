from fastapi import (
    APIRouter,
    status,
    Depends,
)
from fastapi_jwt_auth import AuthJWT


from orm.schema import UserAuthSchema
from services.auth import AuthService

router = APIRouter(
    prefix='/auth',
    tags=['Auth'],
)


@router.post('/register/', status_code=status.HTTP_201_CREATED)
async def register(user_data: UserAuthSchema, auth_service: AuthService = Depends()):
    """ Регистрация пользователя """
    return await auth_service.register_new_user(user_data)

@router.post('/login/')
async def login(user_data: UserAuthSchema, auth_service: AuthService = Depends(), Authorize: AuthJWT = Depends()):
    return await auth_service.authenticate_user(user_data, Authorize)

@router.post('/refresh')
def refresh(Authorize: AuthJWT = Depends()):
  
    Authorize.jwt_refresh_token_required()

    current_user = Authorize.get_jwt_subject()
    new_access_token = Authorize.create_access_token(subject=current_user)
    Authorize.set_access_cookies(new_access_token)

    return {"access_token": new_access_token}
