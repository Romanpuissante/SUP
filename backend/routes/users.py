from typing import List

from fastapi import (
    APIRouter,
)

from orm.schema import UserSchema
from services.users import UserService, UserAuthSchema

router = APIRouter(
    prefix='',
    tags=['User'],
)


@router.post("/user/")
async def create_user(user: UserSchema):
    return await UserService.create(**user.dict())


@router.get("/user/{id}", response_model=UserSchema)
async def get_user(id: int):
    return await UserService.get(id)

# @router.get("/users/", response_model=List[UserSchema])
# async def get_users():
#     users = await User.all()
#     return [UserSchema(**user) for user in users]