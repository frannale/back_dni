import base64
from datetime import datetime
from sqlalchemy import null
from sqlalchemy.orm import Session
from . import models
from .schemas import registros as RegistroSchema

def get_registros(db: Session,params):
    
    empresa_id= params.get('empresa_id','0')
    linea_id= params.get('linea_id','0')
    usuario_id= params.get('usuario_id','0')
    fecha_inicio = params.get('fecha_inicio','0')
    fecha_fin = params.get('fecha_fin','0')
    
    query = db.query(models.Registro).join(models.Registro.linea,models.Linea.empresa)
    if(empresa_id != '0'):
        query = query.filter(models.Linea.empresa_id == empresa_id)

    if(linea_id != '0'):
        query = query.filter(models.Linea.id == linea_id)

    if(usuario_id != '0'):
        query = query.filter(models.Registro.usuario_id == usuario_id)
        
    if(fecha_inicio != '0' ):    
        query = query.filter(models.Registro.fecha >= fecha_inicio + 'T00:00:00')

    if(fecha_fin != '0' ):    
        query = query.filter(models.Registro.fecha <= fecha_fin + 'T23:59:59' )

    query = query.filter(models.Registro.fecha_eliminado.is_(None) )
    
    registros = query.order_by(models.Registro.fecha.desc()).all()

    return registros

def get_registro_by_id(db: Session, id_registro: int):
    return db.query(models.Registro).filter(models.Registro.id == id_registro).first()

def validate_patente(db: Session, patente: str):
    return db.query(models.Registro).filter(models.Registro.patente == patente).first()

def validate_numero_serie_validador(db: Session, numero_serie: str):
    return db.query(models.Registro).filter(models.Registro.numero_serie_validador == numero_serie).first()

def validate_numero_serie_mk(db: Session, numero_serie: str):
    return db.query(models.Registro).filter(models.Registro.numero_serie_mk == numero_serie).first()

def validate_numero_serie_teclado(db: Session, numero_serie: str):
    return db.query(models.Registro).filter(models.Registro.numero_serie_teclado == numero_serie).first()

def delete_registro_by_id(db: Session, id_registro: int):
    registro = db.query(models.Registro).filter(models.Registro.id == id_registro).first()
    registro.fecha_eliminado = datetime.now()
    
    db.commit()
    db.refresh(registro)
    return True


def crear_registro(db: Session, registro: RegistroSchema.RegistroCreate,user_id: int):
    nueva_registro = models.Registro(
        fecha= datetime.now(),
        fecha_editado= datetime.now(),
        interno= registro.interno,
        patente= registro.patente,
        numero_serie_validador= registro.numero_serie_validador,
        numero_serie_mk= registro.numero_serie_mk,
        numero_serie_teclado= registro.numero_serie_teclado,
        luz_alta= registro.luz_alta,
        luz_posicionamiento= registro.luz_posicionamiento,
        luz_giro= registro.luz_giro,
        luz_tablero= registro.luz_tablero,
        balizas= registro.balizas,
        limpia_parabrisas= registro.limpia_parabrisas,
        bocina= registro.bocina,
        encendido= registro.encendido,
        espejos= registro.espejos,
        parabrisas= registro.parabrisas,
        fusilera= registro.fusilera,
        fotos_ig_originales= registro.fotos_ig_originales,
        mk_orientacion_orificio= registro.mk_orientacion_orificio,
        mk_rebarbado_orificio= registro.mk_rebarbado_orificio,
        mk_antena_gps= registro.mk_antena_gps,
        mk_criptado_rj45= registro.mk_criptado_rj45,
        consola_proteccion_cables= registro.consola_proteccion_cables,
        consola_soporte= registro.consola_soporte,
        consola_cableado_mk= registro.consola_cableado_mk,
        consola_criptado_rj45= registro.consola_criptado_rj45,
        general_colocacion_gps= registro.general_colocacion_gps,
        general_tension_power= registro.general_tension_power,
        general_fotos_instalacion= registro.general_fotos_instalacion,
        general_configuracion= registro.general_configuracion,
        observaciones= registro.observaciones,
        puntos_imagen= registro.puntos_imagen,
        linea_id=registro.linea_id,
        usuario_id= user_id,
        responsable_empresa_nombre= registro.responsable_empresa_nombre,
        responsable_empresa_telefono= registro.responsable_empresa_telefono
    )

    # RELACIONA TECNICOS
    tecnicos = []
    if registro.id_tecnicos != '':
        for id_tecnico in registro.id_tecnicos.split(','):
            tecnicos.append(db.query(models.Tecnico).filter(models.Tecnico.id == id_tecnico).first())
    nueva_registro.tecnicos = tecnicos

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

def modificar_registro(db: Session, id_registro: int ,registro: RegistroSchema.RegistroCreate):

    registro_db = db.query(models.Registro).filter(models.Registro.id == id_registro).first()
    # registro_db.interno= registro.interno,
    # registro_db.patente= registro.patente,
    # registro_db.numero_serie_= registro.numero_serie,
    registro_db.fecha_editado= datetime.now(),
    registro_db.luz_alta= registro.luz_alta,
    registro_db.luz_posicionamiento= registro.luz_posicionamiento,
    registro_db.luz_giro= registro.luz_giro,
    registro_db.luz_tablero= registro.luz_tablero,
    registro_db.balizas= registro.balizas,
    registro_db.limpia_parabrisas= registro.limpia_parabrisas,
    registro_db.bocina= registro.bocina,
    registro_db.encendido= registro.encendido,
    registro_db.espejos= registro.espejos,
    registro_db.parabrisas= registro.parabrisas,
    registro_db.fusilera= registro.fusilera,
    registro_db.fotos_ig_originales= registro.fotos_ig_originales,
    registro_db.mk_orientacion_orificio= registro.mk_orientacion_orificio,
    registro_db.mk_rebarbado_orificio= registro.mk_rebarbado_orificio,
    registro_db.mk_antena_gps= registro.mk_antena_gps,
    registro_db.mk_criptado_rj45= registro.mk_criptado_rj45,
    registro_db.consola_proteccion_cables= registro.consola_proteccion_cables,
    registro_db.consola_soporte= registro.consola_soporte,
    registro_db.consola_cableado_mk= registro.consola_cableado_mk,
    registro_db.consola_criptado_rj45= registro.consola_criptado_rj45,
    registro_db.general_colocacion_gps= registro.general_colocacion_gps,
    registro_db.general_tension_power= registro.general_tension_power,
    registro_db.general_fotos_instalacion= registro.general_fotos_instalacion,
    registro_db.general_configuracion= registro.general_configuracion,
    registro_db.observaciones= registro.observaciones,
    registro_db.puntos_imagen= registro.puntos_imagen,
    # registro_db.linea_id=registro.linea_id,
    registro_db.responsable_empresa_nombre= registro.responsable_empresa_nombre,
    registro_db.responsable_empresa_telefono= registro.responsable_empresa_telefono
    db.commit()
    db.refresh(registro_db)
    return registro_db
