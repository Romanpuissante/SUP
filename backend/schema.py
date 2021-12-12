from pydantic import BaseModel


class User(BaseModel):
    first_name: str
    last_name: str
    middle_name: str

    class Config:
        orm_mode = True
