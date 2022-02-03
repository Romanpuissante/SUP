from typing import Optional
from datetime import date, datetime

from ormar import Integer, String, Boolean, ForeignKey, Model, ModelMeta, ManyToMany, Date, Text, DateTime, pre_save, pre_update
from conf.sessions import database, metadata

# *-------------------- Base --------------------* #
async def change_lastchanged(sender,instance):  
    ttoup=await Project.objects.get(id=instance.project.id)
    
    upit = {'lastchanged':datetime.now()}
    
    if instance.datestart and (not ttoup.datestart or instance.datestart < ttoup.datestart):
        upit['datestart'] = instance.datestart
    if instance.dateend and (not ttoup.dateend or instance.dateend < ttoup.dateend):
        upit['dateend'] = instance.dateend
    await ttoup.update(**upit)


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
    

class UserHardSkill(Model, BaseId):
    class Meta(BaseMeta):
        ...
    level: Optional[int] = Integer(nullable=True)



class GroupSoftSkill(Model, BaseId):
    class Meta(BaseMeta):
        ...
    name: str = String(max_length=500,unique=True)
    

class SoftSkill(Model, BaseId):
    class Meta(BaseMeta):
        ...
    name: str = String(max_length=200,unique=True)
    group: GroupSoftSkill = ForeignKey(GroupSoftSkill)
    

class UserSoftSkill(Model, BaseId):
    class Meta(BaseMeta):
        ...
    level: Optional[int] = Integer(nullable=True)

# *-------------------- Base --------------------* #

class User(Model, BaseId):
 
    username: str = String(max_length=100, unique=True, sql_nullable=False, nullable=True)
    password: str = String(max_length=200, sql_nullable=False, nullable=True)

    first_name: str = String(max_length=100, sql_nullable=False, nullable=True)
    last_name: str = String(max_length=100, sql_nullable=False, nullable=True)
    middle_name: Optional[str] = String(max_length=100, nullable=True)

    innerphone: Optional[str] = String(max_length=50, nullable=True)
    phone: Optional[str] = String(max_length=50, nullable=True)
    email: Optional[str] = String(max_length=150, nullable=True)

    otdel: Otdel = ForeignKey(Otdel)
    position: Position = ForeignKey(Position)
    rank: Rank = ForeignKey(Rank)

    hardskills: Optional[list[UserHardSkill]] = ManyToMany(HardSkill,through=UserHardSkill)
    softskills: Optional[list[UserSoftSkill]] = ManyToMany(SoftSkill,through=UserSoftSkill)

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

class DocType(Model, BaseId):
    class Meta(BaseMeta):
        ...
    name:str = String(max_length=100,unique=True)
    

class ProjectStatus(Model, BaseId):
    class Meta(BaseMeta):
        tablename: str = "projectstatuses"
    name:str = String(max_length=100,unique=True)


class ProjectUser(Model, BaseId):
    class Meta(BaseMeta):
        ...
    involved:Optional[Boolean] = Boolean(default=False)

# *-------------------- Base --------------------* #

class Project(Model, BaseId):

    class Meta(BaseMeta):
        ...

    name: str = String(max_length=255, sql_nullable=False, nullable=True)
    description: Optional[str] = Text(nullable=True)
    status: Optional[ProjectStatus] = ForeignKey(ProjectStatus,nullable=True)
    customer: Optional[str] = String(max_length=250, nullable=True)
    author: User = ForeignKey(User, related_name = "author_user")
    leader: User = ForeignKey(User, related_name = "leader_user")
    users: Optional[list[ProjectUser]] = ManyToMany(User, through= ProjectUser)
    datestart: Optional[date] = Date(nullable=True)
    dateend: Optional[date] = Date(nullable=True)
    lastchanged: Optional[datetime] = DateTime(nullable=True)
 

# 

# @pre_update(Project)
# async def before_update(sender, instance, **kwargs):
#     change_lastchanged(instance)

# @pre_save(Project)
# async def before_update(sender, instance, **kwargs):
#     change_lastchanged(instance)


# *-------------------- Documentation --------------------* #

class Documentation(Model, BaseId):

    class Meta(BaseMeta):
        ...
    project: Project = ForeignKey(Project) 
    doctype: DocType =  ForeignKey(DocType)
    created: datetime = DateTime()
    accepted: Optional[datetime]= DateTime()

# *-------------------- History --------------------* #

class HistoryLevel(Model, BaseId):
    class Meta(BaseMeta):
        ...
    name: str = String(max_length=100,unique=True)

class HistoryAction(Model, BaseId):
    class Meta(BaseMeta):
        ...
    name: str = String(max_length=100,unique=True)

class ProjectHistory(Model, BaseId):

    class Meta(BaseMeta):
        tablename: str = "projecthistories"
    

    text: str = Text()
    level: HistoryLevel = ForeignKey(HistoryLevel)
    project: Project = ForeignKey(Project)
    action: HistoryAction = ForeignKey(HistoryAction)    
    createdate: datetime = DateTime(default=datetime.now())

# !-------------------- Task --------------------! # 
# *-------------------- Foreign Key --------------------* #

class TaskStatus(Model, BaseId):
    class Meta(BaseMeta):
        tablename: str = "taskstatuses"
    name:str = String(max_length=100,unique=True)

class TaskStage(Model, BaseId):
    class Meta(BaseMeta):
        ...
    name:str = String(max_length=500,unique=True)

# *-------------------- Base --------------------* #
class TaskUser(Model, BaseId):
    class Meta(BaseMeta):
        ...

class Task(Model, BaseId):
    class Meta(BaseMeta):
        ...
    project: Project = ForeignKey(Project, related_name = "project_task")
    name: Optional[str] = String(max_length=500, sql_nullable=False, nullable=False)
    status: TaskStatus = ForeignKey(TaskStatus)
    description: Optional[Text] = Text(nullable=True)
    datestart: Optional[date] = Date(nullable=True)
    dateend: Optional[date] = Date(nullable=True)
    dateendchanged: bool = Boolean(default=False)
    responsible: Optional[User] = ForeignKey(User, nullable=True, related_name = "responsible_user")
    stage: Optional[TaskStage] = ForeignKey(TaskStage, nullable=True)
    users: Optional[list[TaskUser]] = ManyToMany(User, through= TaskUser)

@pre_save(Task)
async def before_update(sender, instance, **kwargs):
    await change_lastchanged(sender,instance)
@pre_update(Task)
async def before_update(sender, instance, **kwargs):
    await change_lastchanged(sender, instance)

# !-------------------- Assignment --------------------! #
# *-------------------- Foreign Key --------------------* #

class AssignmentStatus(Model, BaseId):
    class Meta(BaseMeta):
        tablename: str = "assignmentstatuses"
    name: str = String(max_length=100,unique=True)

# *-------------------- Base --------------------* #

class Assignment(Model, BaseId):
    class Meta(BaseMeta):
        ...
    task = ForeignKey(Task)
    name: str = String(max_length=255)
    user: Optional[User] = ForeignKey(User)
    status: Optional[AssignmentStatus] = ForeignKey(AssignmentStatus)
    datetimestart: Optional[datetime] = DateTime(nullable=True)
    datetimeend: Optional[datetime] = DateTime(nullable=True)
    timeneeded: Optional[int] = Integer(default=0)

# *-------------------- Chat --------------------* #

class AssignmentChat(Model, BaseId):
    class Meta(BaseMeta):
        ...
    message: str = Text()
    sender: User = ForeignKey(User)
    datetime: datetime = DateTime()
    assignment: Assignment = ForeignKey(Assignment)

# *-------------------- Files --------------------* #

class AssignmentFile(Model, BaseId):
    class Meta(BaseMeta):
        ...
    assignment: Assignment = ForeignKey(Assignment)
    sender: User = ForeignKey(User)
    datetime: datetime = DateTime()
    filepath: str = Text()


# !-------------------- Event --------------------! #
# *-------------------- Foreign Key --------------------* #

class Eventstatus(Model, BaseId):
    class Meta(BaseMeta):
        tablename: str = "eventstatuses"
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
    event: Event = ForeignKey(Event) 
    name: str = String(max_length=500)
    user: User = ForeignKey(User)
    checked: bool = Boolean(default = False)
    datestart: datetime = DateTime() 
    timeneeded: int = Integer()    

class EventChat(Model,BaseId):
    class Meta(BaseMeta):
        ...
    chlist: EventCheckList = ForeignKey(EventCheckList)
    message: str = Text()
    sender: User = ForeignKey(User)
    datetime: datetime = DateTime() 


class EventFile(Model, BaseId):
    class Meta(BaseMeta):
        ...
    chlist: EventCheckList = ForeignKey(EventCheckList)
    sender: User = ForeignKey(User)
    datetime: datetime = DateTime()
    filepath: str = Text()

class EventHistory(Model, BaseId):
    class Meta(BaseMeta):
        tablename: str = "eventhistories"
    text: str = Text()
    level: HistoryLevel = ForeignKey(HistoryLevel)
    event: Event = ForeignKey(Event)
    action: HistoryAction = ForeignKey(HistoryAction)    
    createdate: datetime = DateTime(default=datetime.now())

# !-------------------- Notes --------------------! #

class Note(Model, BaseId):
    class Meta(BaseMeta):
        ...
    message: Optional[str] = Text()
    user:User = ForeignKey(User, related_name='author') 
    datetime:datetime = DateTime()
    note:bool = Boolean() 
    visiblefor: Optional[list[User]] = ManyToMany(User, related_name = "visiblefor_x_user") 

class NoteCheckList(Model, BaseId):
    class Meta(BaseMeta):
        ...
    note: Note = ForeignKey(Note)
    name:str = String(max_length=300)
    checked:bool = Boolean(default=False) 

class NoteFile(Model, BaseId):
    class Meta(BaseMeta):
        ...
    note: Note =  ForeignKey(Note)
    filepath: str = String(max_length=1000)
    sender: User = ForeignKey(User)
    datetime: datetime = DateTime()

# !-------------------- Canban --------------------! #

class Canban(Model, BaseId):
    class Meta(BaseMeta):
        ...
    name: str = String(max_length=100)
    author: User=ForeignKey(User,related_name="author_canban") 
    users: User = ManyToMany(User, related_name="canbanuser_x_user")
    
class CanbanStage(Model, BaseId):
    class Meta(BaseMeta):
        ...
    canban: Canban = ForeignKey(Canban)
    name:str = String(max_length=100, default='Не распределено')
    tasks: Optional[list[Task]]= ManyToMany(Task,nullable=True)
    notes: Optional[list[Note]]= ManyToMany(Note,nullable=True)