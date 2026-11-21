---
title: "2025 10 05 Airflow Submit 2025"
summary: ""
description: ""
date: 2025-10-05T23:03:10+08:00
slug: "airflow-submit-2025"
tags: ["blog","zh-tw"]
# series: ["Documentation"]
# series_order: 9
cascade:
  showEdit: true
  showSummary: true
  hideFeatureImage: false
draft: false
---

## 最忙碌的一週

- 準備 Databricks 的 Coding Interview 和 System Design Interview
- 準備研究所推甄資料
- 準備 Airflow Submit 的內容與簡報
- 準備行李

到出發的前一天都還沒準備好簡報
也還在寫推甄資料

## 到美國的第一餐

遇到快要所有在貢獻 Airflow 的面孔，包括 Jarek, Jens, Sharar, Wei, TP, Elad, 也有一起從台灣來的 Seb

## Day 1

### Key Note: Airflow 3 

- TaskSDK
  - security
    - not allow direct DB access
  - compliance
    - e.g. When maintaining dags will not produce audit logs since it's directly Metadata DB access
  - performance
    - e.g. Bad Dags could lock the metadata DB
  - Client / Server separation
    - e.g. User can update the latest TaskSDK without updating Core Airflow version
    - As long as the Execution API are version aware


With Execution API
- Solve all these problems
- in process API server

More questions
- How can Dag Processor access to Metadata DB?
  - Dag File Processor Manager -> still have access to Metadata DB currently
  - Dag File Processor Process -> no access to Metadata DB
    - Since they are user code


After TaskSDK
- User code should only import from `airflow.sdk` instead of `airflow.models`
  - User code should not access Metadata DB directly

Assets and Event Driven Scheduling
- Assets as first class citizen
- Still depends on users' choice

What execution result API for inference usage:
- e.g. Chat APP
  - Poll the result from `wait_dag_run_until_finished` ( `/{dag_run_id}/wait` ) endpoint
  - The API will Keep stream the XCom result until the Dag is in Finish state
    - e.g. Usage for the inference result

大家都跟 GitHub Profile 長不一樣，都多人 GitHub 看起來很瘦實際很粗
以後 Code Review 會小心講話，不然一拳我人也沒了

### Scaling in LinkedIn

- Gateway for routing Airflow clusters
  - multi-tenant
  - multi-cluster
  - multi-region

### Scaling in GCP

- performance testing framework
  - Compare Airflow 2 and Airflow 3
  - scaling limits
- reproducible
- flexible

AIP-59 Performance tests framework
https://cwiki.apache.org/confluence/display/AIRFLOW/AIP-59+Performance+tests+framework

- instance
  - instance type: e.g. docker-compose, k8s, gcp-composer
  - instance template
- test site
  - values file
  - setup instance (if needed)
  - upload dags
  - run dags
  - write metrics
  - teardown instance (if needed)

Note:
- e.g. selected check for the performance test in GitHub Action
- run daily, by release, on demand ( adding tag of `performance-test` ) for performance-sensitive PRs
- for testing type
  - assets related 
  - event driven scheduling related ( assets watchers )

Bottleneck of scheduler for scheduling scaling
- rethink scheduling algorithm
- more based on your workload
- avoid task starvation

QA:
- for providers related performance test? 
  - e2e test with providers?
- Add executor type for performance test?
  - e.g. Celery, K8s, Local
  - Maybe can be added in the instance level
- How do we collect these metrics?
  - More fine-grained metrics?
  - It's depends on the instance level
    - The framework should be flexible enough to collect different metrics from different instance types
    - or adding new metrics

### OTel in Airflow 3

OTel specifications
- span should be thread specific
  - introduce context propagation
      - share span context across services

Why OTel with Airflow?
- root span to represent the entire DagRun
- sub-span to represent each task

How to use OTel in Airflow?
- store span context in DB (TaskInstance)
  - retrieve span context when picking up the task
- Create sub-span using context propagation (from context variable)
  - `ti.context_carrier`
  - https://github.com/apache/airflow/pull/43941
  - Example Dags:
    - airflow-core/tests/integration/otel/dags
    - airflow-core/tests/integration/otel/dags/otel_test_dag.py
- https://github.com/xBis7/airflow-summit-2025-demo

Note:
- Plugin view for OTel with Airflow
- Improve debug experience in Airflow: Integrate with OTel collector?
- Limitation for custom operator?
  - e.g. BashOperator
  - Maybe can use context manager to create sub-span


We talk about
- Maybe parent span instead of root span for DagRun
  - Since User might trigger DagRun via RestAPI from other services
    - We need to consider the trace context from the upstream service instead of creating a new root span

### Assets and Triggerer Potential Issues

- concurrent issue for multiple triggerers
  - e.g. The multiple triggerers are not aware of each other
  - we are not able to make HA triggerer horizontally scalable
- A lot of features are start built on top of Assets and Triggerer
  - Should make sure it's stable enough
- Event driven scheduling might get wrong if there are multiple AssetEvent arrive in the same schedule loop
  - scheduler will deduple the AssetEvent in the same loop
  - We might need to create another EventAssetEvent to solve this problem
    - Or having a better way to **not** deduple the AssetEvent in the same loop for Event driven scheduling

### Data Platform in Uber

- Migration might take half of the working time
  - e.g. Upgrade Python, Airflow version, Cloud infra etc.
- High watermark for incremental data processing
  - concurrent issue for multiple triggerers

### Meet Airflow Contributors in Person

I almost met all the core contributors of Airflow, everyone is super friendly and nice
Even though I can't hardly tell person by their GitHub profile picture

## Day 2

### 幫忙 Hosting

這次出發前 Jarek 有寄信給一些人問能不能幫忙主持
所以我幫忙主持前二三大的會議聽早上跟下午的議程
其實就介紹一下講者，然後幫忙控制時間，最後幫忙傳麥克風

### Airflow 3 - An Open Heart Surgery


從 user 的角度用 OTel 看所有 span 去了解 Airflow Core 的運作
把 span 分類為 4 種 catagories
把一個 BashOperator 需要 150+ function call, 40+ uniques function, 25+ module involved, 5 個 component
所有 function call 的過程的可以倍 trace
確實可以當作

- Less unique module involved in Airflow 3
  - It's because of only SDK involved.
  - Airflow Core will be call by internal API Server
- py-spy: framegraph for python program
  - 從 Profiler 去看 Airflow 2 跟 Airflow 3 去看 function call 的差別

GitHub: 

Note:
- OTel Airflow for User Debugging Improving

### Uber AirLift to Airflow

- Use API gateway to route between Airflow or Piper
- Read Replica for Metadata DB (MySQL, normal replica setup)


## Day 3

### 自己的 talk

### OpenSource4You 中午聚會

### Workshop: Contributing to Airflow

## Day 4

### Cycling Day


## Day 5

### Settle 觀光

## Day 6

### 準備回家

## 從 User 的角度去看 Airflow