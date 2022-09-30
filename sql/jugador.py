from fastapi import File
from sqlalchemy.orm import Session
from . import models
from .schemas import jugador as JugadorSchema
from sqlalchemy import or_

import base64

def get_jugadores(db: Session,params):
    
    inactivos= params.get('inactivos','False')
    nombre= params.get('nombre','')

    query = db.query(models.Jugador)
    if inactivos == 'False' :
        query = query.filter(models.Jugador.activo == 'True')
    if nombre != '' :
        query = query.filter((models.Jugador.nombre + " " + models.Jugador.apellido).like("%" + nombre + "%"))

    jugadores = query.order_by(models.Jugador.apellido,models.Jugador.nombre).all()

    return jugadores

def get_jugador_by_id(db: Session, id_jugador: int):
    return db.query(models.Jugador).filter(models.Jugador.id == id_jugador).first()

def get_jugador_activo_by_dni(db: Session, dni_jugador: int):
    return db.query(models.Jugador).filter(models.Jugador.dni == dni_jugador).filter(models.Jugador.activo == "True").first()

def validate_alta_jugador_by_id(db: Session, id_jugador: int):
    registro = db.query(models.Registro).filter(models.Registro.jugador_id == id_jugador).join(models.Especialista).filter(models.Especialista.especialidad == "CARDIOLOGIA").first()
    if registro == None:
        return False
    return True

def delete_jugador_by_id(db: Session, id_jugador: int):
    jugador = db.query(models.Jugador).filter(models.Jugador.id == id_jugador).first()
    db.delete(jugador)
    db.commit()
    return True


def crear_jugador(db: Session, jugador: JugadorSchema.JugadorCreate):
    nueva_jugador = models.Jugador(
        dni= jugador.dni, 
        disciplina= jugador.disciplina,
        nombre= jugador.nombre,
        apellido= jugador.apellido,
        activo= jugador.activo,
        nombre_responsable= jugador.nombre_responsable,
        telefono_responsable= jugador.telefono_responsable,
        fecha_nacimiento= jugador.fecha_nacimiento,
        filename=""
    )
    db.add(nueva_jugador)
    db.commit()
    db.refresh(nueva_jugador)
    return nueva_jugador

def modificar_jugador(db: Session, id_jugador: int ,jugador: JugadorSchema.JugadorCreate):

    jugador_db = db.query(models.Jugador).filter(models.Jugador.id == id_jugador).first()
    jugador_db.disciplina = jugador.disciplina
    jugador_db.nombre = jugador.nombre
    jugador_db.apellido = jugador.apellido
    jugador_db.nombre_responsable = jugador.nombre_responsable
    jugador_db.telefono_responsable = jugador.telefono_responsable
    jugador_db.fecha_nacimiento = jugador.fecha_nacimiento
    jugador_db.activo = jugador.activo
    
    db.commit()
    db.refresh(jugador_db)
    return jugador_db

def modificar_foto(db: Session, id_jugador: int ,file):

    jugador = db.query(models.Jugador).filter(models.Jugador.id == id_jugador).first()
    jugador.filename = base64.b64encode(file)
    db.commit()
    db.refresh(jugador)
    return jugador


def get_jugador_by_nombre(db, nombre: str):
    jugador = (
        db.query(models.Jugador).filter(models.Jugador.nombre == nombre).first()
    )
    return jugador

def get_jugador_by_dni(db, dni: str):
    jugador = (
        db.query(models.Jugador).filter(models.Jugador.dni == dni).first()
    )
    return jugador