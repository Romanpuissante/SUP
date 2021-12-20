from conf.db import db
from sqlalchemy import Table




class CRUD:

    model: Table
    schema = None

    @classmethod
    async def get(cls, params:dict):
        """
        params={"field":'id',"searchval":id} \n
        Метод принимает параметры поиска, в которых следует указать поле, по которому ищем и искомое значение \n
        К выводу - один единственный результат
        """
        query = cls.model.select().where(cls.model.c[params["field"]] == params["searchval"])
        result = await db.fetch_one(query)
        return cls.schema(**result).dict()


    @classmethod
    async def create(cls, **kwarg):  
        """
        Возвращает весь созданный объект, а не только его ID
        """      
        query = cls.model.insert().values(**kwarg)
        kwarg['id']  = await db.execute(query)
        return kwarg


    @classmethod
    async def checkForeign(cls,name:str)->int:
        """Проверка форинов по полю name - названию. Если отсутствует - добавляется в базу данных"""
        query = cls.model.select().where(cls.model.c.name == name)
        result =  await db.fetch_one(query)   
        
        if result==None:            
            result = await cls.create(name=name)             
        return  cls.schema(**result).dict()['id']

    

    #     @classmethod
#     def model(cls) -> Table:
#         return cls.tables[cls.__name__]

#     @classmethod
#     def othermodel(cls, name) -> Table:
#         return cls.tables[name]

#     @classmethod
#     async def get(cls, id):
#         query = cls.model().select().where(cls.model().c.id == id)
#         return await db.fetch_one(query)

#     @classmethod
#     async def get_join(cls, id, childs):
#         query = cls.model().select(cls.model().c.id == id)

#     @classmethod
#     async def create(cls, **kwarg):
#         query = cls.model().insert().values(**kwarg)
#         return await db.execute(query)

#     @classmethod
#     async def all(cls):
#         query = cls.model().select()
#         return await db.fetch_all(query)