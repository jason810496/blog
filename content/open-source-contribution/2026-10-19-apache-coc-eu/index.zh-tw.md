---
title: "Apache CommunityOverCode Europe 2026 參與心得：Airflow Contributor Day、多語言 SDK 與 Lakehouse 趨勢"
summary: "在格拉斯哥的 CommunityOverCode EU 2026，首屆 Airflow Contributor Day、分享 Airflow 的非 Python SDK，以及 Lakehouse Day 上關於 Agent、權限控制、semantic catalog 與 REST Catalog 的觀察。"
description: "記錄 2026 年 Apache CommunityOverCode Europe（Glasgow）的參與心得：Airflow Contributor Day 與 Community over Code 的實踐、Airflow Beyond Python 議程、Lakehouse Day 的所見所聞，以及 OpenAI、LinkedIn、Apple 等團隊的 Data Infra 實戰分享。"
date: 2026-10-24T18:52:40+08:00
slug: "apache-coc-eu"
tags: ["blog","zh-tw","open-source-contribution","data-engineering","airflow","lakehouse","apache-iceberg","conference"]
# series: ["Documentation"]
# series_order: 9
cascade:
  showEdit: true
  showSummary: true
  hideFeatureImage: false
draft: false
---

## 前言

> ![featured](featured.jpg)
> 這次一同從台灣出發的夥伴們，從左到右：[KuanHao](https://github.com/rich7420)、我、[Peter](https://github.com/peterxcli)、[GuanMing](https://github.com/guan404ming)  
> 最右邊的 [李唯](https://github.com/Lee-W) 是從日本出發的 XD  

在今年 Lakehouse 相關議程討論到許多 Agent 在 Data Infra 扮演的角色或 Agent 對 Data Infra 的影響  
當然也有長年以來大家如何解決擴展性的問題  

今年也有第一次的 Airflow Contributor Day  
有許多的 Airflow PMC 成員、Committer、Contributor 以及使用者聚集在一起討論 Airflow 的未來


## Airflow Contributor Day：真正的 Community over Code 

很不幸在前一段時間，Airflow 的其中一位 PMC 成員 [Jens](https://github.com/jscheffl) 出了一些狀況
所以他沒辦法參與今年的 Airflow Summit 和 CommunityOverCode  
不過好消息是 Jens 目前狀況好很多了！

> ![airflow-contributor-day-group-photo](airflow-contributor-day-group-photo.jpeg)
> [One picture worth more than 1000 words: this is the summary of the Airflow](https://lists.apache.org/thread.html/5b0ok7fr6tc6lzslvcgx4nhbxkfcwq22)

我們的資深成員 [Jarek](https://github.com/potiuk) 把 Jens 「帶」來會場，他甚至在我們大部分人出發前就已經到會場了  
大約在 CoC 的前一個月，Jarek 邀請大家一行人在 CoC 後再一起飛去德國拜訪 Jens  
所以除了 Jarek 之外，其他人都沒辦法調整行程，只能帶一些小禮物與卡片  
再由 Jarek 送給 Jens 並且把 Jens 的近況帶回來給大家！

這也是真正體現了「Community over Code」的精神  
大家最一開始確實是為了專案技術本身而聚集在一起  
但更長期來說大家早已經把彼此當作朋友  

題外話是，在去年的 Airflow Summit 跟 Jens 一行人還有在西雅圖騎腳踏車  
結果都是爬坡路，我真的追不到大家
希望 Jens 今年可以早日康復後
大家有機會可以再一起去騎腳踏車（但下次先不要上坡路了，我真的追不上大家！）


## Airflow 除了 Python 以外的新語言

這是也跟 [李唯](https://github.com/Lee-W) 一起講一場  

![talk-airflow-beyond-python](talk-airflow-beyond-python.jpg)

切入的角度就是「語言」，Airflow 可以說是描述 workflow 的一種語言  
但過去 10 多年都只能用 Python 來寫這個語言，今年開始可以用 Go, TypeScript, Java 來寫了  
既然可以用其他程式語言，那我們有辦法用自然語言來寫嗎？  

我這邊是現場 Live Demo 一個零售業下有三個工程團隊各自使用不同程式語言  
在同一座 Airflow 環境中來做到一個跨團隊的 workflow 但同樣維持各個團隊的管理和保留技術選擇  
最後再帶過我們怎麼做到執行多語言的 workflow 但同時維持 Airflow 核心控制平面  
而不是連核心都由各個語言重新實作一次

![airflow-contributor-day-dag-level-queue-demo](airflow-contributor-day-dag-level-queue-demo.jpeg)

[李唯](https://github.com/Lee-W) 這邊就從用自然語言與 Airflow 溝通來說到 [Common AI Provider](https://airflow.apache.org/blog/common-ai-provider-1.0/)，讓 Airflow 可以打造 AI native workflow

![wei-lee-common-ai](wei-lee-common-ai.jpg)

簡報：[Airflow-Beyond-Python-New-Languages-for-Tasks-and-Workflows](https://www.zhu424.dev/slides/2026-10-11-Airflow-Beyond-Python-New-Languages-for-Tasks-and-Workflows.pdf)

這是在一個月前才敲定的議程，因為 Airflow Track 有人臨時取消，加上 non-Python SDKs 在當時架構已經有具體的方向了
最後由 Jarek 幫忙排進 Airflow Track 的議程中  
再次感謝 [Jarek](https://github.com/potiuk) 的幫忙，讓我們有機會在 CoC EU 分享這個議！


## Lakehouse Day 的所見所聞：Agent 時代的 Lakehouse

### Agent 帶來更精細的資料權限控制

Lakehouse round table 的主軸是當 Agent 開始成為資料的使用者時，整個 Lakehouse stack 需要跟著改變什麼，講者們談到幾個觀察：
- **Agent workload 的衝擊**：過去只有人會讀寫資料表，現在 Agent 也會隨時與資料表互動，因此對安全性的要求更高，也需要更細粒度的存取控制
- **On-prem 的回潮**：On-prem 也被視為安全策略的一種，Lakehouse stack 不能只考慮雲端，也要能在地端部署
- **新的檔案格式**：在資料檔與 in-memory format 層面，針對不同使用情境開始出現 Parquet 以外的選擇（例如 Lance），但這些格式需要達成共識並標準化，避免生態系分裂

![lakehouse-day-round-table-wide](lakehouse-day-round-table-wide.jpeg)

### 當開源專案與公司業務對標時的影響力

這場是 Sean 大大與同事們在 Lakehouse Day 的 talk，分享 Apple 在 Lakehouse 上的經驗與實作：
- 從 HDFS 遷移到 Lakehouse 的過程中，一系列搬遷與架構上的取捨
- 主要使用 [Apache DataFusion Comet](https://github.com/apache/datafusion-comet)。當組織在專案中有足夠的影響力時，可以影響專案的功能與 release 週期，讓組織內的目標與專案功能對齊
- 需要盡可能提高 Comet 的 operator 覆蓋率，避免退回 JVM-based execution（fallback）或產生多餘的資料搬遷

![lakehouse-day-apple-iceberg-at-scale-talk](lakehouse-day-apple-iceberg-at-scale-talk.jpeg)

### Lakehouse stack 的整合與 semantic catalog

- Table format 與 compute engine 各自分歧，如何整合是共同的課題
- 當 Agent 存取資料表時，需要一個統一的標準：我的 revenue 和你的 revenue 是同一個東西嗎？就像 UTC 讓大家有共同的時間基準，大家需要遵守同一份定義
- [Apache Ossie](https://github.com/apache/ossie) 正是針對這個問題，提出商業語意的開放標準；各個 Data infra vendor 與 catalog service 都有投入，Apache Polaris 也已經完成整合

### REST Catalog 對 Lakehouse 效能的影響

Apache Polaris 這類 REST Catalog 的實作，能加速 metadata lookup，對整體 Lakehouse 的 throughput 有相當大的影響。  
沒有 REST Catalog 時，engine 必須自行處理 metadata 的查找，這個成本相當高。

## 有印象的 Talks

### Re-Architecting Airflow at OpenAI

![airflow-contributor-day-openai-rhino-talk](airflow-contributor-day-openai-rhino-talk.jpeg)

這次 OpenAI 的 Data Infra 團隊有來分享他們如何在 Airflow 2 做的優化來解決他們新業務需要的擴展性問題  
在當時他們的 cluster 已經在瓶頸附近了，並且六周後需要上線更大量級的新業務，是當時一定無法承受的 workload

他們將重寫的 Core 命名為 Rhino API 主要解決這兩項 Airflow 2 的主要問題
- Scheduler isn’t horizontal scalable
- Rhino API to avoid the direct DB connection for each task runner pod
- 比較有趣的是他們的新架構選擇解決 Scheduler 瓶頸問題時，選擇 single scheduler 而不是 scheduler replica 但有用非同步在 non-blocking 的去 pre-fetch 要執行的 task instance
- 大家當然有提出未來擴展性的疑慮，但據他們所說在新業務上線後，目前的 capacity 已經足夠應付未來的 workload

不過從 Airflow maintainers 的角度來看，Airflow 3 本身已經解決許多他們所做的改動了  
如果有用戶在 Airflow 2 上遇到類似的問題，也有時間做 migration 的話  
會建議直接升級到 Airflow 3 而不是在 Airflow 2 上做這些改動  
避免後續更難升級

### Zero downtime Kubernetes cluster migration for Airflow at LinkedIn

LinkedIn 一直都是全球最大的其中一個 Airflow cluster  
LinkedIn 的 Data Infra 團隊的 [Stefan](https://github.com/1fanwang) 分享他們如何在 Airflow 2 上做 zero downtime 的 Kubernetes cluster migration  
這邊是單純升級 Kubernetes cluster 的版本，而不是升級 Airflow 版本  

![airflow-contributor-day-linkedin-airflow-talk.jpeg](airflow-contributor-day-linkedin-airflow-talk.jpeg)

他們達到的 zero downtime semantic 是連單一個 running 的 task instance 都不會被中斷，也不需要重試  
整體概念是： 讓在新、舊 kubernetes cluster 的兩座 Airflow cluster 共享同一個 DB instance，並且在切換時，下一個 task instance 會在新的 cluster 上啟動，而不是舊的 cluster，即使是在同一個 DagRun 也不會有感知  

而他們的下一步會是嘗試支援 zero downtime 的 Airflow 版本升級，這會是非常有趣且有挑戰性的題目  
因為這包含了 DB schema migration, Airflow core code change  

### Optimizing Lakehouse at OpenAI

這一場比較晚進去沒有聽到最一開頭的上下文，不過是在講 OpenAI 內部如何在 Lakehouse 上做優化  
不論是對 Delta table 或是 Iceberg table 都有做一些優化，主要是針對小檔案的問題  

但因為業務時程壓力，都是不可能等社群的下一個 patch 或 minor release  
必須要在內部 fork 來改自己的 in-house solution，我覺得某種程度呼應了我在 [Apache CommunityOverCode Asia 2025](https://blog.zhu424.dev/open-source-contribution/apache-coc-asia/) 的感想  
但這長期也會造成組織無法按照 upstream 的 release 週期來做升級
甚至可能會造成技術債的累積  

### Apache Mahout 

最後當然還有一起參加的 [GuanMing](https://github.com/guan404ming) 與 [KuanHao](https://github.com/rich7420) 分享 Apache Mahout QDP 功能與接下來的 roadmap  
應該也是前無古人在 CoC 的會場分享 Quantum ML 這種深奧的題目  

> ![coc-qdp-gate-simulation-vs-fused-kernel-talk](coc-qdp-gate-simulation-vs-fused-kernel-talk.jpeg)
> [GuanMing](https://github.com/guan404ming)

> ![coc-qdp-architecture-engine-talk](coc-qdp-architecture-engine-talk.jpeg)
> [KuanHao](https://github.com/rich7420)

## 路上的新朋友、食物與風景

### ASF Pokémon

在會議第一天，附近剛好有[寶可夢展](https://www.facebook.com/TheVideoGameMarket/posts/glasgow-gaming-market-starts-at-1100am-tomorrow-at-the-glasgow-club-bellahouston/1443770044600684/)
所以 CoC 籌辦出了 ASF 版的寶可夢「Inframon」

{{< gallery >}}
  <img src="coc-inframon-cards-and-stickers.jpeg" alt="ASF 版寶可夢 Inframon 卡片與貼紙" class="grid-w50" />
  <img src="coc-inframon-cards-and-stickers-face.jpeg" alt="ASF 版寶可夢 Inframon 卡片與貼紙（卡面）" class="grid-w50" />
{{< /gallery >}}

或許下次 [Apache Taipei](https://github.com/opensource4you/) 辦活動可以出一下！

### ICLA 會保護你

我們剛好跟負責當 Committer 時需要簽 ICLA 的秘書 Craig 聊到天，學到一些冷知識： 
- 大約有 1/3 的 ICLA 被拒絕，因為大家在 id 填 GitHub id，但 GitHub id 不能代表一個 「人」 
- 如果有公司因為你在 Apache 專案寫的 code 要告你時，ICLA 可以保護你不被告，公司只有辦法起訴 ASF

### Apache Taipei 的夥伴們

![team-dinner-steakhouse](team-dinner-steakhouse.jpeg)

感謝 [嘉平](https://github.com/chia7712) 在台灣即使公務纏身，也還是贊助我們 Apache Taipei 夥伴們的大聚餐  
也在這邊感謝 Sean 大大在會場帶我們認識許多水果的 Data Infra 團隊，讓我們有機會與更多在 Lakehouse 的專家們交流  

### 會場與蘇格蘭的食物

![conference-lunch-scottish-beef-pie](conference-lunch-scottish-beef-pie.jpeg)

會場的中餐的 buffet 都還不錯吃  
比較特別的是今年的晚宴舉辦在一個科學博物館  

{{< gallery >}}
  <img src="glasgow-science-centre-entrance.jpeg" alt="格拉斯哥科學中心入口" class="grid-w50" />
  <img src="glasgow-science-centre-interior.jpeg" alt="格拉斯哥科學中心內部" class="grid-w50" />
{{< /gallery >}}

我們在蘇格蘭的吃到的食物都蠻好吃的

{{< gallery >}}
  <img src="pub-steak-and-fries.jpeg" alt="牛排與薯條" class="grid-w100 md:grid-w33" />
  <img src="steakhouse-t-bone-steak.jpeg" alt="牛排館的 T-bone 牛排" class="grid-w100 md:grid-w33" />
  <img src="hotel-breakfast.jpeg" alt="飯店早餐" class="grid-w100 md:grid-w33" />
{{< /gallery >}}

### 路上的一些風景

{{< gallery >}}
  <img src="airport-mirror-selfie.jpeg" alt="機場玻璃倒影的合照" class="grid-w100 md:grid-w33 xl:grid-w25" />
  <img src="flight-seat-entertainment-system.jpeg" alt="飛機座位上的娛樂系統" class="grid-w100 md:grid-w33 xl:grid-w25" />
  <img src="glasgow-airport-wall-mural-group-photo.jpeg" alt="在格拉斯哥機場彩繪牆前的合照" class="grid-w100 md:grid-w33 xl:grid-w25" />
  <img src="supermarket-security-monitor.jpeg" alt="超市裡的監視器畫面" class="grid-w100 md:grid-w33 xl:grid-w25" />
  <img src="glasgow-church-tower.jpeg" alt="格拉斯哥街頭的教堂鐘塔" class="grid-w100 md:grid-w33 xl:grid-w25" />
  <img src="glasgow-red-sandstone-building.jpeg" alt="格拉斯哥的紅砂岩建築" class="grid-w100 md:grid-w33 xl:grid-w25" />
  <img src="edinburgh-scott-monument.jpeg" alt="愛丁堡的史考特紀念塔" class="grid-w100 md:grid-w33 xl:grid-w25" />
  <img src="lakehouse-day-conference-hall.jpeg" alt="Lakehouse Day 會場" class="grid-w100 md:grid-w33 xl:grid-w25" />
  <img src="lakehouse-day-collaboration-is-the-architecture-slide.jpeg" alt="Lakehouse Day 的 Collaboration is the architecture 簡報" class="grid-w100 md:grid-w33 xl:grid-w25" />
  <img src="lakehouse-day-round-table-panelists.jpeg" alt="Lakehouse round table 的講者們" class="grid-w100 md:grid-w33 xl:grid-w25" />
  <img src="airflow-contributor-day-opening-and-cardboard-cutout.jpeg" alt="Airflow Contributor Day 開場與立牌" class="grid-w100 md:grid-w33 xl:grid-w25" />
  <img src="airflow-contributor-day-our-talk-airflow-beyond-python.jpeg" alt="Airflow Beyond Python 議程的簡報首頁" class="grid-w100 md:grid-w33 xl:grid-w25" />
  <img src="airflow-contributor-day-durable-execution-talk.jpeg" alt="The evolution of durable execution in Airflow 議程" class="grid-w100 md:grid-w33 xl:grid-w25" />
{{< /gallery >}}

## 參與感想


**持續的參與的重要性**

今年又遇到一些在去年 CoC NA 場遇到的大大們，許多 Big tech 的 Data infra 團隊都有連續參與  
可以看到大家正在專注的領域有什麼變化、接下來的方向、以及他們如何解決這些問題等資訊差  
透過這些實際參與來了解還有那些專案值得關注，這些專案的活躍方向

對於在參與的 Airflow 專案本身，很高興這次有參與到 CoC EU
尤其是有一整天 Airflow 自己的 Track，也有參加到社群自己的重要時刻

**很多東西都是在會場內談出來的**

這次除了 Airflow 社群的暖心時刻，也討論到許多關於 Airflow 的未來  
又或是[某些值得 follow-up 的題目](https://cwiki.apache.org/confluence/spaces/AIRFLOW/pages/311626658/Airflow+3+Workstreams) 如： [Improve Airflow's debugging story](https://github.com/apache/airflow/issues/40975)、Airflow Standalone Improvements、Workflow-in-Workflow 等
大家或許要有更多時間在 dev call 從 Airflow users 角度出發討論哪些功能真的需要且合理的  
現在有很多新功能是因為把其他類調度引擎作為競爭對手，但或許從既有用戶角度或從對方調度引擎用戶角度角度出發，這些新功能在某些情境下可能不一定完全合理  
換句話說，有可能解決一些 Airflow 既有的問題或許比增加新功能可以帶來更多價值  

或是跟同行的 [Peter](https://github.com/peterxcli) - Apache Ozone PMC 成員，聊到 Ozone 都會先在 contributor fork 上跑 CI runner，再在 main repo 上跑實際的測試，這樣可以確保代碼的品質和安全性。還有各個 repo 應該要有自己的 workflow 來做類似 GitHub copilot、code rabbit 的自動 AI review，能對 harness 設定有更好的控制不會被 vendor 綁死


## 特別感謝

**最後要特別感謝[嘉平](https://github.com/chia7712)。在我還是初級大人，也沒有申請到今年 Apache CommunityOverCode EU 的補助;**
**如果不是嘉平的幫忙，我也不會參與到這次對 Airflow 社群特別有意義的 Contributor Day，也不會有機會在 CoC EU 分享 Airflow 的新語言議程。**