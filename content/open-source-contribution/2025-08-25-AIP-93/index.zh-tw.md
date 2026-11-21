---
title: "2025 08 25 AIP 93"
summary: ""
description: ""
date: 2025-08-25T22:44:31+08:00
slug: "AIP-93"
tags: ["blog","zh-tw"]
# series: ["Documentation"]
# series_order: 9
cascade:
  showEdit: true
  showSummary: true
  hideFeatureImage: false
draft: false
---

這份文件提出在 Airflow 中引入 Asset Watermarks 以支援增量處理和事件驅動排程。

狀態

狀態

草稿

討論串

https://lists.apache.org/thread/vftpzrwb34xr2xbfsx7qtbxn5w6h3f2b (url://4)

投票串

 

投票結果串

 

進度追蹤 (PR/GitHub Project/Issue Label)

 

建立日期

2025-07-28

版本釋出

 

作者

Jake Roach (url://5) Guangyang Li (url://6)



動機

增量處理是 Airflow 使用案例中非常常見的模式，在某些資料管道中甚至是必要的。雖然 Airflow 目前透過 AIP-82 (url://7) 支援外部事件驅動排程，但原生並不支援增量 polling。在某些情境下，使用者被迫使用 XCom 或 Variables 來處理增量處理的 watermark，或自行發明並實作解決方案。對於事件驅動觸發的情境，因缺乏 XCom 和 Variable 支援，使用者自訂增量處理更具挑戰性。

社群曾嘗試在 BaseEventTrigger 的子類中儲存狀態以管理增量流程，但都未能有效或穩健地運作。這嚴重阻礙了社群建立監控 Asset（如物件儲存、SQL 資料庫及其他非 queue/stream 型 Asset）邏輯的能力。

對於用於 Asset “watching” 的 Trigger，能夠持久化某些狀態是非常有幫助，甚至是必要的。

考量事項

你建議做哪些改變？

高層次來說，建議做以下改變：
 • 引入 ‎⁠asset_watermarks⁠ 模型，用於持久化 Asset/Trigger 狀態 metadata。此模型讓 Airflow 使用者能在 EventTrigger 程式碼中儲存與讀取狀態。儲存在 ‎⁠asset_watermarks⁠ 的紀錄（watermark）包含 ‎⁠asset_name⁠ 和 ‎⁠namespace⁠，以及一組唯一的 key 和 value（key 在 namespace 中必須唯一）。
 • 增加輔助工具或更新 BaseEventTrigger，讓使用者能儲存與讀取 watermark。
 • 建立可插拔的 backend，類似 XCom 模型，供不想用「內建」模型的使用者作為狀態儲存。

它解決了什麼問題？

這解決了建立可用於 “Asset-watching” 或事件驅動排程的 Trigger 時，無法持久化狀態的重大問題。沒有像 ‎⁠asset_watermarks⁠ 這樣的模型，幾乎無法監控 S3 bucket 是否有新檔案，或處理 SQL 資料庫新增/移除資料列。儘管 Airflow 3.0 強調此功能，社群在開發與分發可用於 “Asset-watching” 的 Event Trigger 上進展緩慢。此 AIP 旨在以優雅且「Airflow 式」的方式解決此問題，採用「內建」模型並搭配可插拔 backend。

技術細節

建立模型

建立 ‎⁠asset_watermarks⁠ 模型所需工作量不大。類似 Variable 模型，這是「獨立」於其他模型的，建立上較容易。此模型包含四個欄位：Asset name、namespace、key 和 value。namespace 讓使用者能區分同名 Asset。以下是 ‎⁠asset_watermarks⁠ 模型的偽程式碼：class AssetWatermark:
    """
    Watermark class allows pluggable db backend.
    """
    def __init__(self, asset_name: str, namespace: str, key: str):
        self.asset_name = asset_name
        self.namespace = namespace
        self.key = key

    def set_value(self, value):
        db_backend.set_value(asset_name=self.asset_name, namespace=self.namespace, watermark_key=self.key, watermark_value=value)

    def get_value(self):
        return db_backend.get_value(asset_name=self.asset_name, namespace=self.namespace, watermark_key=self.key)

建立可插拔 backend

對於打算大量使用 ‎⁠asset_watermarks⁠ 的使用者，可插拔 backend 能讓他們更靈活控制狀態儲存資源。此 backend 會仿效 XComObjectStorageBackend，提供現成模型並可設定「可插拔」 backend。

實作 “get/set” 邏輯

需在繼承自 BaseEventTrigger 的類別中實作 get 和 set 邏輯，以儲存與讀取 watermark 值。這通常會以 BaseEventTrigger 類別的方法形式出現。具體來說，遵循 ETL 常見的增量載入界線追蹤慣例：low_watermark 代表 DB 中目前持久化的值，即資料流或時間範圍中最後成功處理的點；high_watermark 代表本次處理後要儲存的新 watermark 值，即本次處理的資料上界。high watermark 會成為未來執行的 low watermark。

偽程式碼如下：class BaseEventTrigger(BaseTrigger):
    @property
    def asset_watermark(self):
        return AssetWatermark(asset_name=self.asset_name, namespace=self.watermark_namespace, key=self.watermark_key)

    @abstractmethod
    def get_high_watermark(self, *args, **kwargs):
        # put the logic to calculate the watermark here
        pass

    def persist_watermark(self, value):
        self.asset_watermark.set_value(value=value)

    @property
    def low_watermark(self):
        return self.asset_watermark.get_value()

範例

監控 S3 Bucket

事件驅動排程最常見的用例之一是監控物件儲存的變化。理想情況下，每次 AssetWatcher 的 Trigger 執行時，不會重新掃描整個 bucket。流程如下：
 1. 第一次 Trigger 執行後，記錄本次資料掃描的 timestamp。
 2. 第二次執行時，Trigger 讀取上次執行完成的 timestamp（watermark），只掃描該 watermark 之後的檔案。
 3. Trigger 再次寫入 watermark。
 4. 後續 N 次 Trigger 執行皆重複此流程。

SQL 資料庫的增量資料

另一常見用例是監控關聯式資料庫的資料表（以 Postgres 為例）。除了傳統 CDC，資料團隊常用 Postgres 的 ‎⁠updated⁠ 欄位來 upsert 資料。利用 ‎⁠asset_watermark⁠，可採以下流程。這與監控 S3 Bucket 的流程非常類似，目的是建立可重複使用的模式。
 1. 第一次 Trigger 執行後，記錄本次資料掃描的 timestamp。
 2. 第二次執行時，Trigger 讀取上次執行完成的 watermark，只掃描目標資料表 ‎⁠updated⁠ 欄位大於 watermark 的紀錄。
 3. Trigger 再次寫入 watermark。
 4. 後續 N 次 Trigger 執行皆重複此流程。

以下是以 watermark 執行 SQL 查詢的 Trigger 範例：class SQLIncrementalQueryTrigger(BaseEventTrigger):
    ...
    def get_high_watermark(self, *args, **kwargs):
        return pendulum.now().to_date_string()

    async def run(self):
        while True:
            results = conn.get_records("SELECT * FROM table WHERE updated_at > '%s'", self.low_watermark)
            self.persist_watermark(key="table_last_updated_at", value=self.get_high_watermark())
            if results:
                yield TriggerEvent({"status": "success", "results": results})
                break
            else:
                await asyncio.sleep(self.poke_interval)

為什麼需要這麼做？

讓 Airflow 支援持久化 watermark 的方法，並解鎖事件驅動 Trigger 的開發，特別是針對有 “Asset-watching” 需求的使用者。

此改變有什麼缺點？

理論上的缺點是 Airflow 使用者可能會將 ‎⁠asset_watermarks⁠ 模型當作 Event Trigger 以外的 key-value store。但這並不令人擔憂，因為更可能被濫用的是 ‎⁠Variable⁠ 模型。此外，增加複雜度的缺點也很小。

哪些使用者會受到影響？

DAG 作者： 這些使用者將能更容易撰寫用於增量流程的 Trigger、Sensor 和 Task，並能進一步建立事件驅動邏輯。

部署管理者： 引入可插拔 backend 的模式，可能讓部署管理者需額外管理 Airflow “stack” 的新元件。此改變也需要 DB migration，詳見下方。

使用者會受到什麼影響？（例如需要 DB 升級？）

目前未使用增量事件 Trigger 的使用者不受影響。但此新功能需 DB migration，因為要新增新模型。唯一需要的改變是新增一個資料表。

使用者適應破壞性改變所需的遷移努力（手動與自動）

此 AIP 不包含破壞性改變。新增 ‎⁠asset_watermarks⁠ 模型只需 DB migration，不會強制使用者改變現有流程。

其他考量
 • 此功能可與 Asset partitions 相容。
 • 目前此「狀態儲存」僅限於 Asset “watching”。

目前最大挑戰之一是此功能如何與 Asset 綁定。為 ‎⁠AssetWatcher⁠ 定義的 Trigger 並不直接與 Asset 綁定。這種斷裂讓命名與實作更具挑戰。此功能應與 Asset 綁定嗎？還是僅適用於 Trigger 層級？總體目標是讓事件驅動排程對 Airflow 使用者更直覺。

此 AIP 何時算「完成」？

當 PR 建立模型並合併可插拔 backend，且解決方案有完善文件時，即算完成。

---

https://github.com/apache/airflow/pull/19051/files#diff-1f5a17488436bc655465a7750dcb62e2c514d003c0e5c4a6a6be499afc4850c7

---

以下是該討論串的完整繁體中文翻譯，保留所有專有英文名詞：

[討論] 在 Trigger 中持久化狀態

Jake Roach - 2025年6月5日 星期四 3:12:16 AM GMT+8*問題*

目前，Trigger 或任何 Airflow 物件都無法持久化狀態。

這對 Airflow 使用者來說是一個挑戰，特別是那些希望“監控”Assets的人。AssetWatcher 利用 Trigger（繼承自 BaseEventTrigger）來創建 Asset 事件並觸發 DAG 執行，以實現事件驅動的 DAGs。到目前為止，唯一的實作都是基於 queue/stream。然而，還有許多其他“增量”事件，使用者可能希望在這些事件發生時觸發 DAG，例如：

   - 新檔案落地或在 S3 中被更新
   - 新紀錄被加入 Postgres 資料表

為了在 trigger 中實現這類邏輯，需要某種“水位標記”（watermark）。這可以是“最後處理的檔案”或“最後修改時間”。例如，Trigger 應只“回溯”自上次觸發 TriggerEvent 以來落地的 S3 檔案。否則，可能會產生無限迴圈
<https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/event-scheduling.html#avoid-infinite-scheduling>
。

由於目前沒有可靠的方法在 Trigger 中儲存狀態，這個“水位標記”無法被持久化並由其他 Trigger 執行取得。*這使得針對增量事件創建 Trigger 變得非常困難。*

先前的工作

Daniel Standish 創建了 AIP-30
<https://cwiki.apache.org/confluence/display/AIRFLOW/AIP-30%3A+State+persistence>
來解決這個問題。他在 AIP 中提到的使用案例與 Airflow 使用者希望透過事件驅動排程解決的問題高度相關。雖然尚未實作，但仍然很有參考價值。

Airflow 使用者和貢獻者也開始自行實作“變通方法”來推動事件驅動排程，但至今尚未有健全的解決方案。

提案

在提出以下解決方案之前，我測試並觀察了社群的不同做法。以下方法在被拒絕前曾被考慮：

   1. 使用 Airflow Variables 設定和取得 key-value 對。可惜 Variable.set(...) 無法在 Triggerer 上執行。此外，這種做法還有其他缺點，例如變數被意外修改的風險。
   2. 將 key-value 對儲存在外部儲存。這需要 Airflow 使用者額外設置，且會讓事件驅動排程感覺不夠“原生”。
   3. 使用 /assets endpoint 取得 last_asset_event.timestamp。由於 Trigger 是獨立於 Asset 定義的，沒有直接方式取得這個 timestamp。此外，這對非時間型水位標記也不夠彈性。

大量借鑑 AIP-30 的想法，我提議在 Airflow 中新增一個 model，稱為 process_state（或類似名稱），包含 namespace、name、key、value 欄位。定義 Trigger 時可提供 process namespace 和 name，允許在 Trigger 內部儲存和取得 key-value 對。process_state model 也可供實作 Trigger-like 邏輯的 Sensors 使用。

對於幾乎所有“增量”流程，這提供了一種維持狀態的方法，並解決事件 Trigger 的開發障礙。

如果社群決定推進這個方案，我願意主導開發、測試和文件撰寫工作。

*Jake Roach*
Field Data Engineer
(he/him/his)

Email: jake.roach@astronomer.io

Mobile: ( <555-555-5555>716) 364-4203

Jarek Potiuk - 2025年6月9日 星期一 8:54:16 PM GMT+8一些鬆散的想法以激發討論：

過去 Airflow 的基本架構假設讓我們對這類需求說“不”——因為我們對資料區間和“冪等性”有強烈假設（你可以查閱 devlist，了解 Airflow 中冪等性的討論）。

但在 Airflow 3 中，我們有更多方式看待 DAGs 和排程，我同意“如何儲存狀態”的通用抽象會很有用。

我認為應該考慮誰是這個狀態的“擁有者”——即狀態附屬於哪裡，以及使用場景，因為這會影響特性——例如可擴展性和效能。如果我們希望有“水位標記”以達到類似 streaming kafka 的效能和可擴展性，那和粗粒度的狀態存取完全不同。

如果我們對延遲等期望不高，我認為我們幾乎已經有一個“中等重量”的狀態儲存機制——“airflow.io”。使用者可以選擇自己喜歡的物件儲存作為狀態儲存（即使是 LocalFileStorage，如果他們用 Local Executor 跑小型 airflow 實例）。在許多情況下，這可以在 triggers 中以非同步方式存取（我猜我們應該檢查現有 ffspec 實作的“async”程度）。

所以**也許**這可以透過“最佳實踐”來告訴大家、測試並確保 triggers 能夠存取 common.io 的 async 抽象。

當然——也許我們對這類狀態有其他效能/延遲需求，所以物件儲存不夠？但我不確定 Another Task SDK Model 和 API 是否是正確方式。Airflow 3 反正都要經過 API server，所以已經有一些集中處理和延遲，分散式物件儲存可能是更好的狀態儲存方式？

J.

Ryan Hatter - 2025年6月11日 星期三 1:58:44 AM GMT+8我認為我們不應該試圖挑戰 Kafka，但更好地支援事件驅動排程是 Airflow 3 經常被提及的亮點之一。

在我看來，用物件儲存管理狀態不合理。Airflow 中一個簡單的 model 就很合適。

Ryan Hatter - 2025年6月11日 星期三 2:08:28 AM GMT+8像 XComs 這種需要在任務間共享大量資料的，確實適合用物件儲存。但用來追蹤事件驅動排程的 trigger 狀態應該始終很小吧？

Ash Berlin-Taylor - 2025年6月12日 星期四 4:23:34 AM GMT+8呼叫 Daniel Standish——他有一份舊的 AIP（我記得是30）專門針對這個問題，但 Airflow 的“model”已經有些變化，可能需要針對 Airflow 3 重新設計。

-ash

Jarek Potiuk - 2025年6月12日 星期四 5:01:52 PM GMT+8確實，我認為用 metadata db 儲存狀態還是用外部儲存並不明顯哪個更好。我們可能低估了現代分散式物件儲存的速度和延遲，相較於我們的集中式 api server（每次請求基本上都有 http 開銷加上 DB 讀寫）。在同一個已經很忙的 DB 上寫入和讀取，可能實際上更慢、延遲更高。（這也是我之前提到要考慮所需特性的原因）

我認為關鍵在於我們能否用 async 介面來寫入水位標記——比起是 DB、物件儲存還是 Redis 等等更重要。

對於小型安裝，DB 延遲肯定較低，但分散式物件儲存的可擴展性肯定比我們能用單一關聯式 DB 做到的高（而且我們的 DB 不支援 active/active 複寫）。我會對在 DB 上增加“更多”壓力保持謹慎——這也是我認為用其他通用儲存 key-value 的方式有其美感（而且更分散）。理想情況下我們可以用專用的 redis/valkey 叢集（但我們可能不想再加一個元件）給 Airflow。

長期以來討論“asset watchers”時，我都把它看作 Airflow 提供“streamish”體驗的方式——雖然我們沒有 Kafka 那種每秒處理大量訊息的能力，但我們可以有更高的訊息處理量/啟動 dag runs，延遲也更低（這對推論型工作流也很重要）。在這種情況下，如果能利用 async 介面（大多數物件儲存都自帶），節省可能很大。如果我們讓 Task SDK + DB 寫入也 async，延遲也能很小——也許。

特別是 asset watcher，其實就是：

1) 啟動時讀取水位標記（並在 asset watcher 執行時保存在記憶體）
2) 每次 trigger 被喚醒時（可能）非同步寫入水位標記——同時在 DB 創建 DagRun（透過 TaskSDK/trigger DAG）

所以啟動時讀一次，然後是一連串寫入（根據我們想要的保證——at-most-once、at-least-once、exactly-once（千萬不要！）等——可能是非同步的）。
如果訊息很小且 API 是同步的，2) 幾乎必然比 watermark 和 DagRun 都用同一 API/DB（兩次小型 DB 呼叫）慢兩倍——相比用 async watermark 寫入到不同（分散式）系統，可擴展性肯定更高。

但“思考儲存”只是個想法，可以嘗試。Async API-server + Async DB 也許也行（而且不需要外部儲存）。

我也認為“通用”狀態儲存未必是最佳做法——如果想讓它“airflow native”，應該仔細看使用場景，也許不同情境可以有不同解決方案。asset watcher 是一個明確案例（也許不用新增 DB model 就能解決），但 Daniel 的文件裡有 ProcessState、TaskState、TaskInstanceState 的提案——每個用途和狀態數量都不同，可能要分開實作。

J.

Daniel Standish - 2025年6月13日 星期五 1:22:13 AM GMT+8既然被點名了...

我以前是 airflow 使用者，做了很多增量流程。幾乎所有東西都是增量的。資料倉儲/分析、電商報表、整合這類。

一個常見用例是實作類似 fivetran 的東西，我做過好幾次。

對我來說，execution date 幾乎沒用。execution date 是給分區型工作負載用的。

做增量時，你必須追蹤自己的狀態。

這也是我嘗試各種狀態儲存介面、開發 watermark operator 的原因，我們用得很多。我也在這裡 demo 過一個版本 <https://github.com/apache/airflow/pull/19051>，並寫了 AIP-30
<https://cwiki.apache.org/confluence/display/AIRFLOW/AIP-30%3A+State+persistence>
。

我寫 AIP-30 時還只是為了好玩在貢獻 Airflow，沒太多人回應所以就擱置了，後來成為全職 airflow 開發者時有其他優先事項。

但對我來說這個用例還是很明顯。到現在我們加的功能都沒明確支援增量工作流。

我認為問題（當時也是，AIP 裡也提過）是：要不要提供一個通用介面，讓使用者自己控制要持久化狀態的 namespace 和 name？還是要在現有物件上提供儲存狀態的機制？例如在 trigger、task 等等可以做 `self.save_state(key...)`。我當時偏向通用，Jake 似乎也是。各有優缺點。

至於底層儲存機制，像其他東西一樣可插拔很合理。我以前用過不同“後端”——s3 或資料庫。通常 Airflow 用的任務不需要超低延遲。

Karen Braganza - 2025年6月13日 星期五 4:48:09 AM GMT+8我認為 process_state model 對我正在開發的 HttpEventTrigger 很有用。HttpEventTrigger 會向 API 發送請求，並根據使用者定義的 response_check 函數觸發事件。如果 response_check 需要累積評估多個 API 回應，能儲存和取得過去的 API 回應會很有幫助。task instances 也能取得 process_state 資料。對 HttpEventTrigger 來說，這表示 task instances 能取得並處理 trigger 內收到的 API 回應資料。

我相信其他 EventTriggers 也會有類似需求。

Guangyang Li - 2025年7月26日 星期六 9:11:20 AM GMT+8Jake 和我已經把細節寫在這份 AIP 草稿文件
<https://docs.google.com/document/d/1gnGpTDhTpxpC48-kvr3jxL4GWyagMKzItWV-30GZu2U/edit?tab=t.0>
。

我們決定不叫 state persisting，而是叫 asset watermark，
因為這主要是資產導向處理的增強。細節和範例都在文件裡，請大家評論。我們打算等穩定後轉成正式 AIP 文件。

Guangyang

Jake Roach - 2025年7月28日 星期一 10:16:10 PM GMT+8Guangyang 和我已經創建了 AIP 草稿，大家可以在這裡看到：
https://cwiki.apache.org/confluence/display/AIRFLOW/%5BDRAFT%5D+AIP-93。
很期待大家的想法和意見！

Vincent Beck - 2025年8月1日 星期五 4:46:05 AM GMT+8我已在 AIP 上留言。總體來說，我同意這個問題，這確實需要解決。我在寫 AIP-82 時也提過“無限排程問題”（但沒給出解法 :))。我也認為這是實作許多基於非 queue 資產的 triggers 的阻礙。

如果有人對這主題有興趣，歡迎多多回饋 :)

Powered by Apache Pony Mail (Foal v/1.0.1 ~78ad7bf)。如需資料隱私請求，請聯絡：privacy@apache.org。如有服務問題，請聯絡：users@infra.apache.org。