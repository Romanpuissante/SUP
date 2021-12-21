from typing import List

from fastapi import (
    APIRouter,
    Depends,
)

from fastapi_jwt_auth import AuthJWT
from conf.jwt import APIAuth

from orm.schema import UserFull
# from services.depends import currentuserID
# from orm.schema import UserInfoNoPwd
from services.users import UserService

router = APIRouter(
    prefix='/user',
    tags=['User'],
    
)

# , operation_id="authorize"
# @router.get("/{id}", response_model=UserInfoNoPwd)
# async def get_user(id: int, user_id = Depends(currentuserID)):        
#     return await UserService.get(params={"field":'id',"searchval":id})

@router.get("/user/{id}", response_model=UserFull)
async def get_user(id: int, Authorize: AuthJWT = Depends(), apikey = Depends(APIAuth().set)):
  
    Authorize.jwt_required()
    return await UserService.get(id)

# @router.get("/users/", response_model=List[UserSchema])
# @router.get("/users/", response_model=List[])
# async def get_users():
#     users = await User.all()
#     return [UserSchema(**user) for user in users]