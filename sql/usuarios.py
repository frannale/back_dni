from sqlalchemy.orm import Session
from . import models
from .schemas import usuarios as UsuarioSchema
from security import utils

import os

from dotenv import dotenv_values
BASEDIR = os.path.abspath(os.path.dirname("./"))
config = dotenv_values(os.path.join(BASEDIR, ".env"))

def get_usuarios(db: Session):
    
    usuarios = db.query(models.Usuario).order_by(models.Usuario.username).all()
    return usuarios

def get_usuario_by_id(db: Session, id_usuario: int):
    return db.query(models.Usuario).filter(models.Usuario.id == id_usuario).first()

def delete_usuario_by_id(db: Session, id_usuario: int):
    usuario = db.query(models.Usuario).filter(models.Usuario.id == id_usuario).first()
    db.delete(usuario)
    db.commit()
    return True

def check_admin(db: Session):
    usuario = db.query(models.Usuario).first()
    if usuario == None:
        nuevo_usuario = models.Usuario(
            username= "admin",
            mail= config["MAIL_USERNAME"],
            role= "True",
            password= utils.get_hash_password("admin") ,
            activo= "True"
        )
        db.add(nuevo_usuario)
        db.commit()
        db.refresh(nuevo_usuario)
    return True


def crear_usuario(db: Session, usuario: UsuarioSchema.UsuarioCreate):
    nuevo_usuario = models.Usuario(
        username= usuario.username,
        mail= usuario.mail,
        role= usuario.role,
        password= utils.get_hash_password(usuario.password) ,
        activo= usuario.activo
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario

def modificar_usuario(db: Session, id_usuario: int ,usuario: UsuarioSchema.UsuarioCreate):

    usuario_db = db.query(models.Usuario).filter(models.Usuario.id == id_usuario).first()
    usuario_db.username = usuario.username
    usuario_db.mail = usuario.mail
    usuario_db.activo = usuario.activo
    if(usuario.password != ""):
        usuario_db.password= utils.get_hash_password(usuario.password)
    
    # usuario_db.role = usuario.role
    db.commit()
    db.refresh(usuario_db)
    return usuario_db

def get_usuario_by_nombre(db: Session, username: str):
    usuario = (
        db.query(models.Usuario).filter(models.Usuario.username == username).filter(models.Usuario.activo == 'True').first()
    )
    if usuario != None:
        return UsuarioSchema.UsuarioEnDB(
            id=usuario.id, username=usuario.username, hashed_password=usuario.password, activo=usuario.activo,role=usuario.role
        )

def get_admin_by_nombre(db: Session, username: str):
    usuario = (
        db.query(models.Usuario).filter(models.Usuario.role == 'True').filter(models.Usuario.username == username).filter(models.Usuario.activo == 'True').first()
    )
    if usuario != None:
        return UsuarioSchema.UsuarioEnDB(
            id=usuario.id, username=usuario.username, hashed_password=usuario.password, activo=usuario.activo,role=usuario.role
        )
