from sqlalchemy.orm import Session
from . import models
from .schemas import especialista as EspecialistaSchema
from sqlalchemy import or_
from security import utils

def get_especialistas(db: Session,params):
    
    inactivos= params.get('inactivos','False')
    nombre= params.get('nombre','')

    query = db.query(models.Especialista)
    if inactivos == 'False' :
        query = query.filter(models.Especialista.usuario.activo == 'True')
    if nombre != '' :
        query = query.filter((models.Especialista.nombre + " " + models.Especialista.apellido).like("%" + nombre + "%"))

    especialistas = query.order_by(models.Especialista.nombre).all()

    return especialistas

def get_especialista_by_id(db: Session, id_especialista: int):
    return db.query(models.Especialista).filter(models.Especialista.id == id_especialista).first()

def delete_especialista_by_id(db: Session, id_especialista: int):
    especialista = db.query(models.Especialista).filter(models.Especialista.id == id_especialista).first()
    id_usuario = especialista.usuario.id
    db.delete(especialista)
    # delete user
    usuario = db.query(models.Usuario).filter(models.Usuario.id == id_usuario).first()
    db.delete(usuario)
    db.commit()
    db.commit()
    return True


def crear_especialista(db: Session, especialista: EspecialistaSchema.EspecialistaCreate):
    nuevo_usuario = models.Usuario(
        username= especialista.username,
        mail= especialista.mail,
        role= especialista.especialidad,
        password= utils.get_hash_password(especialista.password) ,
        activo= especialista.activo
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    nuevo_especialista = models.Especialista(
        matricula= especialista.matricula, 
        nombre= especialista.nombre,
        apellido= especialista.apellido,
        especialidad= especialista.especialidad,
        usuario_id=nuevo_usuario.id

    )
    db.add(nuevo_especialista)
    db.commit()
    db.refresh(nuevo_especialista)
    return nuevo_especialista

def modificar_especialista(db: Session, id_especialista: int ,especialista: EspecialistaSchema.EspecialistaCreate):

    especialista_db = db.query(models.Especialista).filter(models.Especialista.id == id_especialista).first()
    especialista_db.nombre = especialista.nombre
    especialista_db.apellido = especialista.apellido
    especialista_db.matricula = especialista.matricula
    especialista_db.especialista = especialista.especialista
    # USER
    usuario_db = db.query(models.Usuario).filter(models.Usuario.id == especialista.usuario.id).first()
    # usuario_db.username = especialista.username
    usuario_db.mail = especialista.mail
    usuario_db.activo = especialista.activo
    if(especialista.password != ""):
        usuario_db.password= utils.get_hash_password(especialista.password)
    
    db.commit()
    db.refresh(usuario_db)
    db.refresh(especialista_db)
    return especialista_db

def get_especialista_by_nombre(db, nombre: str):
    especialista = (
        db.query(models.Especialista).filter(models.Especialista.nombre == nombre).first()
    )
    return especialista

def get_especialista_by_matricula(db, matricula: str):
    especialista = (
        db.query(models.Especialista).filter(models.Especialista.matricula == matricula).first()
    )
    return especialista