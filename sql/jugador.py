from fastapi import File
from sqlalchemy.orm import Session
from . import models
from .schemas import jugador as JugadorSchema
from sqlalchemy import or_

import base64

def get_jugadores(db: Session, params):
    inactivos = params.get('inactivos', 'False')
    nombre = params.get('nombre', '')
    estado = params.get('estado', '0')  # Nuevo parámetro para filtrar por estudios aprobados

    # Iniciar la consulta base
    query = db.query(models.Jugador)

    # Filtrar jugadores activos o inactivos
    if inactivos == 'False':
        query = query.filter(models.Jugador.activo == 'True')

    # Filtrar por nombre (nombre completo)
    if nombre != '':
        query = query.filter((models.Jugador.nombre + " " + models.Jugador.apellido).like("%" + nombre + "%"))

    if estado == 'APTO':
        # Filtrar jugadores que tienen al menos un registro aprobado
        query = query.join(models.Registro).filter(models.Registro.aprobado == 'True')
    elif estado == 'REEVALUAR':
        # Filtrar jugadores que no tienen ningún registro aprobado
        subquery = db.query(models.Registro.jugador_id).filter(models.Registro.aprobado == 'True').distinct()
        query = query.filter(~models.Jugador.id.in_(subquery))

    # Ordenar por apellido y nombre
    jugadores = query.order_by(models.Jugador.apellido, models.Jugador.nombre).all()

    return jugadores

def get_jugador_by_id(db: Session, id_jugador: int):
    return db.query(models.Jugador).filter(models.Jugador.id == id_jugador).first()

def get_jugador_activo_by_dni(db: Session, dni_jugador: int):
    return db.query(models.Jugador).filter(models.Jugador.dni == dni_jugador).filter(models.Jugador.activo == "True").first()

def validate_alta_jugador_by_id(db: Session, id_jugador: int) -> bool:
    return db.query(models.Registro) \
        .filter(
            models.Registro.jugador_id == id_jugador,
            models.Registro.aprobado == "True"  # Verificar que el registro esté aprobado
        ) \
        .first() is not None

def delete_jugador_by_id(db: Session, id_jugador: int):
    jugador = db.query(models.Jugador).filter(models.Jugador.id == id_jugador).first()
    db.delete(jugador)
    db.commit()
    return True


def crear_jugador(db: Session, jugador: JugadorSchema.JugadorCreate):
    nueva_jugador = models.Jugador(
        dni= jugador.dni, 
        disciplina= jugador.disciplina,
        club= jugador.club,
        nombre= jugador.nombre,
        apellido= jugador.apellido,
        obra_social= jugador.obra_social,
        activo= jugador.activo,
        nombre_responsable= jugador.nombre_responsable,
        telefono_responsable= jugador.telefono_responsable,
        fecha_nacimiento= jugador.fecha_nacimiento,
        fecha_vencimiento_dni= jugador.fecha_vencimiento_dni,
        nro_tramite_dni= jugador.nro_tramite_dni,
        nro_pasaporte= jugador.nro_pasaporte,
        posicion= jugador.posicion,
        filename=""
    )
    db.add(nueva_jugador)
    db.commit()
    db.refresh(nueva_jugador)
    return nueva_jugador

def modificar_jugador(db: Session, id_jugador: int ,jugador: JugadorSchema.JugadorCreate):

    jugador_db = db.query(models.Jugador).filter(models.Jugador.id == id_jugador).first()
    jugador_db.dni = jugador.dni
    jugador_db.obra_social = jugador.obra_social
    jugador_db.disciplina = jugador.disciplina
    jugador_db.club = jugador.club
    jugador_db.nombre = jugador.nombre
    jugador_db.apellido = jugador.apellido
    jugador_db.nombre_responsable = jugador.nombre_responsable
    jugador_db.telefono_responsable = jugador.telefono_responsable
    jugador_db.fecha_nacimiento = jugador.fecha_nacimiento
    jugador_db.activo = jugador.activo
    jugador_db.fecha_vencimiento_dni = jugador.fecha_vencimiento_dni
    jugador_db.nro_tramite_dni = jugador.nro_tramite_dni
    jugador_db.nro_pasaporte = jugador.nro_pasaporte
    jugador_db.posicion = jugador.posicion
    
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