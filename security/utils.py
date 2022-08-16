import os
from fastapi import Depends, FastAPI, HTTPException, status,APIRouter
from dotenv import dotenv_values

from passlib.context import CryptContext

from datetime import datetime, timedelta
import time

from fastapi.security import OAuth2PasswordBearer

from jose import JWTError, jwt

from sqlalchemy.orm import Session

from typing import Optional

from sql import usuarios
import sql.schemas.usuarios as UsuarioSchema

BASEDIR = os.path.abspath(os.path.dirname("./"))

config = dotenv_values(os.path.join(BASEDIR, ".env"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

from sql.database import SessionLocal

# Conexion con DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def verificar_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_hash_password(password):
    return pwd_context.hash(password)


def check_token_user(db,token: str):
    try:
        payload = jwt.decode(
            token, config["SECRET_KEY"], algorithms=[config["ALGORITHM"]]
        )
        if(time.time() < payload["exp"]):
            user = usuarios.get_usuario_by_nombre(db, payload["sub"])
            return user
        return None
    except Exception as e:
        return None

def check_token_admin(db,token: str):
    try:
        payload = jwt.decode(
            token, config["SECRET_KEY"], algorithms=[config["ALGORITHM"]]
        )
        if(time.time() < payload["exp"]):
            user = usuarios.get_admin_by_nombre(db, payload["sub"])
            return user
        return None
    except Exception as e:
        return None


def autentificar_usuario(db, username: str, password: str):

    user = usuarios.get_usuario_by_nombre(db, username)
    if not user:
        return False
    if not verificar_password(password, user.hashed_password):
        return False
    return user


def crear_token_acceso(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, config["SECRET_KEY"], algorithm=config["ALGORITHM"]
    )
    return encoded_jwt
