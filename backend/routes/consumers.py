from fastapi_jwt_auth import AuthJWT
from fastapi import (
    APIRouter,
    WebSocket,WebSocketDisconnect,
    Depends,
    Query,
    status
)
import asyncio
import async_timeout
import aioredis

from fastapi_jwt_auth.exceptions import AuthJWTException
from conf.sessions import redis
from starlette.concurrency import run_until_first_complete
# from conf.db import broadcast, redis
import json


router = APIRouter(
    prefix='',
    tags=['WS'],
)


# async def receiver(websocket: WebSocket, user_id: int):
    
#     async for data in websocket.iter_json():
#         await broadcast.publish(channel=f"chatroom3", message=json.dumps(data))
#         await broadcast.publish(channel=f"chatroom4", message=json.dumps(data))


# async def sender(websocket: WebSocket, user_id: int):


#         async with broadcast.subscribe(channel=f"chatroom{user_id}") as subscriber:
#             async for event in subscriber:
#                 await websocket.send_text(event.message)
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:           
            await connection.send_text(message)


manager = ConnectionManager()

@router.websocket("/")
async def websocket(websocket: WebSocket):
    client_id=1
    # token: str = Query(...), Authorize: AuthJWT = Depends()   
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json(mode="text")
            print(data)            
            print("отправлено")
           
            pubsub = redis.pubsub()
            await pubsub.subscribe("channel:1", "channel:2")

            future = asyncio.create_task(reader(pubsub, websocket))

            await redis.publish("channel:1", "Hello")
            await redis.publish("channel:2", "World")
            await redis.publish("channel:1", STOPWORD)

            await future
           
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client # left the chat")
#     try:

#         token = token.replace('Bearer ', '')
#         Authorize.jwt_required("websocket", token=token)
#         user_id = Authorize.get_raw_jwt(token)['user']['id']

#         await run_until_first_complete(
#             (receiver, {"websocket": websocket, "user_id": user_id}),
#             (sender, {"websocket": websocket, "user_id": user_id}),
#         )
#     except AuthJWTException as err:
#         await websocket.close(code=status.WS_1008_POLICY_VIOLATION)

    

STOPWORD = "STOP"


async def reader(channel: aioredis.client.PubSub, websocket: WebSocket):
    while True:
        try:
            async with async_timeout.timeout(1):
                message = await channel.get_message(ignore_subscribe_messages=True)
                if message is not None:
                    await manager.send_personal_message(f"You wrote:", websocket)
                    await manager.broadcast(f"Client #1 says: {message}")
                    print(f"(Reader) Message Received: {message}")
                    if message["data"] == STOPWORD:
                        print("(Reader) STOP")
                        break
                await asyncio.sleep(0.01)
        except asyncio.TimeoutError:
            pass


# async def main():
    