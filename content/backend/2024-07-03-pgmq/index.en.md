---
title: "PGMQ(PostgreSQL Message Queue) Setup"
summary: "PGMQ is a lightweight message queue. Like AWS SQS and RSMQ but on Postgres. The article is about how to setup PGMQ with Docker Compose to connect with official Python client"
description: "PGMQ is a lightweight message queue. Like AWS SQS and RSMQ but on Postgres. The article is about how to setup PGMQ with Docker Compose to connect with official Python client"
date: 2024-07-03T21:46:28+08:00
slug: "pgmq-docker-compose"
tags: ["blog","en","database","postgresql"]
# series: ["Documentation"]
# series_order: 9
cascade:
  showEdit: true
  showSummary: true
  hideFeatureImage: false
draft: false
---


## PGMQ (PostgreSQL Message Queue)

{{< github repo="tembo-io/pgmq" >}}

> https://github.com/tembo-io/pgmq <br>
> **PGMQ** is a lightweight message queue based on PostgreSQL. <br>
> It is implemented using a PostgreSQL Extension.

Since it is based solely on PostgreSQL, it is very suitable for lightweight business needs that require an MQ.

Currently, the usage scenario is using the existing API Server + PGMQ + consumer to handle some asynchronous tasks and retry mechanisms with third-party services.

## Installation

### Tembo Docker Image

First, ensure your system has the following installed:
- Docker
- Docker Compose

The simplest way is to use the official Tembo Docker Image:

```bash
docker run -d --name postgres -e POSTGRES_PASSWORD=postgres -p 5432:5432 quay.io/tembo/pg16-pgmq:latest
```

### Installing from Extension

If you want to install using the original `postgres` image as an extension:

1. Download the latest PGMQ SQL and Control files:
```bash
curl -o pgmq.sql https://raw.githubusercontent.com/tembo-io/pgmq/main/pgmq-extension/sql/pgmq.sql
curl -o pgmq.control https://raw.githubusercontent.com/tembo-io/pgmq/main/pgmq-extension/pgmq.control
```

2. Update `docker-compose.yml` to add the volume settings:
- `db.sql` contains some initialization SQL files (depending on the project's needs)
- `pgmq.sql` and `pgmq.control` are the PGMQ SQL and Control files
  - The version number in `pgmq--1.3.3.sql` should match the version number in `pgmq.control`
- `stateful_volumes/postgresql` is the directory mounted for `postgres` container persistence

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15.1
    container_name: postgres
    ports:
      - 5432:5432
    env_file:
      - postgres.env
    restart: always
    volumes:
      - ./db.sql:/docker-entrypoint-initdb.d/db.sql
      - ./pgmq.control:/usr/share/postgresql/15/extension/pgmq.control
      - ./pgmq.sql:/usr/share/postgresql/15/extension/pgmq--1.3.3.sql
      - ./stateful_volumes/postgresql:/var/lib/postgresql/data/
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "your_postgres_user", "-d", "your_postgres_db"]
      interval: 2s
      timeout: 5s
      retries: 3
```

3. Start the `postgres` container:
> If you have previously run a `postgres` container, remember to delete the volume first!

```bash
docker compose up postgres -d
```

## PGMQ Python Client

- Install the `pgmq` Python Client:
```bash
pip install tembo-pgmq-python
```
> Since `tembo-pgmq-python` directly uses `psycopg` (which is `psycopg3`, not `psycopg2`) <br>
>  it may have issues when installed with `poetry` on Mac. <br>
> It is recommended to install it directly with `pip`.

- Using the `pgmq` Python Client:

The [tembo-pgmq-python README](https://github.com/tembo-io/pgmq/tree/main/tembo-pgmq-python) is quite clear. <br> 
The main components are the `PGMQueue` and `Message` data classes. <br>
The `vt` stands for `visibility timeout`, which is the time duration during which a message will not be re-read after being read. 

Here is a simple example:
```python
from tembo_pgmq_python import PGMQueue, Message

queue = PGMQueue(
    host="0.0.0.0",
    port="5432",
    username="postgres",
    password="postgres",
    database="postgres"
)

msg_id: int = queue.send("my_queue", {"hello": "world"})

read_message: Message = queue.read("my_queue", vt=30)
print(read_message)

deleted: bool = queue.delete("my_queue", read_message.msg_id)

dropped: bool = queue.drop_queue("my_queue")
```

For more examples, refer to the [tembo-pgmq-python README](https://github.com/tembo-io/pgmq/tree/main/tembo-pgmq-python).

## Reference

- [PGMQ GitHub Repository](https://github.com/tembo-io/pgmq)
- [Psycopg3 Documentation](https://www.psycopg.org/psycopg3/docs/basic/install.html)
- [tembo-pgmq-python GitHub Repository](https://github.com/tembo-io/pgmq/tree/main/tembo-pgmq-python)
- [Stack Overflow: Postgres Error Installing My Own Extension](https://stackoverflow.com/questions/59901605/postgres-error-installing-my-own-extension)