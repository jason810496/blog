---
title: "2025 03 17 What I Learn From Contributing Apache Airflow"
summary: ""
description: ""
date: 2025-03-17T23:37:28+08:00
slug: "what-I-learn-from-contributing-apache-airflow"
tags: ["blog","zh-tw"]
# series: ["Documentation"]
# series_order: 9
cascade:
  showEdit: true
  showSummary: true
  hideFeatureImage: false
draft: false
---


## Apache Airflow 的開發者體驗

Apache Airflow 是一個**有非常好開發者體驗**的開源專案 <br>
( 從來沒有想過會有一個專案可以有專門為了 contributor 的 CLI, 跑 unit test, integration test, kubernetes test, 跑起不同 executor 的 Airflow 系統都只需要**一行指令**就可以搞定 ) <br>
> ![breeze-screenshot](breeze-screenshot.png)
> [`Breeze` CLI](https://github.com/apache/airflow/blob/main/dev/breeze/doc/03_developer_tasks.rst)

並且**有非常完整的 CI** <br>
有超過 100 個 [pre-commit hooks](https://pre-commit.com/) (git hooks) 包括基本的 linting, type checking, 或是生成 documentation , ERD, Frontend API Service 等 
就連 [Available pre-commit checks](https://github.com/apache/airflow/blob/db4689f3c720056fba1c6bbe81decd2e4b1267be/contributing-docs/08_static_code_checks.rst#available-pre-commit-checks) 的文件也是由其中一個 pre-commit 更新的 !

> ![pre-commit-hooks](pre-commit-hooks.png)
> 在 `git commit` 時會自動跑的 pre-commit hooks

在 [GitHub 的 Label](https://github.com/apache/airflow/labels) 也都有很清楚的定義 <br>
到目前有超過 250 個 Label，可以很方便的細分不同 Issue 的 Scope <br>



## 從貢獻開源學到什麼？



### 目前對 Airflow 的了解


對 `api-server` , kubernetes test, executor, task log 


### 開源 == 開緣

## 未來的方向



### Review PR

## 教朋友