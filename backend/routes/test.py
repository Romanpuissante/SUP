from fastapi import (
    APIRouter,
    Depends,
    status
)
from services.depends import AD
from orm.models import *
from services.auth import AuthService
from orm.schema import UserRegister, ProjectCreate

router = APIRouter(
    prefix='/test',
    tags=['Всяческое тестирование'], 
    
)
# AS = AD(ProjectService)

@router.post("/",  status_code=status.HTTP_201_CREATED)
#  ! 
async def create_projects(project: ProjectCreate, user=Depends(AD.protect_claim)):
   
    print("-----!---------!------------!-")
    print(user)
    # ! PK ONLY
    # u = User(id = user["id"], __pk_only__ = True)
    # ! И
    # (Project.author==User(id = user["id"]))|(Project.leader==user["id"])|(Project.author==user["id"])
    # ! VALUES
    # pr = await Project.objects.filter(author=u.pk).values()
    # ! MANY 2 MANY SAVE
    pr = await Project.objects.create( **project.dict(exclude={'users','id'}))
    for user in project.users:    
        await pr.users.add(User(id = user.id, __pk_only__ = True))
    return {"mess": "ok"}

@router.post("/updateproj",  status_code=status.HTTP_201_CREATED)
#  ! 
async def get_my_projects(project: ProjectCreate, user=Depends(AD.protect_claim)):
#    В апдейте надо придумать,чтобы при добавлении юзера или удалении его из проекта, 
#  происходила отправка только тем, кому надо.
    print("-----!---------!------------!-")
    
    
    pr = await Project.objects.select_related("users").get(id=project.id)
    print(pr)
    # await pr.users.clear()
    await pr.update( **project.dict(exclude={'users'}))
    
    for user in project.users:    
        await pr.users.add(User(id = user.id, __pk_only__ = True))
    return {"mess": "ok"}


# post = await Post(title="Test post").save() 
# await post.categories.create( name="Test category1",  postcategory={"sort_order": 1, "param_name": "volume"}, )

# @router.post('/auth/register', status_code=status.HTTP_201_CREATED, response_model=UserFull, tags=['Авторизация'])
# async def register(user_data: UserRegister, auth_service: AuthService = Depends(AS.serv)):
#     """ Регистрация пользователя """
 
#     return await auth_service.create(user_data)

# await ProjectService.get_list(params={"field":"", 'searchval':""})

# @router.post("/")
# async def Check_This_Out(user_data: BaseOtdel,        
#                         check_otdel: OtdelService=Depends()):        
#         name= await check_otdel.checkForeign(user_data.name.lower().title())
        
#         return  name

# #    , Authorize: AuthJWT = Depends()
# @router.get("/{id}")
# async def geto_user(id: int, user_id = Depends(currentuserID)):
   
#     # текущий ид пользователя
#     print("------------------------------")
#     print('current_user')
    
#     return {"field":'id',"searchval":'id'}


# async def receiver(websocket: WebSocket, user_id: int):
    
#     async for data in websocket.iter_json():
#         await broadcast.publish(channel=f"chatroom3", message=json.dumps(data))
#         await broadcast.publish(channel=f"chatroom4", message=json.dumps(data))


# async def sender(websocket: WebSocket, user_id: int):


#         async with broadcast.subscribe(channel=f"chatroom{user_id}") as subscriber:
#             async for event in subscriber:
#                 await websocket.send_text(event.message)
# class ConnectionManager:
#     def __init__(self):
#         self.active_connections: list[WebSocket] = []
    

#     async def connect(self, websocket: WebSocket):
#         await websocket.accept()
#         self.active_connections.append(websocket)
        

#     def disconnect(self, websocket: WebSocket):
#         self.active_connections.remove(websocket)

#     async def send_personal_message(self, message: str, websocket: WebSocket):
#         await websocket.send_text(message)

#     async def broadcast(self, message: str):
#         for connection in self.active_connections:           
#             await connection.send_text(message)

# STOPWORD = "STOP"


# async def reader(channel: aioredis.client.PubSub, websocket: WebSocket):
#     while True:
#         try:
#             async with async_timeout.timeout(1):
#                 message = await channel.get_message(ignore_subscribe_messages=True)
#                 if message is not None:
#                     if message["data"] == STOPWORD:
#                         print("(Reader) STOP")
#                         break
#                     # await manager.send_personal_message(f"You wrote:", websocket)
#                     await websocket.send_text(f"Client #1 says: {message}")
#                     print(f"(Reader) Message Received: {message}")
                    
#                 await asyncio.sleep(0.01)
#         except asyncio.TimeoutError:
#             pass
   # try:
        
    #     while True:
    #         data = await websocket.receive_json(mode="text")
    #         print(data)            
    #         print("отправлено")
        
            

    #         future = asyncio.create_task(reader(pubsub, websocket))

    #         await redis.publish("channel:1", json.dumps(data))
    #         await redis.publish("channel:2", "World")
    #         await redis.publish("channel:1", STOPWORD)

    #         await future
        
            
    # except WebSocketDisconnect:
    #     # manager.disconnect(websocket)
    #     # await manager.broadcast(f"Client # left the chat")
    #     print("foooooooooooooooooooooooooooooooooooooooooooo, disconnect")
    



# async def main():