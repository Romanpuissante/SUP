from sqlalchemy import select, func, or_
from conf.sessions import database
from ormar import or_ as orm_or

from orm.models import *

class ProjectService():

    @classmethod
    async def give_list_projects(cls, userid, is_superuser=False):

        project = Project.Meta.table
        task = Task.Meta.table
        pruser = ProjectUser.Meta.table
        status = ProjectStatus.Meta.table
        
        completed_task = (
            select(func.count(task.c.id))
            .where(task.c.status == 4)
            .where(task.c.project == project.c.id)
            .select_from(task).scalar_subquery().correlate(project)
        )

        filter_user = True if is_superuser else or_(pruser.c.user == userid, project.c.author == userid, project.c.leader==userid)

        q = (
            select(
                func.count(task.c.id).label("all_tasks"), completed_task.label("completed_tasks"),  project.c.id, project.c.name, status.c.name.label("status"), status.c.id.label("status_id"), project.c.lastchanged, project.c.dateend
            ).where(filter_user)
            .join(status, project.c.status == status.c.id)
            .join(task, task.c.project == project.c.id, isouter=True)
            .join(pruser, pruser.c.project == project.c.id, isouter=True)
            
            .select_from(project).group_by(project.c.id, status.c.id)
        )

        return [dict(x) for x in await database.fetch_all(q)]

    @classmethod
    async def give_list_tasks(cls, userid, projectid, is_superuser=False):

        task = Task.Meta.table
        assigment = Assignment.Meta.table
        status = TaskStatus.Meta.table

        completed_assigment = (
            select(func.count(assigment.c.id))
            .where(assigment.c.status == 5)
            .where(assigment.c.task == task.c.id)
            .select_from(assigment).scalar_subquery().correlate(task)
        )
        
        if not is_superuser:
            if not await Project.objects.select_related(["users"]).filter(orm_or(users__id=userid, author=userid, leader=userid), id=projectid).exists():
                return None

        q = (
            select(
                func.count(assigment.c.id).label("all_assigments"), completed_assigment.label("completed_assigments"), task.c.id, task.c.name, status.c.name.label("status"), status.c.id.label("status_id"), task.c.dateend
            )
            .where(task.c.project == projectid)
            .join(status, task.c.status == status.c.id)
            .join(assigment, assigment.c.task == task.c.id, isouter=True)
            .select_from(task).group_by(task.c.id, status.c.id)
        )

        return [dict(x) for x in await database.fetch_all(q)]
        



        # print(dict(r[0]))
    # print(select([Task]).select_from(table))
    
    # prlist = await Project.objects.select_related(["users","tasks"]).filter(or_(users__id=userid, author = userid, leader=userid)).fields(['id', 'name','lastchanged', 'status','author','users__id','dateend','tasks__id','tasks__name','tasks__status']).all()
    # for x in prlist:        
    #     setattr(x, "taskall", await x.tasks.count())
    #     setattr(x, "taskchecked", await x.tasks.filter(status=4).count())