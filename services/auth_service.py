from config.database_connection import SessionLocal
from config import jwt_setting as jw
from model import mainapp_models as md
from sqlalchemy import select ,or_
from selector.common_function import message

from datetime import datetime

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
            
    async def login_user(self ,data):
        try:
            email = data['email']
            password = data['password']

            user = await jw.authenticate_user(email=email ,password= password)
            if user is None : return message("Email or Password Not Match") ,400

            token = jw.create_access_token({"email": user.email} ,expires_delta= 60)

            async with SessionLocal() as db:
                user.last_login = datetime.utcnow()
                db.add(user)
                await db.commit()

            data = {
                    'firstName' : user.first_name ,
                    'lastName' : user.last_name ,
                    'email' : user.email ,
                    'token' : token,
                    'phoneNo' : user.phone_number,
                    'userTypeId' : user.user_type_id,
                    'userType' : user.user_type.user_type
                }

            return data ,200
        except KeyError as k:
                return message(f'{k} is Missing') ,404
        except Exception as e:
                print(e)
                return message('Something Went Wrong') ,500

