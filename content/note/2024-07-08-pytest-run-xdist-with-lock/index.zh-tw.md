---
title: "2024 07 08 Pytest Run Xdist With Lock"
summary: ""
description: ""
date: 2024-07-08T09:45:14+08:00
slug: "pytest-run-xdist-with-lock"
tags: ["blog","zh-tw"]
# series: ["Documentation"]
# series_order: 9
cascade:
  showEdit: true
  showSummary: true
  hideFeatureImage: false
draft: false
---

short solution: using `filelock` 

since `pytest-xdist` is **multi-process** !

>multiprocessing locks will only work if you spawn the subprocesses using multiprocessing (with Pool, Process, etc), it will not work with processes spawned by other means -- pytest-xdist uses execnet to spawn the processes.

https://github.com/pytest-dev/pytest-xdist/issues/668