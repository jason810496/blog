---
title: "2024 Dcard 暑期實習後端作業"
summary: "2024 Dcard 暑期實習後端作業"
description: "2024 Dcard 暑期實習後端作業"
date: 2024-09-21T21:52:52+08:00
slug: "dcard-backend-intern-assignment-2024"
tags: ["blog","zh-tw","backend","intern","system-design","dcard"]
# series: ["Documentation"]
# series_order: 9
cascade:
  showEdit: true
  showSummary: true
  hideFeatureImage: false
draft: false
---

關於面試 Dcard 的記錄放在： <br>

{{< article link="/zh-tw/intern/summer-intern-interview-2024-appier/" >}}

本篇著重在實際分析、設計、實作 Dcard 2024 後端暑期實習作業。 <br>
最後的實作是放在： <br>

{{< github repo="jason810496/Dcard-Advertisement-API" >}}

- [直接跳到: Final Solution](#final-solution)
- [直接跳到: 系統架構](#系統架構)
- [直接跳到: 實作](#實作)

## 作業說明

完整的作業說明放在： <br>
https://github.com/jason810496/Dcard-Advertisement-API/blob/main/2024%20Backend%20Intern%20Assignment.pdf <br>
以下是簡化的說明：

### 情境

用 Golang 實作一個簡化的**廣告投放服務**，服務包括 2 個 RESTful API <br>
1. 管理者 API: 帶入廣告的條件來建立廣告
2. 投放 API: 依據搜索條件列出所有符合的廣告

### 詳細說明

#### 管理者 API

> 只需要實作 Create 不用 List/ Update/ Delete <br>
欄位結構：
- `Title`: 廣告標題
- `StartAt`: 廣告開始活躍時間
- `EndAt`: 廣告結束活躍時間
- `Conditions`: 廣告顯示條件
  - 每個條件都是 **optional**
  - 每個條件可以是 **多選**
  - 條件結構：
    - `Age`: `int:1~100`
    - `Gender`: `enum:M, F`
    - `Country`: `enum:TW, JP, ...` 符合 ISO 3166-1
    - `Platform`: `enum:android, ios, web`

#### 投放 API

> 只需要實作 List 不用 Create/ Update/ Delete <br>
- 列出符合條件的活躍廣告 ( `StartAt < Now < EndAt` )
- 支援 query parameter 來過濾廣告
- 支援分頁
  - 用 `limit` 和 `offset` 來控制
  - 以 `endAt` 來排序 (ASC)
  

### 實作需求、前提與限制

#### 實作需求

- 投放 API 能夠超過 **10000** RPS
- **不需要**實作身份驗證
- 對 API 進行參數驗證和錯誤處理
- 寫適當的測試
- 在文件說明想法與設計的選擇

#### 前提與限制

- 每天建立的廣告**不會超過 3000** 個
- 可以使用任意第三方套件
- 可以使用任意外部儲存

### API 範例

管理者 API: 以下代表這則廣告⽬的是給 20~30 歲在台灣或⽇本且是使⽤ Android 或 iOS，不限制性別
```bash
curl -X POST -H "Content-Type: application/json" \
  "http://<host>/api/v1/ad" \
  --data '{
     "title" "AD 55",
     "startAt" "2023-12-10T03:00:00.000Z",
     "endAt" "2023-12-31T16:00:00.000Z",
     "conditions": {
        {
           "ageStart": 20,
           "ageEnd": 30,
           "country: ["TW", "JP"],
           "platform": ["android", "ios"]
        }
     }  
  }
```

投放 API: 請求範例
```bash
curl -X GET -H "Content-Type: application/json" \
  "http://<host>/api/v1/ad?offset=10&limit=3&age=24&gender=F&country=TW&platform=ios"
```
投放 API: 回應範例
```json
{
    "items": [
        {
            "title": "AD 1",
            "endAt" "2023-12-22T01:00:00.000Z"
        },
        {
            "title": "AD 31",
            "endAt" "2023-12-30T12:00:00.000Z"
        },
        {
            "title": "AD 10",
            "endAt" "2023-12-31T16:00:00.000Z"
        }
    ]
}
```

## 分析｀

作業的需求可以被理解成： <br>
**設計一個 read-heavy 的 API 能夠以多條件查詢特定時序區間的所有資料** 

最基本的出發點就是從 Cache 下手 <br>
主要使用 Redis 來做 Server Side Cache <br>
但要如何設計低成本、有效率的 Cache 是一個只得思考的問題 <br>


## Solution 1

當建立廣告時，也會同步在建立在 Redis <br>
開一個 `Gender:Platform:Country:AgeRange:uuid` 作為 Key 的 String <br>
並將 TTL 為 `EndAt` 

```
`F:android:TW:20-30:uuid1` : "title1,end1",
`M:ios:JP:30-40:uuid2` : "title2,end2",
```

**建立廣告:** <br>
在 DB 建立廣告同時，也會同時開一個 goroutine 去建立 Redis 的 Key <br>

**查詢廣告:** <br>
以 `SCAN` 來查詢 <br>
並存到 `cache:Gender:Platform:Country:Age` 作為 Key 的 ZSet <br>
TTL 會設的相對短，例如 5 ~ 10 分鐘 <br>
> 方便下次用相同查詢條件下，不同 offset,limit 時去做查詢 <br>
> 有點像是建立第二層針對搜尋的 Cache，不用每次都需要重新 `SCAN` 

**刪除廣告:** <br>
- 對於 String 的 Key: 在建立時就會設定 TTL，不需要額外處理
- 對於 ZSet 的 Key: 因為 TTL 只會設 5 ~ 10 分鐘，也不需要額外處理

### Pros

- 每個廣告都以獨立的 Key 存，如果有修改廣告很好改
- 每個廣告有相對應的 TTL ，不需要額外的機制去淘汰 Redis 中的廣告

### Cons

- 沒有效率的使用 Redis
  - 需要把所有 DB 存的都存到 Redis，並不是以 Redis 當作 Cache 的概念去使用
- 佔用太多 Key
  - 以 10 個國家的條件假設
    - 3000 個 String ( 活躍廣告數量 )
    - 2 * 3 * 100 * 10 ( Gender * Platform * Age * Country )
6000 個 ZSet ( 搜尋廣告組合 )
    - 至少 9000 個 Key
- 搜尋效率不高
  - 在沒有搜尋 Cache 的情況下，每次的 `SCAN` 都是 `O(N)` 的時間複雜度
  - 並且對**年齡**這個條件的查詢還需要做額外的處理

## Solution 2

對 Age 做 Partition <br>
開 101 個 Hash 來存 <br>
- Key: `ad:Age` ( Age = `all` 代表所有年齡 )
- Mapping:
  - Key: `Gender:Platform:Country`
  - Value: 序列化的廣告列表
```
ad:0 : {
        `F:android:TW` : [],
        `M:ios:JP` : [],
        ...
},
ad:1 : {
        `Gender:Platform:Country` : [],
        `Gender:Platform:Country` : [],
        ...
},
ad:2 : {
    ....
}
...
ad:99 : {
        `Gender:Platform:Country` : [],
        `Gender:Platform:Country` : [],
        ...
},
ad:all : {
        `Gender:Platform:Country` : [],
        `Gender:Platform:Country` : [],
        ...
}
```

**建立廣告:** <br>
會把該廣告 `ageStart` ~ `ageEnd` 的廣告都存到對應的 Partition 中 <br>
這邊會需要寫成 `Lua Script` 來保證 ACID <br>

**查詢廣告:** <br>
會用 `HSCAN` 搭配 `MATCH` 選項來過過濾相對應 Partition 的廣告 <br>
並且 `HSCAN` 會回傳 `cursor`可以用來做分頁 <br>

**刪除廣告:** <br>
需要額外寫一個 Cron Job 跑過所有年齡的 Partition 來做淘汰 <br>
看對於一致性的要求有多高，再看有沒有需要使用 `Lua Script` 來保證 ACID <br>
不然 `HSCAN` + `HDEL` 也是可以的

### 問題

1. Data Hotspot
   - 如果這些廣告都是 20 ~ 30 歲的，那這個年齡區間的 Partition 就會變成 Data Hotspot
2. 資料冗余
   - 如果每個廣告**都沒有設定年齡**，所有 Partition 都會有這個廣告的資料 ( 同一份資料存了 101 次 )

## Final Solution 

直接到 DB 查詢不包含 offset, limit 的條件 <br>
對條件搜尋的結果做 Cache <br>
以 `ad:Gender:Country:Platform:Age` 做 Key 使用 `ZSet` 來存

- **Gender** : 2+1 種可能 ( F , M , * )
- **Platform** : 3+1 種可能 ( ios , andriod , web , * )
- **Country** : 這邊假設 10+1 種 ( 假設只針對 10 個國家)
- **Age** : 100+1 種 ( 1-99 歲 )
> 這邊的 `*` 代表 wildcard

```
ad:F:TW:android:20 : {
    "uuid1" : "title1,end1",
    "uuid2" : "title2,end2",
    ...
},
ad:M:JP:android:* : {
    "uuid1" : "title1,end1",
    "uuid2" : "title2,end2",
    ...
},
```

### 問題

簡單分析一下組合數量： <br>
3 * 4 * 11 * 101 = **13,332** <br>
這比剛剛的所有解法都多了更多 Key <br>

但真的需要存這麼多搜尋組合嗎？ <br>

### 分析實際資料

根據：
- [Dcard News 描述](https://about.dcard.tw/news/25)
    > Dcard 站上有超過八成的「卡友」（意指 Dcard 站上的用戶）介於 18 - 35 歲年齡區段
- [similarweb.com 對 Dcard 網站流量分析](https://www.similarweb.com/zh-tw/website/dcard.tw/#demographics)
    > 25 - 34 歲的訪客占最多數。 （電腦上）
可以假設 `[ 18 , 35 ]` 的年齡的熱點區間 <br>
( 因為 Dcard 要滿 18 才能註冊，所以只對多數用戶年齡的上界做 ) <br>

實際 Data Hotspot 可以限縮在 `18 ~ 35` 歲的年齡區間 <br>
那組合數量就會變成：3 * 4 * 11 * (35-18+1) = **2,376** ! <br>
這樣的組合數量就可以接受了 <br>

## 系統架構


### 預設架構

原本在 Redis Cache 的部分是想要用 **Redis Sentinel** 的架構 <br>
- 來達到 **High Availability** 和 **Read Scalability** 的目的

{{< mermaid >}}
flowchart TD
    Ingress[Ingress] 

    subgraph APCluster["`**Stateless AP**`"]
        subgraph AP1LocalCache[Local Cache]
        AP1[AP 1]
        end
        subgraph AP2LocalCache[Local Cache]
        AP2[AP 2]
        end
        subgraph AP3LocalCache[Local Cache]
        AP3[scale by k8s ...]
        end
    end
    %% Ingress --> AP1 & AP2 & AP3
    
    subgraph HAProxyCluster[HAProxy Deployment]
    HAProxy1[Proxy instance]
    HAProxy2[Standby]
    end

    subgraph RedisCluster["`Redis **sentinel**`"]
    RedisReplica1[(Replica 1)]
    RedisMaster[(Primary)]
    RedisReplica2[(Replica 2)]
    end

    Ingress --> APCluster -- Public API
    ( Query active AD )--> HAProxyCluster 
    HAProxyCluster -- load balance Read request --> RedisCluster
    %% HAProxyCluster --> RedisReplica1 & RedisReplica2

    subgraph PgCluster["`Postgres **Primary Replica**`"]
    PG[(Postgres\nPrimary)]
    PgReplica[(Postgres\nReplica)]
    PG -- WAL --> PgReplica
    end

    RedisMaster & RedisReplica1 & RedisReplica2 ---> PG & PgReplica
    APCluster == Admin API
    ( Create AD ) ==> PG


    %% subgraph CornWorkers[Cornjob Workers]
    %% ActiveWorker[Cornjob: Pre-heat AD]
    %% DeactiveWorkder[Cornjob: Deactive AD]
    Corn[CornJob]
    %% end
  
    %% PG <--> ActiveWorker --> RedisMaster
    %% PG <--> DeactiveWorkder --> RedisMaster

    RedisMaster <-- Pre-heat or aeactive AD
    ( use Lua script for atomic operation ) --> Corn <-- Query oncomming AD--> PG
{{< /mermaid >}}


### 實際架構

{{< mermaid >}}
flowchart TD
    Ingress[Ingress] 

    
    Ingress --> APCluster

    subgraph APCluster["`**Stateless AP**`"]
        
        subgraph AP2LocalCache[Local Cache]
        AP2[AP 2]
        BG2[BG goroutine]
        AP2 -.- BG2
        end

        subgraph AP1LocalCache[Local Cache]
        AP1[AP 1]
        BG1["`Internal goroutine
        refresh local Cache`"]
        AP1 -.- BG1
        end

        
        
        
        subgraph AP3LocalCache[Local Cache]
        AP3[scale by k8s ...]
        BG3[BG goroutine]
        AP3 -.- BG3
        end
    end
    

    Redis[("Redis standalone")]


    AP1LocalCache -. "`Public API
    (if cached)`" .-> Redis

    AP1LocalCache -. "`Public API
    (if cached)`" .-> Redis


    subgraph PgCluster["`Postgres **Primary Replica**`"]
    PG[(Postgres\nPrimary)]
    PgReplica[(Postgres\nReplica)]
    PG -- WAL --> PgReplica
    end

    AP2LocalCache -. "`Public API
    (if not cache)`" .-> PG & PgReplica

    AP3LocalCache -. "`Public API
    (if not cache)`" .-> PG & PgReplica

    AP3LocalCache == Admin API
    ( Create AD ) ==> PG


    Corn[CornJob]

    Redis <-. "`Pre-heat or daeactive AD
    ( use **Lua** script for atomic operation )`" .-> Corn <-.-> PG
{{< /mermaid >}}


## 實作


## 新問題: 還是不夠快

## 資料瓶頸: Database

## 可以改進的地方

寫這篇回顧文章時其實是 2024 年的 9 月 <br>
有發現一些當時實作沒有注意到的細節 <br>

1. Database Index 
2. 先從 Database 層面優化