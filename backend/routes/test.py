from fastapi import (
    APIRouter,
    Depends
)
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