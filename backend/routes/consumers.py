
import json
import asyncio
import logging

from fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi_jwt_auth import AuthJWT
from fastapi import (
    APIRouter,
    WebSocket,
    WebSocketDisconnect,
    Depends,
    Query,
    status
)

from aioredis.client import PubSub, Redis
from conf.sessions import get_redis_pool

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix='',
    tags=['WS'],
)

@router.websocket("/")
async def websocketwork(websocket: WebSocket, token: str = Query(...),Authorize: AuthJWT = Depends() ):
    
    await websocket.accept()

    try:
        token = token.replace('Bearer ', '')
        Authorize.jwt_required("websocket", token=token)
        user_id = Authorize.get_raw_jwt(token)['user']['id']
        await redis_connector(websocket, user_id)


    except AuthJWTException as err:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)            
        
        
async def redis_connector(websocket: WebSocket, id_user: int):

    async def consumer_handler(conn: Redis, ws: WebSocket, id_user: int):
        try:
            while True:
                message = await ws.receive_text()
                if message:
                    await conn.publish(f"user:{id_user}", message)
                    await conn.publish("main", "hello")
        except WebSocketDisconnect as exc:
            # TODO this needs handling better
            logger.error(exc)

    async def producer_handler(pubsub: PubSub, ws: WebSocket, id_user: int):
        await pubsub.subscribe(f"user:{id_user}", "main")
        # assert isinstance(channel, PubSub)
        try:
            while True:
                message = await pubsub.get_message(ignore_subscribe_messages=True)
                if message:
                    await ws.send_text(message.get('data'))
        except Exception as exc:
            # TODO this needs handling better
            logger.error(exc)

    conn = await get_redis_pool()
    pubsub = conn.pubsub()

    consumer_task = consumer_handler(conn=conn, ws=websocket, id_user=id_user)
    producer_task = producer_handler(pubsub=pubsub, ws=websocket, id_user=id_user)
    
    done, pending = await asyncio.wait(
        [consumer_task, producer_task], return_when=asyncio.FIRST_COMPLETED,
    )

    for task in pending:
        task.cancel()