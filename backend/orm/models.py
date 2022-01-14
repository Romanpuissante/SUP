from ormar import Integer, String, Boolean, ForeignKey, Model, ModelMeta
from conf.sessions import database, metadata
from typing import Optional

# *-------------------- Base --------------------* #

class BaseId():
    id: int = Integer(primary_key=True)

class BaseMeta(ModelMeta):
    metadata = metadata
    database = database

# *-------------------- Foreign Key Users --------------------* #

class Otdel(Model, BaseId):
    name: str = String(max_length=100, unique=True)
    class Meta(BaseMeta):
        ...

class Position(Model, BaseId):
    name: str = String(max_length=100, unique=True)
    class Meta(BaseMeta):
        ...

class Rank(Model, BaseId):
    name: str = String(max_length=100, unique=True)
    class Meta(BaseMeta):
        ...

# *-------------------- User --------------------* #

class User(Model, BaseId):
 
    username: str = String(max_length=100, unique=True)
    password: str = String(max_length=200)

    first_name: str = String(max_length=100)
    last_name: str = String(max_length=100)
    middle_name: str = String(max_length=100, nullable=True)

    innerphone: str = String(max_length=50, nullable=True)
    phone: str = String(max_length=50, nullable=True)
    email: str = String(max_length=150, nullable=True)

    otdel: Otdel = ForeignKey(Otdel)
    position: Position = ForeignKey(Position)
    rank: Rank = ForeignKey(Rank)

    superuser: bool = Boolean(default=False)

    class Meta(BaseMeta):
        ...

    


# # *Many-to-many Users

# # ----- Hard Skill

# class AssocHardUser(Base): 
#     user_id = Column(ForeignKey("user.id"), primary_key=True)
#     hardskill_id = Column(ForeignKey('hardskill.id'), primary_key=True)
#     level = Column(Integer)
#     user = relationship("User", back_populates="hardskills")
#     hardskill = relationship("HardSkill", back_populates="users")

# class GroupHardSkill(Base):

#     name = Column(String(200), unique=True)
#     hardskills = relationship("HardSkill", back_populates="group")

# class HardSkill(Base):

#     name = Column(String(200), unique=True)
#     group_id = Column(Integer, ForeignKey('grouphardskill.id'))
#     group = relationship("GroupHardSkill", back_populates="hardskills")

#     users = relationship("AssocHardUser", back_populates="hardskill")

# # ----- Soft Skill

# class AssocSoftUser(Base): 
#     user_id = Column(ForeignKey("user.id"), primary_key=True)
#     softskill_id = Column(ForeignKey('softskill.id'), primary_key=True)
#     level = Column(Integer)
#     user = relationship("User", back_populates="softskills")
#     softskill = relationship("SoftSkill", back_populates="users")

# class GroupSoftSkill(Base):

#     name = Column(String(200), unique=True)
#     softskills = relationship("SoftSkill", back_populates="group")

# class SoftSkill(Base):

#     name = Column(String(200), unique=True)

#     group_id = Column(Integer, ForeignKey('groupsoftskill.id'))

#     group = relationship("GroupSoftSkill", back_populates="softskills")
#     users = relationship("AssocSoftUser", back_populates="softskill")

# # *User

# class User(Base):

#     username = Column(String(100), unique=True)
#     password = Column(String)

#     first_name = Column(String(100))
#     last_name = Column(String(100))
#     middle_name = Column(String(100), nullable=True)

#     innerphone = Column(String(50), nullable=True)
#     phone = Column(String(50), nullable=True)
#     email = Column(String(150), nullable=True)

#     otdel_id = Column(Integer, ForeignKey('otdel.id'))
#     otdel = relationship("Otdel", back_populates="users")

#     position_id = Column(Integer, ForeignKey('position.id'))
#     position = relationship("Position", back_populates="users")

#     rank_id = Column(Integer, ForeignKey('rank.id'))
#     rank = relationship("Rank", back_populates="users")

#     superuser = Column(Boolean, default=False)

#     hardskills = relationship("AssocHardUser", back_populates="user")
#     softskills = relationship("AssocSoftUser", back_populates="user")
#     userprojectlink = relationship("AssocProjects", back_populates="user")


# # PROJECTS

# #PROJEСTS FROREIGNS
# class Projectstatus(Base):
#     name = Column(String(200), unique=True)


# class Projects(Base):
#     name = Column(String(200))
#     description = Column(String(500), nullable=True)
#     status_id = Column(Integer, ForeignKey('projectstatus.id'))
#     customer = Column(String(500), nullable=True)
#     author = Column(ForeignKey("user.id"))
#     leader = Column(ForeignKey("user.id"))
#     datestart = Column(Date, nullable=True)
#     dateend = Column(Date,nullable=True)
#     lastchanged = Column(Date, nullable=True)

#     projectlink = relationship("AssocProjects", back_populates="projects")



# class AssocProjects(Base):
#     __table_args__ = (
#         UniqueConstraint('user_id', 'project_id', name='unique_projectUser'),
#     )
#     user_id = Column(Integer,ForeignKey("user.id"), primary_key=True)
#     project_id = Column(Integer,ForeignKey("projects.id"), primary_key=True)
#     involved = Column(Boolean, default=False)

#     user = relationship("User", back_populates="userprojectlink")
#     projects = relationship("Projects", back_populates="projectlink")
    

# # TASKS
# # TASKS FOREIGNS
# # Надо посмотреть, может быть статусы и объединить в одну таблицу? Толку плодить-то?

# class Taskstatus(Base):
#     name = Column(String(200), unique=True)

# class Taskstage(Base):
#     name = Column(String(200), unique=True)
# # TASKS BASE

# class Task(Base):
#     parent_project = Column(ForeignKey("projects.id"))
#     name = Column(String(200))
#     status_id = Column(Integer, ForeignKey('taskstatus.id'))
#     description = Column(String(500), nullable=True)
#     datestart = Column(Date, nullable=True)
#     dateend = Column(Date, nullable=True)
#     responsible_id = Column(ForeignKey("user.id"))
#     stage = Column(ForeignKey("taskstage.id"))

# # Taskchecklist

# class TaskChecklist(Base):
#     parent_task = Column(ForeignKey("task.id"))
#     name = Column(String(200))
#     user_id = Column(ForeignKey("user.id"))
#     # status = 
#     datetimestart = Column(DateTime, nullable=True)
#     datetimeend = Column(DateTime)
#     timeneeded = Column(BIGINT)

# # TaskCheckListChat

# class Taskchecklistchat(Base):
#     message = Column(String(500))
#     sender = Column(ForeignKey("user.id"))
#     datetime = Column(DateTime)
#     parent_taskchecklist_id = Column(ForeignKey("taskchecklist.id"))


# # Files

# class Fileschecklist(Base):
#     parent_taskchecklist_id = Column(ForeignKey("taskchecklist.id"))
#     sender = Column(ForeignKey("user.id"))
#     datetime = Column(DateTime)
#     file_path = Column(String(500))

# # PROJECTHISTORY
# class Hislevel(Base):
#     name = Column(String(200), unique=True)

# class ProjectHistory(Base):
#     text = Column(String(200))
#     level = Column(ForeignKey("hislevel.id"))
#     parent_project= Column(ForeignKey("projects.id"))
#     ids =  Column(Integer)


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

