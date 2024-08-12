from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Table,Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import null

from .database import Base

class Usuario(Base):
    __tablename__ = "usuario"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(20), unique=True)
    password = Column(String(800))
    role = Column(String(20))
    mail = Column(String(80))
    activo = Column(String(20), nullable=False)

class Especialista(Base):
    __tablename__ = "especialista"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(30), nullable=False)
    apellido = Column(String(30), nullable=False)
    matricula = Column(String(30), nullable=False)
    especialidad = Column(String(30), nullable=False)
    registros = relationship( "Registro", back_populates="especialista")
    usuario_id = Column(Integer, ForeignKey('usuario.id'))
    usuario = relationship("Usuario") 

class Jugador(Base):
    __tablename__ = "jugador"

    id = Column(Integer, primary_key=True, index=True)
    disciplina = Column(String(30), nullable=False)
    club = Column(String(30), nullable=False)
    nombre = Column(String(30), nullable=False)
    apellido = Column(String(30), nullable=False)
    dni = Column(String(20), nullable=False)
    nombre_responsable = Column(String(30), nullable=False)
    telefono_responsable = Column(String(30), nullable=False)
    fecha_nacimiento = Column(DateTime)
    fecha_vencimiento_dni = Column(DateTime)
    filename = Column(Text(4294000000))
    activo = Column(String(20), nullable=False)
    nro_pasaporte = Column(String(40), nullable=False)
    nro_tramite_dni = Column(String(40), nullable=False)
    posicion = Column(String(40), nullable=False)
    obra_social = Column(String(40), nullable=False)
    registros = relationship("Registro", back_populates="jugador")

registro_imagen_table = Table('mm_registro_imagen', Base.metadata,
    Column("id", Integer, primary_key=True),
    Column('registro_id', ForeignKey('registro.id')),
    Column('imagen_id', ForeignKey('imagen_registro.id'))
) 

class Registro(Base):
    __tablename__ = "registro"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(DateTime)
    fecha_editado = Column(DateTime)
    fecha_eliminado = Column(DateTime)
    aprobado = Column(String(20))
    observaciones = Column(Text(1000))
    detalle = Column(Text(10000))
    jugador_id = Column(Integer, ForeignKey('jugador.id'))
    jugador = relationship("Jugador", back_populates="registros")
    especialista_id = Column(Integer, ForeignKey('especialista.id'))
    especialista = relationship("Especialista", back_populates="registros")
    imagenes = relationship("ImagenRegistro", secondary=registro_imagen_table, back_populates="registros")

class ImagenRegistro(Base):
    __tablename__ = "imagen_registro"

    id = Column(Integer, primary_key=True, index=True)
    file = Column(Text(4294000000), nullable=False)
    registros = relationship("Registro",secondary=registro_imagen_table, back_populates="imagenes")
