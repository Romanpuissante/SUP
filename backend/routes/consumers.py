import json

from fastapi import (
    APIRouter,
    WebSocket,
    Depends,
)
from orm.models import Project

from services.depends import AD
from orm.redis import RedisWorker
from orm.models import User
from conf.log import logger

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
    projects = await Project.objects.filter((Project.author==user_id)|(Project.leader==user_id)|(Project.author==user_id)).all()
    await websocket.send_json({"data": projects})

    await RedisWorker.create_channels(websocket, channels=(f"user:{user_id}", "reestr:project"))


@router.websocket("/project/new/")
async def websocketwork(websocket: WebSocket, user=Depends(AD.protect_ws)):

    allusers = await User.objects.values("id", "first_name","middle_name","last_name","otdel__name")
    await websocket.send_json({"users": allusers})

    async def consumer(message):
        project = await Project.objects.create(json.loads(message))
        



    await RedisWorker.create_channels(websocket, consumer, channels=(f"user:{user['id']}"))

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
