
import json

from fastapi import (
    APIRouter,
    WebSocket,
    Depends,
)

from services.depends import AD
from orm.redis import RedisWorker

router = APIRouter(
    prefix='',
    tags=['WS'],
)
# message.get('data')


@router.websocket("/")
async def websocketwork(websocket: WebSocket, user=Depends(AD.protect_ws)):
    
    if user:

        async def consumer(message):

            return {
                f"user:{user['id']}": message,
                "main": "hello"
            }
            
            
        await RedisWorker.create_channels(websocket, consumer, channels=(f"user:{user['id']}", "main"))