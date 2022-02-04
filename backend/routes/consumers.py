from asyncio import log
import json

from fastapi import (
    APIRouter,
    WebSocket,
    Depends,
)
from orm.models import Project

from services.depends import AD
from services.projects import ProjectService
from orm.redis import RedisWorker
from orm.models import *
from conf.log import logger
from orm.schema import *


router = APIRouter(
    prefix='',
    tags=['WS'],
)
# message.get('data')


@router.websocket("/")
async def websocketwork(websocket: WebSocket, user=Depends(AD.protect_ws)):
    
    if not user:
        return

    async def consumer(message):

        print(message)

        return {
            f"user:{user['id']}": message,
            "main": "hello"
        }
        
    await RedisWorker.create_channels(websocket, consumer, channels=(f"user:{user['id']}", "main"))

@router.websocket("/reestr/project")
async def reestr(websocket: WebSocket, user=Depends(AD.protect_ws)):

    if not user:
        return

    user_id = user['id']
    projects = await ProjectService.give_list_projects(user_id, is_superuser=user["superuser"])
    # json.dumps({"projects": projects}, default=str)
    await websocket.send_text(json.dumps({"projects": projects}, default=str))

    await RedisWorker.create_channels(websocket, channels=(f"user:{user_id}", "reestr:project"))


@router.websocket("/projectnew")
async def websocketwork(websocket: WebSocket, user=Depends(AD.protect_ws)):
  
    if not user:
        return

 
    allusers = await User.objects.select_related("otdel").order_by(["otdel__name", "last_name", "first_name"]).values({"id", "first_name","middle_name","last_name","otdel__name"})
    # logger.debug([ u.dict(include={"id", "first_name","middle_name","last_name","otdel"}) for u in allusers]) Если используем метод all, то в списке хранится пайдантик схема, которую надо конвертировать в словарь
    await websocket.send_json({"users": allusers})
 

    async def consumer(project: ProjectCreate, conn):
        # async def create_projects(project: ProjectCreate):  
        
        newpr =project.dict(exclude={'users','id'})

        newpr["lastchanged"] = datetime.now()
        pr = await Project.objects.create(**newpr)
        for user in project.users:  
            await pr.users.add(User(id = user.id, __pk_only__ = True))
    
        project = await Project.objects.create(json.loads(project))
        



    await RedisWorker.create_channels(websocket, channels=(f"user:{user['id']}"))

@router.websocket("/project/{idp}")
async def websocketwork(idp:int ,websocket: WebSocket, user=Depends(AD.protect_ws)):
    
    if not user:
        return

    print(idp)

    async def consumer(message):

        print(message)


        users = [{"id": 1}, {"id": 3}, {"id": 2}]

        answer = {
            # f"user:{user['id']}": message,
            f"project:{idp}":f"projectmessage{idp}",
            # "main": "hello"
        }

        for user1 in users:
            answer[f"user:{user1['id']}"] = message
        return answer
        
    await RedisWorker.create_channels(websocket, consumer, channels=(f"user:{user['id']}", f"project:{idp}"))
