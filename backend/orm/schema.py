from datetime import date
from pydantic import BaseModel
from typing import Optional
#  *ProjectStatuses
class BaseProjectstatuses(BaseModel):
    id: int
    name: str

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

class BaseProject(BaseModel):
    id: int
    name: str    
    status: int
    dateend: date
    lastchanged:date
    tasksCompleted: Optional[int]=None
    tasksAll: Optional[int]=None


# class ProjectGet(BaseModel):
#     name: str
#     description: str
#     author: UserSchema


