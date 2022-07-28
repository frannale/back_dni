import os

from dotenv import dotenv_values

from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse
from security import utils

from sqlalchemy.orm import Session

from sql import tecnicos as RepoTecnico
import sql.schemas.tecnicos as TecnicoShema
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
    "/tecnicos",
    response_model=TecnicoShema.GetTecnicos,
    description="Retorna todos los tecnicos instaladores",
    responses={500: {"model": ResponseSchema.MensajeError500}},
    tags=["Tecnicos"],
)
def Get_Tecnicos_Instaladores(
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
        tecnico = RepoTecnico.get_tecnicos(db,request.query_params)
        return {"code": 200, "tecnicos": tecnico}
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "code": 500,
                "error": "Internal Server Error - Detalle: {0}".format(str(e)),
            },
        )


@router.get(
    "/tecnicos/{id_tecnico}",
    response_model=TecnicoShema.GetTecnico,
    description="Retorna la información de un tecnico",
    responses={
        500: {"model": ResponseSchema.MensajeError500},
        404: {"model": ResponseSchema.MensajeError404},
    },
    tags=["Tecnicos"],
)
def Get_Tecnico(
    id_tecnico: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
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
        tecnico = RepoTecnico.get_tecnico_by_id(db, id_tecnico)
        if tecnico == None:
            return JSONResponse(
                status_code=404,
                content={
                    "code": 404,
                    "error": "Not Found - Ese ID no corresponde a un tecnico registrado",
                },
            )
        else:
            return {
                "code": 200,
                "tecnico": tecnico
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
    "/tecnicos/{id_tecnico}",
    response_model=TecnicoShema.DeleteTecnico,
    description="Elimina el tecnico",
    responses={
        500: {"model": ResponseSchema.MensajeError500},
        404: {"model": ResponseSchema.MensajeError404},
    },
    tags=["Tecnicos"],
)
def Delete_Tecnico(
    id_tecnico: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
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
        tecnico = RepoTecnico.get_tecnico_by_id(db, id_tecnico)
        if tecnico == None:
            return JSONResponse(
                status_code=404,
                content={
                    "code": 404,
                    "error": "Not Found - Ese ID no corresponde a un tecnico registrado",
                },
            )
        else:
            RepoTecnico.delete_tecnico_by_id(db, id_tecnico)
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
    "/tecnicos/{id_tecnico}",
    response_model=TecnicoShema.UpdateTecnico,
    description="Modifica una tecnico",
    responses={
        500: {"model": ResponseSchema.MensajeError500},
        404: {"model": ResponseSchema.MensajeError404},
    },
    tags=["Tecnicos"],
)
def Put_Tecnico(
    tecnico: TecnicoShema.TecnicoUpdate,
    id_tecnico: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
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
       
        exist_tecnico = RepoTecnico.get_tecnico_by_id(db, id_tecnico)
        if exist_tecnico == None:
            return JSONResponse(
                status_code=404,
                content={
                    "code": 404,
                    "error": "Not Found - Ese ID no corresponde a un tecnico registrado",
                },
            )
        else:
            updated_user = RepoTecnico.modificar_tecnico(db, id_tecnico,tecnico)
            return {
                "code": 200,
                "tecnico": updated_user
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
    "/tecnicos/crear",
    status_code=201,
    description="Crea un nuevo tecnico",
    response_model=TecnicoShema.CrearTecnico,
    responses={
        500: {"model": ResponseSchema.MensajeError500},
        409: {"model": ResponseSchema.MensajeErrorGenerico},
    },
    tags=["Tecnicos"],
)
def Crear_Nuevo_Tecnico(
    tecnico: TecnicoShema.TecnicoCreate,
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
        if RepoTecnico.get_tecnico_by_nombre(db, tecnico.nombre) == None:
            nuevo_tecnico = RepoTecnico.crear_tecnico(db, tecnico)
            return {
                "code": 201,
                "mensaje": "Tecnico creado exitosamente",
                "tecnico": nuevo_tecnico,
            }
        else:
            return JSONResponse(
                status_code=409,
                content={
                    "code": 409,
                    "error": "Duplicate - Ese nombre ya corresponde a un tecnico registrado",
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


