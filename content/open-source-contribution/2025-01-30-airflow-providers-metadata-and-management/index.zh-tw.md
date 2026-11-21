---
title: "2025 01 30 Airflow Providers Metadata and Management"
summary: ""
description: ""
date: 2026-01-30T14:17:10+08:00
slug: "airflow-providers-metadata-and-management"
tags: ["blog","zh-tw"]
# series: ["Documentation"]
# series_order: 9
cascade:
  showEdit: true
  showSummary: true
  hideFeatureImage: false
draft: false
---

## provider.yaml v.s. get_provider_info.py

- will be update by `update-providers-build-files` pre-commit hook
  - it run `update-providers-build-files` breeze command under the hook
    - `jinja_context = get_provider_documentation_jinja_context`
      - `get_provider_jinja_context`
        - `"PROVIDER_INFO": get_provider_info_dict(provider_id)`
          - get the `provider.yaml` content as dict
          - `get_provider_info_dict`: Retrieves provider info from the provider yaml file
    - `_generate_build_files_for_provider`
      - `_generate_get_provider_info_py`
        - `get_provider_info_TEMPLATE.py.jinja2`
          ```python
          def get_provider_info():
            return {{ PROVIDER_INFO }}
          ```
- who is source of truth?
  - `provider.yaml` is source of truth at codebase level
  - since `prek` (pre-commit) will update the `provider.yaml` to `get_provider_info.py`
  - `get_provider_info.py` is source of truth at runtime level
  - since we will use `importlib_metadata.metadata` to discover (import) the `get_provider_info.py::get_provider_info`