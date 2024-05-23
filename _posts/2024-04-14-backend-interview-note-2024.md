---
title: Baackend Interview Note 2024
subtitle: Ngrok 的替代方案
date:   2023-09-15 16:00:00 +0800

tag: [notes]

thumbnail-img: "https://raw.githubusercontent.com/jason810496/blog/main/_images/20230915_tunnel.png" #1:1 (450:450)

cover-img: "https://raw.githubusercontent.com/jason810496/blog/main/_images/20230915_start_tunnel.png"

comments: true

# ======= Other parameters ========
layout: post
readtime: true

# test local : bundle exec jekyll serve
---



# Backend Internview Note 2024

## OAuth 2.0


## CORS

## TCP/UDP

![截圖 2024-04-15 下午12.49.29](https://hackmd.io/_uploads/Sy_1MN5xA.png)

### TCP Flow
1. Client 跟 Server 要求連線封包
2. Server 接收並確認封包
    - 也會傳一個相對應的封包給 Client
    - Wait
3. Client 收到 Server 的封包後
    - = 確認 1. 的封包有正確接收
    - 如果 Client 也同意與 Server 建立連線
    - 會再回傳一個確認封包給 Server
4. Server 也收到後
    - 完成 3 項交握
    - 建立連線

### TCP Feature

- 建立完連線後
    - 會對 packet 加上序號
- 利用 Sliding window 傳輸
    - 不是一個一個傳

- 完整性：
    - 接收端能夠確認封包是否傳送完畢，判斷是否有缺漏。
- 重傳處理：
    - 當發現有缺少封包或者逾時，則會在一定的時間內重新傳送。
- 順序性：
    - 封包的序號可以確保接收方在收到封包時，重建順序。

reference:
https://www.explainthis.io/zh-hant/swe/tcp-udp

### UDP

![UDP Flow](https://explainthis.s3-ap-northeast-1.amazonaws.com/7f2f72eec9a5476b90d8ce8e1d65d09a.png)

- Server 不需要確認 Client 使否接收到 packet
- Header 比較少
- 少一些確認機制


## HTTP 1 1.1 2

### HTTP/1

- 每次發 Request 都需要先建立一個新連線
    - ( TCP 連線 )

### HTTP/1.1
- HTTP/1.1 解決什麼？
- `keep-alive` : 持久連接
- ==**同一個 TCP 連接**可以**重複多個 HTTP 請求**==
- 更多 HTTP Method
    - `PUT`
    - `PATCH`
    - `DELETE`

### Head-of-Line blocking (HOL)


- Server 是 FIFO 處理
- 但最前面有一個很大的文件要 response

Exampe:
```
1: script.js
2: style.css

11111111111111111112 
# 2 被 1 Block 住了
```

### HTTP/2

- HTTP/2 為了解決 

- https://www.explainthis.io/zh-hant/swe/http1.0-http1.1-http2.0-difference

### TLS

## Git

### rebase

### cherry pick

## Postgres: View

## SQL

## ACID

在 Database 處理 Transaction 需要注意的事情

### Atomicity : 原子性

- 一個 transaction 要麼全部執行，要麼全部不執行
- 如果中間出錯就被 rollback
- 如果中間沒出錯，就 commit

### Consistency : 一致性

- 在事務開始之前和事務結束以後，資料庫的完整性沒有被破壞。
- 這表示寫入的資料必須完全符合所有的預設約束
- 不同的數據都會有一些基本的約束，而這些約束在交易前跟交易後都必須要遵守

### Consistency: Example

- 雙方的錢都不能小於 0
- 雙方錢的總和不能改變

上面兩個限制在交易前跟交易後都必須要遵守，這就是一致性

## Isolation : 事務隔離
- snapshot isolation
    - in `Postgres` 
        - Read Committed
    - MVCC : multi-version concurrency control
- repeatable read
- serializable : 可串列化

## Durability : 持久性

- 事務處理結束後，對數據的修改就是永久的
- 即便系統故障也不會丟失
        

## Postgres Isolation

:::warning
default isolation level is **`Read Committed`**
:::


![截圖 2024-04-14 下午4.14.13](https://hackmd.io/_uploads/SyDwezYl0.png)

### phantom read : 幻讀 

> 導致寫入偏差的幻讀

只有 **Serializable** 可以解決幻讀問題
> 或是使用 **Lock** 來解決

Example:
預約會議室：
- 有一個 transaction 搜尋一個時間區段的會議室現有的預定
- 則另一個 transaction 不能同時插入或更新通一時間區段的預定
    > ( 但可以同時插入其他房間的預定 <br>
    > 或是在不影響另一個預定條件下，預定同一房間的其他時段 )
    
```SQL
SELECT * FROM bookings
WHERE room_id = 123 AND
      end_time > '2018-01-01 12:00' AND
      start_time < '2018-01-01 13:00';
```

#### Common Issue 

- `SELECT FOR UPDATE` 有時候會有 Deadlock 的問題
    - Thread-1 run `SELECT` and acquire row lock .
    - Thread-2 run `SELECT` 
        - Thread-2 enters the lock's wait queue.
    - Thread-1 run `UPDATE` / `COMMIT` and release lock.
    - Thread-2 acquires the lock.
        - Detects that the row has been updated since its `SELECT`
        - It rechecks the data against its WHERE condition. 
            - The check fails
            - the row is filtered out of the result set
            - but **the lock is still held !!!!!**
- common solution : 
    - SELECT ... SKIP LOCKED 
    - retry-loop approach would be to skip the SELECT altogether, and just run an UPDATE ... WHERE locked = false, committing each time. 
    - The easiest way might be to implement acquire as SELECT FROM my_locks FOR UPDATE, release simply as COMMIT, and let the processes contend for the row lock. If you need more flexibility (e.g. blocking/non-blocking calls, transaction/session/custom scope), advisory locks should prove useful.

> https://stackoverflow.com/questions/31850567/strange-deadlock-postgresql-deadlock-issue-with-select-for-update#answers

#### Solution
1. 將 Isolation 設為 **Serializable**
    - Cons:
        - 會導致 throughput 下降
2. 一樣在預設的 Isolation 
    - 不過在 Redis 上 Lock
        - 防止超賣 
            - ( Redis 是 single-thread , 可以用 Lua Script 達到 Atomic 操作)
        - 物化鎖
        - 在 Redis 上去得 Lock 後再去更新 DB
            - 應該算一種：Write Back （？
        


### Read Committed

其他更複雜的使用狀況，在 Read Committed 模式中可以產生出並非期望的結果。例如考慮一個 DELETE 指令，要操作正好從它的限制條件中加入和移除的資料，像是假設 website 是一張有兩個資料列的表格，其中 website.hits 分別為 9 和 10：

```SQL
BEGIN;
UPDATE website SET hits = hits + 1;
-- run from another session:  DELETE FROM website WHERE hits = 10;
COMMIT;
```

即使在 UPDATE 之前與之後，都存在 website.hits = 10 的資料列，但 DELETE 指令不會產生任何影響。這是因為更新前值為 9 的資料列已經被忽略了，並且當 UPDATE 執行完成且 DELETE 取得鎖，新的資料列的值已經不是 10 而是 11，不再滿足限制條件了。

### Repeatable Read

Repeatable Read（重複讀取） 隔離等級只會看到在交易開始前已經被提交的資料；它永遠不會看見尚未提交的資料或者在交易期間被並行交易提交的變更。

### Serializable

Serializable（序列化） 隔離等級提供了最嚴格的交易隔離。這個等級模擬了對所有提交的交易的一系列交易執行；如同交易們被一個接著一個地執行，連續地、而不是並行地。


### About concurrent control
- 
- https://ithelp.ithome.com.tw/articles/10302070
- https://notes.andywu.tw/2022/%E6%B7%BA%E8%AB%87mysql%E9%9A%94%E9%9B%A2%E5%B1%A4%E7%B4%9A%E7%82%BA%E5%8F%AF%E9%87%8D%E5%BE%A9%E8%AE%80%E6%99%82%E4%B8%8D%E8%83%BD%E9%81%BF%E5%85%8D%E5%B9%BB%E8%AE%80/

## Redis 

### RDB vs AOF

## Sharding

### Cross Shards Transations

## Cache Stratege

https://www.ifb.me/blog/backend/kong-zhi-shu-ju-yi-z

## Cache Stratege : Read
- Cache Aside vs Read Through
    - 進行  read from db 誒update cache 的 **角色不同**
        - Cache Aside 的角色都是 AP
        - Read Through 的角色都是 Cache 本身
- Cache Aside : 
    1. AP read from cache
    2. AP cache miss
    3. AP read from db
    4. AP get data from DB
    5. AP update cache 
- Read Through : 
    1. AP read from cache
    2. Cache Miss
    3. Cache read from db
    4. Cache get data from DB
    5. Cache update cache

## Write Stratege : Write

- Write Around
    1. AP write to db
    2. read from cache if data exists in cache
    3. read from db if data not exists in cache
        - update cache
- Write Back
    1. AP write to cache
    2. write to cache constantly
    3. write to db in a while
- Write Through
    1. AP write to db
    2. update cache

## Parition




