---
title: "2025 08 25 AIP 92"
summary: ""
description: ""
date: 2025-08-25T22:33:58+08:00
slug: "AIP-92"
tags: ["blog","zh-tw"]
# series: ["Documentation"]
# series_order: 9
cascade:
  showEdit: true
  showSummary: true
  hideFeatureImage: false
draft: false
---
以下是頁面內容的繁體中文翻譯。

狀態

狀態

草稿

討論串

https://lists.apache.org/thread/8vopwr8rydogf9ynfspsglqhw3lcblk5 (url://1)

投票結果討論串

 

進度追蹤（PR/GitHub 專案/Issue 標籤）

 

建立日期

2025 年 7 月 24 日

發佈版本

 

作者

Sumit Maheshwari (url://2)



動機

它解決了什麼問題？為什麼需要？

隨著 Airflow 3 的推出，任務執行已從核心服務中分離，並永久失去對 Airflow 中介資料庫的直接存取。下方的示意圖（以 K8sExecutors 為例）鬆散地代表了目前的 Airflow 架構，其中任務執行的 Pod 透過 API 呼叫更新其狀態。為了讓執行 Pod 能呼叫 API，它們需要對 Airflow 的 API 伺服器具備 ingress 存取，以及由 Scheduler 在建立任務負載時產生的驗證 token。

此變更大幅提升了 Airflow 的整體安全性，使其免於意外的資料庫更動。然而，在 Airflow 的控制平面中仍有其他服務可能執行使用者撰寫的程式碼，該程式碼仍可存取中介資料庫，雖說必須是蓄意行為，因為非蓄意存取會被程式性阻擋。這對 多租戶、且核心服務由中央團隊管理而無法控制使用者程式碼的環境，構成更大的風險。只有在任何使用者程式碼在任何情況下都不可能意圖或非意圖地存取中介資料庫時，才能確保完整的安全性。

下方示意圖顯示一個閒置狀態，其中所有使用者程式碼僅透過 API 與核心服務互動。這些 API 可（選擇性地）拆分成不同的網頁服務，以提升整體安全性與可擴展性。

由於目前有太多地方可能讓使用者程式碼直接存取資料庫，我們將此 AIP 拆分為 3 個階段：

階段 1：讓 DAG Processor 與 API 相容

此階段我們將建立所需的 API（如下），並提供旗標讓使用者決定 DAG Processor 運作時是採用現有的資料庫模式，或改用 API 模式。在此階段，Callbacks 部分仍保留在 DAG Processor 之中，但在旗標為真時也必須透過 API 運作。簡言之，DAG Processor 與 Callbacks 在此階段仍緊密耦合。

階段 2：將 Callback 處理從 DAG Processor 中抽離

此階段，我們會讓 DAG Processor 僅能透過 API 運作，並提供功能旗標讓使用者選擇是否將 Callback Processor 以獨立方式執行。我們也會加入可獨立執行 Callback Processor 的 CLI 指令。

階段 2.5：移除將 Callback Processor 作為 DAG Processor 一部分執行的選項。

階段 3：讓 Triggerer 也僅透過 API 運作

最後，我們會建立所需的 API 並對外提供，使 Triggerer 不再需要直接存取資料庫即可完成其工作。

此外，我們需要讓使用者能選擇將所有這些 API 以獨立服務（即 Web、Execution、Internal）運作，或自由組合。例如，使用者可以選擇讓部分 API 作為同一服務的一部分，或將它們分開運行。對大型企業的 Airflow 叢集而言，分開運行更為合理，因為每個服務都能獨立部署、設定網路策略分隔、選擇機器類型等；但對較小的 Airflow 設定來說，這可能造成過度負擔。因此我們相信應提供足夠選項以同時滿足兩種需求。

考量

你提議做出什麼變更？

階段 1

自始至終，Airflow 依賴 DAG 解析迴圈不斷地重新解析並維護部署中的 DAG 狀態。此簡單方法長期以來運作良好，但也帶來一個問題：執行使用者程式碼（DAG）的程序具備對 Airflow 中介資料庫的讀寫存取。

DAG Processor 原先是 Airflow Scheduler 的一部分，但最近已被拆分為獨立的 CLI 指令。然而，以下程式碼仍在 DAG Processor 中執行，並直接將序列化的 DAG 更新至資料庫。這使得 DAG Processor 無論部署在哪裡都必須取得資料庫憑證，削弱了 Airflow 的整體安全性以及 Airflow 3 所釋出的任務執行隔離的部分好處。

在 Airflow 3 中，已實作防護機制，避免 DAG 存取底層中介資料庫，但該機制仍可能被一些技巧繞過。此外，在 Airflow 管理團隊與 DAG 撰寫團隊彼此分離的環境中，這會構成安全風險。

作為 AIP-85 可擴展的 DAG 解析控制 (url://3) 的一部分，另有工作正在進行以使 DAG Processor 更具可擴展性，但那是另一個問題；此處的作法應與 AIP-85 (url://3) 相容。

我傾向於暴露一個新的 API 命名空間（例如 internal），讓 DAG Processor 能用來在處理 DAG 時保存其所發現的變更：
 1. GET /internal_api/dag_processor/dags?dir=path_to_dag_dir
 2. POST /internal_api/dag_processor/update
 3. GET /internal_api/callbacks?dir=path_to_dag_dir
 4. DELETE /internal_api/callback?id=?

第一個 API 會提供 DAG 清單與其他資訊，例如上次解析時間，以便 DAG Processor 判斷是否需要重新解析。第二個 API 用來將序列化的 DAG 資訊更新至 Airflow 資料庫。第三個 GET API 用來擷取在指定 DAG 目錄下所有 DAG 的回呼列表，最後第四個 API 用來刪除已成功處理的回呼。前三個 API 具冪等性，可安全重試；但第四個需更嚴謹的處理與防護，因為它可能導致回呼被多次執行。

此外，這些 API 也可以改以「套件（bundle）」層級運作，而非資料夾層級，但我目前沒有強烈意見。若改用套件層級，那麼每個客戶的 DAG 目錄應分類為不同的 DAG 套件。我們也需要釐清一種長效 token 的驗證機制，讓這些程序能與 API 伺服器進行驗證。

階段 2

Callbacks 主要分為兩種類型：DagCallbackRequests 與 TaskCallbackRequests。這些回呼會被儲存在名為「callback_request」的資料表中，以 JSON 欄位存放回呼資料，並以多型方式標示是 DAG 回呼或 Task 回呼。

以下是由 GenAI 產生的回呼生成與儲存流程概述。

另一張 GenAI 圖則顯示這些回呼是從哪裡生成。這些回呼可能在 Scheduler 或 Trigger 程式碼中生成，並以直接資料庫連線的方式儲存，或在執行流程中以 TI 事件傳送至執行 API，接著再儲存至資料庫（依我的理解，需要確認）。

之後，這些回呼會在 DAG Processor 的程式碼中被擷取、執行並刪除。我認為也存在少數情況下回呼未被執行，因基礎設施問題（如節點重啟）。也就是 DAG Processor 已將回呼放入記憶體佇列準備處理並刪除了資料庫條目，但在真正執行之前就被關閉（需引文）。

因此，要將 Callback Processor 與核心服務解耦，我們必須確保回呼的儲存與擷取可以透過 API 進行，這在階段 1 已提到。使用者需確保其控制平面與執行平面的服務能存取這些 API。
 1. GET /internal_api/callbacks?dir=path_to_dag_dir
 2. DELETE /internal_api/callback?id=?

下一步，我們會將 Callback Processor 拆成獨立的 CLI 指令，類似如下：airflow callback-processor

此指令會建立並執行獨立的 Callback Processor，從 internal API 伺服器擷取回呼清單、執行並刪除（透過 DELETE API）。

階段 3

在最後階段，我們的目標是讓 Triggerer 服務不再使用直接的資料庫操作，而改為透過 API。現階段 Triggerer 為了運作會進行多次資料庫呼叫（清單可能不完整），要讓 Triggerer 不需直接存取資料庫，就必須為下列方法建立等效的 API（部分 API 可能已存在）：
 • bulk_fetch()
 • fetch_trigger_ids_with_non_task_associations()
 • clean_unused()
 • submit_event()
 • submit_failure()
 • ids_for_triggerer()
 • assign_unassigned()
 • get_sorted_triggers()
 • handle_event_submit()（兩個版本）
 • _submit_callback_if_necessary()
 • _push_xcoms_if_necessary()

實作途徑

階段 1 的實作相對簡單，並會由旗標控制是否採用目前直接更新 DAG 至資料庫的方式，或改為透過 API 送出。

1. 呼叫 GET API 以擷取 DAG 清單與相關中介資料

在 DAG Processor 迴圈開始時，提供應處理的路徑/目錄來呼叫 GET API，以擷取 DAG 清單與所有相關中介資料。該中介資料包含基本資訊與上次解析時間等，以便 DAG Processor 決定該檔案是否需要在本次迴圈重新處理。

2. 迭代檔案並收集 DAG

接著 DAG Processor 按現行方式迭代檔案，收集 DAG 並將其序列化為 JSON。同時，它也會在處理 DAG 時執行任何發現的回呼。

3. 呼叫 POST API 以儲存序列化的 DAG

最後，DAG Processor 會呼叫 Airflow Web 服務的 API，將 DAG 的 JSON 更新至資料庫，使 Scheduler 與 Web 伺服器能照常使用。

4. 取得回呼清單、執行並刪除

從資料庫迭代所有已註冊的回呼並執行。同時持續呼叫 DELETE 回呼 API 以清除 Airflow 資料庫中的回呼。

驗證

然而，我們必須釐清 DAG Processor 如何向 Web 伺服器驗證。任務執行期間，Scheduler 在啟動作業時會分享預先建立的短效 JWT token，使其得以存取 API 端點。但在 DAG Processor 的情境下，我們需要新的作法。我認為有兩種可能方式：
 1. 將 JWT 秘鑰分享給 DAG Processor：讓它自行產生 JWT token 並呼叫 API 端點。DAG Processor 可以建立短效 token 並在到期前刷新。此作法容易，但存在重大安全風險，即將 JWT 秘鑰分享至執行側。我們假設 DAG Processor 會運行在較靠近執行平面的環境，而非控制平面。有人可能濫用此秘鑰提交惡意資料，並提交造成其他合法 DAG 類似 DDOS 的 DAG。然而，這在今日也並非完全不可行：某人可以撰寫一個 Python 檔案並生成大量每秒執行的 DAG。
 2. 將 DAG Processor 視為工作負載擴展，類似任務工作負載。也就是 Scheduler 僅在需要時，將 DAG Processor 作為系統作業啟動，例如 DAG 已不再新鮮、或新增了新的 dag_bundle 等。當 Scheduler 啟動 DAG Processor 時，可以提供 JWT token，與任務執行的方式相同，並以類似流程運作。此作法在安全性上較佳，但可能需要較大幅度的重構。

API 版本控管

由於我們將 DAG Processor 自 Scheduler 中分離，並改為呼叫 API，因此必須確保用戶端（DAG Processor）與伺服端（API 伺服器）之間的合約不會破壞且保持相容。我們可以採用版本化路徑，例如從 /api/internal/v1/ 命名空間開始，當有破壞性變更時就提升版本，讓舊用戶端仍能將負載提交至前一版本的 URL。然而，若用戶端在伺服端之前升級，可能導致合約破裂。此外，若資料庫綱要發生更動，則不同 API 版本可能無法運作。

DAG Processor 的封裝

由於 DAG Processor 將從控制平面移至執行平面，並使用 Airflow Task SDK 運作，因此將 DAG Processor 從 Airflow-core 移至 Task-sdk 套件，或獨立為另一套件，會更合理。

（階段 2 與 3 的實作細節可稍後討論。）

效能

在傳送或接收大型負載時可能會出現問題，因此我們可能需要在接收或傳送資料時實作分頁。實際限制將在測試功能並遇到瓶頸時浮現。此外，由於擷取與刪除回呼而產生的額外網路負載也須考量。另一個潛在瓶頸是 API 伺服器端對大型 JSON 負載的反序列化，Python 在這方面並不擅長。因此，一項可行的最佳化是：API 伺服器不反序列化或檢查收到的負載，而是直接儲存至資料庫。負載會是字串（壓縮並編碼的 JSON），僅在稍後 Scheduler 或 Web 伺服器需要時再進行反序列化。

也就是：DAG Processor 讀取 DAG 程式碼，將產生的 JSON 壓縮與編碼成純字串並送到 internal API 儲存。API 只將其存入資料庫，無需處理或反序列化。稍後當 Scheduler 或 Web 伺服器需要時，再即時反序列化。

為了實驗上述作法，我取了 1 萬個 DAG 的序列化 JSON 資料（完全隨機）進行測試，結果顯示可將 44MB 的 JSON 文字壓縮到僅 3.5MB 的文字。當然，現代資料庫在儲存 JSON 欄位時已具備最佳化與壓縮，但此作法可以幫助 API 伺服器端。然而，這會使直接在資料庫中查詢 JSON 欄位的能力受限。>>> f = open('/Users/sumitm/Downloads/json_dump')
>>> json_data = f.read()
>>> sys.getsizeof(json_data)
45800102
>>> compressed_data = compress_json(json_data)
>>> sys.getsizeof(compressed_data)
3606773
>>> reconstructed_json = decompress_json(compressed_data)
>>> sys.getsizeof(reconstructed_json)
45800102
>>> reconstructed_json == json_data
True

相容性／哪些使用者會受影響？

理想狀況下，對使用者不會有任何可見的變更，前提是他們沒有在 DAG 中連接到 Airflow 資料庫。對於在 DAG 中連接資料庫的情況，將拋出 DAG 匯入錯誤，但這不應造成問題，因為在 Airflow 3 已有相同檢查：若 DAG 嘗試連接資料庫則拋出錯誤。不過，隨著此變更，我們不再僅依賴一段程式碼，而是將 DAG Processor 隔離在一個甚至不具資料庫憑證資訊的環境。

可維護性

若 DAG 在資料庫中的儲存方式變動，API 也需要更新；API 與呼叫端程式碼都需相應調整。

執行相依性

目前想不到。

此變更有何缺點？

唯一可能的缺點是：在序列化 DAG 時新增了對健康 Web 伺服器的依賴。然而在 Airflow 3，任務執行也依賴同一服務，因此這應屬合理；如果因 Web 伺服器停擺而無法執行任務，解析 DAG 也沒有意義。

使用者如何受影響？（例如是否需要資料庫升級？）

此變更應與下一版 Airflow 相容，除更改旗標外，使用者不需額外動作。若我們選擇改變在資料庫中儲存序列化 DAG 資料的方式，可能需要新增另一欄位。

需要多少遷移努力（手動與自動）以讓使用者因應破壞性變更？（尤其針對 Airflow 3）

完成所有階段後，使用者需更加留意其 Airflow 基礎設施的設定。也就是如何部署不同的 API 伺服器、以及將 DAG Processor 與 Callback Processor 放置於何處，將會是重要考量。

何謂此 AIP 的「完成」？

當三個階段皆完成，且 DAG Processor、Callback Processor 與 Triggerer 服務在執行上均不需直接存取資料庫，即視為完成。