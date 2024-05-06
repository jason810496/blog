---
title: "k8s: Extract ConfigMap or Secret to .env file"
subtitle: "Kubernetes cheat sheet: ConfigMap/Secret to .env format"
date:   2024-05-06 16:00:00 +0800

tag: [notes]

thumbnail-img: "https://raw.githubusercontent.com/jason810496/blog/main/_images/k8s-thumbnail.png" #1:1 (450:450)

cover-img: "https://raw.githubusercontent.com/jason810496/blog/main/_images/k8s-banner.png"

comments: true

# ======= Other parameters ========
layout: post
readtime: true

# test local : bundle exec jekyll serve
---

# Kubernetes Cheat Sheet: Extract `ConfigMap` or `Secret` to .env file

* [Kubernetes Cheat Sheet: Extract ConfigMap or Secret to .env file](#kubernetes-cheat-sheet-extract-configmap-or-secret-to-env-file)
    * [Extract from ConfigMap](#extract-from-configmap)
    * [Extract from Secret](#extract-from-secret)
    * [Extract from helm](#extract-from-helm)
    * [refenece:](#refenece)

## Extract from `ConfigMap`

```bash
kubectl get configmap my-map --output json |
    # Extract the data section.
    jq '.data' |
    # Replace each "key": "value" pair with "key=value"
    jq -r 'to_entries | map(.key + "=" + (.value)) | .[]' >> .env
```


## Extract from `Secret`

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

## refenece:
- https://www.jujens.eu/posts/en/2021/Mar/21/kubectl-cfg-to-env/