# services/user_type_service.py

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from config.database_connection import SessionLocal
from model.mainapp_models import UserType
from selector.common_function import message


class UserTypeModule:

    async def create(self, user_type: str):
        async with SessionLocal() as db:
            try:
                result = await db.execute(select(UserType).where(UserType.user_type == user_type))
                if result.scalar_one_or_none():
                    return message(message="UserType Already Exists"), 400

                obj = UserType(user_type=user_type)
                db.add(obj)
                await db.commit()
                await db.refresh(obj)

                return message(message="UserType Created Successfully"), 201

            except IntegrityError:
                await db.rollback()
                return message(message="UserType Already Exists"), 400

            except Exception as e:
                await db.rollback()
                print(e)
                return message(message="Something Went Wrong"), 500

    async def get_all(self):
        async with SessionLocal() as db:
            result = await db.execute(select(UserType))
            data = result.scalars().all()
            return [{"id": str(item.id), "userType": item.user_type} for item in data], 200

    async def get_by_id(self, user_type_id: str):
        async with SessionLocal() as db:
            data = await db.get(UserType, user_type_id)
            if not data: return message("UserType not found"), 404
            return {"id": str(data.id),"userType": data.user_type}, 200

    async def update(self, data: dict):
        async with SessionLocal() as db:
            try:
                user_type = data["userType"]
                user_type_id = data["userTypeId"]

                obj = await db.get(UserType, user_type_id)
                if not obj:
                    return message("UserType not found"), 404

                obj.user_type = user_type
                await db.commit()
                await db.refresh(obj)
                return message("UserType updated successfully"), 200

            except KeyError as k:
                return message(f"{k} Field is Missing"), 400

            except Exception as e:
                await db.rollback()
                print(e)
                return message("Something Went Wrong"), 500



