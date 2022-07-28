import datetime
from typing import List

from pydantic import BaseModel, Field

from sql.schemas.lineas import Linea as LineaSchema

from fastapi_pagination import Page


class ImagenRegistro(BaseModel):
    file: str

    class Config:
        orm_mode = True

class Tecnico(BaseModel):
    id: int
    nombre: str

    class Config:
        orm_mode = True


class Registro(BaseModel):

    interno: str = Field(
        ...,
        title="Numero de interno",
        example="True",
        max_length=200
    )
    patente: str = Field(
        ...,
        title="Patente",
        example="True",
        max_length=200
    )
    numero_serie_validador: str = Field(
        ...,
        title="Numero de serie validador",
        example="True",
        max_length=200
    )
    numero_serie_mk: str = Field(
        ...,
        title="Numero de serie mk",
        example="True",
        max_length=200
    )
    numero_serie_teclado: str = Field(
        ...,
        title="Numero de serie teclado",
        example="True",
        max_length=200
    )
    luz_alta: str = Field(
        ...,
        title="Estado luz alta -> True/False",
        example="True",
        max_length=200
    )
    luz_posicionamiento: str = Field(
        ...,
        title="Estado luz posicionamiento -> True/False",
        example="True",
        max_length=200
    )
    luz_giro: str = Field(
        ...,
        title="Estado luz giro -> True/False",
        example="True",
        max_length=200
    )
    luz_tablero: str = Field(
        ...,
        title="Estado luz tablero -> True/False",
        example="True",
        max_length=200
    )
    balizas: str = Field(
        ...,
        title="Estado balizas -> True/False",
        example="True",
        max_length=200
    )
    limpia_parabrisas: str = Field(
        ...,
        title="Estado limpia parabrisas -> True/False",
        example="True",
        max_length=200
    )
    bocina: str = Field(
        ...,
        title="Estado bocina -> True/False",
        example="True",
        max_length=200
    )
    encendido: str = Field(
        ...,
        title="Estado encendido -> True/False",
        example="True",
        max_length=200
    )
    espejos: str = Field(
        ...,
        title="Estado espejos -> True/False",
        example="True",
        max_length=200
    )
    parabrisas: str = Field(
        ...,
        title="Estado parabrisas -> True/False",
        example="True",
        max_length=200
    )
    fusilera: str = Field(
        ...,
        title="Estado fusilera -> True/False",
        example="True",
        max_length=200
    )
    fotos_ig_originales: str = Field(
        ...,
        title="Fotos de IG originales -> True/False",
        example="True",
        max_length=200
    )
    mk_orientacion_orificio: str = Field(
        ...,
        title="Corrrecto MK orientacion orificio -> True/False",
        example="True",
        max_length=200
    )
    mk_rebarbado_orificio: str = Field(
        ...,
        title="Corrrecto MK rebarbado orificio -> True/False",
        example="True",
        max_length=200
    )

    mk_antena_gps: str = Field(
        ...,
        title="Corrrecto MK antena GPS -> True/False",
        example="True",
        max_length=200
    )
    mk_criptado_rj45: str = Field(
        ...,
        title="Corrrecto MK criptado cable RJ45 -> True/False",
        example="True",
        max_length=200
    )
    consola_proteccion_cables: str = Field(
        ...,
        title="Corrrecto proteccion de cables de consola -> True/False",
        example="True",
        max_length=200
    )
    consola_soporte: str = Field(
        ...,
        title="Corrrecto soporte de consola -> True/False",
        example="True",
        max_length=200
    )
    consola_cableado_mk: str = Field(
        ...,
        title="Corrrecto cableado en consola -> True/False",
        example="True",
        max_length=200
    )
    consola_criptado_rj45: str = Field(
        ...,
        title="Corrrecto criptado RJ45 en consola -> True/False",
        example="True",
        max_length=200
    )
    general_colocacion_gps: str = Field(
        ...,
        title="Corrrecta colocacion de antena GPS -> True/False",
        example="True",
        max_length=200
    )
    general_tension_power: str = Field(
        ...,
        title="Corrrecto tension de encendido -> True/False",
        example="True",
        max_length=200
    )
    general_fotos_instalacion: str = Field(
        ...,
        title="Posee fotos instalacion -> True/False",
        example="True",
        max_length=200
    )
    general_configuracion: str = Field(
        ...,
        title="Corrrecta configuracion -> True/False",
        example="True",
        max_length=200
    )
    observaciones: str = Field(
        ...,
        title="Observaciones",
        example="Muchas cosas",
        max_length=1000
    )
    puntos_imagen: str = Field(
        ...,
        title="Areglo str de puntos imagen",
        example="[]",
        max_length=2000
    )
    responsable_empresa_nombre: str = Field(
        ...,
        title="Nombre responsable de empresa",
        example="Pedro",
        max_length=100
    )
    responsable_empresa_telefono: str = Field(
        ...,
        title="Telefono responsable de empresa",
        example="4765465",
        max_length=100
    )
    linea_id: str = Field(
        ...,
        title="1",
        example="4765465",
        max_length=100
    )




class RegistroCreate(Registro):

    id_tecnicos: str = Field(
        ...,
        title="ID tecnicos separados por coma",
        example="1,2",
        max_length=200
    )

class RegistroUpdate(Registro):
    
    id_tecnicos: str = Field(
        ...,
        title="ID tecnicos separados por coma",
        example="1,2",
        max_length=200
    )

class RegistroGet(Registro):
    id: int = Field(..., title="ID de la Base de Datos", example=1)
    fecha: datetime.datetime = Field(
        ...,
        title="Fecha de carga registro",
        example="2021-08-19",
    )
    linea: LineaSchema

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
    linea: LineaSchema
    imagenes: List[ImagenRegistro]
    tecnicos: List[Tecnico]

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

class ExportarRegistros(BaseModel):
    code: int = Field(200, const=True, title="Código de respuesta", example=200)

class UpdateRegistro(BaseModel):
    code: int = Field(200, const=True, title="Código de respuesta", example=200)
    registro_id: int

    class Config:
        orm_mode = True


class GetRegistros(BaseModel):
    code: int = Field(200, const=True, title="Código de respuesta", example=200)
    registros: Page[RegistroGet]

    class Config:
        orm_mode = True

 