---
title: "2025 06 29 Triggerer in Airflow"
summary: ""
description: ""
date: 2025-06-29T00:35:18+08:00
slug: "triggerer-in-airflow"
tags: ["blog","zh-tw"]
# series: ["Documentation"]
# series_order: 9
cascade:
  showEdit: true
  showSummary: true
  hideFeatureImage: false
draft: false
---


在介紹如何在如何用 Airflow 寫 Event Driven 的 Dag 前  
需要先介紹兩個名詞

- **Trigger**
  - Trigger 是一小段非同步 ( 由 `asyncio` 實作 ) 程式
  - 專門負責 **polling**，如：等待 X 小時、等外部系統的狀態
  - https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/deferring.html#writing-triggers
- **為什麼需要 Trigger ?**
  - 一般的 Operator 或 Sensor 都會**佔用一個 Worker Slot**
  - 如果我們設定最多 10 個 Worker Slot
    - 又剛好有 10 個 Sensor 在 polling
    - 會**導至 Worker 沒辦法再跑任何東西**
  - 所以應該要有一個專門負責 polling 的角色，也就是這邊的 Trigger！
  - 當遇到需要**等待某種條件**時，應該要 **offload** 給 Trigger 來避免 Worker Slot 的浪費
- **Triggerer**
  - 這些 Triggers 會在 Airflow Deployment 中的 Trigger**er** 上執行
  - 因為這些 `asyncio` 的 `coroutine` 非常輕量
  - 所以可以在 Triggerer 中執行**數百、數千**個 Triggers
