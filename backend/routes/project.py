
from fastapi import (
    APIRouter,
)

from orm.models import Project
from orm.schema import ProjectSchema, ProjectGet

router = APIRouter(
    prefix='/project',
    tags=['Project'],
)

@router.post("/")
async def create_project(project: ProjectSchema):
    project_id = await Project.create(**project.dict())
    return {"project_id": project_id}


@router.get("/{id}")
async def get_project(id: int):
    project = await Project.get_join(id, ("User",))
    return {'project': project}