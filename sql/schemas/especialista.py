from typing import List
import datetime
from pydantic import BaseModel, Field
from fastapi_pagination import Page


class Especialista(BaseModel):

    username: str = Field(
        ...,
        title="Nombre descriptivo del usuario",
        example="Especialista_1",
        max_length=50
    )
    matricula: str = Field(
        ...,
        title="Matricula de especialista",
        example="12312",
        max_length=200
    )
    nombre: str = Field(
        ...,
        title="Nombre de especialista",
        example="Pedro",
        max_length=200
    )
    apellido: str = Field(
        ...,
        title="Apellido de especialista",
        example="Gomez",
        max_length=200
    )
    mail: str = Field(
        ...,
        title="Mail de especialista",
        example="Gomez@gmail.com",
        max_length=200
    )
    especialidad: str = Field(
        ...,
        title="Especialidad de especialista",
        example="Cardiologia",
        max_length=200
    )
    activo: str = Field(
        ...,
        title="Estado activo de la especialista",
        example="True",
        max_length=20
    )

class EspecialistaCreate(Especialista):
    password: str = Field(
        ...,
        title="Contraseña",
        example="12345678",
        max_length=100
    )

class EspecialistaUpdate(Especialista):
    password: str = Field(
        ...,
        title="Contraseña",
        example="12345678",
        max_length=100
    )

class UsuarioEspecialista(BaseModel):
    username: str = Field(
        ...,
        title="Nombre descriptivo del usuario",
        example="Especialista_1",
        max_length=50
    )
    activo: str = Field(
        ...,
        title="Estado activo de la especialista",
        example="True",
        max_length=20
    )
    mail: str = Field(
        ...,
        title="Mail de especialista",
        example="Gomez@gmail.com",
        max_length=200
    )
    class Config:
        orm_mode = True

class EspecialistaGet(BaseModel):
    id: int = Field(..., title="ID de la Base de Datos", example=1)

    matricula: str = Field(
        ...,
        title="Matricula de especialista",
        example="12312",
        max_length=200
    )
    nombre: str = Field(
        ...,
        title="Nombre de especialista",
        example="Pedro",
        max_length=200
    )
    apellido: str = Field(
        ...,
        title="Apellido de especialista",
        example="Gomez",
        max_length=200
    )

    especialidad: str = Field(
        ...,
        title="Especialidad de especialista",
        example="Cardiologia",
        max_length=200
    )
    usuario: UsuarioEspecialista
    class Config:
        orm_mode = True


class Especialista(Especialista):
    id: int = Field(..., title="ID de la Base de Datos", example=1)

    class Config:
        orm_mode = True

class GetEspecialista(BaseModel):
    code: int = Field(200, const=True, title="Código de respuesta", example=200)
    especialista: EspecialistaGet

    class Config:
        orm_mode = True

class DeleteEspecialista(BaseModel):
    code: int = Field(200, const=True, title="Código de respuesta", example=200)

class CrearEspecialista(BaseModel):
    code: int = Field(201, const=True, title="Código de respuesta", example=200)

    class Config:
        orm_mode = True

class UpdateEspecialista(BaseModel):
    code: int = Field(200, const=True, title="Código de respuesta", example=200)

    class Config:
        orm_mode = True

class GetEspecialistas(BaseModel):
    code: int = Field(200, const=True, title="Código de respuesta", example=200)
    especialistas: Page[EspecialistaGet]
    class Config:
        orm_mode = True

