---
title: "Python: Read File(BinaryIO) Multiple Time"
summary: "Read file (`BinaryIO`) multiple time in Python. Solution to prevent empty content in the second read."
description: "Read file (`BinaryIO`) multiple time in Python. Solution to prevent empty content in the second read."
date: 2024-06-14T23:43:15+08:00
slug: "python-read-file-multiple-time"
tags: ["blog","en","python"]
# series: ["Documentation"]
# series_order: 9
cascade:
  showEdit: true
  showSummary: true
  hideFeatureImage: false
draft: false
---

# Python: read file(BinaryIO) multiple time


Recently, I need to read `BinaryIO` object multiple time when handling `Minio` file.


## solution : `seek(0)`

The reason is that the cursor of `BinaryIO` object will stay at the end of the file after reading it.
So, we need to reset the cursor by `seek(0)`.
```python
f = open(f)
content = f.read()

f.seek(0) # reset !!!!
content = f.read()
```

## Read `UploadFile` object multiple time in `FastAPI`

Because `UploadFile` object in `FastAPI` also encapsulates `BinaryIO` object.
We can also reset the cursor by `seek(0)`.

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