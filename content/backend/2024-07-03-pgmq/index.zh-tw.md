---
title: "為什麼選擇 PGMQ？在 PostgreSQL 實現 ACID 交易的消息隊列"
summary: "當你的架構只需要 Postgres 時，為何還要引入額外的 MQ？本文探討 PGMQ 在輕量級非同步任務中的優勢，教你如何用 Docker 快速架設，並整合至 Python 專案中。"
description: "PGMQ 提供類似 AWS SQS 的功能但運行於 Postgres 之上。本文介紹如何設定 PGMQ，並重點展示如何透過 Python SQLAlchemy 整合，確保消息與業務數據操作的一致性。"
date: 2024-07-03T21:46:28+08:00
slug: "pgmq-docker-compose"
tags: ["blog","zh-tw","backend","postgresql"]
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

> https://github.com/pgmq/pgmq  
> **PGMQ** 是一個基於 PostgreSQL 的輕量消息隊列  
> 使用 PostgrSQL Extension 實現  

因為只有基於 PostgreSQL 
所以對於需要非同步處理的輕量業務需求非常適合  

目前使用的情境是以原有的 API Server + PGMQ + consumer  
來做一些非同步任務和第三方服務的 retry 機制  

> 更廣泛的來說  
> 尤其是在業務場景當前只有 PostgreSQL 而不想額外引入 RabbitMQ, 或各大雲端服務的消息隊列解決方案，但是需要 Pub/Sub, SQS 相似的應用場景時  
> PGMQ 是一個不錯的選擇

## PGMQ vs AWS SQS / GCP Pub/Sub / RabbitMQ / Redis / Apache Kafka

個人認為 Kafka 其實不應該與這邊列出的消息隊列做比較  
因為 Kafka 內的消息應該是 "data point" 而不是 "task"  
適合使用在 data streaming 等，需要傳輸大量 "數據" 的場景  
當然也可以把 Kafka 當成 MQ 來用，但這樣有點 overkill

與剩下可以作為消息隊列的技術相比較:  
**PGMQ 是對標與 AWS SQS 一樣的功能**  
如: PGMQ 有實作 `visibility timeout`, `delayed message`, `read_count` 等  
所以我們其是在實在比較 AWS SQS 與剩下的可以作為消息隊列技術的 trade-off  

如果單純比較 PGMQ 與 AWS SQS 的話  
我認為對於消息隊列來說**有幾個優勢**:  

- 達到 **消息與數據的一致性**: 因為 PGMQ 是基於 PostgreSQL 的 Extension  
  所以**可以在同一個 Transaction 中同時處理業務邏輯和消息隊列操作**  
  確保消息與業務數據的操作是 ACID 的
- 無需額外基礎設施: PGMQ 只需要 PostgreSQL 就可以運行

當然也有**相對應的缺點**:

- **Postgres 本身的性能限制**: PGMQ 的性能受到 (Write Ahead Log, Lock contention, MVCC 等) PostgreSQL 本身在寫入性能瓶頸限制。
- **團隊需要對 PostgreSQL 有足夠的了解**: 特別是在性能調優、PostgreSQL Extension 的使用和上述的限制方面。


## 安裝


### PGMQ Docker Image

- 先確認系統是否有安裝:
  - Docker
  - Docker Compose

最簡單的方式是直接使用 PGMQ 官方的 Docker Image  

```bash
docker run -d --name pgmq-postgres -e POSTGRES_PASSWORD=postgres -p 5432:5432 ghcr.io/pgmq/pg18-pgmq:latest
```

### 從 Extension 安裝

如果想要用原本的 `postgres` Image 以 Extension 的方式安裝:

1. 下載最新 PGMQ 的 SQL 和 Control 檔案
```bash
curl -o pgmq.sql https://raw.githubusercontent.com/pgmq/pgmq/main/pgmq-extension/sql/pgmq.sql
curl -o pgmq.control https://raw.githubusercontent.com/pgmq/pgmq/main/pgmq-extension/pgmq.control
```
2. 更新 `docker-compose.yml` 加上 Volume 的設定
- `db.sql` 是一些初始化的 SQL 檔案(看專案有沒有需要)
- `pgmq.sql` 和 `pgmq.control` 是 PGMQ 的 SQL 和 Control 檔案
  - 而 `pgmq--1.3.3.sql` 的版本號需要看 `pgmq.control` 內的版本號
- `stateful_volumes/postgresql` 是 `postgres` container 持久化 mount 的目錄
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

3. 啟動 `postgres` container
> 如果原本有跑過 `postgres` container 記得先把 volume 刪掉 !
```bash
docker compose up postgres -d
```

## 使用

這邊都以 Python 來作為使用 PGMQ 的範例

### PGMQ-SQLAlchemy

對我來說，應該沒有任何 Python 後端專案不是使用 SQLAlchemy ORM 來操作資料庫的吧？  
但是 PGMQ 官方的 Python package 並沒有支援 SQLAlchemy ORM，這對於需要整合 PGMQ 到現有的專案會是一個大問題

所以我寫了一個 [pgmq-sqlalchemy](https://github.com/jason810496/pgmq-sqlalchemy) 這個 package 來支援 SQLAlchemy ORM 來操作 PGMQ

- **安裝 `pgmq-sqlalchemy`**
  ```bash
  pip install pgmq-sqlalchemy
  ```
  - 也可以依據現有專案使用的 PostgreSQL driver 安裝對應的 package

    ```bash
    # psycopg
    pip install pgmq-sqlalchemy[psycopg]

    # asyncpg
    pip install pgmq-sqlalchemy[asyncpg]
    ```

    > 所有支援的 extras 可以參考 [`pgmq-sqlalchemy` 的 PyPi page](https://pypi.org/project/pgmq-sqlalchemy/)

- **使用 `pgmq-sqlalchemy`**
  1. **直接使用 `PGMQueue` class 來操作 PGMQ**

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

      完整範例可以參考 [pgmq-sqlalchemy/examples/fastapi_pub_sub/consumer.py](https://github.com/jason810496/pgmq-sqlalchemy/blob/main/examples/fastapi_pub_sub/consumer.py)

  2. **使用 `op` 模組與 SQLAlchemy ORM Session 搭配使用**

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

      完整範例可以參考 [pgmq-sqlalchemy/examples/fastapi_pub_sub/api.py](https://github.com/jason810496/pgmq-sqlalchemy/blob/main/examples/fastapi_pub_sub/api.py)

### PGMQ Python Client

- **安裝 `pgmq` Python Client**
    ```bash
    pip install pgmq
    ```
    > 因為 `pgmq` 是直接使用 `psycopg` ( 是 `psycopg3` 不是 `psycopg2` )  
    > 在 Mac 上如果用 `poetry` 安裝會有問題  
    > 所以建議直接用 `pip` 安裝  

- **使用 `pgmq` Python Client**

    [pgmq 的 README](https://github.com/pgmq/pgmq/tree/main/pgmq) 其實寫的蠻清楚的，主要就是 `PGMQueue` 和 `Message` 兩個 data class  
    而 `vt` 是 `visibility timeout` 的縮寫，是指消息在被讀取後有多久的時間內不會再被讀取  

    以下是一個簡單的範例:
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

    如果要看更多的範例可以參考 [`pgmq` 的 README](https://github.com/pgmq/pgmq/tree/main/pgmq) 


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