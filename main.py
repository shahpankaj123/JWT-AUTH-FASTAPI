from fastapi import FastAPI
from typing import Union
from config.database_connection import engine, Base

from controller.auth_controller import router as auth_router
from controller.user_type import router as user_type_router

app = FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(auth_router, prefix="/web/api/v1/users", tags=["Users"])
app.include_router(user_type_router, prefix="/web/api/v1/user-type", tags=["UserType"])

