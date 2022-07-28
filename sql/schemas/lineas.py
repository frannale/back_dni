from typing import List

from pydantic import BaseModel, Field

from back_dni.sql.schemas.jugador import Empresa as EmpresaSchema


class Linea(BaseModel):

    nombre: str = Field(
        ...,
        title="Nombre de linea",
        example="18",
        max_length=200
    )
    activo: str = Field(
        ...,
        title="Estado activo de la linea",
        example="True",
        max_length=200
    )
    empresa_id: str = Field(
        ...,
        title="ID Empresa de la linea",
        example="1",
        max_length=200
    )


class LineaCreate(Linea):
    pass

class LineaUpdate(Linea):
    pass

class Linea(Linea):
    id: int = Field(..., title="ID de la Base de Datos", example=1)
    empresa: EmpresaSchema

    class Config:
        orm_mode = True

class GetLinea(BaseModel):
    code: int = Field(200, const=True, title="Código de respuesta", example=200)
    linea: Linea

    class Config:
        orm_mode = True

class DeleteLinea(BaseModel):
    code: int = Field(200, const=True, title="Código de respuesta", example=200)

class CrearLinea(BaseModel):
    code: int = Field(201, const=True, title="Código de respuesta", example=200)

    class Config:
        orm_mode = True

class UpdateLinea(BaseModel):
    code: int = Field(200, const=True, title="Código de respuesta", example=200)
    linea: Linea

    class Config:
        orm_mode = True


class GetLineas(BaseModel):
    code: int = Field(200, const=True, title="Código de respuesta", example=200)
    lineas: List[Linea]

    class Config:
        orm_mode = True

