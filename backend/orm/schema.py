from pydantic import BaseModel
from typing import Optional

# *Users 

class BaseUserAuth(BaseModel):
    username: str
    password: str
    


class UserFull(BaseUserAuth):
    first_name: Optional[str]
    last_name: Optional[str]
    middle_name: Optional[str]
    innerphone: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    superuser: Optional[bool] = False

class UserLogin(BaseUserAuth):
    pass




class UserAuthSchema(BaseModel):
    username: str
    password: str
    

class UserSchema(BaseModel):

    first_name: Optional[str]
    last_name: Optional[str]
    middle_name: Optional[str]

    class Config:
        orm_mode = True

# *Project

class ProjectSchema(BaseModel):
    name: str
    description: str
    author: int


class ProjectGet(BaseModel):
    name: str
    description: str
    author: UserSchema


