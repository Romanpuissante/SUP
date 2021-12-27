# from orm.models import user
# from orm.schema import UserInfoNoPwd
# from .crud import CRUD




# class UserService(CRUD):
#     model = user
#     schema = UserInfoNoPwd



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


# @router.post("/user/")
# async def create_user(user: UserSchema):
#     user_id = await User.create(**user.dict())
#     return {"user_id": user_id}


# @router.get("/user/{id}", response_model=UserSchema)
# async def get_user(id: int):
#     user = await User.get(id)
#     return UserSchema(**user).dict()

# @router.get("/users/", response_model=List[UserSchema])
# async def get_users():
#     users = await User.all()
#     return [UserSchema(**user) for user in users]