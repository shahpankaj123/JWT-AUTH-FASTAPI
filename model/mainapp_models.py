from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from config.database_connection import Base
import uuid


class UserType(Base):
    __tablename__ = "user_types"

    id = Column(CHAR(36),primary_key=True,default=lambda: str(uuid.uuid4()),index=True)
    user_type = Column(String(100), nullable=False, unique=True)
    users = relationship("User", back_populates="user_type")

class User(Base):
    __tablename__ = "users"

    id = Column(CHAR(36),primary_key=True,default=lambda: str(uuid.uuid4()),index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True)
    phone_number = Column(String(100), unique=True, index=True)
    password = Column(String(100), nullable= False)
    user_type_id = Column(CHAR(36),ForeignKey("user_types.id"),nullable=False)

    last_login = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # ✅ FIXED HERE
    user_type = relationship("UserType", back_populates="users")
    








    