from config.database_connection import SessionLocal
from config import jwt_setting as jw
from model import mainapp_models as md
from sqlalchemy import select ,or_
from selector.common_function import message

class AuthService:

    async def create_user(self ,data):
        async with SessionLocal() as db:
            try:
                email = data['email']
                first_name = data['firstName']
                last_name = data['lastName']
                password = data['password']
                ph_no = data['phoneNo']

                query = await db.execute(select(md.User).where(or_(md.User.email == email ,md.User.phone_number == ph_no)))

                if query.scalar_one_or_none() :
                    return message('Phone Number or Email Already Exists !') ,400
                
                query = await db.execute(select(md.UserType).where(md.UserType.user_type == 'Normal'))
                user_type_obj = query.scalar_one_or_none()

                if user_type_obj is None : return message("UserType Not Exists") ,400

                user = md.User(
                    first_name = first_name,
                    last_name = last_name,
                    email = email,
                    phone_number = ph_no,
                    user_type_id = user_type_obj.id,
                    password = jw.get_password_hash(password=password)
                )

                db.add(user)
                await db.commit()
                await db.refresh(user)

                return message('User created successfully'), 201
            
            except KeyError as k:
                return message(f'{k} is Missing') ,404

            except Exception as e:
                await db.rollback()
                print(e)
                return message('Something went wrong'), 500

