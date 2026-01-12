---
title: "PGMQ-SQLAlchemy 0.2.0 Release: Support ACID Transactions and FastAPI Integration"
summary: "PGMQ-SQLAlchemy 0.2.0 introduces support for ACID transactions, enabling developers to handle business logic and message queue operations within the same transaction, ensuring consistency and reliability of data and messages."
description: "This article introduces the new features of PGMQ-SQLAlchemy 0.2.0, specifically the support for ACID transactions. This feature allows developers to handle business logic and message queue operations within the same transaction, ensuring consistency and reliability of data and messages. The article details how to use this new feature, including code examples and practical scenarios, helping developers better understand and apply PGMQ-SQLAlchemy 0.2.0."
date: 2026-01-06T00:00:00+08:00
slug: "pgmq-sqlalchemy-0-2-0"
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

> https://github.com/pgmq/pgmq  
> **PGMQ** is a lightweight message queue based on PostgreSQL.  
> It is implemented using a PostgreSQL Extension.

Since it relies solely on PostgreSQL, it is highly suitable for lightweight business requirements that need a message queue.

Currently, we use it in a scenario with an existing API Server + PGMQ + consumer  
to handle asynchronous tasks and retry mechanisms for third-party services.

> More broadly,  
> especially in scenarios where your infrastructure currently only includes PostgreSQL and you wish to avoid introducing RabbitMQ or major cloud messaging solutions, yet still require Pub/Sub or SQS-like functionality,  
> PGMQ is a compelling choice.


For more detailed comparisons with other message queues and usage examples, please refer to the following article:  
[Why Choose PGMQ? Implementing ACID Transactional Message Queues in PostgreSQL](/backend/2024-07-03-pgmq/)

## PGMQ-SQLAlchemy 0.2.0 New Features

- **Added [`op` (`PGMQOperation`) module](https://pgmq-sqlalchemy.readthedocs.io/en/latest/api-reference.html#pgmqoperation-op)**: Officially supports handling business logic and message queue operations within the same Transaction, ensuring ACID compliance for both messages and business data.
- **Added [FastAPI, `asyncio` Consumer Pub/Sub Example](https://github.com/jason810496/pgmq-sqlalchemy/tree/main/examples/fastapi_pub_sub)**: Demonstrates how to integrate PGMQ-SQLAlchemy with FastAPI and implement asynchronous message consumers. This example is also included in [System Tests](https://github.com/jason810496/pgmq-sqlalchemy/blob/main/.github/workflows/examples.yml) to ensure functional correctness.
- **Improved [Unit (Integration) Test Coverage](https://app.codecov.io/gh/jason810496/pgmq-sqlalchemy/p)**: Test coverage has reached `98.72%`. Why refer to it as "unit (integration)" testing? Because the CI pipeline [runs tests against a real Postgres DB](https://github.com/jason810496/pgmq-sqlalchemy/blob/main/.github/workflows/codecov.yml), making them effectively integration tests.
- **Official Documentation [Supports Dark Mode](https://pgmq-sqlalchemy.readthedocs.io/en/latest/)**: Switched from [sphinx_rtd_theme](https://sphinx-rtd-theme.readthedocs.io/en/stable/) to [furo](https://pradyunsg.me/furo/) to officially support Dark Mode.

## GitHub Coding Agent

A primary motivation for maintaining this package is to evaluate the effectiveness of [GitHub Coding Agent](https://github.com/copilot/agents). Here are some PRs demonstrating impressive results:

- Leveraged [libCST](https://libcst.readthedocs.io/en/latest/) to parse and modify the Python AST to generate corresponding `async` methods ([#36](https://github.com/jason810496/pgmq-sqlalchemy/pull/36))
- Migrated dependency management from Poetry to uv ([#14](https://github.com/jason810496/pgmq-sqlalchemy/pull/14))
- Added support for Dark Theme ([#47](https://github.com/jason810496/pgmq-sqlalchemy/pull/47))
- Resolved an ambiguous error in pgmq function overloading ([#25](https://github.com/jason810496/pgmq-sqlalchemy/pull/25))
