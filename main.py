from fastapi import FastAPI
from config.database_connection import engine, Base

# IMPORTANT: import models
from model import mainapp_models  # noqa

from controller.auth_controller import router as auth_router
from controller.user_type import router as user_type_router

app = FastAPI()

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(auth_router, prefix="/web/api/v1/users", tags=["Users"])
app.include_router(user_type_router, prefix="/web/api/v1/user-type", tags=["UserType"])


