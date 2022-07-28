import os

from dotenv import dotenv_values

from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse
from security import utils

from sqlalchemy.orm import Session

from sql import especialista as RepoEspecialista
import sql.schemas.especialista as EspecialistaSchema
import sql.schemas.responses as ResponseSchema
from sql.database import SessionLocal,engine

from fastapi import FastAPI, Request

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
    "/especialistas",
    response_model=EspecialistaSchema.GetEspecialistas,
    description="Retorna todos los especialistas",
    responses={500: {"model": ResponseSchema.MensajeError500}},
    tags=["Especialistas"],
)
def Get_EspecialGetEspecialistas(
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
        especialista = paginate( 
            RepoEspecialista.get_especialistas(db,request.query_params),params
        )
        return {"code": 200, "especialistas": especialista}
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "code": 500,
                "error": "Internal Server Error - Detalle: {0}".format(str(e)),
            },
        )


@router.get(
    "/especialistas/{id_especialista}",
    response_model=EspecialistaSchema.GetEspecialista,
    description="Retorna la información de una especialista",
    responses={
        500: {"model": ResponseSchema.MensajeError500},
        404: {"model": ResponseSchema.MensajeError404},
    },
    tags=["Especialistas"],
)
def Get_Especialista(
    id_especialista: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
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
        especialista = RepoEspecialista.get_especialista_by_id(db, id_especialista)
        if especialista == None:
            return JSONResponse(
                status_code=404,
                content={
                    "code": 404,
                    "error": "Not Found - Ese ID no corresponde a un especialista registrado",
                },
            )
        else:
            return {
                "code": 200,
                "especialista": especialista
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
    "/especialistas/{id_especialista}",
    response_model=EspecialistaSchema.DeleteEspecialista,
    description="Elimina el especialista",
    responses={
        500: {"model": ResponseSchema.MensajeError500},
        404: {"model": ResponseSchema.MensajeError404},
    },
    tags=["Especialistas"],
)
def Delete_Especialista(
    id_especialista: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
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
        especialista = RepoEspecialista.get_especialista_by_id(db, id_especialista)
        if especialista == None:
            return JSONResponse(
                status_code=404,
                content={
                    "code": 404,
                    "error": "Not Found - Ese ID no corresponde a un especialista registrada",
                },
            )
        else:
            RepoEspecialista.delete_especialista_by_id(db, id_especialista)
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
    "/especialistas/{id_especialista}",
    response_model=EspecialistaSchema.UpdateEspecialista,
    description="Modifica una especialista",
    responses={
        500: {"model": ResponseSchema.MensajeError500},
        404: {"model": ResponseSchema.MensajeError404},
    },
    tags=["Especialistas"],
)
def Put_Especialista(
    especialista: EspecialistaSchema.EspecialistaUpdate,
    id_especialista: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
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
       
        exist_especialista = RepoEspecialista.get_especialista_by_id(db, id_especialista)
        if exist_especialista == None:
            return JSONResponse(
                status_code=404,
                content={
                    "code": 404,
                    "error": "No existe - Ese ID no corresponde a un especialista registrada",
                },
            )
        else:
            updated_user = RepoEspecialista.modificar_especialista(db, id_especialista,especialista)
            return {
                "code": 200,
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
    "/especialistas/crear",
    status_code=201,
    description="Crea un nuevo especialista",
    response_model=EspecialistaSchema.CrearEspecialista,
    responses={
        500: {"model": ResponseSchema.MensajeError500},
        409: {"model": ResponseSchema.MensajeErrorGenerico},
    },
    tags=["Especialistas"],
)
def Crear_Nuevo_Especialista(
    especialista: EspecialistaSchema.EspecialistaCreate,
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
        if RepoEspecialista.get_especialista_by_matricula(db, especialista.matricula) == None:
            nuevo_especialista = RepoEspecialista.crear_especialista(db, especialista)
            return {
                "code": 201,
                "mensaje": "Especialista creado exitosamente",
            }
        else:
            return JSONResponse(
                status_code=409,
                content={
                    "code": 409,
                    "error": "Duplicado - Esa MATRICULA ya corresponde a un especialista registrado",
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


