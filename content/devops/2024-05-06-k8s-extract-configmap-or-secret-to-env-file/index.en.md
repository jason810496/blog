---
title: "k8s: Extract Configmap or Secret to Env File"
summary: "Kubernetes Cheat Sheet: Extract ConfigMap or Secret to .env file"
description: "Kubernetes Cheat Sheet: Extract ConfigMap or Secret to .env file"
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


# Kubernetes Cheat Sheet: <br> Extract `ConfigMap` or `Secret` to .env file




## Extract from `ConfigMap`


```bash
kubectl get configmap my-map --output json | jq '.data' | jq -r 'to_entries | map(.key + "=" + (.value)) | .[]' >> .env
```

Explanation:
```bash
kubectl get configmap my-map --output json |
    # Extract the data section.
    jq '.data' |
    # Replace each "key": "value" pair with "key=value"
    jq -r 'to_entries | map(.key + "=" + (.value)) | .[]' >> .env
```


## Extract from `Secret`



```bash
kubectl get secret my-secret --output json | jq '.data' | jq 'map_values(@base64d)' | jq -r 'to_entries | map(.key + "=" + (.value)) | .[]' >> .env
```

Explanation:
```bash
kubectl get secret my-secret --output json |
    # Extract the data section.
    jq '.data' |
    # Decode the value of each keys.
    jq 'map_values(@base64d)' |
    # Replace each "key": "value" pair with "key=value"
    jq -r 'to_entries | map(.key + "=" + (.value)) | .[]' >> .env
```


## Extract from `helm`


```
# Extract the values with a `awk` script: we print everything starting from the line that contains only `configmap` until the first empty line.
awk '{if ($0 ~ /^configmap:$/) {triggered=1;}if (triggered) {print; if ($0 ~ /^$/) { exit;}}}' "./project/values.yaml" |
    # Keep only the indented lines that contains our configuration values.
    grep '^  ' |
    # Transform key: value into key=value
    sed 's/  //;s/: /=/' >> .env
```

## Refenece
- https://www.jujens.eu/posts/en/2021/Mar/21/kubectl-cfg-to-env/