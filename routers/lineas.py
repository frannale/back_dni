import os

from dotenv import dotenv_values

from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse
from security import utils

from sqlalchemy.orm import Session

from sql import lineas as RepoLinea
import sql.schemas.lineas as LineaSchema
import sql.schemas.responses as ResponseSchema
from sql.database import SessionLocal,engine

from fastapi import FastAPI, Request

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
    "/lineas",
    response_model=LineaSchema.GetLineas,
    description="Retorna todos las lineas",
    responses={500: {"model": ResponseSchema.MensajeError500}},
    tags=["Lineas"],
)
def Get_Lineas(
    request: Request,
    db: Session = Depends(get_db),
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
        linea = RepoLinea.get_lineas(db,request.query_params)
        return {"code": 200, "lineas": linea}
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "code": 500,
                "error": "Internal Server Error - Detalle: {0}".format(str(e)),
            },
        )


@router.get(
    "/lineas/{id_linea}",
    response_model=LineaSchema.GetLinea,
    description="Retorna la información de una linea",
    responses={
        500: {"model": ResponseSchema.MensajeError500},
        404: {"model": ResponseSchema.MensajeError404},
    },
    tags=["Lineas"],
)
def Get_Linea(
    id_linea: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
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
        linea = RepoLinea.get_linea_by_id(db, id_linea)
        if linea == None:
            return JSONResponse(
                status_code=404,
                content={
                    "code": 404,
                    "error": "Not Found - Ese ID no corresponde a un linea registrado",
                },
            )
        else:
            return {
                "code": 200,
                "linea": linea
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
    "/lineas/{id_linea}",
    response_model=LineaSchema.DeleteLinea,
    description="Elimina el linea",
    responses={
        500: {"model": ResponseSchema.MensajeError500},
        404: {"model": ResponseSchema.MensajeError404},
    },
    tags=["Lineas"],
)
def Delete_Linea(
    id_linea: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
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
        linea = RepoLinea.get_linea_by_id(db, id_linea)
        if linea == None:
            return JSONResponse(
                status_code=404,
                content={
                    "code": 404,
                    "error": "Not Found - Ese ID no corresponde a un linea registrado",
                },
            )
        else:
            RepoLinea.delete_linea_by_id(db, id_linea)
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
    "/lineas/{id_linea}",
    response_model=LineaSchema.UpdateLinea,
    description="Modifica una linea",
    responses={
        500: {"model": ResponseSchema.MensajeError500},
        404: {"model": ResponseSchema.MensajeError404},
    },
    tags=["Lineas"],
)
def Put_Linea(
    linea: LineaSchema.LineaUpdate,
    id_linea: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
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
       
        exist_linea = RepoLinea.get_linea_by_id(db, id_linea)
        if exist_linea == None:
            return JSONResponse(
                status_code=404,
                content={
                    "code": 404,
                    "error": "Not Found - Ese ID no corresponde a un linea registrado",
                },
            )
        else:
            updated_user = RepoLinea.modificar_linea(db, id_linea,linea)
            return {
                "code": 200,
                "linea": updated_user
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
    "/lineas/crear",
    status_code=201,
    description="Crea un nueva linea",
    response_model=LineaSchema.CrearLinea,
    responses={
        500: {"model": ResponseSchema.MensajeError500},
        409: {"model": ResponseSchema.MensajeErrorGenerico},
    },
    tags=["Lineas"],
)
def Crear_Nueva_Linea(
    linea: LineaSchema.LineaCreate,
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
        if RepoLinea.get_linea_by_nombre(db, linea.nombre,linea.empresa_id) == None:
            nueva_linea = RepoLinea.crear_linea(db, linea)
            return {
                "code": 201,
                "mensaje": "Linea creada exitosamente"
            }
        else:
            return JSONResponse(
                status_code=409,
                content={
                    "code": 409,
                    "error": "Duplicate - Ese nombre ya corresponde a un linea registrado",
                },
            )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "code": 500,
                "error": "Internal Server Error - Detalle: {0}".format(str(e)),
            },
        )


