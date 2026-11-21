---
title: "2026 03 23 Edge Worker"
summary: ""
description: ""
date: 2026-03-23T16:27:47+08:00
slug: "edge-worker"
tags: ["blog","en"]
# series: ["Documentation"]
# series_order: 9
cascade:
  showEdit: true
  showSummary: true
  hideFeatureImage: false
draft: false
---

• airflow.providers.edge3 is a pull-based remote execution provider for Airflow. The central Airflow cluster still does scheduling and state management; remote “edge” machines only run an airflow edge worker process that polls for
work over HTTP, executes tasks locally, and reports status/logs back.

Main Pieces

- Provider registration is in providers/edge3/src/airflow/providers/edge3/get_provider_info.py:24. That wires in the executor, CLI, DB manager, and plugin.
- The scheduler-side executor is providers/edge3/src/airflow/providers/edge3/executors/edge_executor.py:55. It does not execute tasks itself; it writes serialized workloads into provider tables.
- The provider-owned tables are providers/edge3/src/airflow/providers/edge3/models/edge_job.py:37, providers/edge3/src/airflow/providers/edge3/models/edge_worker.py:91, and providers/edge3/src/airflow/providers/edge3/models/
  edge_logs.py:36, managed by providers/edge3/src/airflow/providers/edge3/models/db.py:51.
- The API/UI plugin is providers/edge3/src/airflow/providers/edge3/plugins/edge_executor_plugin.py:94. It mounts a FastAPI app from providers/edge3/src/airflow/providers/edge3/worker_api/app.py:31 under /edge_worker and, on newer
  Airflow, a React admin UI.
- The worker process is started by the CLI in providers/edge3/src/airflow/providers/edge3/cli/edge_command.py:107 and implemented in providers/edge3/src/airflow/providers/edge3/cli/worker.py:94.

Runtime Flow

1. A task targeted at EdgeExecutor gets serialized and inserted into edge_job by providers/edge3/src/airflow/providers/edge3/executors/edge_executor.py:85. The row stores queue, pool-slot-based concurrency, and the serialized
    ExecuteTask payload.
2. A remote worker starts with airflow edge worker. It registers itself and begins heartbeating via providers/edge3/src/airflow/providers/edge3/cli/api_client.py:114 and providers/edge3/src/airflow/providers/edge3/cli/
    api_client.py:138. Server handlers are providers/edge3/src/airflow/providers/edge3/worker_api/routes/worker.py:166 and providers/edge3/src/airflow/providers/edge3/worker_api/routes/worker.py:202.
3. When the worker has free capacity, providers/edge3/src/airflow/providers/edge3/cli/worker.py:334 calls providers/edge3/src/airflow/providers/edge3/cli/api_client.py:166, which hits providers/edge3/src/airflow/providers/edge3/
    worker_api/routes/jobs.py:61. That query claims one queued job with FOR UPDATE SKIP LOCKED, filtered by queue and concurrency_slots <= free_concurrency.
4. The worker launches a child process to run the task through Task SDK supervision in providers/edge3/src/airflow/providers/edge3/cli/worker.py:199. The worker process talks to the edge API; the supervised task talks to the
    normal execution API URL, derived in providers/edge3/src/airflow/providers/edge3/cli/worker.py:83.
5. While the task runs, the worker updates job state through providers/edge3/src/airflow/providers/edge3/cli/api_client.py:180 into providers/edge3/src/airflow/providers/edge3/worker_api/routes/jobs.py:120, and streams log chunks
    through providers/edge3/src/airflow/providers/edge3/cli/api_client.py:198 into providers/edge3/src/airflow/providers/edge3/worker_api/routes/logs.py:92.
6. The scheduler periodically reconciles everything in providers/edge3/src/airflow/providers/edge3/executors/edge_executor.py:282: it marks dead workers as unknown/offline, handles orphaned jobs, and purges old finished jobs/
    logs.

A few important details:

- Worker auth is JWT-based and tied to the exact REST path being called, implemented in providers/edge3/src/airflow/providers/edge3/worker_api/auth.py:103 and generated client-side in providers/edge3/src/airflow/providers/edge3/
  cli/api_client.py:97.
- The server enforces exact Airflow and edge-provider version matches in providers/edge3/src/airflow/providers/edge3/worker_api/routes/worker.py:57.
- Maintenance/shutdown/queue/concurrency changes are centrally stored in edge_worker, then picked up by the worker on heartbeat in providers/edge3/src/airflow/providers/edge3/cli/worker.py:389. The same controls are exposed via
  CLI definitions in providers/edge3/src/airflow/providers/edge3/cli/definition.py and UI endpoints in providers/edge3/src/airflow/providers/edge3/worker_api/routes/ui.py:65.

If you want, I can next walk through one specific part line by line:

1. executors/edge_executor.py
2. cli/worker.py
3. worker_api/routes/jobs.py
4. worker_api/routes/worker.py