# PLATAFORMA ESCOLAR API

## Tecnologías
Tecnologías y frameworks que usa la aplicación.
- [Python 3.11](https://www.python.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Pydantic V2](https://docs.pydantic.dev/latest/)
- [SQLAlchemy 2](https://www.sqlalchemy.org/)
- [PostgreSQL](https://www.postgresql.org/)

## Instalación
Dentro de un entorno virtual de Python ejecutar lo siguiente:
```
pip install -r requirements.dev.txt
```

## Base de datos
Asegúrese de tener instalado e inicializado PostgreSQL, cree la base de datos de la aplicación, un usuario y contraseña.

```
sudo -u postgres psql
```

```
CREATE database my_db;
CREATE USER myuser WITH PASSWORD 'mypassword';
GRANT ALL PRIVILEGES ON DATABASE my_db TO myuser;
```

Debe crear también una base de datos adicional para los tests, el nombre de la base de datos debe ser el mismo de la base de datos de la aplicación con el sufijo **_test**.

```
CREATE database my_db_test;
GRANT ALL PRIVILEGES ON DATABASE my_db_test TO myuser;
```


## Variables de entorno
Debe crear un archivo **.env** para establecer las variables de entorno, un archivo **.env.example** contiene la estructura de ejemplo.

- **ENV**: Indica el modo de ejecución de la aplicación, posibles valores son DEV, PROD, TEST
- **DEBUG**: Indica si se hará un muestreo más detallado sobre los errores o eventos que ocurran en la aplicación.
- **DATABASE_URL**: Url de conexión con PostgreSQL usado por SQLAlchemy, para mayor información visite este [link](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#module-sqlalchemy.dialects.postgresql.psycopg).


## VS CODE
TODO