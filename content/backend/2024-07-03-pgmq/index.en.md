---
title: "Why Choose PGMQ? Implementing ACID Transactional Message Queues in PostgreSQL"
summary: "When your architecture only involves Postgres, why introduce an additional MQ? This article explores the advantages of PGMQ for lightweight asynchronous tasks, teaches you how to deploy it quickly with Docker, and integrates it into Python projects."
description: "PGMQ provides functionality similar to AWS SQS but runs on top of Postgres. This article describes how to set up PGMQ and highlights how to integrate it using Python SQLAlchemy to ensure consistency between messaging and business data operations."
date: 2024-07-03T21:46:28+08:00
slug: "pgmq-docker-compose"
tags: ["blog","en","backend","postgresql"]
# series: ["Documentation"]
# series_order: 9
cascade:
  showEdit: true
  showSummary: true
  hideFeatureImage: false
draft: false
---


## PGMQ (PostgreSQL Message Queue)

{{< github repo="pgmq/pgmq" >}}

> https://github.com/pgmq/pgmq <br>
> **PGMQ** is a lightweight message queue based on PostgreSQL. <br>
> It is implemented using a PostgreSQL Extension.

Since it is based solely on PostgreSQL, it is very suitable for lightweight business needs that require an MQ.

Currently, the usage scenario is using the existing API Server + PGMQ + consumer to handle some asynchronous tasks and retry mechanisms with third-party services.

> Broadly speaking, specially in scenarios where only PostgreSQL is available and you don't want to introduce RabbitMQ or cloud-based MQ solutions, but need Pub/Sub or SQS-like features, PGMQ is a great choice.

## PGMQ vs AWS SQS / GCP Pub/Sub / RabbitMQ / Redis / Apache Kafka

I believe Kafka shouldn't be compared with the message queues listed here because messages in Kafka are more like "data points" rather than "tasks". It fits scenarios requiring massive "data" transmission like data streaming. You could use Kafka as an MQ, but it's often overkill.

Comparing with the remaining technologies:
**PGMQ benchmarking function targets AWS SQS.**
For example: PGMQ implements `visibility timeout`, `delayed message`, `read_count`, etc.
So we are essentially trading off between PGMQ/AWS SQS and other technologies.

Comparing PGMQ with AWS SQS directly, I think there are **several advantages**:

- **Message and Data Consistency**: Since PGMQ is a Postgres Extension, **you can handle business logic and message queue operations within the same Transaction**, ensuring ACID compliance.
- **No Extra Infrastructure**: PGMQ requires only PostgreSQL to run.

Of course, there are **disadvantages**:

- **Postgres Performance Limits**: PGMQ's performance is bound by Postgres write bottlenecks (WAL, Lock contention, MVCC, etc.).
- **Team Knowledge**: The team needs sufficient understanding of PostgreSQL, especially regarding performance tuning, Extension usage, and the aforementioned limitations.

## Installation

### PGMQ Docker Image

- First ensure the system has installed:
  - Docker
  - Docker Compose

The simplest way is to use the official PGMQ Docker Image directly:

```bash
docker run -d --name pgmq-postgres -e POSTGRES_PASSWORD=postgres -p 5432:5432 ghcr.io/pgmq/pg18-pgmq:latest
```

### Installing from Extension

If you want to use the original `postgres` Image and install via Extension:

1. Download the latest PGMQ SQL and Control files:
```bash
curl -o pgmq.sql https://raw.githubusercontent.com/pgmq/pgmq/main/pgmq-extension/sql/pgmq.sql
curl -o pgmq.control https://raw.githubusercontent.com/pgmq/pgmq/main/pgmq-extension/pgmq.control
```

2. Update `docker-compose.yml` to add the volume settings:
- `db.sql` contains some initialization SQL files (depending on the project's needs)
- `pgmq.sql` and `pgmq.control` are the PGMQ SQL and Control files
  - The version number in `pgmq--1.3.3.sql` should match the version number in `pgmq.control`
- `stateful_volumes/postgresql` is the directory mounted for `postgres` container persistence

```yaml
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

## Usage

Here we use Python as an example for using PGMQ.

### PGMQ-SQLAlchemy

For me, there shouldn't be any Python backend project that doesn't use SQLAlchemy ORM to operate the database, right?
However, the official PGMQ Python package does not support SQLAlchemy ORM, which is a big issue for integrating PGMQ into existing projects.

So I wrote the [pgmq-sqlalchemy](https://github.com/jason810496/pgmq-sqlalchemy) package to support SQLAlchemy ORM for PGMQ operations.

- **Install `pgmq-sqlalchemy`**
  ```bash
  pip install pgmq-sqlalchemy
  ```
  - You can also install the corresponding package based on the PostgreSQL driver used in your project:

    ```bash
    # psycopg
    pip install pgmq-sqlalchemy[psycopg]

    # asyncpg
    pip install pgmq-sqlalchemy[asyncpg]
    ```

    > Refer to [`pgmq-sqlalchemy` PyPi page](https://pypi.org/project/pgmq-sqlalchemy/) for all supported extras.

- **Using `pgmq-sqlalchemy`**
  1. **Using `PGMQueue` class directly to operate PGMQ**

      ```python
      from pgmq_sqlalchemy import PGMQueue

      pgmq = PGMQueue(dsn="postgresql+asyncpg://postgres:postgres@localhost:5432/postgres")

      async def consume_messages(
          pgmq: PGMQueue, batch_size: int, vt: int, verbose: bool = False
      ):
          logger.info(f"Starting consumer for queue: {QUEUE_NAME}")
          logger.info(f"Batch size: {batch_size}, Visibility timeout: {vt}s")
          if verbose:
              logger.info("Verbose mode enabled")

          while True:
              try:
                  # Read a batch of messages using pgmq instance method
                  messages = await pgmq.read_batch_async(
                      QUEUE_NAME, vt=vt, batch_size=batch_size
                  )

                  if not messages:
                      logger.debug("No messages available, waiting...")
                      await asyncio.sleep(1)
                      continue

                  logger.info(f"Received {len(messages)} messages")
      ```

      Complete example: [pgmq-sqlalchemy/examples/fastapi_pub_sub/consumer.py](https://github.com/jason810496/pgmq-sqlalchemy/blob/main/examples/fastapi_pub_sub/consumer.py)

  2. **Using `op` module with SQLAlchemy ORM Session**

      ```python
      @app.post("/orders", status_code=status.HTTP_201_CREATED)
      def create_order(
          order_data: OrderCreate, db: Session = Depends(get_db)
      ) -> CreateOrderResponse:
          # Create order in database
          db_order = Order(
              customer_name=order_data.customer_name,
              product_name=order_data.product_name,
              quantity=order_data.quantity,
              price=order_data.price,
          )
          db.add(db_order)
          db.flush()  # Flush to get the ID without committing

          # Publish message to PGMQ using op in the same transaction
          message_data = {
              "order_id": db_order.id,
              "customer_name": db_order.customer_name,
              "product_name": db_order.product_name,
              "quantity": db_order.quantity,
              "price": db_order.price,
              "created_at": db_order.created_at.isoformat(),
          }

          msg_id = op.send(QUEUE_NAME, message_data, session=db, commit=False)

          # Commit both order and message in the same transaction
          db.commit()
          db.refresh(db_order)

          # Return order with message ID
          return CreateOrderResponse(
              id=db_order.id,
              customer_name=db_order.customer_name,
              product_name=db_order.product_name,
              quantity=db_order.quantity,
              price=db_order.price,
              created_at=db_order.created_at,
              message_id=msg_id,
          )
      ```

      Complete example: [pgmq-sqlalchemy/examples/fastapi_pub_sub/api.py](https://github.com/jason810496/pgmq-sqlalchemy/blob/main/examples/fastapi_pub_sub/api.py)

### PGMQ Python Client

- **Install `pgmq` Python Client**
    ```bash
    pip install pgmq
    ```
    > Since `pgmq` directly uses `psycopg` (which is `psycopg3` not `psycopg2`)
    > It might have issues on Mac with `poetry`
    > So direct `pip` install is recommended

- **Using `pgmq` Python Client**
    
    The [pgmq README](https://github.com/pgmq/pgmq/tree/main/pgmq) is quite clear. Main components are `PGMQueue` and `Message` data classes.
    `vt` stands for `visibility timeout`.

    Simple example:
    ```python
    from pgmq import PGMQueue, Message

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

    For more examples refer to [`pgmq` README](https://github.com/pgmq/pgmq/tree/main/pgmq).

## Reference

- https://github.com/pgmq/pgmq
- https://www.psycopg.org/psycopg3/docs/basic/install.html
- https://github.com/pgmq/pgmq/tree/main/pgmq
- https://stackoverflow.com/questions/59901605/postgres-error-installing-my-own-extension
- PGMQ vs Other Message Queue Solutions:
  - https://news.ycombinator.com/item?id=45747018
  - https://topicpartition.io/blog/postgres-pubsub-queue-benchmarks#pg-as-a-queue
  - https://lobste.rs/s/oj3ce4/kafka_is_fast_i_ll_use_postgres#c_dvehfa
  - https://kmoppel.github.io/2025-11-13-postgres-kafka-and-event-queues/
  - https://www.reddit.com/r/SQL/comments/1mmz0st/i_chose_postgresql_over_kafka_for_streaming_engine/
  - https://www.reddit.com/r/PostgreSQL/comments/1ln74ae/why_i_chose_postgres_over_kafka_to_stream_100k/
- Postgres MVCC and Performance:
  - https://www.cs.cmu.edu/~pavlo/blog/2023/04/the-part-of-postgresql-we-hate-the-most.html
  - https://news.ycombinator.com/item?id=41895951
  - https://dev.to/prabhu_balaji_1997/why-your-fast-postgresql-query-suddenly-became-slow-a-deep-dive-into-mvcc-and-index-bloat-44jh