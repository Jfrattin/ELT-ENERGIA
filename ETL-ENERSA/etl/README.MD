# Pasos para configurar la conexión a la base de datos

1. Primero, crear un archivo llamado `config.py` en la carpeta etl con este formato:

```
DB_CONNECTIONS = {
    "engine_sf": "postgresql://<username>:<password>@<host>/<database_name_sf>",
    "engine_cubo": "postgresql://<username>:<password>@<host>/<database_name_cubo>"
}
```

El archivo ya está en `.gitignore` por lo que no se va a subir.