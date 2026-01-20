from sqlalchemy.exc import IntegrityError
from config.database_connection import SessionLocal
from model.mainapp_models import UserType
from selector.common_function import message

from sqlalchemy import select

class UserTypeModule:

    def create(self, user_type: str):
        db = SessionLocal()
        try:
            if db.query(UserType).filter(UserType.user_type == user_type).first():
                return message(mesaage='UserType Already Exists'), 400

            user_type_obj = UserType(user_type=user_type)
            db.add(user_type_obj)
            db.commit()
            db.refresh(user_type_obj)
            return message(mesaage='UserType Created Successfully'), 201

        except IntegrityError:
            db.rollback()
            return message(mesaage='UserType Already Exists'), 400

        except Exception as e:
            db.rollback()
            print(e)
            return message(mesaage='Something Went Wrong'), 500

        finally:
            db.close()

    def get_all(self):
        db = SessionLocal()
        try:
            data = db.query(UserType).all()
            res_dict = [{"id": str(item.id), "userType": item.user_type} for item in data]
            return res_dict, 200
        finally:
            db.close()

    def get_by_id(self ,user_type_id):
        db = SessionLocal()
        try:
            data = db.get(UserType, user_type_id)
            return {"id" : data.id , "userType" : data.user_type} ,200
        except KeyError as k:
            return message(f'{k} Field is Missing') ,404
        except Exception as e:
            db.rollback()
            return message('Something Went Wrong'), 500
        finally:
            db.close()


    def update(self ,data):
        db = SessionLocal()
        try:
            user_type = data['userType']
            user_type_id = data['userTypeId']

            user_type_obj = db.get(UserType, user_type_id)
            if not user_type_obj: return message("UserType not found"), 404

            user_type_obj.user_type = user_type
            db.commit()
            db.refresh(user_type_obj)
            return message("UserType updated successfully"), 200

        except KeyError as k:
            return message(f'{k} Field is Missing') ,404
        except Exception as e:
            db.rollback()
            return message('Something Went Wrong'), 500
        finally:
            db.close()


