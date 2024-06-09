---
title: "PgBouncer: Lightweight Postgres Connection Pool"
summary: "Solving Django backend DB connection overload with PgBouncer"
description: "Solving Django backend DB connection overload with PgBouncer"
date: 2024-06-09T11:36:24+08:00
slug: "pgbouncer"
tags: ["blog","database","en"]
# series: ["Documentation"]
# series_order: 9
cascade:
  showEdit: true
  showSummary: true
  hideFeatureImage: false
draft: false
---

## Context

> While `Django` allows setting configurations like `CONNECTION_MAX_AGE`, using `gunicorn` (multi-process) to run multiple API instances or using HPA to scale API instances in k8s can still lead to **DB connection overload issues!**

## About PgBouncer

{{< github repo="pgbouncer/pgbouncer" >}}

`PgBouncer` serves as middleware for centralized DB connection pooling.
> It enables backend service instances to reuse DB connections through `PgBouncer`.

As illustrated:

- The `Transactions per second` on the right shows the number of transactions spiking during three load tests.
    - The **2nd** load test used **Django's native DB connection method**.
    - The **1st and 3rd** load tests used **`pgbouncer` for connecting WebService instances**.
- The `Server sessions` on the left (representing the number of current DB connections) indicate:
    - During the **2nd** load test: **DB connection overload occurred!**
    - During the **1st and 3rd** load tests: DB connections **stably remained around 20**.

![load-test.png](load-test.png)

## Backend Service Configuration

Special settings needed:

1. `docker-compose.yml`
2. `.env`

- `docker-compose.yml`
    - Ensure `db` and `pgbouncer` are **on the same network**.
    - Since it's on Docker's internal network,
        - The `postgres` HOST for `pgbouncer` should be set to `db`.

```yaml
db:
    image: postgres:15.1
    container_name: postgres
    restart: always
    environment:
      POSTGRES_USER: your_postgres_user
      POSTGRES_PASSWORD: your_postgres_password
      POSTGRES_DB: dev
    ports:
      - 5432:5432
    volumes:
      - pg_data:/var/lib/postgresql/data
    networks:
      - django_network
pgbouncer:
    image: bitnami/pgbouncer
    container_name: pgbouncer
    restart: always
    ports:
      - 6432:6432 # Connect to `pgbouncer` on port 6432
    environment:
      POSTGRESQL_USERNAME: your_postgres_user
      POSTGRESQL_PASSWORD: your_postgres_password
      POSTGRESQL_HOST: db
      POSTGRESQL_PORT: 5432
      POSTGRESQL_DATABASE: dev
      PGBOUNCER_DATABASE: dev
    networks:
      - django_network # Ensure `db` and `pgbouncer` are on the same network
```

- `.env`
    - To connect to `pgbouncer`:
        - Set `DB_BOUNCER=True`
        - Set `DB_PORT=6432`
```bash
# if you want to use postgres you should set DB_ENGINE
DB_ENGINE=django.db.backends.postgresql
DB_HOST=127.0.0.1
# DB_PORT=5432
DB_NAME=postgres
DB_USER=USER_NAME
DB_PASSWORD=PASSWORD12345678
# if you want to use `pgbouncer` you should set DB_BOUNCER=True
# and set DB_PORT to 6432
DB_BOUNCER=True
DB_PORT=6432
```

## Backend Service `settings.py` Modification

Details of changes:
- Using `pydantic`'s `BaseSettings` for `DB` configuration.
- In `settings.py`, determining whether to connect to `DB` or `pgbouncer` based on `DB_BOUNCER`.

`config.py`
```python
from pydantic import BaseSettings, Field

class DATABASE_SETTINGS(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='DB_')

    ENGINE: str = Field(default='django.db.backends.sqlite3')
    HOST: str = Field(default='')
    PORT: int = Field(default='')
    NAME: str = Field(default='')
    USER: str = Field(default='')
    PASSWORD: str = Field(default='')
    CONN_MAX_AGE: int = Field(default=1)
    CONN_HEALTH_CHECKS: bool = Field(default=True)
    BOUNCER: bool = Field(default=False)

database_settings = DATABASE_SETTINGS()
```

`settings.py`
```python
from config import database_settings

DATABASES = {
  'default': database_settings.model_dump(mode="json")
}
if database_settings.BOUNCER:
  DATABASES['default']['DISABLE_SERVER_SIDE_CURSORS'] = True
```

## Reference
- https://saadmk11.github.io/blog/posts/django-postgresql-database-connection-pooling-with-pgbouncer/
- https://stackoverflow.com/questions/76046768/configure-pgbouncer-and-postgresql-in-docker-compose
- https://hub.docker.com/r/bitnami/pgbouncer/
- https://www.pgbouncer.org/config.html