from fastapi import (
    APIRouter,
    Depends
)
from sqlalchemy.sql.functions import current_user
from orm.schema import UserInfoNoPwd   
from fastapi_jwt_auth import AuthJWT  
from services.otdels import OtdelService
from orm.schema import BaseOtdel



router = APIRouter(
    prefix='/test',
    tags=['Test'],
  
   
    
)



@router.post("/")
async def Check_This_Out(user_data: BaseOtdel,        
                        check_otdel: OtdelService=Depends()):        
        name= await check_otdel.checkForeign(user_data.name.lower().title())
        
        return  name

#    , Authorize: AuthJWT = Depends()
@router.get("/")
async def geto_user(id: int):
   
    # текущий ид пользователя
    print("------------------------------")
    print('current_user')
    
    return {"field":'id',"searchval":'id'}
