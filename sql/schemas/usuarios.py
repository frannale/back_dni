from typing import List, Optional, Dict
from xmlrpc.client import Boolean

from pydantic import BaseModel, Field


class UsuarioBase(BaseModel):

    username: str = Field(
        ...,
        title="Nombre descriptivo del usuario",
        example="Administrador",
        max_length=50
    )
    mail: str = Field(
        ...,
        title="Email del usuario",
        example="usuario@gmail.com",
        max_length=100,
    )
    activo: str = Field(
        ...,
        title="Estado del usuario",
        example="True",
        max_length=10
    )
    role: str = Field(
        ...,
        title="Rol del usuario",
        example="admin",
        max_length=10,
    )
    password: str = Field(
        ...,
        title="Contraseña",
        example="12345678",
        max_length=100
    )

class UsuarioBaseGet(BaseModel):
    
    class Config:
        underscore_attrs_are_private = True

    username: str = Field(
        ...,
        title="Nombre descriptivo del usuario",
        example="Administrador",
        max_length=50
    )
    mail: str = Field(
        ...,
        title="Email del usuario",
        example="usuario@gmail.com",
        max_length=100,
    )
    activo: str = Field(
        ...,
        title="Estado del usuario",
        example="True",
        max_length=10
    )
    role: str = Field(
        ...,
        title="Rol del usuario",
        example="admin",
        max_length=10,
    )
    _password: str = Field(
        ...,
        title="Contraseña",
        example="12345678",
        max_length=100
    )



class UsuarioCreate(UsuarioBase):
    pass

class UsuarioUpdate(UsuarioBase):
    pass


class Usuario(UsuarioBaseGet):
    id: int = Field(..., title="ID de la Base de Datos", example=1)

    class Config:
        orm_mode = True

class GetUsuario(BaseModel):
    code: int = Field(200, const=True, title="Código de respuesta", example=200)
    usuario: Usuario

    class Config:
        orm_mode = True

class UpdateUsuario(BaseModel):
    code: int = Field(200, const=True, title="Código de respuesta", example=200)
    usuario: Usuario

    class Config:
        orm_mode = True

class DeleteUsuario(BaseModel):
    code: int = Field(200, const=True, title="Código de respuesta", example=200)



""" <--- SCHEMAS DE RESPUESTA ---> """


class GetUsuarios(BaseModel):
    code: int = Field(200, const=True, title="Código de respuesta", example=200)
    usuarios: List[Usuario]

    class Config:
        orm_mode = True


class CrearUsuario(BaseModel):
    code: int = Field(201, const=True, title="Código de respuesta", example=201)
    mensaje: str = "Usuario creado exitosamente"
    usuario: Usuario


""" <--- SCHEMAS DE USUARIO Y SEGURIDAD ---> """


class Token(BaseModel):
    access_token: str = Field(
        ...,
        title="JWT Token válido",
        example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9[...]",
    )
    token_type: str = Field(..., title="El tipo de Token", example="Bearer")


class TokenData(BaseModel):
    username: Optional[str] = None


class Usuario(BaseModel):
    id: int
    username: str
    activo: bool = Field(
        ...,
        title="Booleando que indica si el usuario está activo o no",
        example=True
    )
    role: str = Field(
        ...,
        title="Rol del usuario",
        example="admin",
        max_length=10,
    )


class UsuarioEnDB(Usuario):
    hashed_password: str
