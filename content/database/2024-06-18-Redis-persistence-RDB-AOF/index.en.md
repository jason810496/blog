---
title: "Redis Persistence: RDB and AOF"
summary: "Redis Persistence: RDB and AOF"
description: "Why Redis needs persistence? Detailed explanation of Redis persistence settings: RDB and AOF"
date: 2024-06-18T23:10:43+08:00
slug: "redis-persistence-RDB-AOF"
tags: ["blog","en","database","redis"]
# series: ["Documentation"]
# series_order: 9
cascade:
  showEdit: true
  showSummary: true
  hideFeatureImage: false
draft: true
---

# Redis Persistence: `RDB` and `AOF`

## Why Redis needs persistence?

Because Redis is an in-memory database
So when the Redis service restarts, all data will disappear

However, you can use persistence settings
Let Redis recover its state when it restarts !

## Redis persistence settings

Redis provides two persistence settings
They are **RDB** and **AOF**

- **RDB**: Redis Database
  {{< lead >}}
  RDB persistence performs **point-in-time snapshots** of your dataset **at specified intervals**.
  {{< /lead >}}
- **AOF**: Append Only File
  {{< lead >}}
  AOF persistence **logs every write operation** received by the server. These operations can then be **replayed again** at server startup, reconstructing the original dataset. 
  {{< /lead >}}
- **RDB+AOF**: RDB and AOF
  {{< lead >}}
  You can enable both RDB and AOF persistence to provide a more robust data protection mechanism.
  {{< /lead >}}


## RDB: Redis Database

`RDB` needs to `fork()` a child process to save the dataset to disk.

### Advantages of `RDB`

> `RDB` is a very **compact single-file point-in-time representation of your Redis data**.
- **Space-efficient**: RDB is more space-efficient than AOF
- **Easier to Backup**: RDB is easier to backup and restore
  > since it is a single file, you can just copy it to any storage such as S3, Google Cloud Storage, etc.
- **Faster restart with large datasets**: `RDB` is faster to recover when you have a large dataset compared to `AOF`

### Disadvantages of `RDB`

- **Data loss**: `RDB` is not good if you need to minimize data loss
  > because it only saves the dataset at specified intervals
- **Not suitable for large datasets**: `RDB` is not suitable for large datasets
  > Since it needs to `fork()` a child process to save the dataset to disk <br>
  > `fork()` can **be slow** if you have a **large** dataset <br>
  > may stop serving clients for some milliseconds or even seconds !

### Detailed Implementation of `RDB`

{{< code url="https://raw.githubusercontent.com/redis/redis/811c5d7aeb0b76494d78efe61e418f574c310ec0/src/rdb.c" type="c" startLine="3907" endLine="3942">}}


## AOF: Append Only File

`AOF` logs every write operation received by the server.

### Advantages of `AOF`


## Reference 

- https://redis.io/docs/latest/operate/oss_and_stack/management/persistence/