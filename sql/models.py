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
    nombre = Column(String(30), nullable=False)
    apellido = Column(String(30), nullable=False)
    dni = Column(String(20), nullable=False)
    nombre_responsable = Column(String(30), nullable=False)
    telefono_responsable = Column(String(30), nullable=False)
    fecha_nacimiento = Column(DateTime)
    filename = Column(Text(4294000000))
    activo = Column(String(20), nullable=False)
    registros = relationship("Registro", back_populates="jugador")

class Registro(Base):
    __tablename__ = "registro"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(DateTime)
    fecha_editado = Column(DateTime)
    fecha_eliminado = Column(DateTime)
    aprobado = Column(String(20))
    jugador_id = Column(Integer, ForeignKey('jugador.id'))
    jugador = relationship("Jugador", back_populates="registros")
    especialista_id = Column(Integer, ForeignKey('especialista.id'))
    especialista = relationship("Especialista", back_populates="registros")
