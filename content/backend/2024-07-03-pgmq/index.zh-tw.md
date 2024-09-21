---
title: "PGMQ(PostgreSQL Message Queue) 設定"
summary: "PGMQ 是一個運行在 Postgres 上的輕量級 Message Queue，類似於 AWS SQS 和 RSMQ。 本篇介紹如何使用使用 Docker Compose 設定 PGMQ 並以官方 Python 客戶端連接"
description: "PGMQ 是一個運行在 Postgres 上的輕量級 Message Queue，類似於 AWS SQS 和 RSMQ。 本篇介紹如何使用使用 Docker Compose 設定 PGMQ 並以官方 Python 客戶端連接"
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

## PGMQ(PostgreSQL Message Queue) 


{{< github repo="tembo-io/pgmq" >}}

> https://github.com/tembo-io/pgmq <br>
> **PGMQ** 是一個基於 PostgreSQL 的輕量消息隊列 <br>
> 使用 PostgrSQL Extension 實現 <br>

因為只有基於 PostgreSQL 
所以對於需要 MQ 的輕量業務需求非常適合 <br>

目前使用的情境是以原有的 API Server + PGMQ + consumer <br>
來做一些非同步任務和第三方服務的 retry 機制 <br>

## 安裝


### Tembo Docker Image

- 先確認系統是否有安裝:
  - Docker
  - Docker Compose

最簡單的方式是直接使用 Tembo 官方的 Docker Image <br>

```bash
docker run -d --name postgres -e POSTGRES_PASSWORD=postgres -p 5432:5432 quay.io/tembo/pg16-pgmq:latest
```

### 從 Extension 安裝

如果想要用原本的 `postgres` Image 以 Extension 的方式安裝:

1. 下載最新 PGMQ 的 SQL 和 Control 檔案
```bash
curl -o pgmq.sql https://raw.githubusercontent.com/tembo-io/pgmq/main/pgmq-extension/sql/pgmq.sql
curl -o pgmq.control https://raw.githubusercontent.com/tembo-io/pgmq/main/pgmq-extension/pgmq.control
```
2. 更新 `docker-compose.yml` 加上 Volume 的設定
- `db.sql` 是一些初始化的 SQL 檔案(看專案有沒有需要)
- `pgmq.sql` 和 `pgmq.control` 是 PGMQ 的 SQL 和 Control 檔案
  - 而 `pgmq--1.3.3.sql` 的版本號需要看 `pgmq.control` 內的版本號
- `stateful_volumes/postgresql` 是 `postgres` container 持久化 mount 的目錄
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

3. 啟動 `postgres` container
> 如果原本有跑過 `postgres` container 記得先把 volume 刪掉 !
```bash
docker compose up postgres -d
```

## PGMQ Python Client

- 安裝 `pgmq` Python Client
```bash
pip install tembo-pgmq-python
```
> 因為 `tembo-pgmq-python` 是直接使用 `psycopg` ( 是 `psycopg3` 不是 `psycopg2` ) <br>
> 在 Mac 上如果用 `poetry` 安裝會有問題 <br>
> 所以建議直接用 `pip` 安裝 <br>

- 使用 `pgmq` Python Client

[tembo-pgmq-python 的 README](https://github.com/tembo-io/pgmq/tree/main/tembo-pgmq-python) 其實寫的蠻清楚的，主要就是 `PGMQueue` 和 `Message` 兩個 data class <br>
而 `vt` 是 `visibility timeout` 的縮寫，是指消息在被讀取後有多久的時間內不會再被讀取 <br>

以下是一個簡單的範例:
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

如果要看更多的範例可以參考[tembo-pgmq-python的 README](https://github.com/tembo-io/pgmq/tree/main/tembo-pgmq-python) 


## Reference

- https://github.com/tembo-io/pgmq
- https://www.psycopg.org/psycopg3/docs/basic/install.html
- https://github.com/tembo-io/pgmq/tree/main/tembo-pgmq-python
- https://stackoverflow.com/questions/59901605/postgres-error-installing-my-own-extension