---
title: "Redis 持久化設定：RDB 與 AOF"
summary: "Redis 持久化設定：RDB 與 AOF"
description: "為什麼 Redis 需要持久化？ 詳細解說 Redis 持久化設定：RDB 與 AOF"
date: 2024-06-18T23:10:43+08:00
slug: "redis-persistence-RDB-AOF"
tags: ["blog","zh-tw","database","redis"]
# series: ["Documentation"]
# series_order: 9
cascade:
  showEdit: true
  showSummary: true
  hideFeatureImage: false
draft: true
---

# Redis 持久化設定：RDB 與 AOF

## 為什麼需要 Redis 持久化？

因為 Redis 是一個 in-memory 的資料庫
所以當 Redis 服務重啟時，所有資料都會消失

不過可以透過持久化設定
讓 Redis 在重啟時，能夠恢復狀態 !

## Redis 持久化設定

Redis 提供了兩種持久化設定
分別是 **RDB** 與 **AOF**

- **RDB**：Redis Database
  {{< lead >}}
  RDB 會在**指定的間隔時間內**執行對資料庫的**快照** (snapshot)。
  {{< /lead >}}
- **AOF**：Append Only File
  {{< lead >}}
  AOF 會將伺服器接收到的每個寫入操作**記錄**下來。這些操作可以在伺服器啟動時**重新執行**，以重建原始資料集。
  {{< /lead >}}
- **RDB+AOF**：RDB 與 AOF
  {{< lead >}}
  您可以同時啟用 RDB 與 AOF 持久化，以提供更強大的資料保護機制。
  {{< /lead >}}

## RDB