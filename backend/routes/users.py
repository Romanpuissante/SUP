from typing import List

from fastapi import (
    APIRouter,
    Depends
)

from fastapi_jwt_auth import AuthJWT

from orm.schema import UserFull
from services.users import UserService

router = APIRouter(
    prefix='/user',
    tags=['User'],
    
)


@router.get("/{id}", response_model=UserFull)
async def get_user(id: int, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    return await UserService.get(id)

# @router.get("/users/", response_model=List[UserSchema])
# async def get_users():
#     users = await User.all()
#     return [UserSchema(**user) for user in users]