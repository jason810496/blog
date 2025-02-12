---
title: "什麼是 Embedded Database？ 簡介 RocksDB"
summary: "簡介 Embedded Database 和 RocksDB 的基本概念"
description: "Embedded Database 與 RocksDB 的簡單介紹"
date: 2025-02-12T00:57:41+08:00
slug: "what-is-embedded-database"
tags: ["blog","zh-tw","database"]
# series: ["Documentation"]
# series_order: 9
cascade:
  showEdit: true
  showSummary: true
  hideFeatureImage: false
draft: false
---

> 封面來自 [`rocksdb`](https://rocksdb.org/) 官方文件。

{{< alert "circle-info">}}

這篇文章談論的是**Embedded Database**，而非**Embedding Database (Vector Database)**。

{{< /alert >}}

最近我剛好看到 **Embedded Database**，所以順手紀錄一下 !

# 什麼是Embedded Database？

**Embedded Database**是一種緊密整合到應用程式中的 DBMS，它在同一個程序中執行。與傳統的 Client-Server 資料庫不同，Embedded Database 不需要單獨的伺服器來管理查詢和交易。這使得它們對於需要快速、本機資料儲存且**沒有網路通訊的 overhead**的應用程式來說，效率非常高。

![Application with Traditional Database](https://raw.githubusercontent.com/erhwenkuo/rocksdb-lab/refs/heads/master/docs/c-s-with-fast-storage.png)

![Application with Embedded Database](https://raw.githubusercontent.com/erhwenkuo/rocksdb-lab/refs/heads/master/docs/architecture-embed-db.png)

> 上述圖片引用自 [@erhwenkuo](https://github.com/erhwenkuo) 的 [rocksdb-lab](https://github.com/erhwenkuo/rocksdb-lab/blob/master/)

## RocksDB 簡介

目前最受歡迎的Embedded Database之一是 **RocksDB**，它是由 Facebook 開發的開源、高效能Key-Value儲存。RocksDB 基於 **LevelDB**，但針對更好的寫入效能、更低的延遲和高擴展性進行了優化。

### RocksDB 的主要特性

- **Log-Structured Merge (LSM) 樹**: RocksDB 使用 LSM 樹來優化寫入操作，並實現快速的資料導入。
- **針對 SSD 優化**: 它利用現代 SSD 儲存來實現高效的讀/寫操作。
- **可配置壓縮**: 支援多種壓縮演算法，如 Zstandard 和 Snappy，以優化儲存。
- **高並發**: 支援多個讀寫操作同時進行，而不會降低效能。
- **點查詢和範圍查詢**: 允許個別Key-Value檢索和高效的範圍掃描。

### RocksDB 的容錯能力

RocksDB 的設計具有彈性，可應對故障，並提供多種功能來確保資料持久性和復原：

- **Write-Ahead Logging (WAL)**: 透過在提交變更之前記錄變更，確保資料完整性。
- **Snapshots**: 透過捕捉特定時刻的資料庫狀態，實現時間點復原。
- **自動復原**: 重新啟動後，RocksDB 可以偵測到不一致並從 WAL 中復原資料。
- **Replication**: 可以配置 RocksDB 進行複寫，以在分散式系統中提供更高的可用性。

### RocksDB 的應用場景

RocksDB 廣泛應用於需要高速資料處理和高效儲存解決方案的應用程式中，其中大多數將 RocksDB 作為**storage engine**：

- **Real-time streaming**: 整合到 Apache Kafka Streams 等系統中，用於狀態管理。
- **Real-time stateful stream processing**: 用於 Apache Flink 等系統中，進行 stateful stream processing。
- **Distributed object storage**: 用於 Apache Ozone 等系統中，用於 Distributed object storage 中的metadata儲存。

> [RocksDB Users and Their Use Cases](https://github.com/facebook/rocksdb/wiki/RocksDB-Users-and-Use-Cases)

## 範例：在 Python 中使用 RocksDB

讓我們看一個在 Python 中使用 RocksDB 儲存和檢索Key-Value Pair的簡單範例。

**Note**: <br>
對於 RocksDB 本身，它提供 C++ 和 Java API，但對於 Python，可以使用 `rocksdict` 套件，它提供了 RocksDB 的 Pythonic 介面。

### 安裝

使用 `uv` 安裝 RocksDB 的 Python bindings:

```sh
uv pip install rocksdict
```

> [RocksDict](https://github.com/rocksdict/RocksDict)

### Sample Code

```python
import rocksdict

# 開啟 RocksDB 資料庫
db = rocksdict.Rdict("./testdb")

# 插入資料
db[b"name"] = b"Alice"
db[b"age"] = b"25"

# 檢索資料
print(db[b"name"].decode())  # 輸出: Alice
print(db[b"age"].decode())   # 輸出: 25

# 關閉資料庫
db.close()
```

## 關於 RocksDB 的更多操作

RocksDB 提供了更進階的操作，可以有效地管理資料：

- **Snapshotting**: 建立資料庫的快照，以捕捉其在特定時刻的狀態。
- **Batch Writes**: 原子性地執行多個寫入操作，以獲得更好的效能。
- **Iterators**:: 有效率地遍歷資料庫中的Key-Value Pair。
- **Transactions**: 確保多個讀寫操作的原子性和一致性。
- **Column Families (列族)**: 將資料組織成多個列族，以更好地管理資料。
- **Statistics**: 使用內建的統計資訊監控資料庫的效能。
- **Observability**: 使用 Prometheus 和 Grafana 等工具監控。

> 對於上述操作，可以參考 [rocksdb-lab](https://github.com/erhwenkuo/rocksdb-lab/tree/master) 上的更多 hands-on 的 Java 範例。


## 參考文獻

- [rocksdb-lab](https://github.com/erhwenkuo/rocksdb-lab/tree/master)
- [RocksDB GitHub 倉庫](https://github.com/facebook/rocksdb)
- [RocksDB 文件](https://rocksdb.org/)
- [RocksDB 部落格](https://rocksdb.blogspot.com/2013/11/the-history-of-rocksdb.html)
- [RocksDB 概念及簡單範例 (中文)](https://blog.csdn.net/weixin_44607611/article/details/113742388)
- [深入了解三大Embedded Database：SQLite、RocksDB 和 DuckDB](https://hackernoon.com/a-closer-look-at-the-top-3-embedded-databases-sqlite-rocksdb-and-duckdb)
