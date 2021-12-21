from fastapi_jwt_auth import AuthJWT
from fastapi import (
    APIRouter,
    WebSocket,
    Depends,
    Query
)

from fastapi_jwt_auth.exceptions import AuthJWTException

from starlette.concurrency import run_until_first_complete
from conf.db import broadcast
import json


router = APIRouter(
    prefix='',
    tags=['WS'],
)

async def receiver(websocket: WebSocket):
    
    async for data in websocket.iter_json():
        await broadcast.publish(channel=f"chatroom", message=json.dumps(data))

async def sender(websocket: WebSocket):
    
    async with broadcast.subscribe(channel=f"chatroom") as subscriber:
        async for event in subscriber:
            await websocket.send_json(event.message)


@router.websocket("/")
async def websocket(websocket: WebSocket, token: str = Query(...), Authorize: AuthJWT = Depends()):
    
    await websocket.accept()
    try:

        Authorize.jwt_required("websocket", token=token.replace('Bearer ', ''))

        await run_until_first_complete(
            (receiver, {"websocket": websocket}),
            (sender, {"websocket": websocket}),
        )
    except AuthJWTException as err:
        await websocket.send_text(err.message)
        await websocket.close()

    