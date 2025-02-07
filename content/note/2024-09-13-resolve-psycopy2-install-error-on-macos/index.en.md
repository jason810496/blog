---
title: "Resolve `psycopg2` Install Error on MacOS"
summary: "Resolve `psycopg2` Install Error on MacOS"
description: "Resolve `psycopg2` Install Error on MacOS"
date: 2024-09-13T15:48:30+08:00
slug: "resolve-psycopy2-install-error-on-macos"
tags: ["blog","en"]
# series: ["Documentation"]
# series_order: 9
cascade:
  showEdit: true
  showSummary: true
  hideFeatureImage: false
draft: false
---

{{< alert "circle-info">}}

The cover is from the official [`psycopg`](https://www.psycopg.org/psycopg3/docs/) documentation.

{{< /alert >}}

<br>

# Common Issues When Installing `psycopg2` on MacOS

```bash
brew install libpq --build-from-source
brew install openssl
```

Add the following environment variables to your `dotfiles` or `~/.zshrc` (depending on the shell you are using):

```bash
export LDFLAGS="-L$(brew --prefix openssl)/lib"
export CPPFLAGS="-I$(brew --prefix openssl)/include"
export PKG_CONFIG_PATH="$(brew --prefix openssl)/lib/pkgconfig"
```

Then, you should be able to install `psycopg2`:

```bash
pip install psycopg2
```