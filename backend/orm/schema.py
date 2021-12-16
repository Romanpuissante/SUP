from pydantic import BaseModel


# *Users 

class UserAuthSchema(BaseModel):
    username: str
    password: str
    

class UserSchema(BaseModel):

    first_name: str = ""
    last_name: str = ""
    middle_name: str = ""

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


