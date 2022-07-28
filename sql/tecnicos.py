from sqlalchemy.orm import Session
from . import models
from .schemas import tecnicos as TecnicoSchema

def get_tecnicos(db: Session,params):
    
    inactivos= params.get('inactivos','False')

    query = db.query(models.Tecnico)
    if inactivos == 'False' :
        query = query.filter(models.Tecnico.activo == 'True')

    tecnicos = query.order_by(models.Tecnico.nombre).all()

    return tecnicos

def get_tecnico_by_id(db: Session, id_tecnico: int):
    return db.query(models.Tecnico).filter(models.Tecnico.id == id_tecnico).first()

def delete_tecnico_by_id(db: Session, id_tecnico: int):
    tecnico = db.query(models.Tecnico).filter(models.Tecnico.id == id_tecnico).first()
    db.delete(tecnico)
    db.commit()
    return True


def crear_tecnico(db: Session, tecnico: TecnicoSchema.TecnicoCreate):
    nueva_tecnico = models.Tecnico(
        nombre= tecnico.nombre,
        activo= tecnico.activo
    )
    db.add(nueva_tecnico)
    db.commit()
    db.refresh(nueva_tecnico)
    return nueva_tecnico

def modificar_tecnico(db: Session, id_tecnico: int ,tecnico: TecnicoSchema.TecnicoCreate):

    tecnico_db = db.query(models.Tecnico).filter(models.Tecnico.id == id_tecnico).first()
    tecnico_db.nombre = tecnico.nombre
    tecnico_db.activo = tecnico.activo
    db.commit()
    db.refresh(tecnico_db)
    return tecnico_db

def get_tecnico_by_nombre(db, nombre: str):
    tecnico = (
        db.query(models.Tecnico).filter(models.Tecnico.nombre == nombre).first()
    )
    return tecnico