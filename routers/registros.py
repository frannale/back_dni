import os

from dotenv import dotenv_values

from typing import List

from fastapi import Depends, APIRouter, UploadFile
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse
from security import utils

from sqlalchemy.orm import Session

from sql import registros as RepoRegistro
from sql import especialista as RepoEspecialista
import sql.schemas.registros as RegistroSchema
import sql.schemas.responses as ResponseSchema
from sql.database import SessionLocal,engine

from fastapi_mail import FastMail, MessageSchema,ConnectionConfig

from fastapi import FastAPI, Request, File

from fastapi_pagination import paginate, Params

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

BASEDIR = os.path.abspath(os.path.dirname("./"))

config = dotenv_values(os.path.join(BASEDIR, ".env"))

# Conexion con DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get(
    "/registros",
    response_model=RegistroSchema.GetRegistros,
    description="Retorna todos los estudios",
    responses={500: {"model": ResponseSchema.MensajeError500}},
    tags=["Registros"],
)
async def Get_Registros(
    request: Request,
    db: Session = Depends(get_db),
    params: Params = Depends(), 
    token: str = Depends(oauth2_scheme)
):

    # CHEQUE TOKEN
    logged_user = utils.check_token_user(db,token)
    
    if logged_user == None:
        return JSONResponse(
            status_code=401,
            content={
                "code": 401,
                "error": "Acceso no autorizado",
            },
        )

    try:

        registro = paginate( 
            RepoRegistro.get_registros(db,request.query_params,logged_user),params
        )
        return {"code": 200, "registros": registro}
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "code": 500,
                "error": "Internal Server Error - Detalle: {0}".format(str(e)),
            },
        )


@router.get(
    "/registros/{id_registro}",
    response_model=RegistroSchema.GetRegistro,
    description="Retorna la información de un estudio",
    responses={
        500: {"model": ResponseSchema.MensajeError500},
        404: {"model": ResponseSchema.MensajeError404},
    },
    tags=["Registros"],
)
def Get_Registro(
    id_registro: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
):

    # CHEQUE TOKEN
    logged_user = utils.check_token_user(db,token)
    if logged_user == None:
        return JSONResponse(
            status_code=401,
            content={
                "code": 401,
                "error": "Acceso no autorizado",
            },
        )

    try:
        registro = RepoRegistro.get_registro_by_id(db, id_registro)
        if registro == None:
            return JSONResponse(
                status_code=404,
                content={
                    "code": 404,
                    "error": "Not Found - Ese ID no corresponde a un estudio registrado",
                },
            )
        else:
            return {
                "code": 200,
                "registro": registro
            }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "code": 500,
                "error": "Internal Server Error - Detalle: {0}".format(str(e)),
            },
        )

@router.delete(
    "/registros/{id_registro}",
    response_model=RegistroSchema.DeleteRegistro,
    description="Elimina el estudio",
    responses={
        500: {"model": ResponseSchema.MensajeError500},
        404: {"model": ResponseSchema.MensajeError404},
    },
    tags=["Registros"],
)
def Delete_Registro(
    id_registro: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
):

    # CHEQUE TOKEN
    logged_user = utils.check_token_user(db,token)
    if logged_user == None:
        return JSONResponse(
            status_code=401,
            content={
                "code": 401,
                "error": "Acceso no autorizado",
            },
        )

    try:
        registro = RepoRegistro.get_registro_by_id(db, id_registro)
        if registro == None:
            return JSONResponse(
                status_code=404,
                content={
                    "code": 404,
                    "error": "Not Found - Ese ID no corresponde a un estudio registrado",
                },
            )
        # CHECK REGISTRO LE PERTENECE O ES ADMIN
        if logged_user.role == "False" and registro.usuario_id != logged_user.id:
            return JSONResponse(
                status_code=401,
                content={
                    "code": 401,
                    "error": "El estudio no le pertenece",
                },
            )
        else:
            RepoRegistro.delete_registro_by_id(db, id_registro)
            return {
                "code": 200
            }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "code": 500,
                "error": "Internal Server Error - Detalle: {0}".format(str(e)),
            },
        )


@router.post(
    "/registros/crear",
    status_code=201,
    description="Crea un nuevo estudio",
    response_model=RegistroSchema.CrearRegistro,
    responses={
        500: {"model": ResponseSchema.MensajeError500},
        409: {"model": ResponseSchema.MensajeErrorGenerico},
    },
    tags=["Registros"],
)
def Crear_Nuevo_Registro(
    registro: RegistroSchema.RegistroCreate,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):

    # CHEQUE TOKEN
    logged_user = utils.check_token_user(db,token)
    if logged_user == None:
        return JSONResponse(
            status_code=401,
            content={
                "code": 401,
                "error": "Acceso no autorizado",
            },
        )

    try:
        especialista= RepoEspecialista.get_especialista_by_user_id(db,logged_user.id)
        registro = RepoRegistro.crear_registro(db, registro,especialista.id)
        return {
                "code": 201,
                "registro_id": registro.id,
                "mensaje": "Estudio creado exitosamente"
            }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "code": 500,
                "error": "Internal Server Error - Detalle: {0}".format(str(e)),
            },
        )

@router.post(
    "/registros/files/{id_registro}",
    status_code=201,
    description="Modifica los archivos de un registro",
    response_model=RegistroSchema.CrearRegistro,
    responses={
        500: {"model": ResponseSchema.MensajeError500},
        409: {"model": ResponseSchema.MensajeErrorGenerico},
    },
    tags=["Empresas"],
)
def Modificar_Files(
    id_registro: int,
    files: List[bytes] = File(...),
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):

    # CHEQUE TOKEN
    logged_user = utils.check_token_user(db,token)
    if logged_user == None:
        return JSONResponse(
            status_code=401,
            content={
                "code": 401,
                "error": "Acceso no autorizado",
            },
        )

    try:
        exist_registro = RepoRegistro.get_registro_by_id(db, id_registro)
        if exist_registro == None:
            return JSONResponse(
                status_code=404,
                content={
                    "code": 404,
                    "error": "No existe - Ese ID no corresponde a un estudio",
                },
            )
        else:
            RepoRegistro.modificar_files(db, id_registro,files)
            return {
                "code": 201,
                "registro_id": id_registro
            }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "code": 500,
                "error": "Internal Server Error - Detalle: {0}".format(str(e)),
            },
        )



