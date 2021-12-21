from typing import List

from fastapi import (
    APIRouter,
    Depends
)

from fastapi_jwt_auth import AuthJWT
from services.depends import currentuserID
from orm.schema import UserInfoNoPwd
from services.users import UserService

router = APIRouter(
    prefix='/user',
    tags=['User'],
    
)

# , operation_id="authorize"
@router.get("/{id}", response_model=UserInfoNoPwd)
async def get_user(id: int, user_id = Depends(currentuserID)):        
    return await UserService.get(params={"field":'id',"searchval":id})

# @router.get("/users/", response_model=List[])
# async def get_users():
#     users = await User.all()
#     return [UserSchema(**user) for user in users]