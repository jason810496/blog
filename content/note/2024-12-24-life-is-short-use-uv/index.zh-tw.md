---
title: "Life Is Short Use `uv`"
summary: "如何使用 `uv` 來管理你的 Python 專案"
description: "如何使用 `uv` 來管理你的 Python 專案"
date: 2024-12-24T15:56:37+08:00
slug: "life-is-short-use-uv"
tags: ["blog","zh-tw"]
# series: ["Documentation"]
# series_order: 9
cascade:
  showEdit: true
  showSummary: true
  hideFeatureImage: false
thumbnail: "https://avatars.githubusercontent.com/u/115962839?v=4"
draft: false
---

{{< alert "circle-info">}}

封面來自 [`uv`](https://docs.astral.sh/uv/) 官方文件

{{< /alert >}}

# Life Is Short Use `uv`

> An extremely fast Python package and project manager, written in Rust.

只有 **快** 可以形容`uv` 用過就回不去 `poetry` 了 !


## 下載

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## 使用

### 管理虛擬環境


會產生虛擬環境在 `.venv` 資料夾
```bash
uv python pin 3.12
uv venv

# or inline command
uv venv --python 3.12
```


### 安裝套件

同步 `pyproject.toml` 的 dependencies 到虛擬環境
```bash
uv sync
```

安裝套件
```bash
uv add requests
```

### pip 介面

`uv` 有提供 `pip` 的介面
```bash
uv pip install -r requirements.txt
```

## 常見問題



MacOS 預設的 `ulimit` 設定 ( 預設 `256` ) 對於開啟的 file descriptor 數量來說太低了 <br> 
這在安裝時可能會遇到 `Too many open files` 的錯誤。

可以修改 file descriptor 的限制，如把它設定為 `2048` :

```bash
ulimit -n 2048
```
