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
draft: false
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
  可以同時啟用 RDB 與 AOF 持久化，以提供更強大的資料保護機制。
  {{< /lead >}}

## RDB: Redis Database

簡而言之，<br>
`RDB` 需要 `fork()` 一個子 process 來建立資料庫的快照到磁碟上。

### `RDB` 的優點

> `RDB` 其實只是一個非常**緊湊的檔案，能夠表示你在某一時間點的 Redis 快照**。
- **省空間**：RDB 比 AOF 更節省空間
- **備份更簡單**：RDB 更容易備份和恢復
  > 因為它是一個單文件，可以把它複製到任何存儲，如 S3、Google Cloud Storage 等。
- **對於大 datasets 能夠更快恢復**：與 `AOF` 相比，`RDB` 在擁有大數據集時能夠更快地恢復

### `RDB` 的缺點

- **數據丟失**：如果你需要最小化數據丟失，`RDB` 並不是一個好的選擇
  > 因為它只在指定的間隔時間保存數據集
- **不適合大數據集**：`RDB` 不適合大數據集
  > 因為它需要 `fork()` 一個子進程來將數據集保存到磁碟 <br>
  > 如果你有一個**大的**數據集，`fork()` 會**很慢** <br>
  > 可能會停止服務客戶端數毫秒甚至數秒！

### `RDB` 的詳細實作

我們提到 `RDB` 需要 `fork()` 一個子進程來將數據集保存到磁碟。<br>

讓我們來看看 Redis 源碼中 `RDB` 的g6yji4。<br>
1. 從 `redis/src/rdb.c`：定義了 `bgsaveCommand` 命令入口函數。
{{< code url="https://raw.githubusercontent.com/redis/redis/811c5d7aeb0b76494d78efe61e418f574c310ec0/src/rdb.c" type="c" startLine="3907" endLine="3942" hl_lines="3937">}}

2. 而 `bgsaveCommand` 實際上會調用 `rdbSaveBackground`。<br>
   `rdbSaveBackground` 會檢查是否已經有子 process 在運行，如果沒有，會調用 `redisFork` 來 fork 一個子進程將數據集保存到磁碟。
{{< code url="https://raw.githubusercontent.com/redis/redis/811c5d7aeb0b76494d78efe61e418f574c310ec0/src/rdb.c" type="c" startLine="1612" endLine="1646" hl_lines="1615,1621" >}}

{{< alert "circle-info">}}
由於 `fork()` 是一個system call ，它會將 parent process 的**整個 memory**複製到子進程。這就是為什麼當你有一個大數據集時，`fork()` 會很慢！
>  Redis 有使用 CoW (Copy-on-Write) 來優化 `fork()`

此外，如果你有一個大數據集並且**剩餘記憶體有限**，這可能會導致 **OOM (Out of Memory)**。

{{< /alert >}}

## AOF： Append Only File

`AOF` 利用 `fsync()` system call 將每次寫操作保存到磁碟。
> 就像關聯數據庫中的 WAL (Write-Ahead Logging)
`fsync` 在後台執行，以避免阻塞 Redis 主事件循環。

`AOF` 有三種 `fsync` 策略：
- `always`：每次寫操作後都進行 `fsync()`
- `everysec`：每秒進行一次 `fsync()` (**默認**)
- `no`：只有在明確調用 `fsync()` 時才進行
  > 這是更快但不太安全的方法。<br>
  > 只需將數據交給操作系統處理。通常 Linux 在這種配置下會每 30 秒刷新數據，但這取決於內核的具體調整。

**`AOF` 重寫**：<br>
- Redis 將在後台重寫 `AOF` 文件，避免文件變得過大。
- `serverCron` 會檢查 `AOF` 文件是否過大，如果是，會調用 `rewriteAppendOnlyFileBackground` 在後台重寫 `AOF` 文件。
> 類似於 RDB，**`AOF` 重寫** 也需要 `fork()` 一個子進程將數據集保存到磁碟。<br>
> 當你有一個大數據集時，可能會遇到與 `RDB` 相同的問題。

### `AOF` 的優點

- **丟失較少數據**：如果你需要最小化數據丟失，`AOF` 更好
  > 因為它將每次寫操作保存到磁碟

### `AOF` 的缺點

- **文件大小較大**：`AOF` 文件通常比相應的 `RDB` 文件大
- **比 `RDB` 慢（取決於 `fsync()` 策略）**：
  - 默認的 `everysec` 策略仍然非常高效！
  - 但如果你設置 `always` 策略，它會比 `RDB` 慢，因為它需要在每次寫操作後進行 `fsync()`



## Reference 

- redis: RDB and AOF
  - https://redis.io/docs/latest/operate/oss_and_stack/management/persistence/
  - https://www.littlewaterdrop.com/cs/redis/persistence
- Redis source code explanation
  - RDB
    - https://blog.csdn.net/u012785877/article/details/131281282
  - AOF rewrite
    - https://blog.csdn.net/u012785877/article/details/131283626
  - AOF append
    - https://blog.csdn.net/Nuan_Feng/article/details/129282720
    - https://youjiali1995.github.io/redis/persistence/
    - https://www.jianshu.com/p/70b3115cd604
- Linux : `fork()` and `fsync()`
  - [sysprog : history and detail of `fork()`](https://hackmd.io/@sysprog/unix-fork-exec)
  - [CSDN : Linux I/O : Is data safe after calling `fsync()`?(fsync、fwrite、fflush、mmap、write barriers) ](https://blog.csdn.net/hilaryfrank/article/details/112200420)