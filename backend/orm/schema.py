from pydantic import BaseModel
from typing import Optional


# *Users 

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


