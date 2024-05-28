---
title: "{{ replace .File.ContentBaseName "-" " " | title }}"
summary: "Link to external site"
description: ""
date: {{ .Date }}
slug: "{{ .File.Dir | replaceRE `^content/` "" | replaceRE `[0-9]{4}-[0-9]{2}-[0-9]{2}-` "" }}"
tags: []
externalUrl: "https://example.com"
cascade:
  showEdit: true
  showSummary: true
  hideFeatureImage: false
draft: true
---