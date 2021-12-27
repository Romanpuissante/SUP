from fastapi import (
    APIRouter,
    Depends
)


# from services.otdels import OtdelService
# from orm.schema import BaseOtdel
# from services.depends import currentuserID



# router = APIRouter(
#     prefix='/test',
#     tags=['Test'],
  
   
    
# )



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
