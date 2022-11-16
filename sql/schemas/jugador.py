from typing import List
import datetime
from pydantic import BaseModel, Field
from fastapi_pagination import Page


class Jugador(BaseModel):

    dni: str = Field(
        ...,
        title="Dni de jugador",
        example="Pedro",
        max_length=200
    )
    disciplina: str = Field(
        ...,
        title="Disciplina del jugador",
        example="Futbol",
        max_length=200
    )
    club: str = Field(
        ...,
        title="Club del jugador",
        example="Futbol",
        max_length=200
    )
    nombre: str = Field(
        ...,
        title="Nombre de jugador",
        example="Pedro",
        max_length=200
    )
    apellido: str = Field(
        ...,
        title="Apellido de jugador",
        example="Gomez",
        max_length=200
    )
    nombre_responsable: str = Field(
        ...,
        title="Nombre y apellido del responsable",
        example="Gomez",
        max_length=200
    )
    telefono_responsable: str = Field(
        ...,
        title="Telefono del responsable",
        example="Gomez",
        max_length=200
    )
    fecha_nacimiento: datetime.date = Field(
        ...,
        title="Telefono del responsable",
        example="2021-08-19",
    )
    activo: str = Field(
        ...,
        title="Estado activo de la jugador",
        example="True",
        max_length=20
    )
    obra_social: str = Field(
        ...,
        title="Estado activo de la jugador",
        example="True",
        max_length=20
    )

class JugadorCreate(Jugador):
    pass

class JugadorUpdate(Jugador):
    pass

class JugadorGet(Jugador):
    id: int = Field(..., title="ID de la Base de Datos", example=1)
    filename: str
    class Config:
        orm_mode = True


class Jugador(Jugador):
    id: int = Field(..., title="ID de la Base de Datos", example=1)

    class Config:
        orm_mode = True

class GetJugador(BaseModel):
    code: int = Field(200, const=True, title="Código de respuesta", example=200)
    jugador: JugadorGet

    class Config:
        orm_mode = True

class JugadorValidado(BaseModel):

    nombre: str = Field(
        ...,
        title="Nombre de jugador",
        example="Pedro",
        max_length=200
    )
    apellido: str = Field(
        ...,
        title="Apellido de jugador",
        example="Gomez",
        max_length=200
    )
    dni: str = Field(
        ...,
        title="DNI de jugador",
        example="Gomez",
        max_length=200
    )
    filename: str

    class Config:
        orm_mode = True

class GetJugadorValidado(BaseModel):
    code: int = Field(200, const=True, title="Código de respuesta", example=200)
    jugador: JugadorValidado
    aprobado: str

    class Config:
        orm_mode = True

class DeleteJugador(BaseModel):
    code: int = Field(200, const=True, title="Código de respuesta", example=200)

class CrearJugador(BaseModel):
    code: int = Field(201, const=True, title="Código de respuesta", example=200)
    jugador: Jugador

    class Config:
        orm_mode = True

class UpdateJugador(BaseModel):
    code: int = Field(200, const=True, title="Código de respuesta", example=200)
    jugador: Jugador

    class Config:
        orm_mode = True


class GetJugadores(BaseModel):
    code: int = Field(200, const=True, title="Código de respuesta", example=200)
    jugadores: Page[Jugador]

    class Config:
        orm_mode = True

