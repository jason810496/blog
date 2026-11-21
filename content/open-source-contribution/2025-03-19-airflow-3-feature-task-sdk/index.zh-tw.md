---
title: "2025 03 19 Airflow 3 Feature Task Sdk"
summary: ""
description: ""
date: 2025-03-19T15:05:17+08:00
slug: "airflow-3-feature-task-sdk"
tags: ["blog","zh-tw"]
# series: ["Documentation"]
# series_order: 9
cascade:
  showEdit: true
  showSummary: true
  hideFeatureImage: false
draft: false
---

## How to understand the TaskSDK implementation in Airflow 3.0 ( without breaking your brain )

Reference:
- https://github.com/apache/airflow/pull/46869/files
- https://github.com/apache/airflow/pull/44605/files

## Note

This note is written after [`airflow` module moving to `airflow-core`](https://lists.apache.org/thread/vjx3j1o5j1h2m6qdcqpmt35wq5lwbsl9)


## Execution API ( and its Client )

Though we have Core API ( Public API ), however for Airflow 3.0, we need to **block** dags directly access to DB.
So there will be a new API : Execution API ( `airflow.api_fastapi.execution_api` )

The generated datamodels ( via pre-commit to generate ) will be in `airflow.sdk.api.datamodels._generated`

https://github.com/apache/airflow/pull/44449/files

### Execution API Client

The API client of Execution API will be in `airflow.sdk.api.client.Client`.
And there are `<Entity>Operations` classes in `airflow.sdk.api.client` to handle the operations of each entity.

e.g.
```python
class VariableOperations:
    __slots__ = ("client",)

    def __init__(self, client: Client):
        self.client = client

    def get(self, key: str) -> VariableResponse | ErrorResponse:
        """Get a variable from the API server."""
        try:
            resp = self.client.get(f"variables/{key}")
        except ServerResponseError as e:
            if e.response.status_code == HTTPStatus.NOT_FOUND:
                log.error(
                    "Variable not found",
                    key=key,
                    detail=e.detail,
                    status_code=e.response.status_code,
                )
                return ErrorResponse(error=ErrorType.VARIABLE_NOT_FOUND, detail={"key": key})
            raise
        return VariableResponse.model_validate_json(resp.read())

    def set(self, key: str, value: str | None, description: str | None = None):
        """Set an Airflow Variable via the API server."""
        body = VariablePostBody(val=value, description=description)
        self.client.put(f"variables/{key}", content=body.model_dump_json())
        # Any error from the server will anyway be propagated down to the supervisor,
        # so we choose to send a generic response to the supervisor over the server response to
        # decouple from the server response string
        return {"ok": True}
```

## `airflow.models` -> `airflow.sdk.definition.<Entity>`

## Execution Time

### `airflow.sdk.execution_time.comms` Communication protocol between the Supervisor and the task process

The reason to having this communication protocol is detailed in the following docstring:

airflow.sdk.execution_time.comms.py#L18-L42