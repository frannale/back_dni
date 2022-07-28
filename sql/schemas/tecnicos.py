from typing import List

from pydantic import BaseModel, Field


class Tecnico(BaseModel):

    nombre: str = Field(
        ...,
        title="Nombre de tecnico",
        example="TALP",
        max_length=200
    )
    activo: str = Field(
        ...,
        title="Estado activo de la tecnico",
        example="True",
        max_length=200
    )


class TecnicoCreate(Tecnico):
    pass

class TecnicoUpdate(Tecnico):
    pass

class Tecnico(Tecnico):
    id: int = Field(..., title="ID de la Base de Datos", example=1)

    class Config:
        orm_mode = True

class GetTecnico(BaseModel):
    code: int = Field(200, const=True, title="Código de respuesta", example=200)
    tecnico: Tecnico

    class Config:
        orm_mode = True

class DeleteTecnico(BaseModel):
    code: int = Field(200, const=True, title="Código de respuesta", example=200)

class CrearTecnico(BaseModel):
    code: int = Field(201, const=True, title="Código de respuesta", example=200)
    tecnico: Tecnico

    class Config:
        orm_mode = True

class UpdateTecnico(BaseModel):
    code: int = Field(200, const=True, title="Código de respuesta", example=200)
    tecnico: Tecnico

    class Config:
        orm_mode = True


class GetTecnicos(BaseModel):
    code: int = Field(200, const=True, title="Código de respuesta", example=200)
    tecnicos: List[Tecnico]

    class Config:
        orm_mode = True

