from sqlalchemy import Column, String, ForeignKey, Integer, Boolean, Text, ARRAY, Date
from .base import create_table
# *Statuses PROJECT
projectstatuses = create_table("projectstatuses",(
    Column("name", String(100), unique=True),    
) )

# *Positions USER
positions = create_table("positions",(
    Column("name", String(100), unique=True),    
) )

#  *Ranks USER
ranks = create_table("ranks",(
    Column("name", String(100), unique=True),    
) )
# *Otdels USER

otdels = create_table("otdels",(
    Column("name", String(100), unique=True),    
) )

# *User

user = create_table("user", (
    Column("username", String(100), unique=True),
    Column("password", String),
    Column("first_name", String(100)),
    Column("last_name", String(100)),
    Column("middle_name", String(100), nullable=True),
    Column("innerphone", String(50), nullable=True),
    Column("phone", String(50), nullable=True),
    Column("email", String(150), nullable=True),
    Column("superuser", Boolean, default=False),
    Column('otdel', Integer, ForeignKey("otdels.id"), nullable=True),
    Column('position', Integer, ForeignKey("positions.id"), nullable=True),
    Column('rank', Integer, ForeignKey("ranks.id"), nullable=True),
    Column("hardskills", ARRAY(Integer)),
    Column("softskills", ARRAY(Integer)),
))

project = create_table("projects",(
    Column("name", String(255)),
    Column("description", Text),
    Column("status", Integer, ForeignKey("projectstatuses.id"), nullable=False),
    Column("customer", String(100)),
    Column("author", Integer, ForeignKey("user.id"), nullable=False),
    Column("leader", Integer, ForeignKey("user.id"), nullable=False),
    Column("datestart", Date, nullable=True),
    Column("dateend", Date, nullable=True),
    Column("lastchanged", Date, nullable=True),
    

))

