from sqlalchemy import Column, String, ForeignKey, Integer, Boolean, Text
from .base import create_table

# *User

user = create_table("user", (
    Column("username", String(100)),
    Column("password", String),
    Column("first_name", String(100), nullable=True),
    Column("last_name", String(100), nullable=True),
    Column("middle_name", String(100), nullable=True),
    
))



# class Project(BaseModel):
#     fields = (
#         Column("name", String(150)),
#         Column("description", Text()),
#         Column("author", ForeignKey("user.id", ondelete="CASCADE", onupdate="CASCADE")),
#     )