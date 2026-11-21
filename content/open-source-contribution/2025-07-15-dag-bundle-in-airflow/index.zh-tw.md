---
title: "2025 07 15 Dag Bundle in Airflow"
summary: ""
description: ""
date: 2025-07-15T12:51:23+08:00
slug: "dag-bundle-in-airflow"
tags: ["blog","zh-tw"]
# series: ["Documentation"]
# series_order: 9
cascade:
  showEdit: true
  showSummary: true
  hideFeatureImage: false
draft: false
---


{{< alert "circle-info">}}

[**源來適你**](https://www.facebook.com/opensource4you) 是在台灣積極貢獻大型開源軟體的社群  
接下來我會在以下時間地點主持 **Airflow 中文會議**

**時間**： **7 月 2 日**起**隔週三晚上 20:30** (台灣時區 UTC+8)    
**地點**： [https://opensource4you.tw/airflow/meeting](https://opensource4you.tw/airflow/meeting)  
**行事曆**： [https://opensource4you.tw/readme/calendar](https://opensource4you.tw/readme/calendar)  


如果你也對 Airflow 的技術新知或對貢獻 Airflow 本身感興趣  
歡迎來 Airflow 會議共襄盛舉！

{{< /alert >}}

## Python 的 Dag 檔案是如何被 Airflow 解析的？


![dag-parsing-in-high-level](dag-parsing-in-high-level.png)



## 什麼情境適合使用 Dynamic Dags (Programmatic Dags)

也會順便了解 Airflow 3 是如何 Parsing Dags 的  

https://www.astronomer.io/docs/learn/dag-best-practices/
https://github.com/astronomer/dag-factory
https://www.astronomer.io/docs/learn/airflow-dag-versioning/


## 使用 Dynamic Dags 的 Best Practices

https://github.com/apache/airflow/issues/51816

## 在 Dag Bundle 之前

S3 sync
- https://github.com/apache/airflow/discussions/24049
- https://janetvn.medium.com/s3-sync-sidecar-to-continuously-deploy-dags-for-airflow-running-on-kubernetes-ab4d417dd8e6

## Dag Processor 與 Dag Bundle

## AIP-66: DAG Bundles & Parsing

**Dag Bundle** 主要是為了支援 [AIP-63: DAG Versioning](https://cwiki.apache.org/confluence/display/AIRFLOW/AIP-63%3A+DAG+Versioning) 而多引入的新提案  

### 解決的問題

```python
with open("config.yaml", 'r') as f:
  customers = yaml.safe_load(f)

for customer in customers:

    @dag(
      dag_id=f"{customer}_dag",
      start_date=datetime(2022, 2, 1)
    )
    def dynamic_generated_dag():
        @task
        def print_message(message):
            print(message)
    
    dynamic_generated_dag()
```



https://cwiki.apache.org/confluence/pages/viewpage.action?pageId=294816356

https://github.com/apache/airflow/blob/7654e1a49b074d5dc06dd1218369399430dfcfc9/airflow-core/src/airflow/dag_processing/bundles/base.py#L229-L247

- **DagProcessor**: 
- **DagFileProcessorManager**:
- **DagFileProcessorProcess**:
- **DagBag**:

## Python 的 Dag 檔案是如何被 Airflow 解析的？ (以 Airflow 2 為例)


{{< alert "circle-info">}}

Airflow 3 會牽涉 [AIP-72 TaskSDK](https://cwiki.apache.org/confluence/display/AIRFLOW/Test+cases+AIP-72+Task+Execution+Interface+aka+Task+SDK) 的核心細節  
所以這邊會以 Airflow 2 的 Dag Processing 機制來說明比較簡單  


因為無論 2 或 3  
都有 DagFileProcessorManager, DagFileProcessorProcess 和 DagBag 這幾個核心概念  

{{< /alert >}}


### DagFileProcessorManager

![dag-file-processor-manager](dag-file-processor-manager.png)


- [_run_parsing_loop](https://github.com/apache/airflow/blob/b3a3591c946326467cf9c54115b9b514d89e7645/airflow/dag_processing/manager.py#L555) 是整個 Manager 的核心
- Manager 會以 `_file_paths`, `_file_path_queue`, `_file_stats` 這 3 個屬性來記錄 Dag File 的狀態
    - [self._file_paths: list[str]](https://github.com/apache/airflow/blob/b3a3591c946326467cf9c54115b9b514d89e7645/airflow/dag_processing/manager.py#L381) 記錄所有 Dag File 的路徑
    - [self._file_path_queue: deque[str]](https://github.com/apache/airflow/blob/b3a3591c946326467cf9c54115b9b514d89e7645/airflow/dag_processing/manager.py#L382-L383) 記錄還有哪些 Dag File 的路徑需要解析
    - [self._file_stats: dict[str, DagFileStat]](https://github.com/apache/airflow/blob/b3a3591c946326467cf9c54115b9b514d89e7645/airflow/dag_processing/manager.py#L425) 記錄每個 Dag File 的狀態
        - `num_dags: int`, `import_errors: int`, `last_finish_time: datetime | None`, `last_duration: timedelta | None`, `run_count: int`, `last_num_of_db_queries: int` 等
- 並由以下屬性來管理 `DagFileProcessorProcess` instance
    - [self.waitables](https://github.com/apache/airflow/blob/b3a3591c946326467cf9c54115b9b514d89e7645/airflow/dag_processing/manager.py#L447) 來追蹤所有活躍的 process 或連線
    - [self._processors: dict[str, DagFileProcessorProcess]](https://github.com/apache/airflow/blob/b3a3591c946326467cf9c54115b9b514d89e7645/airflow/dag_processing/manager.py#L420) 來記錄每個 Dag File 相相對應的 process
- 也提供 [def set_file_paths(self, new_file_paths: list[str]):](https://github.com/apache/airflow/blob/b3a3591c946326467cf9c54115b9b514d89e7645/airflow/dag_processing/manager.py#L1094) 來
    1. 更新上面所提的 `self._file_paths`, `self._file_path_queue`, `self._file_stats` 
    2. Terminate 正在處理 "被刪除檔案的" DagFileProcessorProcess
        - [processor.terminate()](https://github.com/apache/airflow/blob/b3a3591c946326467cf9c54115b9b514d89e7645/airflow/dag_processing/manager.py#L1119)
        - [self._file_stats.pop(file_path)](https://github.com/apache/airflow/blob/b3a3591c946326467cf9c54115b9b514d89e7645/airflow/dag_processing/manager.py#L1120)
- **在每次 loop 中會做以下幾件事**： 這邊只有列出跟與解析 Dag 最相關的步驟
1. [self._refresh_dag_dir()](https://github.com/apache/airflow/blob/b3a3591c946326467cf9c54115b9b514d89e7645/airflow/dag_processing/manager.py#L562)
    1. 更新距離上次 refresh 的時間差，如果大於 `[scheduler/dag_dir_list_interval]` 設定才會重新讀取 Dag Directory [dag_filelocs = {full_loc for path in self._file_paths for full_loc in _iter_dag_filelocs(path)}](https://github.com/apache/airflow/blob/b3a3591c946326467cf9c54115b9b514d89e7645/airflow/dag_processing/manager.py#L852)]
    2. 在最後把 "被刪除檔案的 Dag" 從 Metadata DB 中刪除 [SerializedDagModel.remove_deleted_dags](https://github.com/apache/airflow/blob/b3a3591c946326467cf9c54115b9b514d89e7645/airflow/dag_processing/manager.py#L856)
2. [self.prepare_file_path_queue()](https://github.com/apache/airflow/blob/b3a3591c946326467cf9c54115b9b514d89e7645/airflow/dag_processing/manager.py#L640)
    1. 如果發現 "有檔案被刪除" 的情況，也會透過剛剛所提的 [set_file_paths](https://github.com/apache/airflow/blob/b3a3591c946326467cf9c54115b9b514d89e7645/airflow/dag_processing/manager.py#L1094) 來更新 `self._file_paths`, `self._file_path_queue`, `self._file_stats`
    2. 再把 [file_paths_in_progress = set(self._processors)](https://github.com/apache/airflow/blob/b3a3591c946326467cf9c54115b9b514d89e7645/airflow/dag_processing/manager.py#L1271), [file_paths_recently_processed](https://github.com/apache/airflow/blob/b3a3591c946326467cf9c54115b9b514d89e7645/airflow/dag_processing/manager.py#L1307) 和 [files_paths_at_run_limit](https://github.com/apache/airflow/blob/b3a3591c946326467cf9c54115b9b514d89e7645/airflow/dag_processing/manager.py#L1324) 這 3 者取聯集完 **以外** 的 Dag File 路徑加入到 `self._file_path_queue` 中
3. [self.start_new_processes()](https://github.com/apache/airflow/blob/b3a3591c946326467cf9c54115b9b514d89e7645/airflow/dag_processing/manager.py#L651)
    - 會在 `[dag_processor/parsing_processes]` 限制下   [while self._parallelism > len(self._processors) and self._file_path_queue:](https://github.com/apache/airflow/blob/b3a3591c946326467cf9c54115b9b514d89e7645/airflow/dag_processing/manager.py#L1217)
    - 對於每一個 Dag File 都起一個 `DagFileProcessorProcess` 來解析 [processor = self._create_process(](https://github.com/apache/airflow/blob/b3a3591c946326467cf9c54115b9b514d89e7645/airflow/dag_processing/manager.py#L1224)
    - 並把 `DagFileProcessorProcess` 的 instance 加到 [self.waitables](https://github.com/apache/airflow/blob/b3a3591c946326467cf9c54115b9b514d89e7645/airflow/dag_processing/manager.py#L447) 和 [self._processors](https://github.com/apache/airflow/blob/b3a3591c946326467cf9c54115b9b514d89e7645/airflow/dag_processing/manager.py#L420) 中
      - [self._processors[file_path] = processor](https://github.com/apache/airflow/blob/b3a3591c946326467cf9c54115b9b514d89e7645/airflow/dag_processing/manager.py#L1243)
      - [self.waitables[processor.waitable_handle] = processor](https://github.com/apache/airflow/blob/b3a3591c946326467cf9c54115b9b514d89e7645/airflow/dag_processing/manager.py#L1244)
4. [self.collect_results()](https://github.com/apache/airflow/blob/b3a3591c946326467cf9c54115b9b514d89e7645/airflow/dag_processing/manager.py#L667)
    - 等待多個 `DagFileProcessorProcess` 的結果並更新到 `self._file_stats` 中
    - 也清理 `self.waitables` 和 `self._processors` 中已經完成的 process
    - ```python
      ready = multiprocessing.connection.wait(
          self.waitables.keys() - [self._direct_scheduler_conn], timeout=0
      )

      for sentinel in ready:
          if sentinel is not self._direct_scheduler_conn:
              processor = cast(DagFileProcessorProcess, self.waitables[sentinel])
              self.waitables.pop(processor.waitable_handle)
              self._processors.pop(processor.file_path)
              self._collect_results_from_processor(processor)
      ```

### DagFileProcessorProcess

![dag-file-processor-process](dag-file-processor-process.png)
          
- `DagFileProcessorProcess` 會以 [DagBag](#dagbag) 去拿到該路徑下解析完 Dags 的結果
- [_run_file_processor](https://github.com/apache/airflow/blob/b3a3591c946326467cf9c54115b9b514d89e7645/airflow/dag_processing/processor.py#L248) 是 `DagFileProcessorProcess` 實際的 target function
    - 主要執行 [dag_file_processor.process_file](https://github.com/apache/airflow/blob/b3a3591c946326467cf9c54115b9b514d89e7645/airflow/dag_processing/processor.py#L188) 並回傳 `tuple[number of dags found, count of import errors, last number of db queries]` 作為 `self._result`
      1. 先以 `file_path` 拿到 DagBag [dagbag = DagFileProcessor._get_dagbag(file_path)](https://github.com/apache/airflow/blob/b3a3591c946326467cf9c54115b9b514d89e7645/airflow/dag_processing/processor.py#L918)
        - 而 `_get_dagbag` method 就真的是 construct 一個 DagBag [DagBag(file_path, include_examples=False)](https://github.com/apache/airflow/blob/b3a3591c946326467cf9c54115b9b514d89e7645/airflow/dag_processing/processor.py#L882)
        - 關於 DagBag 的細節可以參考 [DagBag](#dagbag) 這個章節
      2. 把透過 DagBag 拿到的 Dag 都同步到 Metadata DB [serialize_errors = DagFileProcessor.save_dag_to_db(dags=dagbag.dags, dag_directory=self._dag_directory, pickle_dags=False)](https://github.com/apache/airflow/blob/b3a3591c946326467cf9c54115b9b514d89e7645/airflow/dag_processing/processor.py#L976)
        - [DagBag.sync_to_db](https://github.com/apache/airflow/blob/b3a3591c946326467cf9c54115b9b514d89e7645/airflow/models/dagbag.py#L736)
            - [DAG.bulk_write_to_db](https://github.com/apache/airflow/blob/b3a3591c946326467cf9c54115b9b514d89e7645/airflow/models/dagbag.py#L724)
      3. 把上一步拿到的 `serialize_errors` 更新到 `import_errors` 中 [DagFileProcessor.update_import_errors(file_last_changed=dagbag.file_last_changed, import_errors=dagbag.import_errors, processor_subdir=self._dag_directory, )](https://github.com/apache/airflow/blob/b3a3591c946326467cf9c54115b9b514d89e7645/airflow/dag_processing/processor.py#L952-L956)
      4. 最後更新 Dag 的警告 [self.update_dag_warnings(dagbag=dagbag)](https://github.com/apache/airflow/blob/b3a3591c946326467cf9c54115b9b514d89e7645/airflow/dag_processing/processor.py#L962)
        > 到這邊我們也可以知道 UI 上 import errors 或 Dag 警告的 Lifecycle 都是由 DagFileProcessorProcess 來處理的!    


### DagBag

![dag-bag](dag-bag.png)

- `DagBag` 是 Airflow 內部最終讀取 Dag File 的介面
  - 無論是 Dag Processor 要把 Dag 寫入到 Metadata DB 中
  - 或是 Scheduler 或 API Server 要讀取 Dag 
  - 都會透過 `DagBag` 來處理，而`DagBag` 的 constructor 有 [read_dags_from_db: bool](https://github.com/apache/airflow/blob/b3a3591c946326467cf9c54115b9b514d89e7645/airflow/models/dagbag.py#L129) 選項
    - 所對於 Dag Processor 來說： 一定會把 `read_dags_from_db` 設定為 `False`，因為 Dag Processor 的確需要從 Dag File 中讀取 Dag 來同步 Dag 的狀態
    - 但對於 Scheduler 或 API Server 來說： `read_dags_from_db` 會被設定為 `True`，可以保證在不同 deployment 中讀到的 Dag 是一致的
  - 並提供以下屬性讓其他 Airflow 的 component 使用：
    1. [self.dags: dict[str, DAG]](https://github.com/apache/airflow/blob/b3a3591c946326467cf9c54115b9b514d89e7645/airflow/models/dagbag.py#L158) 
    2. [self.file_last_changed: dict[str, datetime]](https://github.com/apache/airflow/blob/b3a3591c946326467cf9c54115b9b514d89e7645/airflow/models/dagbag.py#L160)
    3. [self.import_errors: dict[str, str]](https://github.com/apache/airflow/blob/b3a3591c946326467cf9c54115b9b514d89e7645/airflow/models/dagbag.py#L161)
    4. [self.captured_warnings: dict[str, tuple[str, ...]]](https://github.com/apache/airflow/blob/b3a3591c946326467cf9c54115b9b514d89e7645/airflow/models/dagbag.py#L162)
- [collect_dags](https://github.com/apache/airflow/blob/b3a3591c946326467cf9c54115b9b514d89e7645/airflow/models/dagbag.py#L566) 是從 Dag File 中取得 Dag instance 的 entry point
    - 從 `.py` 檔案讀取[self._load_modules_from_file](https://github.com/apache/airflow/blob/7654e1a49b074d5dc06dd1218369399430dfcfc9/airflow-core/src/airflow/models/dagbag.py#L335)
    - 或 `.zip` 壓縮檔讀取 [self._load_modules_from_zip](https://github.com/apache/airflow/blob/7654e1a49b074d5dc06dd1218369399430dfcfc9/airflow-core/src/airflow/models/dagbag.py#L337)
    - [self._process_modules](https://github.com/apache/airflow/blob/7654e1a49b074d5dc06dd1218369399430dfcfc9/airflow-core/src/airflow/models/dagbag.py#L348)
        - 實際從 Python 檔案讀 modules 後，以 `isinstance(o, (DAG, SDKDAG))` 拿到 Dags 的 instance
        - `top_level_dags = {(o, m) for m in mods for o in m.__dict__.values() if isinstance(o, (DAG, SDKDAG))}`
        - 並以 [self.bag_dag](https://github.com/apache/airflow/blob/7654e1a49b074d5dc06dd1218369399430dfcfc9/airflow-core/src/airflow/models/dagbag.py#L538) 檢查該 Dag 是否合法
            1. 是否有 cycle
            2. Dag policies
            3. 是否有重複的 Dag ID
            4. 都沒問題的話才加入到該 DagBag 中 [self.dags[dag.dag_id] = dag](https://github.com/apache/airflow/blob/7654e1a49b074d5dc06dd1218369399430dfcfc9/airflow-core/src/airflow/models/dagbag.py#L591)

## Dag Bundle in Airflow

1. LocalDagBundle
2. GitDagBundle
3. S3DagBundle

## GitDagBundle


## S3DagBundle

https://github.com/apache/airflow/pull/46621

相關的 Issues  
- [Add a configuration option to enable Airflow to look for DAGs in a specified S3 bucket. #8657](https://github.com/apache/airflow/issues/8657)
- [AIP-5 Remote DagFetcher  #9555](https://github.com/apache/airflow/issues/9555)

## RemoteDagBundle 介面 ?


## 總結

![partition-parsing](partition-parsing.png)