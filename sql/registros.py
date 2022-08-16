import base64
from datetime import datetime
from sqlalchemy import null
from sqlalchemy.orm import Session
from . import models
from .schemas import registros as RegistroSchema

def get_registros(db: Session,params):
    
    especialista_id= params.get('especialista_id','0')
    jugador_id= params.get('jugador_id','0')
    fecha_inicio = params.get('fecha_inicio','0')
    fecha_fin = params.get('fecha_fin','0')

    query = db.query(models.Registro)
    if(especialista_id != '0'):
        query = query.filter(models.Registro.especialista_id == especialista_id)

    if(jugador_id != '0'):
        query = query.filter(models.Registro.jugador_id == jugador_id)
        
    if(fecha_inicio != '0' ):    
        query = query.filter(models.Registro.fecha >= fecha_inicio + 'T00:00:00')

    if(fecha_fin != '0' ):    
        query = query.filter(models.Registro.fecha <= fecha_fin + 'T23:59:59' )

    query = query.filter(models.Registro.fecha_eliminado.is_(None) )
    
    registros = query.order_by(models.Registro.fecha.desc()).all()

    return registros

def get_registro_by_id(db: Session, id_registro: int):
    return db.query(models.Registro).filter(models.Registro.id == id_registro).first()

def delete_registro_by_id(db: Session, id_registro: int):
    registro = db.query(models.Registro).filter(models.Registro.id == id_registro).first()
    registro.fecha_eliminado = datetime.now()
    
    db.commit()
    db.refresh(registro)
    return True


def crear_registro(db: Session, registro: RegistroSchema.RegistroCreate,especialista_id: int):
    nueva_registro = models.Registro(
        fecha= datetime.now(),
        observaciones=registro.observaciones,
        detalle= registro.detalle,
        aprobado= registro.aprobado,
        jugador_id= registro.jugador_id,
        especialista_id= especialista_id,

    )

    db.add(nueva_registro)
    db.commit()
    db.refresh(nueva_registro)
    return nueva_registro

def modificar_files(db: Session, id_registro: int ,files):

    registro_db = db.query(models.Registro).filter(models.Registro.id == id_registro).first()
    
    files_base64 = []
    # Recorre archivos y guarda en base64
    for file in files:
        files_base64.append(models.ImagenRegistro(file= base64.b64encode(file) ))

    registro_db.imagenes = files_base64

    db.commit()
    db.refresh(registro_db)
    return registro_db

