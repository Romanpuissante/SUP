# from fastapi_jwt_auth import AuthJWT
# from fastapi import (
#     APIRouter,
#     WebSocket,
#     Depends,
#     Query,
#     status
# )

# from fastapi_jwt_auth.exceptions import AuthJWTException

# from starlette.concurrency import run_until_first_complete
# from conf.db import broadcast, redis
# import json


# router = APIRouter(
#     prefix='',
#     tags=['WS'],
# )


# async def receiver(websocket: WebSocket, user_id: int):
    
#     async for data in websocket.iter_json():
#         await broadcast.publish(channel=f"chatroom3", message=json.dumps(data))
#         await broadcast.publish(channel=f"chatroom4", message=json.dumps(data))


# async def sender(websocket: WebSocket, user_id: int):


#         async with broadcast.subscribe(channel=f"chatroom{user_id}") as subscriber:
#             async for event in subscriber:
#                 await websocket.send_text(event.message)


# @router.websocket("/")
# async def websocket(websocket: WebSocket, token: str = Query(...), Authorize: AuthJWT = Depends()):
    
   
#     await websocket.accept()
    

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

    