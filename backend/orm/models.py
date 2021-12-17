from sqlalchemy import Column, String, ForeignKey, Integer, Boolean, Text
from .base import create_table

# *User

user = create_table("user", (
    Column("username", String(100)),
    Column("password", String),
    Column("first_name", String(100)),
    Column("last_name", String(100)),
    Column("middle_name", String(100), nullable=True),
    Column("innerphone", String(50), nullable=True),
    Column("phone", String(50), nullable=True),
    Column("email", String(150), nullable=True),
    Column("superuser", Boolean, default=False),
))

