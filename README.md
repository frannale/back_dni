# API DNI DEPORTIVO

## Configuración del .env

Para que la API funcione correctamente, se tiene que crear un archivo .env en la raíz del proyecto.
El mismo tiene la siguiente estructura:

```

# JWT Config
SECRET_KEY="SECRET_KEY_GOES_HERE"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES="360"

# Database Config
db_user="DB_USER_GOES_HERE"
db_pass="DB_PASSWORD_GOES_HERE"
db_host="DB_HOST_GOES_HERE"
db_name="DB_NAME_GOES_HERE"


# Email Config
MAIL_USERNAME="EMAIL_USERNAME_GOES_HERE"
MAIL_PASSWORD="EMAIL_PASSWORD_GOES_HERE"

# Frontend URL
FRONTEND_URL="URL_DE_LANDING_DE_IOLA"

```

Estos parámetros son, en orden:

- SECRET_KEY -> Key secreta que se usa para encriptar los tokens JWT. Se recomienda generar
  la key con el comando `openssl rand -hex 32`

- ALGORITHM -> El algoritmo de encriptado que se usa para los tokens.

- ACCESS_TOKEN_EXPIRE_MINUTES -> Tiempo de duración del token en minutos.

- DB_USER -> Usuario para conectarse a la Database

- DB_PASS -> Contraseña del usuario de la Database

- DB_HOST -> Host de la Database

- DB_NAME -> Nombre de la Database

- EMAIL_USERNAME -> Email el cual se utilizará para recibir las propuestas de la Landing

- EMAIL_PASSWORD -> Password del Email

- FRONTEND_URL -> La URL de la Landing

<------------------------------------------------------------>

## Correr el proyecto en modo development

Estando parado en la raíz del proyecto, ejecutar:

- `python -m venv venv`
- `source venv/bin/activate`
- `pip install -r requirements.txt`
- `python -m venv venv`
- `uvicorn main:app --host 0.0.0.0 --reload --port 8000`

Esto levanta el proyecto en el puerto 8000 en modo Hot Reload

Para consultar la documentación, se puede ir a `[URL_API]/redoc`

## Buildear para producción

Teniendo el .env configurado correctamente, es tan simple como ejecutar:

- `docker-compose up`

Esto buildea el proyecto entero y lo deja servido en un container de Uvicorn en el puerto 9080, este puerto es configurable en el archivo de docker-compose
