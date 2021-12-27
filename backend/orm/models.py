from sqlalchemy import Column, String, ForeignKey, Integer, Boolean
from sqlalchemy.orm import relationship
from .base import Base

# *Foreign Key Users
class Otdel(Base):
    name = Column(String(100), unique=True)
    users = relationship("User", back_populates="otdel")

class Position(Base):
    name = Column(String(100), unique=True)
    users = relationship("User", back_populates="position")

class Rank(Base):
    name = Column(String(100), unique=True)
    users = relationship("User", back_populates="rank")

# *Many-to-many Users

# ----- Hard Skill

class AssocHardUser(Base): 
    user_id = Column(ForeignKey("user.id"), primary_key=True)
    hardskill_id = Column(ForeignKey('hardskill.id'), primary_key=True)
    level = Column(Integer)

    user = relationship("User", back_populates="hardskills")
    hardskill = relationship("HardSkill", back_populates="users")

class GroupHardSkill(Base):

    name = Column(String(200), unique=True)
    hardskills = relationship("HardSkill", back_populates="group")

class HardSkill(Base):

    name = Column(String(200), unique=True)

    group_id = Column(Integer, ForeignKey('grouphardskill.id'))
    group = relationship("GroupHardSkill", back_populates="hardskills")

    users = relationship("AssocHardUser", back_populates="hardskill")

# ----- Soft Skill

class AssocSoftUser(Base): 
    user_id = Column(ForeignKey("user.id"), primary_key=True)
    softskill_id = Column(ForeignKey('softskill.id'), primary_key=True)
    level = Column(Integer)

    user = relationship("User", back_populates="softskills")
    softskill = relationship("SoftSkill", back_populates="users")

class GroupSoftSkill(Base):

    name = Column(String(200), unique=True)
    softskills = relationship("SoftSkill", back_populates="group")

class SoftSkill(Base):

    name = Column(String(200), unique=True)

    group_id = Column(Integer, ForeignKey('groupsoftskill.id'))
    group = relationship("GroupSoftSkill", back_populates="softskills")

    users = relationship("AssocSoftUser", back_populates="softskill")

# *User

class User(Base):

    username = Column(String(100), unique=True)
    password = Column(String)

    first_name = Column(String(100))
    last_name = Column(String(100))
    middle_name = Column(String(100), nullable=True)

    innerphone = Column(String(50), nullable=True)
    phone = Column(String(50), nullable=True)
    email = Column(String(150), nullable=True)

    otdel_id = Column(Integer, ForeignKey('otdel.id'))
    otdel = relationship("Otdel", back_populates="users")

    position_id = Column(Integer, ForeignKey('position.id'))
    position = relationship("Position", back_populates="users")

    rank_id = Column(Integer, ForeignKey('rank.id'))
    rank = relationship("Rank", back_populates="users")

    superuser = Column(Boolean, default=False)

    hardskills = relationship("AssocHardUser", back_populates="user")
    softskills = relationship("AssocSoftUser", back_populates="user")

# *Statuses PROJECT
# projectstatuses = create_table("projectstatuses",(
#     Column("name", String(100), unique=True),    
# ) )



# *User

# user = create_table("user", (
#     Column("hardskills", ARRAY(Integer)),
#     Column("softskills", ARRAY(Integer)),
# ))

# project = create_table("projects",(
#     Column("name", String(255)),
#     Column("description", Text),
#     Column("status", Integer, ForeignKey("projectstatuses.id"), nullable=False),
#     Column("customer", String(100)),
#     Column("author", Integer, ForeignKey("user.id"), nullable=False),
#     Column("leader", Integer, ForeignKey("user.id"), nullable=False),
#     Column("datestart", Date, nullable=True),
#     Column("dateend", Date, nullable=True),
#     Column("lastchanged", Date, nullable=True),
    

# ))

