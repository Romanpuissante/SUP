from conf.db import db
from sqlalchemy import Table



class CRUD:

    model: Table
    schema = None

    @classmethod
    async def get(cls, id):
        query = cls.model.select().where(cls.model.c.id == id)
        result = await db.fetch_one(query)
        return cls.schema(**result).dict()

    @classmethod
    async def create(cls, **kwarg):
        query = cls.model.insert().values(**kwarg)
        result = await db.execute(query)
        return { "id": result}




    

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