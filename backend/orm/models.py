from typing import Optional
from datetime import date, datetime

from ormar import Integer, String, Boolean, ForeignKey, Model, ModelMeta, ManyToMany, Date, Text, DateTime
from conf.sessions import database, metadata


# *-------------------- Base --------------------* #

class BaseId():
    """
        Базовый класс, добавляющий в дочерние Первичный ключ ID    
    """
    id: int = Integer(primary_key=True)

class BaseMeta(ModelMeta):
    """
        Обязательно к добавлению во все таблицы
        class Meta(BaseMeta):
        ...
    """
    metadata = metadata
    database = database

# !-------------------- User --------------------! #
# *-------------------- Foreign Key --------------------* #

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

class LeaveType(Model, BaseId):
    class Meta(BaseMeta):
        ...
    name: str = String(max_length=500,unique=True)

class GroupHardSkill(Model, BaseId):
    class Meta(BaseMeta):
        ...
    name: str = String(max_length=500,unique=True)
    

class HardSkill(Model, BaseId):
    class Meta(BaseMeta):
        ...
    name: str = String(max_length=200,unique=True)
    group: GroupHardSkill = ForeignKey(GroupHardSkill)
    

class UserHardSkills(Model, BaseId):
    class Meta(BaseMeta):
        ...
    level: Optional[int] = Integer()



class GroupSoftSkill(Model, BaseId):
    class Meta(BaseMeta):
        ...
    name: str = String(max_length=500,unique=True)
    

class SoftSkill(Model, BaseId):
    class Meta(BaseMeta):
        ...
    name: str = String(max_length=200,unique=True)
    group: GroupSoftSkill = ForeignKey(GroupSoftSkill)
    

class UserSoftSkills(Model, BaseId):
    class Meta(BaseMeta):
        ...
    level: Optional[int] = Integer()

# *-------------------- Base --------------------* #

class User(Model, BaseId):
 
    username: str = String(max_length=100, unique=True)
    password: str = String(max_length=200)

    first_name: str = String(max_length=100)
    last_name: str = String(max_length=100)
    middle_name: Optional[str] = String(max_length=100, nullable=True)

    innerphone: Optional[str] = String(max_length=50, nullable=True)
    phone: Optional[str] = String(max_length=50, nullable=True)
    email: Optional[str] = String(max_length=150, nullable=True)

    otdel: Otdel = ForeignKey(Otdel)
    position: Position = ForeignKey(Position)
    rank: Rank = ForeignKey(Rank)

    hardskills: Optional[list[UserHardSkills]] = ManyToMany(HardSkill,through=UserHardSkills)
    softskills: Optional[list[UserSoftSkills]] = ManyToMany(SoftSkill,through=UserSoftSkills)

    superuser: bool = Boolean(default=False)

    class Meta(BaseMeta):
        ...

class Leave(Model, BaseId):
    """
    Отпуска, больничные итп
    """
    class Meta(BaseMeta):
        ...
    user: User = ForeignKey(User)
    datestart: date = Date()
    dateend: date = Date()
    leavetype: LeaveType = ForeignKey(LeaveType)  

# !-------------------- Project --------------------! # 
# *-------------------- Foreign Key --------------------* #    

class Doctype(Model, BaseId):
    class Meta(BaseMeta):
        ...
    name:str = String(max_length=100,unique=True)
    

class ProjectStatus(Model, BaseId):
    class Meta(BaseMeta):
        ...
    name:str = String(max_length=100,unique=True)


class ProjectUsers(Model, BaseId):
    class Meta(BaseMeta):
        ...
    involved:Optional[Boolean] = Boolean(default=False)

# *-------------------- Base --------------------* #

class Project(Model, BaseId):

    class Meta(BaseMeta):
        ...

    name: str = String(max_length=500)
    description: Optional[str] = Text()
    status: Optional[ProjectStatus] = ForeignKey(ProjectStatus)
    customer: Optional[str] = String(max_length=250, nullable=True)
    author: User = ForeignKey(User, related_name = "author_user")
    leader: User = ForeignKey(User, related_name = "leader_user")
    users: Optional[list[ProjectUsers]]= ManyToMany(User, through= ProjectUsers)
    datestart: Optional[date] = Date()
    dateend: Optional[date] = Date()
    lastchanged: Optional[date] = Date()

# *-------------------- Documentation --------------------* #

class Documentation(Model, BaseId):

    class Meta(BaseMeta):
        ...
    pproject: Project = ForeignKey(Project) 
    doctype: Doctype =  ForeignKey(Doctype)
    created: datetime = DateTime()
    accepted: Optional[datetime]= DateTime()

# *-------------------- History --------------------* #

class HistoryLevel(Model, BaseId):
    class Meta(BaseMeta):
        ...
    name: str = String(max_length=100,unique=True)

class ProjectHistory(Model, BaseId):
    class Meta(BaseMeta):
        ...
    text: str = Text()
    level: HistoryLevel = ForeignKey(HistoryLevel)
    pproject: Project = ForeignKey(Project)
    ids = Integer()

# !-------------------- Task --------------------! # 
# *-------------------- Foreign Key --------------------* #

class TaskStatus(Model, BaseId):
    class Meta(BaseMeta):
        ...
    name:str = String(max_length=100,unique=True)

class TaskStage(Model, BaseId):
    class Meta(BaseMeta):
        ...
    name:str = String(max_length=500,unique=True)

# *-------------------- Base --------------------* #

class Task(Model, BaseId):
    class Meta(BaseMeta):
        ...
    pproject: Project = ForeignKey(Project)
    name: str = String(max_length=500)
    status: TaskStatus = ForeignKey(TaskStatus)
    description: Optional[Text] = Text()
    datestart: Optional[date] = Date()
    dateend: Optional[date] = Date()
    responsible: Optional[User] = ForeignKey(User)
    stage: Optional[TaskStage] = ForeignKey(TaskStage)

# !-------------------- Assignment --------------------! #
# *-------------------- Foreign Key --------------------* #

class AssignmentStatus(Model, BaseId):
    class Meta(BaseMeta):
        ...
    name: str = String(max_length=100,unique=True)

# *-------------------- Base --------------------* #

class Assignment(Model, BaseId):
    class Meta(BaseMeta):
        ...
    ptask = ForeignKey(Task)
    name: str = String(max_length=255)
    user: Optional[User] = ForeignKey(User)
    status: Optional[AssignmentStatus] = ForeignKey(AssignmentStatus)
    datetimestart: Optional[datetime] = DateTime()
    datetimeend: Optional[datetime] = DateTime()
    timeneeded: Optional[int] = Integer(default=0)

# *-------------------- Chat --------------------* #

class AssignmentChat(Model, BaseId):
    class Meta(BaseMeta):
        ...
    message: str = Text()
    sender: User = ForeignKey(User)
    datetime: datetime = DateTime()
    ptaskchlistid: Assignment = ForeignKey(Assignment)

# *-------------------- Files --------------------* #

class AssignmentFiles(Model, BaseId):
    class Meta(BaseMeta):
        ...
    ptaskchlistid: Assignment = ForeignKey(Assignment)
    sender: User = ForeignKey(User)
    datetime: datetime = DateTime()
    filepath: str = Text()


# !-------------------- Event --------------------! #
# *-------------------- Foreign Key --------------------* #

class Eventstatus(Model, BaseId):
    class Meta(BaseMeta):
        ...
    name: str = String(max_length=100,unique=True)

# *-------------------- Base --------------------* #

class Event(Model, BaseId):
    class Meta(BaseMeta):
        ...
    name: str = String(max_length=1000)
    status: Optional[Eventstatus] = ForeignKey(Eventstatus) 
    users: Optional[list[User]] = ManyToMany(User, related_name = "user_x_user")
    description: str = Text()
    dateandtime: datetime = DateTime()
    place: str = String(max_length=1000)
    leader: User = ForeignKey(User, related_name = "leader_x_user")

class EventCheckList(Model,BaseId):
    class Meta(BaseMeta):
        ...
    pevent: Event = ForeignKey(Event) 
    name: str = String(max_length=500)
    user: User = ForeignKey(User)
    checked: bool = Boolean(default = False)
    datestart: datetime = DateTime() 
    timeneeded: int = Integer()    

class EventChat(Model,BaseId):
    class Meta(BaseMeta):
        ...
    pchlist: EventCheckList = ForeignKey(EventCheckList) 
    message: str = Text()
    sender: User = ForeignKey(User)
    datetime: datetime = DateTime() 


class EventFiles(Model, BaseId):
    class Meta(BaseMeta):
        ...
    pchlistchat: EventChat = ForeignKey(EventChat)
    sender: User = ForeignKey(User)
    datetime: datetime = DateTime()
    filepath: str = Text()

# !-------------------- Notes --------------------! #

class Notes(Model, BaseId):
    class Meta(BaseMeta):
        ...
    message: Optional[str] = Text()
    user:User = ForeignKey(User, related_name='author') 
    datetime:datetime = DateTime()
    note:bool = Boolean() 
    visiblefor: Optional[list[User]] = ManyToMany(User, related_name = "visiblefor_x_user") 

class NotesCheckList(Model, BaseId):
    class Meta(BaseMeta):
        ...
    pnote: Notes = ForeignKey(Notes)
    name:str = String(max_length=300)
    checked:bool = Boolean(default=False) 

class NoteFiles(Model, BaseId):
    class Meta(BaseMeta):
        ...
    pnote:Notes =  ForeignKey(Notes)
    filepath:str = String(max_length=1000)
    sender: User = ForeignKey(User)
    datetime: datetime = DateTime()

# !-------------------- Canban --------------------! #

class CanbanTask(Model, BaseId):
    class Meta(BaseMeta):
        ...
    stage:str = String(max_length=100, default='Не распределено')

class CanbanNotes(Model, BaseId):
    class Meta(BaseMeta):
        ...
    stage:str = String(max_length=100, default='Не распределено')      


class Canban(Model, BaseId):
    class Meta(BaseMeta):
        ...
    name:str = String(max_length=100)
    author:User=ForeignKey(User,related_name="author_canban")
    name:str = String(max_length=100)    
    user:User = ManyToMany(User, related_name="canbanuser_x_user")
    task: Optional[list[CanbanTask]]= ManyToMany(Task, through= CanbanTask)
    note:Optional[list[Notes]]= ManyToMany(Notes, through= CanbanTask)