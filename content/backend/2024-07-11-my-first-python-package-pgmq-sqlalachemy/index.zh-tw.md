---
title: "PGMQ SQLAlachemy - 我的第一個 Python 套件"
summary: "PGMQ 是一個運行在 Postgres 上的輕量級 Message Queue，類似於 AWS SQS 和 RSMQ。 而 pgmq-sqlalchemy 是一個 SQLAlchemy 對 PGMQ 的 Python 客戶端套件。同時也是我嘗試寫的第一個公開 python 套件！"
description: "PGMQ 是一個運行在 Postgres 上的輕量級 Message Queue，類似於 AWS SQS 和 RSMQ。 而 pgmq-sqlalchemy 是一個 SQLAlchemy 對 PGMQ 的 Python 客戶端套件。同時也是我嘗試寫的第一個公開 python 套件！"
date: 2024-09-19T14:31:37+08:00
slug: "my-first-python-package-pgmq-sqlalachemy"
tags: ["blog","zh-tw","python","postgresql","sqlalchemy"]
# series: ["Documentation"]
# series_order: 9
cascade:
  showEdit: true
  showSummary: true
  hideFeatureImage: false
draft: false
---

## 關於 PGMQ (PostgreSQL Message Queue)  的介紹與設定

> https://github.com/tembo-io/pgmq <br>
> **PGMQ** 是一個基於 PostgreSQL 的輕量消息隊列 <br>
> 使用 PostgrSQL Extension 實現 <br>

可以參閱

{{< article link="/backend/pgmq/" >}}

## 動機

因為[PGMQ 官方的 Python Package]()是使用[psycopg DBAPI]() ([是 psycopg3 非 psycopg2](https://www.psycopg.org/psycopg3/docs/basic/from_pg2.html) ) 作為 Postgres 的 Connect Driver <br>
而在最近專案使用的 Python Postgres Driver 是 [SQLAlchemy](https://www.sqlalchemy.org/) + [psycopg2](https://www.psycopg.org/docs/) <br>

<br>

發現應該可以寫一個 SQLAlchemy 的 Client 套件來連接 PGMQ <br>
應該對於大部分使用 Python 寫後端的其他開發者會比較方便 ! <br>

## 名詞解釋


在深入實作之前，我們有些名詞需要先了解 <br>
例如前面提到的這些 **Postgres Driver** 的 **Driver** 或 **DBAPI** 是什麼呢？ <br>

### PEP 249 – Python Database API Specification v2.0

其中最重要的就是 **DBAPI** 了！ <br>
Python 的社群有對各種開發實作制定一些規範或介面 <br>
這些都被稱為 **PEP** (Python Enhancement Proposals) <br>
> 與 Web3 很常聽到的 RFC (Request for Comments) 類似 <br>

<br>

而 **DBAPI** (Database API) 就是 Python 的資料庫介面規範 <br>
而 Python 的 DBAPI 有分為 1.0 和 2.0 兩個版本 <br>

- [PEP 248: Python Database API Specification v1.0](https://www.python.org/dev/peps/pep-0248/)
- [PEP 249: Python Database API Specification v2.0](https://www.python.org/dev/peps/pep-0249/)

現在大多人在使用的 Python Postgres Driver 如 [psycopg2](https://www.psycopg.org/docs/) 、[psycopg3](https://www.psycopg.org/psycopg3/docs/) 、[asyncpg](https://magicstack.github.io/asyncpg/current/) 都是實作了 **DBAPI 2.0** 介面 <br>

<br>

而 **DBAPI 2.0** 明確規範了 Python 資料庫連接的介面如： <br>
- **module interface**
  - 使用 `connect()` 方法來建立連接
  - `paramstyle` 來定義 SQL 參數的格式
- **Connection** 是 DBAPI 的連接物件 <br>
  - `cursor()` 方法來取得 **Cursor** 物件 <br>
  - `commit()` 和 `rollback()` 方法來提交或回滾交易 <br>
- **Cursor** 代表一個 Database Connection 的指針 <br>
  - `execute()` 和 `executemany()` 方法來執行 SQL 語句 <br>
  - `fetchone()`、`fetchmany()` 和 `fetchall()` 方法來取得查詢結果 <br>

### Driver

而 **Driver** 就是實作了 **DBAPI** 的資料庫連接驅動程式 <br>
例如 [psycopg2](https://www.psycopg.org/docs/) 、[psycopg3](https://www.psycopg.org/psycopg3/docs/) 、[asyncpg](https://magicstack.github.io/asyncpg/current/) <br>

這些 **Driver** 大多照著 **DBAPI** 規範實作，不過不完全相同或完全按照 **DBAPI** 規範 <br>
以 `paramstyle` 為例： <br>
> [paramstyle]() 是用來定義 `cursor.execute()` 方法中 SQL 參數的格式 <br>

- psycopg2 與 psycopg3 使用的是 `format` 格式
- asyncpg 使用的是類似 `numeric` 格式 ( 沒有按照 DBAPI 規範 )

### SQLAlchemy Postgres Dialects

SQLAlchemy 是 Python 的 ORM 套件 <br>
並支援大部分的 Postgres Driver <br>
> [SQLAlchemy Postgres Dialects](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html) <br>

而 SQLAlchemy 是使用 `named` 格式的 SQL 參數格式 <br>