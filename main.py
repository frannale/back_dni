
from routers import usuarios, jugador,especialista,registros
from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI
from sql import models
from sql.database import engine

models.Base.metadata.create_all(bind=engine)


description = """
API DNI DEPORTIVO

"""

tags_metadata = [
    {
        "name": "Usuarios",
        "description": "Endpoints de los Usuarios",
    },
    {
        "name": "Jugadores",
        "description": "Endpoints de los Jugadores",
    },
    {"name": "Seguridad", "description": "Endpoints de Seguridad"},
]


app = FastAPI(
    title="API DNI DEPORTIVO",
    description=description,
    version="1.0",
    openapi_tags=tags_metadata,
)

origins = [
    "*",
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:3001",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# IMPORTA CONTROLLERS
app.include_router(usuarios.router)
app.include_router(jugador.router)
app.include_router(especialista.router)
app.include_router(registros.router)




