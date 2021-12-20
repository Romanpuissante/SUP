
from orm.models import otdels
from orm.schema import BaseOtdel
from .crud import CRUD
from conf.db import db

class OtdelService(CRUD):
    model = otdels
    schema = BaseOtdel

class OtdelServ(OtdelService):
   
    @classmethod
    async def checkOtdel(cls,name:str):
        """Проверка отдела по его названию. Если отсутствует - добавляется в базу данных"""
        query = cls.model.select().where(cls.model.c.name == name)
        result =  await db.fetch_one(query)   
        
        if result==None:            
            result = await cls.create(name=name)             
        return  cls.schema(**result).dict()
