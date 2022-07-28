from typing import List, Optional, Dict
from sql.models import Usuario as UsuarioModel

from pydantic import BaseModel, Field

""" <--- SCHEMAS DE MENSAJES DE ERROR ---> """


class MensajeError500(BaseModel):
    code: int = Field(500, const=True, title="Código de respuesta", example=500)
    error: str = Field(
        None,
        title="Mensaje descriptivo del error",
        example="Internal Server Error - Detalle: [Detalle_Del_Error]",
    )


class MensajeError404(BaseModel):
    code: int = Field(404, const=True, title="Código de respuesta", example=404)
    error: str = Field(
        None,
        title="Mensaje descriptivo del error",
        example="Not Found - [Detalle del Error]",
    )


class MensajeErrorGenerico(BaseModel):
    code: int = Field(
        None, ge=400, le=409, title="Código de respuesta", example="[400 .. 409]"
    )
    error: str = Field(
        None,
        title="Mensaje descriptivo del error",
        example="Error: [Detalle del Error]",
    )
