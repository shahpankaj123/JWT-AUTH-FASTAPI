from fastapi import APIRouter
from fastapi.responses import JSONResponse
from services.user_type_service import UserTypeModule
from selector.common_function import message

router = APIRouter()
service = UserTypeModule()


@router.post("/create")
async def create_user_type(data: dict):
    try:
        user_type = data["userType"]
        res, st = await service.create(user_type= user_type)
        return JSONResponse(content=res, status_code=st)
    except KeyError as k:
        return JSONResponse(content=message(f"{k} Field is Missing"),status_code=400)

@router.get("/")
async def get_all_user_type():
    res, st = await service.get_all()
    return JSONResponse(content=res, status_code=st)


@router.post("/update")
async def update_user_type(data: dict):
    res, st = await service.update(data)
    return JSONResponse(content=res, status_code=st)


@router.get("/GetUserTypeById")
async def get_user_type_by_id(user_type_id: str):
    res, st = await service.get_by_id(user_type_id)
    return JSONResponse(content=res, status_code=st)






