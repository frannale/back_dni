import datetime
from typing import List

from pydantic import BaseModel, Field

from fastapi_pagination import Page

class ImagenRegistro(BaseModel):
    file: str

    class Config:
        orm_mode = True

class Especialista(BaseModel):
    id: int
    nombre: str
    apellido: str
    especialidad: str

    class Config:
        orm_mode = True

class Jugador(BaseModel):
    id: int
    nombre: str
    apellido: str
    dni: str

    class Config:
        orm_mode = True


class Registro(BaseModel):

    aprobado: str = Field(
        ...,
        title="True o False",
        example="True",
        max_length=10
    )
    detalle: str = Field(
        ...,
        title="Detalle del estudio",
        example="True",
        max_length=5000
    )
    observaciones: str = Field(
        title="Observaciones generales del estudio",
        example="Muchas cosas",
        max_length=1000
    )
    jugador_id: str = Field(
        ...,
        title="ID del jugador estudiado",
        example="1",
        max_length=100
    )

class RegistroCreate(Registro):

    pass

class RegistroGet(Registro):
    id: int = Field(..., title="ID de la Base de Datos", example=1)
    fecha: datetime.datetime = Field(
        ...,
        title="Fecha de carga registro",
        example="2021-08-19",
    )
    especialista: Especialista
    jugador: Jugador

    class Config:
        orm_mode = True

class RegistroGetOne(Registro):
    id: int = Field(..., title="ID de la Base de Datos", example=1)
    fecha: datetime.datetime = Field(
        ...,
        title="Fecha de carga registro",
        example="2021-08-19",
    )
    fecha_editado: datetime.datetime = Field(
        ...,
        title="Ultima fecha edicion registro",
        example="2021-08-19",
    )
    imagenes: List[ImagenRegistro]

    class Config:
        orm_mode = True

class GetRegistro(BaseModel):
    code: int = Field(200, const=True, title="Código de respuesta", example=200)
    registro: RegistroGetOne

    class Config:
        orm_mode = True

class DeleteRegistro(BaseModel):
    code: int = Field(200, const=True, title="Código de respuesta", example=200)

class CrearRegistro(BaseModel):
    code: int = Field(201, const=True, title="Código de respuesta", example=200)
    registro_id: int

    class Config:
        orm_mode = True


class GetRegistros(BaseModel):
    code: int = Field(200, const=True, title="Código de respuesta", example=200)
    registros: Page[RegistroGet]

    class Config:
        orm_mode = True

 