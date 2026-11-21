---
title: "2025 10 18 Critical Section in Airflow"
summary: ""
description: ""
date: 2025-10-18T14:02:07+08:00
slug: "critical-section-in-airflow"
tags: ["blog","zh-tw"]
# series: ["Documentation"]
# series_order: 9
cascade:
  showEdit: true
  showSummary: true
  hideFeatureImage: false
draft: false
---

## How does Airflow handle critical sections?

state
- SCHEDULED
- QUEUED
- RUNNING
- SUCCESS
- FAILED

- Skip-Locked Rows Lock
- Select with Limit ( don't let 1 scheduler / executors pick up all the works )
- How to ensure the TaskInstance is still alive?
  - heartbeat
  - update the heartbeat timestamp periodically
  - mark as failed if heartbeat timeout


## Row Lock

`with_row_locks` util 提供 row-level lock 避免多個 scheduler / worker 同時處理同一筆資料。

1. **NOWAIT**
When nowait=True is set, PostgreSQL will not wait for locks to be released if the requested rows are already locked by another transaction.

- Default behavior: If a row is locked, the query waits until the lock is released
With NOWAIT: If a row is locked, the query immediately fails with a lock acquisition error
- Use case: Prevents queries from hanging indefinitely when rows are contended
- SQL equivalent: SELECT ... FOR UPDATE NOWAIT

2. **SKIP LOCKED**
When skip_locked=True is set, PostgreSQL will skip over any rows that are currently locked by other transactions.

- Default behavior: Query waits for locked rows or fails (with NOWAIT)
With SKIP LOCKED: Locked rows are simply excluded from the result set
- Use case: Useful for work queue patterns where you want to process available items without waiting
- SQL equivalent: SELECT ... FOR UPDATE SKIP LOCKED


- airflow-core/src/airflow/utils/sqlalchemy.py
- https://github.com/apache/airflow/blob/04d3c440e3c741b0f2d9ac4d34d2f09f8b41a38b/airflow-core/src/airflow/utils/sqlalchemy.py#L314-L355


## DagModel.dags_needing_dagruns

關於 `DagModel.dags_needing_dagruns` 的註解：

```python
"""
Return (and lock) a list of Dag objects that are due to create a new DagRun.

This will return a resultset of rows that is row-level-locked with a "SELECT ... FOR UPDATE" query,
you should ensure that any scheduling decisions are made in a single transaction -- as soon as the
transaction is committed it will be unlocked.
"""
```

Scheduler 的 `_create_dagruns_for_dags` 就是利用到 `dags_needing_dagruns` 的其中一個地方
then create DagRun for Dags that need it.

https://github.com/apache/airflow/blob/04d3c440e3c741b0f2d9ac4d34d2f09f8b41a38b/airflow-core/src/airflow/jobs/scheduler_job_runner.py#L1499


`_critical_section_enqueue_task_instances`
create TaskInstances for execution by moving them from

`_executable_task_instances_to_queued`

use `with_row_locks(query, of=TI, session=session, skip_locked=True)` to avoid multiple executors picking up the same TaskInstance.

## Fully support running more than one scheduler concurrently #10956

https://github.com/apache/airflow/pull/10956