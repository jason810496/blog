---
title: "k8s: 將 ConfigMap 或 Secret 輸出至 .env 格式"
summary: "Kubernetes Cheat Sheet: 將 ConfigMap 或 Secret 輸出至 .env 格式"
description: "Kubernetes Cheat Sheet: 將 ConfigMap 或 Secret 輸出至 .env 格式"
date: 2024-05-28T14:39:15+08:00
slug: "k8s-extract-configmap-or-secret-to-env-file"
tags: ["blog","en","devops","kubernetes"]
# series: ["Documentation"]
# series_order: 9
cascade:
  showEdit: true
  showSummary: true
  hideFeatureImage: false
draft: false
---

# Kubernetes Cheat Sheet: <br> 提取 `ConfigMap` 或 `Secret` 到 .env 文件

## 從 `ConfigMap` 輸出

```bash
kubectl get configmap my-map --output json | jq '.data' | jq -r 'to_entries | map(.key + "=" + (.value)) | .[]' >> .env
```

說明:
```bash
kubectl get configmap my-map --output json |
    # 取出 data 部分。
    jq '.data' |
    # 將每個 "key": "value" 對替換為 "key=value"
    jq -r 'to_entries | map(.key + "=" + (.value)) | .[]' >> .env
```

## 從 `Secret` 輸出

```bash
kubectl get secret my-secret --output json | jq '.data' | jq 'map_values(@base64d)' | jq -r 'to_entries | map(.key + "=" + (.value)) | .[]' >> .env
```

說明:
```bash
kubectl get secret my-secret --output json |
    # 取出 data 部分。
    jq '.data' |
    # base64 decode 每個鍵的值。
    jq 'map_values(@base64d)' |
    # 將每個 "key": "value" 對替換為 "key=value"
    jq -r 'to_entries | map(.key + "=" + (.value)) | .[]' >> .env
```

## 從 `helm` 輸出

```
# 使用 `awk`：我們從包含 `configmap` 的 row 開始輸出，直到第一個空行。
awk '{if ($0 ~ /^configmap:$/) {triggered=1;}if (triggered) {print; if ($0 ~ /^$/) { exit;}}}' "./project/values.yaml" |
    # 只保留包含我們 config
    grep '^  ' |
    # 將 key: value 轉換為 key=value
    sed 's/  //;s/: /=/' >> .env
```

## 參考
- https://www.jujens.eu/posts/en/2021/Mar/21/kubectl-cfg-to-env/