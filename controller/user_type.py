from fastapi import APIRouter 
from services.user_type_service import UserTypeModule

from selector.common_function import message
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post("/create")
def create_user_type(data : dict):
    try:
        user_type = data['userType']
        res , st = UserTypeModule().create(user_type= user_type)
        return JSONResponse(content=res,status_code=st)
    except KeyError as k:
        return JSONResponse(content= message(mesaage=f'{k} Field is Missing') ,status_code=404)
    

@router.get("/")
def get_all_user_type():
    res , st = UserTypeModule().get_all()
    return JSONResponse(content=res,status_code=st)

@router.post("/update")
def update_user_type(data : dict):
    res , st = UserTypeModule().update(data)
    return JSONResponse(content=res,status_code=st)



