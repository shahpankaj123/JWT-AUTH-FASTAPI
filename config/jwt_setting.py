from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from pydantic import BaseModel

from config.database_connection import SessionLocal
from sqlalchemy import select

from model import mainapp_models as md

import os
from dotenv import load_dotenv
load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
password_hash = PasswordHash.recommended()

def verify_password(plain_password, hashed_password): return password_hash.verify(plain_password, hashed_password)

def get_password_hash(password): return password_hash.hash(password)

async def get_user(email):
    async with SessionLocal() as db:
        try:    
            result = await db.execute(select(md.User).where(md.User.email == email))
            user = result.scalar_one_or_none()
            return user
        except Exception as e:
            print(e)
            return None
        
async def authenticate_user(email: str, password: str):
    user = await get_user(email)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user_from_token(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,message="Could not validate credentials",headers={"WWW-Authenticate": "Bearer"},)
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("email")
        if email is None: raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    user = await get_user(email)
    if user is None:
        raise credentials_exception
    return user
        



