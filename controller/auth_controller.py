from fastapi import APIRouter
from fastapi.responses import JSONResponse

from services.auth_service import AuthService
from selector.common_function import message

router = APIRouter()

@router.post("/signup")
async def register_user( data : dict):
    res , st = await AuthService().create_user(data=data)
    return JSONResponse(content=res ,status_code=st)
