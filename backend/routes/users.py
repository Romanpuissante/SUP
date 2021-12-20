from typing import List

from fastapi import (
    APIRouter,
    Depends
)

from fastapi_jwt_auth import AuthJWT

from orm.schema import UserInfoNoPwd
from services.users import UserService

router = APIRouter(
    prefix='/user',
    tags=['User'],
    
)


@router.get("/{id}", response_model=UserInfoNoPwd)
async def get_user(id: int, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    return await UserService.get(params={"field":'id',"searchval":id})

# @router.get("/users/", response_model=List[])
# async def get_users():
#     users = await User.all()
#     return [UserSchema(**user) for user in users]