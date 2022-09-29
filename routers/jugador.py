import os

from dotenv import dotenv_values

from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse
from security import utils

from sqlalchemy.orm import Session

from sql import jugador as RepoJugador
import sql.schemas.jugador as JugadorSchema
import sql.schemas.responses as ResponseSchema
from sql.database import SessionLocal,engine

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
    "/jugadores",
    response_model=JugadorSchema.GetJugadores,
    description="Retorna todos las jugadores",
    responses={500: {"model": ResponseSchema.MensajeError500}},
    tags=["Jugadores"],
)
def Get_Jugadores(
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
        jugador = paginate( 
            RepoJugador.get_jugadores(db,request.query_params),params
        )
        return {"code": 200, "jugadores": jugador}
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "code": 500,
                "error": "Internal Server Error - Detalle: {0}".format(str(e)),
            },
        )


@router.get(
    "/jugadores/{id_jugador}",
    response_model=JugadorSchema.GetJugador,
    description="Retorna la información de una jugador",
    responses={
        500: {"model": ResponseSchema.MensajeError500},
        404: {"model": ResponseSchema.MensajeError404},
    },
    tags=["Jugadores"],
)
def Get_Jugador(
    id_jugador: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
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
        jugador = RepoJugador.get_jugador_by_id(db, id_jugador)
        if jugador == None:
            return JSONResponse(
                status_code=404,
                content={
                    "code": 404,
                    "error": "Not Found - Ese ID no corresponde a un jugador registrado",
                },
            )
        else:
            return {
                "code": 200,
                "jugador": jugador
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
    "/jugadores/{id_jugador}",
    response_model=JugadorSchema.DeleteJugador,
    description="Elimina el jugador",
    responses={
        500: {"model": ResponseSchema.MensajeError500},
        404: {"model": ResponseSchema.MensajeError404},
    },
    tags=["Jugadores"],
)
def Delete_Jugador(
    id_jugador: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
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
        jugador = RepoJugador.get_jugador_by_id(db, id_jugador)
        if jugador == None:
            return JSONResponse(
                status_code=404,
                content={
                    "code": 404,
                    "error": "Not Found - Ese ID no corresponde a un jugador registrada",
                },
            )
        else:
            RepoJugador.delete_jugador_by_id(db, id_jugador)
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
    "/jugadores/{id_jugador}",
    response_model=JugadorSchema.UpdateJugador,
    description="Modifica una jugador",
    responses={
        500: {"model": ResponseSchema.MensajeError500},
        404: {"model": ResponseSchema.MensajeError404},
    },
    tags=["Jugadores"],
)
def Put_Jugador(
    jugador: JugadorSchema.JugadorUpdate,
    id_jugador: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
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
       
        exist_jugador = RepoJugador.get_jugador_by_id(db, id_jugador)
        if exist_jugador == None:
            return JSONResponse(
                status_code=404,
                content={
                    "code": 404,
                    "error": "No existe - Ese ID no corresponde a un jugador registrada",
                },
            )
        else:
            updated_user = RepoJugador.modificar_jugador(db, id_jugador,jugador)
            return {
                "code": 200,
                "jugador": updated_user
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
    "/jugadores/crear",
    status_code=201,
    description="Crea un nuevo jugador",
    response_model=JugadorSchema.CrearJugador,
    responses={
        500: {"model": ResponseSchema.MensajeError500},
        409: {"model": ResponseSchema.MensajeErrorGenerico},
    },
    tags=["Jugadores"],
)
def Crear_Nuevo_jugador(
    jugador: JugadorSchema.JugadorCreate,
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
        if RepoJugador.get_jugador_by_dni(db, jugador.dni) == None:
            nuevo_jugador = RepoJugador.crear_jugador(db, jugador)
            return {
                "code": 201,
                "mensaje": "Jugador creado exitosamente",
                "jugador": nuevo_jugador,
            }
        else:
            return JSONResponse(
                status_code=409,
                content={
                    "code": 409,
                    "error": "Duplicado - Ese DNI ya corresponde a un jugador registrado",
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


@router.post(
    "/jugadores/foto/{id_jugador}",
    status_code=201,
    description="Modifica la firma digital de una jugador",
    response_model=JugadorSchema.CrearJugador,
    responses={
        500: {"model": ResponseSchema.MensajeError500},
        409: {"model": ResponseSchema.MensajeErrorGenerico},
    },
    tags=["Jugadores"],
)
def Modificar_Foto(
    id_jugador: int,
    file: bytes = File(...),
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
        exist_jugador = RepoJugador.get_jugador_by_id(db, id_jugador)
        if exist_jugador == None:
            return JSONResponse(
                status_code=404,
                content={
                    "code": 404,
                    "error": "No existe - Ese ID no corresponde a un jugador registrada",
                },
            )
        else:
            updated_jugador = RepoJugador.modificar_foto(db, id_jugador,file)
            return {
                "code": 201,
                "jugador": updated_jugador
            }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "code": 500,
                "error": "Internal Server Error - Detalle: {0}".format(str(e)),
            },
        )


@router.get(
    "/validacion/{dni_jugador}",
    response_model=JugadorSchema.GetJugadorValidado,
    description="Retorna si un jugador tiene aprobada el alta medica",
    responses={
        500: {"model": ResponseSchema.MensajeError500},
        404: {"model": ResponseSchema.MensajeError404},
    },
    tags=["Jugadores"],
)
def Validate_Jugador(
    dni_jugador: int, db: Session = Depends(get_db)
):
        
    try:
        jugador = RepoJugador.get_jugador_activo_by_dni(db, dni_jugador)
        if jugador == None:
            return JSONResponse(
                status_code=404,
                content={
                    "code": 404,
                    "error": "Not Found - Ese ID no corresponde a un jugador registrado",
                },
            )
        else:
            registro = RepoJugador.validate_alta_jugador_by_id(db, jugador.dni)
            return {
                "code": 200,
                "aprobado": "APTO" if registro else "NO APTO" , 
                "jugador": jugador
            }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "code": 500,
                "error": "Internal Server Error - Detalle: {0}".format(str(e)),
            },
        )


