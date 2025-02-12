---
title: "解決 MacOS 安裝 `psycopg2` 常見的問題"
summary: "解決 MacOS 安裝 `psycopg2` 常見的問題"
description: "解決 MacOS 安裝 `psycopg2` 常見的問題"
date: 2024-09-13T15:48:30+08:00
slug: "resolve-psycopy2-install-error-on-macos"
tags: ["blog","zh-tw","python"]
# series: ["Documentation"]
# series_order: 9
cascade:
  showEdit: true
  showSummary: true
  hideFeatureImage: false
draft: false
---

{{< alert "circle-info">}}

封面來自 [`psycopg`](https://www.psycopg.org/psycopg3/docs/) 官方文件

{{< /alert >}}

<br>

# MacOS 安裝 `psycopg2` 常見的問題


```bash
brew install libpq --build-from-source
brew install openssl
```

在 `dotfiles` 或 `~/.zshrc` ( 跟據當前使用的 shell ) 中加入以下環境變數

```bash
export LDFLAGS="-L$(brew --prefix openssl)/lib"
export CPPFLAGS="-I$(brew --prefix openssl)/include"
export PKG_CONFIG_PATH="$(brew --prefix openssl)/lib/pkgconfig"
```

然後再安裝 `psycopg2` 應該就可以了

```bash
pip install psycopg2
```


