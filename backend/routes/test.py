from fastapi import (
    APIRouter,
    Depends
)
from services.otdels import OtdelServ
from orm.schema import BaseOtdel
router = APIRouter(
    prefix='/test',
    tags=['Test'],
    
)

@router.post("/")
async def Check_This_Out(user_data: BaseOtdel,        
                        check_otdel: OtdelServ=Depends()):        
        name= await check_otdel.checkOtdel(user_data.name.lower().title())
        
        return  name