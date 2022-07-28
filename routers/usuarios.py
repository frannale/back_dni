import os

from dotenv import dotenv_values

from fastapi import Depends, HTTPException, status,APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from sqlalchemy.orm import Session

from sql import usuarios
import sql.schemas.usuarios as UsuarioSchema
import sql.schemas.responses as ResponseSchema
from sql.database import SessionLocal

from security import utils

from datetime import timedelta, datetime


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


# Endpoints de Seguridad

@router.post(
    "/login",
    response_model=UsuarioSchema.Token,
    tags=["Seguridad"],
)
async def Login(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    usuarios.check_admin(db)
    user = utils.autentificar_usuario(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrecta",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=int(config["ACCESS_TOKEN_EXPIRE_MINUTES"]))
    access_token = utils.crear_token_acceso(
        data={"sub": user.username, "user_id": user.id,  "role": user.role}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get(
    "/usuarios/",
    response_model=UsuarioSchema.GetUsuarios,
    description="Retorna todos los usuarios registrados hasta el momento",
    responses={500: {"model": ResponseSchema.MensajeError500}},
    tags=["Usuarios"],
)
async def Get_Usuarios_Registrados(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
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
        usuario = usuarios.get_usuarios(db)
        
        return {"code": 200, "usuarios": usuario}
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "code": 500,
                "error": "Internal Server Error - Detalle: {0}".format(str(e)),
            },
        )


@router.get(
    "/usuarios/{id_usuario}",
    response_model=UsuarioSchema.GetUsuario,
    description="Retorna la información del usuario",
    responses={
        500: {"model": ResponseSchema.MensajeError500},
        404: {"model": ResponseSchema.MensajeError404},
    },
    tags=["Usuarios"],
)
def Get_Usuario(
    id_usuario: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
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
        usuario = usuarios.get_usuario_by_id(db, id_usuario)
        if usuario == None:
            return JSONResponse(
                status_code=404,
                content={
                    "code": 404,
                    "error": "Not Found - Ese ID no corresponde a un usuario registrado",
                },
            )
        else:
            return {
                "code": 200,
                "usuario": usuario
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
    "/usuarios/{id_usuario}",
    response_model=UsuarioSchema.DeleteUsuario,
    description="Elimina el usuario",
    responses={
        500: {"model": ResponseSchema.MensajeError500},
        404: {"model": ResponseSchema.MensajeError404},
    },
    tags=["Usuarios"],
)
def Delete_Usuario(
    id_usuario: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
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
        usuario = usuarios.get_usuario_by_id(db, id_usuario)
        if usuario == None:
            return JSONResponse(
                status_code=404,
                content={
                    "code": 404,
                    "error": "Not Found - Ese ID no corresponde a un usuario registrado",
                },
            )
        else:
            usuarios.delete_usuario_by_id(db, id_usuario)
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
    "/usuarios/{id_usuario}",
    response_model=UsuarioSchema.UpdateUsuario,
    description="Modifica un usuario",
    responses={
        500: {"model": ResponseSchema.MensajeError500},
        404: {"model": ResponseSchema.MensajeError404},
    },
    tags=["Usuarios"],
)
def Put_Usuario(
    usuario: UsuarioSchema.UsuarioUpdate,
    id_usuario: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
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
        exist_usuario = usuarios.get_usuario_by_id(db, id_usuario)
        if exist_usuario == None:
            return JSONResponse(
                status_code=404,
                content={
                    "code": 404,
                    "error": "Not Found - Ese ID no corresponde a un usuario registrado",
                },
            )
        else:
            updated_user = usuarios.modificar_usuario(db, id_usuario,usuario)
            return {
                "code": 200,
                "usuario": updated_user
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
    "/usuarios/crear",
    status_code=201,
    description="Crea un nuevo usuario",
    response_model=UsuarioSchema.CrearUsuario,
    responses={
        500: {"model": ResponseSchema.MensajeError500},
        409: {"model": ResponseSchema.MensajeErrorGenerico},
    },
    tags=["Usuarios"],
)
def Crear_Nuevo_Usuario(
    usuario: UsuarioSchema.UsuarioCreate,
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
        if usuarios.get_usuario_by_nombre(db, usuario.username) == None:
            nuevo_usuario = usuarios.crear_usuario(db, usuario)
            return {
                "code": 201,
                "mensaje": "Usuario creado exitosamente",
                "usuario": nuevo_usuario,
            }
        else:
            return JSONResponse(
                status_code=409,
                content={
                    "code": 409,
                    "error": "Duplicate - Ese nombre ya corresponde a un usuario registrado",
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


