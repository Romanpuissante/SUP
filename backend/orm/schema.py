from pydantic import BaseModel
from typing import Optional

# *Positions

class BasePositions(BaseModel):
    id:Optional[int]
    name: str
#  *Ranks

class BaseRanks(BaseModel):
    id:Optional[int]
    name: str

# *Otdels

class BaseOtdel(BaseModel):
    id:Optional[int]
    name: str


# *Users 
class BaseUserAuth(BaseModel):
    username: str
    password: str
    

class UserInfoNoPwd(BaseModel):    
    username: str
    first_name: Optional[str]
    last_name: Optional[str]
    middle_name: Optional[str]
    innerphone: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    otdel: Optional[str]
    position: Optional[str]
    rank: Optional[str]
    superuser: Optional[bool] = False

class UserFull(BaseUserAuth, UserInfoNoPwd):
    pass

class UserLogin(BaseUserAuth):
    pass

    class Config:
        orm_mode = True


# *Project

# class ProjectSchema(BaseModel):
#     name: str
#     description: str
#     author: int


# class ProjectGet(BaseModel):
#     name: str
#     description: str
#     author: UserSchema


