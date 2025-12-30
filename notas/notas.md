# Ejecutar archivos SQL en `notas/sql` usando `notas/docker-compose.yaml`

Antes de ejecutar los comandos, levante el servicio Postgres con compose:

```bash
docker-compose -f notas/docker-compose.yaml up -d
```

Opciones para ejecutar los .sql (recomendado: 1 o 2):

1) Usar `docker-compose exec` (directo, sencillo)

```bash
# Ejecuta un archivo SQL dentro del contenedor (no requiere copiar archivos)
    docker-compose -f notas/docker-compose.yaml exec -T postgres psql -U agente_user -d midb < notas/sql/01_db_supermercado_DDL.sql

# Ejecutar los demás archivos

cat 01_db_supermercado_DDL.sql | docker exec -i -e PGPASSWORD='agente3_84p' mi_postgres_db psql -U agente_user -d midb
cat 02_db_supermercado_DML_INSERTS.sql | docker exec -i -e PGPASSWORD='agente3_84p' mi_postgres_db psql -U agente_user -d midb
cat 03_db_supermercado_DML_UPDATES.sql | docker exec -i -e PGPASSWORD='agente3_84p' mi_postgres_db psql -U agente_user -d midb


pwd  # linux y MAc
docker-compose -f docker-compose.yaml exec -T postgres psql -U agente_user -d midb < sql/03_db_supermercado_DML_UPDATES.sql
docker-compose -f docker-compose.yaml exec -T postgres psql -U agente_user -d midb < sql/04_db_supermercado_DML_UPDATES.sql
docker-compose -f docker-compose.yaml exec -T postgres psql -U agente_user -d midb < sql/05_db_supermercado_DML_UPDATES.sql

# Windows
cd notas
Get-Content sql/01_db_supermercado_DDL.sql | docker-compose exec -T postgres psql -U agente_user -d midb
Get-Content sql/02_db_supermercado_DML_INSERTS.sql | docker-compose exec -T postgres psql -U agente_user -d midb
Get-Content sql/03_db_supermercado_DML_UPDATES.sql | docker-compose exec -T postgres psql -U agente_user -d midb

# Ejecutar todos los .sql del directorio (en orden por nombre)
for f in sql/*.sql; do
	docker-compose -f docker-compose.yaml exec -T postgres psql -U agente_user -d midb < "$f"
done
```

2) Copiar el archivo al contenedor y usar `psql -f` (útil si prefiere copiar primero)

```bash
# Obtener el id del contenedor postgres gestionado por compose
CONTAINER=$(docker-compose -f notas/docker-compose.yaml ps -q postgres)

# Copiar y ejecutar
docker cp notas/sql/01_db_supermercado_DDL.sql "$CONTAINER":/tmp/01_db_supermercado_DDL.sql
docker exec -i "$CONTAINER" psql -U agente_user -d midb -f /tmp/01_db_supermercado_DDL.sql
```

3) Montar `notas/sql` en `/docker-entrypoint-initdb.d` (se ejecuta sólo en la inicialización de la base de datos)

Agregar al servicio `postgres` en `notas/docker-compose.yaml` (volumen adicional):

```yaml
		volumes:
			- postgres_data:/var/lib/postgresql/data
			- ./notas/sql:/docker-entrypoint-initdb.d:ro
```

Nota: Postgres ejecuta los archivos dentro de `/docker-entrypoint-initdb.d` solo en el primer arranque cuando el directorio de datos está vacío.

Consejos y autenticación
- Si no quiere escribir la contraseña en cada comando, puede exportar la variable temporalmente: `export PGPASSWORD=agente3_%84p` o usar un `.env` y/o Docker secrets.
- Para ejecutar sin pasar contraseña en el comando:

```bash
export PGPASSWORD='agente3_%84p'
docker-compose -f notas/docker-compose.yaml exec -T postgres psql -U agente_user -d midb < notas/sql/01_db_supermercado_DDL.sql
```

Fin.


docker-compose -f docker-compose.yaml down -v
docker-compose -f docker-compose.yaml up -d
# Esto volverá a crear la BD con la contraseña actual en docker-compose.yaml
python3 -m scripts.test_db