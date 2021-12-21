from fastapi import (
    APIRouter,
    WebSocket,
)
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


@router.websocket_route("/")
async def websocket(websocket: WebSocket):

    await websocket.accept()
    print(2)
    await run_until_first_complete(
        (receiver, {"websocket": websocket}),
        (sender, {"websocket": websocket}),
    )
    # await websocket.send_json({"msg": "Hello WebSocket"})
    # await websocket.close()
