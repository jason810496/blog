---
title: "Python: 重複讀取檔案(BinaryIO)"
summary: "在 Python 中重複讀取檔案 (`BinaryIO`)，如何解決在第二次讀取時出現空內容的問題。"
description: "在 Python 中重複讀取檔案 (`BinaryIO`)，如何解決在第二次讀取時出現空內容的問題。"
date: 2024-06-14T23:43:15+08:00
slug: "python-read-file-multiple-time"
tags: ["blog","zh-tw","python"]
# series: ["Documentation"]
# series_order: 9
cascade:
  showEdit: true
  showSummary: true
  hideFeatureImage: false
draft: false
---

# Python: 重複讀取檔案(BinaryIO)

剛好最近處裡讀取 `Minio` 檔案時，需要重複讀取 `BinaryIO` 物件
但是發現第二次讀取時，檔案內容是空的


## solution : `seek(0)`

原因: `BinaryIO` 物件的 cursor 會在讀取完畢後停留在檔案的最後一個位置
所以透過 `seek(0)` 來重設 cursor

```python
f = open(f)
content = f.read()

f.seek(0) # need to reset cursor !!!!
content = f.read()
```

## 多次讀取 `FastAPI` 中的 `UploadFile` 物件

因為 `FastAPI` 中的 `UploadFile` 物件內又封裝了 `BinaryIO` 物件
同樣也可以透過 `seek(0)` 來重設 cursor

```python
from fastapi import FastAPI, UploadFile, status

def file_service(upload_file: UploadFile):
  content = upload_file.file.read() # first read
  another_file_service(upload_file)
  return status.HTTP_200_OK

def another_file_service(upload_file: UploadFile):
  upload_file.file.seek(0) # need to reset cursor !!!!
  content = upload_file.file.read() # third read
```

## reference

https://stackoverflow.com/questions/3906137/why-cant-i-call-read-twice-on-an-open-file