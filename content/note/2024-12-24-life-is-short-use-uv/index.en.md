---
title: "Life Is Short Use `uv`"
summary: "How to use `uv` to manage Python packages and projects"
description: "How to use `uv` to manage Python packages and projects"
date: 2024-12-24T15:56:36+08:00
slug: "life-is-short-use-uv"
tags: ["blog","en"]
# series: ["Documentation"]
# series_order: 9
cascade:
  showEdit: true
  showSummary: true
  hideFeatureImage: false
thumbnail: "https://avatars.githubusercontent.com/u/115962839?v=4"
draft: false
---

{{< alert "circle-info">}}

> The cover is from the official [`uv`](https://docs.astral.sh/uv/) documentation.

{{< /alert >}}

# Life Is Short Use `uv`

> An extremely fast Python package and project manager, written in Rust.

Only **fast** can describe `uv`. Once you use it, you won't go back to `poetry`!

## Download

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Usage

### Manage Virtual Environments

Creates a virtual environment in the `.venv` folder
```bash
uv python pin 3.12
uv venv

# or inline command
uv venv --python 3.12
```

### Install Packages

Sync the dependencies from `pyproject.toml` to the virtual environment
```bash
uv sync
```

Install a package
```bash
uv add requests
```

### pip Interface

`uv` provides an interface for `pip`
```bash
uv pip install -r requirements.txt
```

## FAQ

{{< alert "circle-info">}}

The default `ulimit` setting on MacOS (default `256`) is too low for the number of open file descriptors. <br>
This may cause a `Too many open files` error during installation.

You can change the file descriptor limit, for example, set it to `2048`:

```bash
ulimit -n 2048
```

{{< /alert >}}