
from fastapi import (
    APIRouter,
    Depends
)
from typing import Optional
from fastapi_jwt_auth import AuthJWT
from orm.models import project
from orm.schema import BaseProject,BaseProjectstatuses
from services.projects import ProjectService
from services.projectstatus import ProjectstatussService
router = APIRouter(
    prefix='/project',
    tags=['Project'],
    
)





# operation_id="authorize"
# @router.get("/")
# async def get_all_projects(
#             user_id = Depends(currentuserID),
#             filterstatus: Optional[Depends()]=None):
#     print(user_id)
#     projectsList = await ProjectService.get_list(params={"field":"", 'searchval':""})
#     return []

# @router.get("/")
# async def get_all_projects(user_id = Depends(currentuserID)):
#     print(user_id)

#     return {"a":"b"}

# @router.post("/")
# async def create_project(project: ProjectSchema):
#     project_id = await Project.create(**project.dict())
#     return {"project_id": project_id}


# @router.get("/{id}")
# async def get_project(id: int, ):
#     project = await Project.get_join(id, ("User",))
#     return {'project': project}

