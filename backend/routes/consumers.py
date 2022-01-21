
import json

from fastapi import (
    APIRouter,
    WebSocket,
    Depends,
)

from services.depends import AD
from orm.redis import RedisWorker
from orm.models import User

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

@router.websocket("/project/{idp}")
async def websocketwork(idp:int ,websocket: WebSocket, user=Depends(AD.protect_ws)):
    
    if not user:
        return

    print(idp)

    async def consumer(message):

        print(message)

        users = [{"id": 1}, {"id": 3}, {"id": 2}]

        answer = {
            f"user:{user['id']}": message,
            f"project:{idp}":f"projectmessage{idp}",
            "main": "hello"
        }

        for user1 in users:
            answer[f"user:{user1['id']}"] = message
        return answer
        
    await RedisWorker.create_channels(websocket, consumer, channels=(f"user:{user['id']}", f"project:{idp}", "main"))
