---
title: "Apache Community Over Code NA 2025"
summary: ""
description: ""
date: 2025-09-09T20:40:54-05:00
slug: "apache-community-over-code-na-2025"
tags: ["blog","zh-tw","open-source-contribution"]
## series: ["Documentation"]
## series_order: 9
cascade:
  showEdit: true
  showSummary: true
  hideFeatureImage: false
draft: false
---

## Other

多參加其他技術年會
有很多都有學生補助
KubeCon, PyCon, FOSDEM, All Things Open, DevOpsDays, QCon

KubeCon 可以到 4-5 千人參加
PyCon 大概 2 千人

## 多聽到或更深入了解的一些技術

多了解的新專案和技術

- Apache Cassandra
  - LSM Tree
    - Memtable
    - Append Log structure
    - fast write
  - timestamp
    - last write win
  - Consensus Protocol
    - Paxos
    - Accord (Cassandra)
      - Fast Path
      - Medium Path
      - Slow Path
- Apache Arrow
  - Columnar In-Memory Format
  - Zero Copy
  - Apache Arrow Flight
    - gRPC based high performance data transfer
    - Fast shuffling compare to Ray
      - But still not as fast as Spark
- Apache NiFi
  - Data Ingestion
  - UI-first drag-and-drop
    - Include editing the business logic on the UI
  - Land data as files first
    - Good for retry for future retries
  - Can be both stateless & stateful processing
    - e.g. could also execute 10 steps of task but only commit Kafka offset after all 10 steps are done
  - Copy on write for those files
    - If the content is the same, just create a new pointer to the same file
- Apache Solr
  - Distributed Search Engine
  - Inverted Index
  - Sharding & Replication
  - Faceting
  - Full Text Search

## 從志工變講者

要從台灣出發前
我跟好跟 Jarek 打個招呼說我也會去 CoC NA 到時候見面之類的
結果剛好在我登機的前十分鐘 Jarek 回我
然後突然提到說 Data Engineering Track 剛好有一個講者臨時有事不能來
要不要來講呢？

就思考了一下，想說 COSCUP 的簡報其實也是用英文
只需要換簡報背景就可以了
好像沒有不行

所以就在飛機上突然變成講者了
蠻有趣的

## Apache CoC NA 的規模

我猜是辦的地點的關係
幾年 CoC NA 大概 200 ~ 300 人
其實不算多
大部分的人幾乎都在第一天就報到了

會場大小也不算特別大
就一個 Keynote Room
跟 6 個小會議室
比較小的會議室大概只能 20 人左右
比較大的會議室大概 50 人
其實 COSCUP 或 PyCon TW 的教室可能都比較大
又聽其他 TAC 志工說 KubeCon 都會 4、5 千人
那以人數來說確實算小很多

也有可能是地點的關係？
可能在美國中西部沒有那麼多人會想要來參加
之前在丹佛他們說有 700 人左右

## Quality over Quantity

也有跟其他人聊到人好像沒有想像的多
但他們都說這邊品質很好
跟人聊天別人都聽得懂你在說啥

平常在 linkedin 看到的國外大佬這邊都可以隨便找到
之前 GSoC 申請 Spark Operator 的時後有跟 Apple 開過會的工程師
還有在 Apple 做 Cassandra 有寫過 "Database Internals" 的大大

在幫忙大家 Check-in 的時候
隨便抽一個都是 PPMC 或是 Apache Member

## 食物

技術研討會最重要的部分
都會有早餐跟下午茶，不會有午餐
會有瑪芬、貝果、水果
每天下午都有點心飲料
會有起司德國麵包、軟餅乾、布朗尼
會有一整個冰箱的汽水跟冰紅茶
都超甜或超鹹
但還是會忍不住拿一盤

晚餐的部分
第一天是在附近很有名的 Mill Museum 吃飯
有準備很多食物
但很可惜沒有跟到 Museums Tour

第二三天也有提供晚餐
是在會場的 Keynote 弄小 Buffet 還有小酒吧

## 9/8

9/8 半夜一點到 Minneapolis
搭 Uber 到 Downtown 準備休息
結果到飯店才發現 TAC 的志工是訂 9/9 晚上的飯店
所以我 9/8 晚上沒有地方住

剛好那時候女友也還沒睡覺
就跟我一起找 Downtown 的飯店
在半夜打了 3 通電話才訂到 9/8 當下有空位的飯店

也還好我哥推薦我用的 eSim 有儲值馬上用線上電話的功能
結果還真的有用到

Check-in 的時候櫃台人員說會有早餐
結果進去坐下才發現是要另外付錢的

## 9/9

早上下午都在趕簡報
下午兩點去吃午餐

原本要去北邊的公園走走但是都在下雨而且也不小
就先去下個飯店睡個午覺順便再整理一下簡報
原本是跟 Jarek 約今天晚上吃飯
但很不幸他的行李被航空公司弄丟了
所以就改成明天中午去吃飯

晚上跟其他 3 個 TAC 志工一起去飯店隔壁的美式餐廳吃飯
是 24 小時的那種 Diner
吃完飯就回飯店休息

## 9/10

也是 free day
早上 review 一些 Airflow 的小東西
中午跟 Jarek 和他老婆、還有 Data Engineering Track 的另一個 Chair: Ismaël 
去 Mill Museum 的公園走走然後順便吃午餐
午餐蠻高級的
Ismaël 也分享他之前的工作經驗
也是一路都在做開源然後去 Google 和 Microsoft
還有 Azure for Apache Committer 的酷東西
又多了一個拿到 Committer 的好處了

然後再去 Trader Joe's 買東西
回飯店休息

晚上是第一次 TAC 的志工聚餐
但很好笑的是下午回來睡午覺的時候居然睡過頭
但是下去飯店大廳集合的時候也遇到其他幾個遲到的志工
我們就一起搭公車去餐廳
剛好遇到 Free Bus 所以不用錢
結果到餐廳結果其他人也剛到而已
因為原本那些人是走路去
我們是搭公車去的

是在一個德國餐廳
有點超大的德國麵包
大家就隨便聊聊天
大概 9 10 點走回飯店休息

## 9/11

Apache CoC 第一天
一早 6 點半起床就去會場佈置
然後都在 check-in 的地方幫忙
第一次遇到尾鳩 小聊一下
就去聽 Jarek 分享為什麼 Airflow 3 更適合 AI / MLOps 的 Usecase

下午隨便外帶一份午餐
4 顆炒蛋賣 13 鎂 真的哭了

就準備講自己的 Talk
不過沒什麼人來 xD
大家看起來都比較喜歡高深的技術分享

晚上去 Mill Museum 吃飯
有準備很多食物
但很可惜沒有跟到 Museums Tour

跟 Johnny 聊很多 Casandra
他有在台灣幫中華電信做過一些東西
聊了很多為什麼 Cassandra 會更快
Consensus Protocol 的改進
最新的 Accord Protocol

## 9/12

早上在吃早餐時跟 Bloomberg 的人聊
剛好遇到對貢獻開源有興趣的
就聊一下我是如何開始貢獻 Airflow 的
然後聊一下他是怎麼進入 Bloomberg 的
不過他想要貢獻 Parquet
感覺就比 Airflow 硬蠻多了

然後就去聽 Apache Arrow 的分享
Data Transfer Problem -> 50% ~ 70% of compute & memory usage is for serialization/deserialization
還有 Arrow Flight RPC 架構

中午去吃附近的 Sushi Train
比預期的好吃很多
跟 Jarek 和 TAC 的 Matt 一起去吃中餐

Jarek 也提到做 Open Source 的一些 mindset
像是他同時也有在做 Airflow 的 consulting
所以還是同時可以了解很多企業的 Usecase 和 Pain Point
然後也可以把這些 Usecase 帶回來給 Airflow 的社群
同時從 User 和 Contributor 的角度來看問題
可以更全面的了解問題

還有像是因為現在同時被 Google 和 Astronomer Paid to work on Airflow
也邊做 Consulting
所以可以不會被限制在某個地點 on-site 工作

下午去聽 Apache Cassandra 實作最新的 Accord Consensus Protocol
聽起來分成 Fast Path & Medium Path & Slow Path
剩下的都跟 Cassandra 的實作細節有關
就聽不太懂了

後來去跟 Snowflake 的人聊天
問 Polaris 和 NiFi 的 Usecases 和當時是如何進入 Snowflake 的
做 NiFi 的是因為原本公司就是提供 enterprise NiFi 的服務
然後整個公司被 Snowflake 收購了
變成 OpenFlow 產品
所以就繼續在 Snowflake 做 NiFi 相關的工作
很厲害

## 9/13

早上有去聽 Fineract
看標題原本預期會了解整體 Fineract 的架構、Usecase
但是 Talk 比較是對 Fineract 很了解的人
分享整合 LLM 和 security 比較細部的東西

還有 Live with Accord
在講 Cassandra 實作最新的 Accord Consensus Protocol
要如何 Migrate from Paxos to Accord
主要是維運層面的分享
不是對於 Consensus Protocol 的細節
昨天 Cassandra 才比較深入講解 Cassandra 實作 Accord 的細節

中午跟 OpenAI Data Infra 的人小聊一下
他們有 3 個 Airflow 的 Cluster
大概有 10k 個 Dags
跑在 Kubernetes 上面
會給 Data Scientist 或各種 Team 使用
大概有 40 個人在 Data Infra Team
有 2 個人專門在維護 Airflow
也會用 DBT
Data Infra Team 就單純維護 Data Infra
如: Kafka, Airflow, Spark, Presto, DBT ...etc

目前也不會需要用到 Multi Tenancy 或是分 Team / Group 的功能
( 畢竟都在同一個公司內部使用 )
只有覺得需要把 Airflow 跑在 Kubernetes 上的 Doc 再完善一點
像是什麼時候要用 Kubernetes Executor 或是 Celery Executor
還有一些比較細節的設定

還有跟在 Snowflake 做 Polars Iceberg Rest Catalog 的人聊
他是念 CS PhD、然後從 Cloudera 到 Apple 再到 Snowflake
也拿到 Iceberg Committer、PMC
現在主要在做 Polars
還有聊一些之前設定 Iceberg Lakehouse 的時候有遇到 AWS 只綁 STS Token 的問題
沒有支援 AWS Access Key & Secret Key 直接去連 S3 Protocol 的問題

最近 Iceberg 也支援 MinIO S3 Protocol 了
因為 S3 有支援 STS Token

Polars 還有很多可以做的部分
像是如何處理 concurrent write
目前是 fallback 直接 fail 讓 client 端 retry
但是也要有辦法在 server 端處理

中午去吃附近的 chipotle
但是吃太晚又聊太久
就沒有聽到下午有興趣的 Talk
然後跟其他人聊美國工作 visa 的問題
又知道一個新的 H1B 轉換的方式
也不一定要透過讀書的工作簽
也可以透過 Agentcy 幫忙申請 H1B
但好像不太好

晚上就邊吃晚餐邊聽 Lightning Talk
就回房間睡覺休息了

## 9/14

Spark Structured Streaming 4.0
Object-based API
TransformWithState
Fine Granularity State
New State Store
State TTL

RocksDB
Lineage
Family Group

---

Where’s the Auto in Auto-Instrumentation? A Look at Current Automation Strategies with OTel

完整介紹 OpenTelemetry
蠻新手友善的
之前一直都沒有很了解 OTel 是什麼
也介紹要導入 auto-instrumentation 的步驟

跟 Databricks 的人小聊一下面試的經驗
他說就是大公司的經典面試
所以不管開源做的如何
要進大公司 刷題還是少不了的
除非真的做到那個專案的 Top 1
但忘記問 Databricks 內部有沒有用 Airflow

Tracing the Internals of a Cloud-Native Database

Handling Large Blobs in Apache Cassandra CDC with Kafka and Object Storage Integration

想去聽 Cassandra CDC 結果變成在聽 Kafka
但是學到 Kafka reference-based message 的想法去處理大 Message 的想法蠻有趣的
嘉平老大說之前 eBay 也是用類似的方式去處理大 Message
也是蠻值得做的題目

## 志工

這次遇到 x 個 TAC 志工，希望沒有漏掉誰
大家分別來自印度、巴西、緬甸、斯洛伐克、肯亞、尼泊爾
有些也是 Committer 也有 PMC 的
也有一些跟我一樣是學生
但是有蠻多人都因為 visa 沒過來不了
如果 visa 沒有問題的話應該會有 15 人左右

- Brahma, 印度, 就是 Apache Hadoop 的 PMC
- Kunnath, 印度, 在德國留學的學生, 還在探索要深入學習什麼領域
- Nikhil, 印度, 在 Orcle 工作, 是 Apache Ranger 的 Committer, 去年也有去
- Rodrigo, 巴西, 是 RTOS Apache NuttX 的 Committer, 在 motorola 工作很久了
- Matheus, 巴西, 大概 40 多歲, 準備去金流公司工作, 會去做 GAI Platform
- nazerkes, 斯洛伐克, 在 Slor Search 相關的公司工作, 工作都跟 search 有關，像是 Solr, Elasticsearch, OpenSearch
- Yu, 緬甸, 在美國念書的學生, 也是第一次來，有在貢獻 Apache Fineract
- Everest, 尼泊爾, 在美國念書的學生, 去過很多 conference 對 DevOps 有興趣
- Ceasar, 肯亞, 在 Africa Union 工作, 也是第一次來 Apache CoC

## 英文

跟 TAC 的志工聊天應該算沒問題
但是有時候聽力有點吃力
印度口音大概第二天就可以聽懂了
但是非洲口音要多講幾次才聽得懂
不過大家都很友善
沒聽懂就再問一次就行

講技術相關就最沒有問題
在一般的點餐或單純小聊天都還可以
但如果聊更生活的話題就會比較吃力
像是第二天晚上有舉 Trivia Game
題目就幾乎都聽不懂了


## 交通

這是我第一次去美國
也是我第一次轉機
西雅圖轉機蠻特別的
去程的時候需要重新拿行李再掛行李
回程的時候不需要

不過機場沒有很大
這次大概半小時就到下個登機口了

## 跟 TAC 溝通交通

一開始 Apache 寄信通知說上 TAC 的時後
還需要等好一陣子才會問你說要哪天去、哪天回之類的
應該是因為要先幫其他人處理 visa 問題
像是台灣只需要 ESTA 就方便很多
不太需要擔心簽證會不會過之類的

其實也可以順便趁這個機會去其他州玩
像是 Nikhil 小哥就在一開始跟 TAC 溝通的時候說要去紐約
所以變成 TAC 直接幫他訂紐約回印度的機票
他再自己多訂迷尼蘇達州到紐約的機票
所以就在紐約多玩 4 天，蠻讚的

## 物價

第一次去美國玩
體感是 20 美元的消費力大概等於 200 台幣
像是吃餐廳就大概抓 20 美元左右
這次沒有買 Food Truck 就不確定小吃的那種價格
在餐廳喝酒大概 10 初美金跑不掉

但其中有一餐我去外帶 4 顆蛋的炒蛋
結果被收 13 美元 ...
真的被嚇到了

跟尾鳩聊天問到灣區的物價
就更誇張了
連 Food Truck 都要 20 美元

## 開源與面試

這次去跟很多大公司的人聊天
請教是如何進去的
還有面試的怎麼考

有很多都是 2、3 個 PMC 的大大都是工作都有用到這些開源專案
所以剛好把工作修的 bugs 順便回 upstream
就一路變成 Committer、PMC
然後類似的途徑就變成 2、3 大專案的 Committer、PMC 了

像是請教做 Spark 4.0 Structured Streaming 在 Databricks 的人
也是說就典型大公司面試

開源只是拿到面試的門票
面試還是要靠刷 LeetCode、System Design
除非真的要開源做到該專案前幾頂尖的
不然還是要走正常的面試流程
不過開源可以讓你有更多面試的機會

## 紀念品

這次紀念品有
- 2 件今年最新 Apache Logo 的 T-shirt
- 1 件去年舊款的 T-shirt
- 1 個有印 Apache CoC 2025 的保溫杯
- 很多 Apache 貼紙

## 鳳梨酥

這次帶了 2 盒微熱山丘鳳梨酥去
送給其他 TAC 志工跟認識的人
大家都蠻喜歡的

Nikhil 也有帶印度的小點心
所以下次去 TAC 也可以帶一些台灣的零食去