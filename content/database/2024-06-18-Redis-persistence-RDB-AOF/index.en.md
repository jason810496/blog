---
title: "Redis Persistence: RDB and AOF"
summary: "Detailed explanation of Redis persistence settings: RDB and AOF. Pros and cons of RDB and AOF. Detailed implementation with Redis source code."
description: "Detailed explanation of Redis persistence settings: RDB and AOF. Pros and cons of RDB and AOF. Detailed implementation with Redis source code."
date: 2024-06-18T23:10:43+08:00
slug: "redis-persistence-RDB-AOF"
tags: ["blog","en","database","redis"]
# series: ["Documentation"]
# series_order: 9
cascade:
  showEdit: true
  showSummary: true
  hideFeatureImage: false
draft: false
---



# Redis Persistence: `RDB` and `AOF`


{{< alert >}}

Article's Redis version: **7.4.2**<br>
This information might be wrong if you are using a different version.

{{< /alert >}}



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
  You can enable both `RDB` and `AOF` persistence to provide a more robust data protection mechanism.
  {{< /lead >}}


## RDB: Redis Database

In short, <br>
`RDB` needs to `fork()` a child process to save the point-in-time snapshot of your dataset to disk.

### Advantages of `RDB`

> `RDB` is a very **compact single-file point-in-time representation of your Redis data**.
- **Space-efficient**: RDB is more space-efficient than AOF
- **Easier to Backup**: RDB is easier to backup and restore
  > since it is a single file, you can just copy it to any storage such as S3, Google Cloud Storage, etc.
- **Faster restart with large datasets**: `RDB` is faster to recover when you have a large dataset compared to `AOF`
> Redis have utilized CoW to optimize the `fork()` process

### Disadvantages of `RDB`

- **Data loss**: `RDB` is not good if you need to minimize data loss
  > because it only saves the dataset at specified intervals
- **Not suitable for large datasets**: `RDB` is not suitable for large datasets
  > Since it needs to `fork()` a child process to save the dataset to disk <br>
  > `fork()` can **be slow** if you have a **large** dataset <br>
  > may stop serving clients for some milliseconds or even seconds !

### Detailed Implementation of `RDB`

We have mentioned that `RDB` needs to `fork()` a child process to save the dataset to disk. <br>

Let's take a look at the implementation of `RDB` in Redis source code. <br>
1. From `redis/src/rdb.c` : define `bgsaveCommand` command entry point function.
{{< code url="https://raw.githubusercontent.com/redis/redis/811c5d7aeb0b76494d78efe61e418f574c310ec0/src/rdb.c" type="c" startLine="3907" endLine="3942" hl_lines="3937">}}

2. And `bgsaveCommand` actually calls `rdbSaveBackground`. <br>
   `rdbSaveBackground` will check if there is already a child process running, if not, it will calls `redisFork` to fork a child process to save the dataset to disk.
{{< code url="https://raw.githubusercontent.com/redis/redis/811c5d7aeb0b76494d78efe61e418f574c310ec0/src/rdb.c" type="c" startLine="1612" endLine="1646" hl_lines="1615,1621" >}}

{{< alert "circle-info">}}
Since `fork()` is a system call, it **copies the entire memory space** of the parent process to the child process. This is why `fork()` can be slow if you have a large dataset!

Additionally, it might result in **OOM (Out of Memory)** if you have a large dataset and **limited remaining memory**.

{{< /alert >}}


## AOF: Append Only File

`AOF` utilizes the `fsync()` system call to save every write operation to disk.
> Just like WAL (Write-Ahead Logging) in a relational database
`fsync` is performed in background threads to avoid blocking the main Redis event loop.

`AOF` have 3 `fsync` policies:
- `always`: `fsync()` after every write operation
- `everysec`: `fsync()` every second (**default**)
- `no`: `fsync()` only when `fsync()` is called explicitly
  > The faster and less safe method. <br>
  > Just put your data in the hands of the Operating System. Normally Linux will flush data every 30 seconds with this configuration, but it's up to the kernel's exact tuning.

**`AOF` rewrite** : <br>
- Redis will rewrite the `AOF` file in the background to avoid the file becoming too large.
- `serverCron` will check if the `AOF` file is too large, if so, it will call `rewriteAppendOnlyFileBackground` to rewrite the `AOF` file in the background.
> Similar to RDB, **`AOF` rewrite** also needs to `fork()` a child process to save the dataset to disk. <br>
> Which may encounter the same problems as `RDB` when you have a large dataset.

### Advantages of `AOF`

- **Less data loss**: `AOF` is better if you need to minimize data loss
  > since it saves every write operation to disk

### Disadvantages of `AOF`

- **Larger file size**: `AOF` files are usually larger than the equivalent `RDB` files
- **Slower than `RDB` (depends on `fsync()` policy)**:
  - Default `everysec` policy is still very efficient !
  - But if you set `always` policy, it will be slower than `RDB` since it needs to `fsync()` after every write operation

<!-- 
### Detailed Implementation of `AOF`

> Only show the **Append** part , doesn't show the **Rewrite** part

1. `struct redisServer` structure : defines `aof_buf` field is the buffer to store the write operation before writing to the `AOF` file.

`redis/src/server.h`
{{< code url="https://raw.githubusercontent.com/redis/redis/811c5d7aeb0b76494d78efe61e418f574c310ec0/src/server.h" type="c" startLine="1775" endLine="1785" hl_lines="1782">}}
`redis/src/aof.c` : `void flushAppendOnlyFile(int force)` function
{{< code url="https://raw.githubusercontent.com/redis/redis/811c5d7aeb0b76494d78efe61e418f574c310ec0/src/aof.c" type="c" startLine="1045" endLine="1254" hl_lines="3732-3733">}} -->


## Reference 

- redis: RDB and AOF
  - https://redis.io/docs/latest/operate/oss_and_stack/management/persistence/
  - https://www.littlewaterdrop.com/cs/redis/persistence
- Redis source code explanation
  - RDB
    - https://blog.csdn.net/u012785877/article/details/131281282
  - AOF rewrite
    - https://blog.csdn.net/u012785877/article/details/131283626
  - AOF append
    - https://blog.csdn.net/Nuan_Feng/article/details/129282720
    - https://youjiali1995.github.io/redis/persistence/
    - https://www.jianshu.com/p/70b3115cd604
- Linux : `fork()` and `fsync()`
  - [sysprog : history and detail of `fork()`](https://hackmd.io/@sysprog/unix-fork-exec)
  - [CSDN : Linux I/O : Is data safe after calling `fsync()`?(fsync、fwrite、fflush、mmap、write barriers) ](https://blog.csdn.net/hilaryfrank/article/details/112200420)