---
title: "{{ replace .File.ContentBaseName "-" " " | title }}"
summary: ""
description: ""
slug: "{{ .File.Dir | replaceRE `^content/` "" | replaceRE `[0-9]{4}-[0-9]{2}-[0-9]{2}-` "" | replaceRE "/$" "" | replaceRE `^.+\/` "" }}"
date: {{ .Date }}
tags: ["blog"]
# series: ["Documentation"]
# series_order: 9
cascade:
  showEdit: true
  showSummary: true
  hideFeatureImage: false
draft: true
---