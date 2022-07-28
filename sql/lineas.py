from sqlalchemy.orm import Session
from . import models
from .schemas import lineas as LineaSchema

def get_lineas(db: Session,params):
    
    inactivos= params.get('inactivos','False')
    empresa_id= params.get('empresa_id','0')

    query = db.query(models.Linea)
    if inactivos == 'False' :
        query = query.filter(models.Linea.activo == 'True')

    if empresa_id != '0' :
        query = query.filter(models.Linea.empresa_id == empresa_id)

    lineas = query.order_by(models.Linea.nombre).all()

    return lineas

def get_linea_by_id(db: Session, id_linea: int):
    return db.query(models.Linea).filter(models.Linea.id == id_linea).first()

def delete_linea_by_id(db: Session, id_linea: int):
    linea = db.query(models.Linea).filter(models.Linea.id == id_linea).first()
    db.delete(linea)
    db.commit()
    return True


def crear_linea(db: Session, linea: LineaSchema.LineaCreate):
    nueva_linea = models.Linea(
        nombre= linea.nombre,
        activo= linea.activo,
        empresa_id=linea.empresa_id
    )
    db.add(nueva_linea)
    db.commit()
    db.refresh(nueva_linea)
    return nueva_linea

def modificar_linea(db: Session, id_linea: int ,linea: LineaSchema.LineaCreate):

    linea_db = db.query(models.Linea).filter(models.Linea.id == id_linea).first()
    linea_db.nombre = linea.nombre
    linea_db.activo = linea.activo
    linea_db.empresa_id = linea.empresa_id
    db.commit()
    db.refresh(linea_db)
    return linea_db

def get_linea_by_nombre(db: Session, nombre: str,empresa_id):

    query = db.query(models.Linea)
    query = query.filter(models.Linea.nombre == nombre)
    query = query.filter(models.Linea.empresa_id == empresa_id)
    linea = query.first()

    print(linea)
    return linea