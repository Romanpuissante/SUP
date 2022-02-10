import json

from fastapi import (
    APIRouter,
    WebSocket,
    Depends,
)
from aioredis.client import Redis

from services.depends import AD
from services.projects import ProjectService
from orm.redis import RedisWorker
from orm.models import *
from conf.log import logger
from orm.schema import *


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

    projects = await ProjectService.give_list_projects(user_id, is_superuser=user["superuser"])
    statuses_projects = await ProjectStatus.objects.values()
    statuses_tasks = await TaskStatus.objects.values()

    save_info = {
        f"user:{user_id}": {
            "channel": "reestr:project",
            "give_info": ["list_project"]
        }
    }

    await websocket.send_text(json.dumps({"projects": projects, "action": "build", "statuses_projects": statuses_projects, "statuses_tasks": statuses_tasks}, default=str))

    async def consumer(data, conn: Redis):

        data = json.loads(data)

        if "action" not in data:
            pass
        
        if data["action"] == "tasks":
            
            tasks = await ProjectService.give_list_tasks(user_id, data["project_id"], user["superuser"])

            return {
                f"user:{user_id}": json.dumps({"action": "buildTasks", "tasks": tasks}, default=str)
            }
        
    await RedisWorker.create_channels(websocket, consumer=consumer, channels=(f"user:{user_id}", "reestr:project"), save_info=save_info)


@router.websocket("/project/{id}")
async def websocketwork(id:int ,websocket: WebSocket, user=Depends(AD.protect_ws)):
    
    if not user:
        return

    allusers = await User.objects.select_related("otdel").order_by(["otdel__name", "last_name", "first_name"]).values({"id", "first_name","middle_name","last_name","otdel__name"})
    await websocket.send_json({"users": allusers})

    # save_info = {
    #     f"user:{user['id']}": {
    #         "channel": f"project:{id}",
    #         "give_info": ["list_project"]
    #     }
    # }

    async def consumer(data, conn: Redis):

        if id == 0:
            
            data = json.loads(data)
            newpr =ProjectCreate(**data).dict(exclude={'users','id'})
            newpr["lastchanged"] = datetime.now()
            list_channels = {"reestr:project", f"project:{id}"}
            list_given = {"list_project"}

            pr = await Project.objects.create(**newpr)
            for usert in data["users"]:  
                await pr.users.add(User(id = usert["id"], __pk_only__ = True))

            message_data = {
                "list_project": {"projects": pr},
                "dsafsdf": {"msg2": "notok"}
            }

            result = {}

            users_send = {*set(map(lambda x: x["id"], data["users"])), data["leader"]["id"], data["author"]["id"]}
            for usersend in users_send:
                info_send_user = await conn.get(f"user:{usersend}")
              
                if not info_send_user:
                    continue

                info_send_user = json.loads(info_send_user)
                if info_send_user["channel"] not in list_channels:
                    continue

                list_info = list_given.intersection(info_send_user["give_info"])

                send_data={"action": "update"}
                for info in list_info:
                    send_data.update(message_data[info])

                result[f"user:{usersend}"] = json.dumps(send_data, default=str)

            return result

        # newpr["lastchanged"] = datetime.now()
        # pr = await Project.objects.create(**newpr)
        # for user in data.users:  
        #     await pr.users.add(User(id = user.id, __pk_only__ = True))
    
        

        
        return {
            f"user:{user['id']}": json.dumps({"mess": "ok"}),
        }
        
    await RedisWorker.create_channels(websocket, consumer, channels=(f"user:{user['id']}", f"project:{id}"))
    # , save_info=save_info
