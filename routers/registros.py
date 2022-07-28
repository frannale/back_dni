import os

from dotenv import dotenv_values

from typing import List

from fastapi import Depends, APIRouter, UploadFile
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse
from security import utils

from sqlalchemy.orm import Session

from sql import registros as RepoRegistro
from back_dni.sql import jugador as RepoEmpresa
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
    description="Retorna todos las registros",
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
            RepoRegistro.get_registros(db,request.query_params),params
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
    description="Retorna la información de un registro",
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
                    "error": "Not Found - Ese ID no corresponde a un registro registrado",
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
    description="Elimina el registro",
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
                    "error": "Not Found - Ese ID no corresponde a un registro registrado",
                },
            )
        # CHECK REGISTRO LE PERTENECE O ES ADMIN
        if logged_user.role == "False" and registro.usuario_id != logged_user.id:
            return JSONResponse(
                status_code=401,
                content={
                    "code": 401,
                    "error": "El registro no le pertenece",
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

@router.put(
    "/registros/{id_registro}",
    response_model=RegistroSchema.UpdateRegistro,
    description="Modifica un registro",
    responses={
        500: {"model": ResponseSchema.MensajeError500},
        404: {"model": ResponseSchema.MensajeError404},
    },
    tags=["Registros"],
)
def Put_Registro(
    registro: RegistroSchema.RegistroUpdate,
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
       
        exist_registro = RepoRegistro.get_registro_by_id(db, id_registro)
        if exist_registro == None:
            return JSONResponse(
                status_code=404,
                content={
                    "code": 404,
                    "error": "Not Found - Ese ID no corresponde a un registro registrado",
                },
            )
        # CHECK REGISTRO LE PERTENECE O ES ADMIN
        if logged_user.role == "False" and exist_registro.usuario_id != logged_user.id:
            return JSONResponse(
                status_code=401,
                content={
                    "code": 401,
                    "error": "El registro no le pertenece",
                },
            )
        else:

            updated_user = RepoRegistro.modificar_registro(db, id_registro,registro)
            return {
                "code": 200,
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


@router.post(
    "/registros/crear",
    status_code=201,
    description="Crea un nuevo registro",
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
        # Validaciones
        exist = RepoRegistro.validate_patente(db,registro.patente)
        if exist != None:
            return JSONResponse(
                status_code=404,
                content={
                    "code": 404,
                    "error": "Duplicado - Ya existe un registro con esa patente"
                },
            )
        exist = RepoRegistro.validate_numero_serie_validador(db,registro.numero_serie_validador)
        if exist != None:
            return JSONResponse(
                status_code=404,
                content={
                    "code": 404,
                    "error": " Duplicado - Ya existe un registro con ese numero de serie de validador"

                },
            )
        exist = RepoRegistro.validate_numero_serie_mk(db,registro.numero_serie_mk)
        if exist != None:
            return JSONResponse(
                status_code=404,
                content={
                    "code": 404,
                    "error": " Duplicado - Ya existe un registro con ese numero de serie de mounting kit"

                },
            )
        exist = RepoRegistro.validate_numero_serie_teclado(db,registro.numero_serie_teclado) 
        if exist != None:
            return JSONResponse(
                status_code=404,
                content={
                    "code": 404,
                    "error": " Duplicado - Ya existe un registro con ese numero de serie de teclado"

                },
            )

        registro = RepoRegistro.crear_registro(db, registro,logged_user.id)
        return {
                "code": 201,
                "registro_id": registro.id,
                "mensaje": "Registro creado exitosamente"
            }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "code": 500,
                "error": "Internal Server Error - Detalle: {0}".format(str(e)),
            },
        )


# ENVIO DE MAIL PARA CONTACTO
conf_mail = ConnectionConfig(
    MAIL_USERNAME = config["MAIL_USERNAME"],
    MAIL_PASSWORD = config["MAIL_PASSWORD"],
    MAIL_FROM = config["MAIL_USERNAME"],
    MAIL_PORT = config["MAIL_PORT"],
    MAIL_SERVER = config["MAIL_SERVER"],
    MAIL_TLS = True,
    MAIL_SSL = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
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
                    "error": "No existe - Ese ID no corresponde a un registro",
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

@router.post(
    "/exportar/{id_empresa}",
    status_code=201,
    description="Recibe un archivo y lo envia por email a la empresa",
    response_model=RegistroSchema.ExportarRegistros,
    responses={
        500: {"model": ResponseSchema.MensajeError500},
        409: {"model": ResponseSchema.MensajeErrorGenerico},
    },
    tags=["Empresas"],
)
async def Exportar_Registros(
    id_empresa: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):

    # CHEQUE TOKEN
    logged_user = utils.check_token_admin(db,token)
    if logged_user == None:
        return JSONResponse(
            status_code=401,
            content={
                "code": 401,
                "error": "Acceso no autorizado",
            },
        )

    try:
        exist_empresa = RepoEmpresa.get_empresa_by_id(db, id_empresa)
        if exist_empresa == None:
            return JSONResponse(
                status_code=404,
                content={
                    "code": 404,
                    "error": "No existe - Ese ID no corresponde a un empresa registrada",
                },
            )
        else:

            html = "Se adjunta el archivo correspondiente."

            message = MessageSchema(
                subject="Exportacion para empresa: {}".format(exist_empresa.nombre) ,
                recipients=[exist_empresa.mail], 
                body=html,
                attachments=[file]
            )

            fm = FastMail(conf_mail)
            await fm.send_message(message)
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


