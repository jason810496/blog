---
title: "PGMQ-SQLAlchemy 0.2.0: 支援業務邏輯和消息隊列的 ACID 交易、FastAPI 範例與 Dark Mode 文件"
summary: "解決了 PGMQ 官方 Client 不支援 SQLAlchemy 的痛點，PGMQ-SQLAlchemy 0.2.0 可以在 PostgreSQL 中同時 commit 業務數據與消息，確保絕對的一致性。"
description: "PGMQ-SQLAlchemy 0.2.0 重大更新：新增 op 模組支援 Transaction ACID，確保數據一致性。包含 FastAPI 整合範例、測試覆蓋率提升至 98% 以及全新的 Furo 文件主題。"
date: 2026-01-06T00:00:00+08:00
slug: "pgmq-sqlalchemy-0-2-0"
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


與其他消息隊列更詳細的比較與使用範例可以參考以下文章：  
[為什麼選擇 PGMQ？在 PostgreSQL 實現 ACID 交易的消息隊列](/backend/2024-07-03-pgmq/)

## PGMQ-SQLAlchemy 0.2.0 新功能介紹

- 新增 [`op` (`PGMQOperation`) 模組](https://pgmq-sqlalchemy.readthedocs.io/en/latest/api-reference.html#pgmqoperation-op): 正式 **支援在同一個 Transaction 中同時處理業務邏輯和消息隊列操作，確保消息與業務數據的操作是 ACID 的**
- 新增 [FastAPI, `asyncio` Consumer 的 Pub/Sub 範例](https://github.com/jason810496/pgmq-sqlalchemy/tree/main/examples/fastapi_pub_sub): 示範如何在 FastAPI 中使用 PGMQ-SQLAlchemy，並實現非同步的消息消費者，這個 example 也被加在 [系統測試](https://github.com/jason810496/pgmq-sqlalchemy/blob/main/.github/workflows/examples.yml) 中來保證功能的正確性
- 提高[單元(整合)測試覆蓋率](https://app.codecov.io/gh/jason810496/pgmq-sqlalchemy/): 目前單元(整合)測試覆蓋率達到 `98.72%`，為什麼說是 "單元(整合)" 測試呢? 因為 CI [使用真實的 Postgres DB 來跑測試](https://github.com/jason810496/pgmq-sqlalchemy/blob/main/.github/workflows/codecov.yml)，所以也可以算是整合測試
- 官方文件[支援 Dark Mode](https://pgmq-sqlalchemy.readthedocs.io/en/latest/): 把 [sphinx_rtd_theme](https://sphinx-rtd-theme.readthedocs.io/en/stable/) 換成 [furo](https://pradyunsg.me/furo/) 正式支援 Dark Mode

## GitHub Coding Agent

還會想繼續維護這個 package 主要是因為想測試 [GitHub Coding Agent](https://github.com/copilot/agents) 的效果如何，以下是一些我覺得成果還不錯的 PR:

- 使用 [libCST](https://libcst.readthedocs.io/en/latest/) 來解析並修改 Python AST 來生成相對應的 `async dev` methods ([#36](https://github.com/jason810496/pgmq-sqlalchemy/pull/36))
- 把 Poetry 換成 uv 來管理相依套件 ([#14](https://github.com/jason810496/pgmq-sqlalchemy/pull/14))
- 支援 Dark Theme ([#47](https://github.com/jason810496/pgmq-sqlalchemy/pull/47))
- 修正 pgmq function overloading 的 ambiguous error ([#25](https://github.com/jason810496/pgmq-sqlalchemy/pull/25))
