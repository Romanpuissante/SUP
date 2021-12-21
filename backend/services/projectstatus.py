
from orm.models import  projectstatuses
from orm.schema import BaseProjectstatuses
from .crud import CRUD
from typing import Optional
from sqlalchemy import Table




class ProjectstatussService(CRUD):
    model = projectstatuses
    schema = BaseProjectstatuses


    @classmethod
    async def getstatuslist():
        pass