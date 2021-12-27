from pydantic import BaseModel
from typing import Optional


# *Base

class BaseSchema(BaseModel):
    class Config(BaseModel.Config):
        orm_mode = True

class BaseOnlyId(BaseSchema):
    id: int

class BaseDict(BaseSchema):
    name: str

class BaseDictFull(BaseDict):
    id: int


# *ForeignKey Table For User

class OtdelSimple(BaseDict):
    ...

class OtdelFull(BaseDictFull):
    ...

class PositionSimple(BaseDict):
    ...

class PositionFull(BaseDictFull):
    ...

class RankSimple(BaseDict):
    ...

class RankFull(BaseDictFull):
    ...
# *Users and Auth

class UserSimple(BaseSchema):
    username: str

class UserLogin(UserSimple):
    password: str

class UserFields(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    middle_name: Optional[str]
    innerphone: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    superuser: Optional[bool] = False

class UserAllFields(UserFields):
    otdel_id: Optional[int]
    position_id: Optional[int]
    rank_id: Optional[int]

class UserRegister(UserLogin, UserFields):
    otdel: Optional[OtdelSimple]
    position: Optional[PositionSimple]
    rank: Optional[RankSimple]

class UserAuth(UserLogin, UserAllFields):
    id: int

class UserFull(UserSimple, UserAllFields):
    id: int




# #  *ProjectStatuses
# class BaseProjectstatuses(BaseModel):
#     id: int
#     name: str

# # *Positions

# class BasePositions(BaseModel):
#     id:Optional[int]
#     name: str
# #  *Ranks

# class BaseRanks(BaseModel):
#     id:Optional[int]
#     name: str

# # *Otdels

# class BaseOtdel(BaseModel):
#     id:Optional[int]
#     name: str



    

# class UserInfoNoPwd(BaseModel):    
#     username: str
#     first_name: Optional[str]
#     last_name: Optional[str]
#     middle_name: Optional[str]
#     innerphone: Optional[str]
#     phone: Optional[str]
#     email: Optional[str]
#     # otdel: Optional[str]
#     # position: Optional[str]
#     # rank: Optional[str]
#     superuser: Optional[bool] = False




    



# # *Project

# class BaseProject(BaseModel):
#     id: int
#     name: str    
#     status: int
#     dateend: date
#     lastchanged:date
#     tasksCompleted: Optional[int]=None
#     tasksAll: Optional[int]=None


# class ProjectGet(BaseModel):
#     name: str
#     description: str
#     author: UserSchema


