from fastapi import (
    APIRouter,
    Depends,
    status
)
from sqlalchemy import select, func, or_
from conf.sessions import database
from services.depends import AD
from orm.models import *
from orm.schema import *
from conf.log import logger
from services.projects import ProjectService

router = APIRouter(
    prefix='/test',
    tags=['Всяческое тестирование'], 
    
)


# async def geto_user(id: int, use
# AS = AD(ProjectService)
@router.post("/updateassigment",  status_code=status.HTTP_201_CREATED)
#  ! 
async def updateassigment(assigment: AssigmentUpdate):
    print(assigment)
    return {"mess": "ok"}


@router.get("/getuser")
#  ! 
async def users():
    users = await User.objects.values({"id", "first_name"})
    
    print(users)
    
    return {"mess": users}


@router.post("/createassigment",  status_code=status.HTTP_201_CREATED)
#  ! 
async def createassigment(assigment: AssigmentCreate):
    pr = await Assignment.objects.create(**assigment.dict())
    return {"mess": "ok"}





@router.get("/{userid}/{projectid}/{taskid}",  status_code=status.HTTP_201_CREATED)
#  ! 
async def get_task_list(userid: int, projectid:int):
    
    result = await ProjectService.give_list_tasks(userid, projectid)
    return {"mess": result}






@router.get("/{userid}",  status_code=status.HTTP_201_CREATED)
#  ! 
async def get_project_list(userid: int):
#    ! Нужно создать задачу, только потом получится )
    
    result = await ProjectService.give_list_projects(userid)
    return {"mess": result}



@router.post("/deleteproj",  status_code=status.HTTP_201_CREATED)
#  ! 
async def del_project(projectid: int):
    await Project.objects.delete(id = projectid)
   
    print("-----!---------!------------!-")
    return {"mess": "Проект удален"}

@router.post("/createproj",  status_code=status.HTTP_201_CREATED)
#  ! 
async def create_projects(project: ProjectCreate):
   
    print("-----!---------!------------!-")

    # ! PK ONLY
    # u = User(id = user["id"], __pk_only__ = True)
    # ! И
    # (Project.author==User(id = user["id"]))|(Project.leader==user["id"])|(Project.author==user["id"])
    # ! VALUES
    # pr = await Project.objects.filter(author=u.pk).values()
    # ! MANY 2 MANY SAVE
    newpr =project.dict(exclude={'users','id'})
    newpr["lastchanged"] = datetime.now()
    pr = await Project.objects.create(**newpr)
    for user in project.users:  
        await pr.users.add(User(id = user.id, __pk_only__ = True))
    return {"mess": "ok"}

# , user=Depends(AD.protect_claim)
@router.post("/updateproj",  status_code=status.HTTP_201_CREATED)
#  ! 
async def upd_my_project(project: ProjectUpdate):

    project_field_update = project.dict(exclude={'users'}, exclude_unset=True)
    if len(project_field_update.keys()) > 1:
        project_field_update["lastchanged"] = datetime.now()
        await Project(**project_field_update).update(project_field_update.keys())

    if "users" not in project.dict(exclude_unset=True):
        return {"mess": "Нет юзеров"}
    
    project_with_users = await Project.objects.select_related("users").fields(['id', 'users__id']).get(id=project.id)
    
    projectuser = project_with_users.users
    oldusers = {user.id for user in projectuser}
    currentusers = {user.id for user in project.users}

    for userid in oldusers.difference(currentusers):
        await projectuser.remove(User(id = userid, __pk_only__ = True))
        # "Вас исключили из проекта"

    for userid in currentusers.difference(oldusers):
        await projectuser.add(User(id = userid, __pk_only__ = True))
        # Вы добавлены в проект

    return {"mess": projectuser}




@router.post("/createtask",  status_code=status.HTTP_201_CREATED)
#  ! 
async def create_task(task: TaskCreate):
    newtask =task.dict(exclude={'users','id'})    
    ts = await Task.objects.create(**newtask)
    for user in task.users:  
        await ts.users.add(User(id = user.id, __pk_only__ = True))
    
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