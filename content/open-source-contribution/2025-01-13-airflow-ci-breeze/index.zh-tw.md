---
title: "2025 01 13 Airflow Ci Breeze"
summary: ""
description: ""
date: 2026-01-13T11:46:19+08:00
slug: "airflow-ci-breeze"
tags: ["blog","zh-tw"]
# series: ["Documentation"]
# series_order: 9
cascade:
  showEdit: true
  showSummary: true
  hideFeatureImage: false
draft: false
---

# Apache Airflow 的持續整合 (CI) 系統介紹

持續整合作 (CI, Continuous Integration) 是作為保證 Apache Airflow 軟體品質的重要一環，任何微小的 fix, new feature 或即使是修改一行文件都會經過規模大小不一的整合測試 (integration tests) 來確保不會破壞現有的功能，確保 Apache Airflow 軟體的穩定性與可靠性。

以上個月 (2025 年 12 月) 到今天 (2026 年 1 月 14 日) 為例，**即使是在聖誕和新年假期**，Apache Airflow 合併**超過 600 個 PR**，而每個 PR 都會觸發 CI 系統來執行測試。這些測試涵蓋了從單元測試 (unit tests) 到系統測試 (system tests)，確保每一個改動都不會引入新的錯誤。

在個一個月內，總共跑了超過 **兩十萬** 次 GitHub Action Jobs，跑了接近 **三百萬** 分鐘的測試時間 (約等於 2000 天)。這代表每一個對 CI 的優化都能夠大幅減少整體的測試時間和資源消耗，讓開發者能夠更快地收到回饋，提升開發效率。

這篇文章將介紹 Apache Airflow 的 CI 系統架構，並說明 Apache Airflow 的 CI 是如何達到

- remote 和 local 執行環境的一致性與可重現性
- 如何動態且最大程度自動化的根據 PR 的內容來決定要跑哪些測試
- 

## Highlevel overview

## Get Workflow Info

```bash
breeze ci get-workflow-info 2>> ${GITHUB_OUTPUT}
```

```
pr-labels = ['backport-to-v3-1-test']
target-repo = apache/airflow
head-repo = eladkal/airflow
pr-number = 60446
event-name = pull_request
runs-on = ["ubuntu-22.04"]
canary-run = false
run-coverage = false
head-ref = edge
```

## selective checks

- ci image/ prod image
- selective checks based on files changed
- selective checks based on PR labels
- selective checks based on commit messages



```bash
breeze ci selective-check 2>> ${GITHUB_OUTPUT}
```

`GITHUB_OUTPUT` content:
```
all-python-versions = ['3.10']
all-python-versions-list-as-string = 3.10
all-versions = false
amd-runners = ["ubuntu-22.04"]
any-provider-yaml-or-pyproject-toml-changed = false
arm-runners = ["ubuntu-22.04-arm"]
['airflow-core/docs/core-concepts/executor/index.rst']
basic-checks-only = false
ci-image-build = true
common-compat-changed-without-next-version = false
core-test-types-list-as-strings-in-json = [{"description": "API...Serialization", "test_types": "API Always CLI Core Other Serialization"}]
debug-resources = false
default-branch = main
default-constraints-branch = constraints-main
default-helm-version = v3.17.3
default-kind-version = v0.30.0
default-kubernetes-version = v1.30.13
default-mysql-version = 8.0
default-postgres-version = 14
default-python-version = 3.10
disable-airflow-repo-cache = false
prod-image-build = false
provider-dependency-bump = false
providers-compatibility-tests-matrix = [{"python-version": "3.10", "airflow-version": "2.11.0", "remove-providers": "common.messaging edge3 fab git keycloak", "run-unit-tests": "true"}, 
{"python-version": "3.10", "airflow-version": "3.0.6", "remove-providers": "", "run-unit-tests": "true"}, {"python-version": "3.10", "airflow-version": "3.1.5", "remove-providers": "", "run-unit-tests":
"true"}]
providers-test-types-list-as-strings-in-json = null
pyproject-toml-changed = false
python-versions = ['3.10']
python-versions-list-as-string = 3.10
run-airflow-ctl-integration-tests = false
run-airflow-ctl-tests = false
run-amazon-tests = false
run-api-codegen = false
run-api-tests = false
run-go-sdk-tests = false
run-helm-tests = false
run-javascript-scans = false
run-kubernetes-tests = false
run-mypy = false
run-ol-tests = false
run-python-scans = false
run-system-tests = true
run-task-sdk-integration-tests = false
run-task-sdk-tests = false
run-ui-e2e-tests = false
run-ui-tests = false
run-unit-tests = true
runner-type = ["ubuntu-22.04"]
shared-distributions-as-json = ["secrets_masker", "plugins_manager", "secrets_backend", "listeners", "dagnode", "configuration", "module_loading", "logging", "timezones", "observability"]
skip-prek-hooks = check-provider-yaml-valid,flynt,identity,lint-helm-chart,ts-compile-lint-simple-auth-manager-ui,ts-compile-lint-ui
skip-providers-tests = true
sqlite-exclude = []
testable-core-integrations = ['kerberos', 'redis']
testable-providers-integrations = ['celery', 'cassandra', 'drill', 'tinkerpop', 'kafka', 'mongo', 'pinot', 'qdrant', 'redis', 'trino', 'ydb']
ui-english-translation-changed = false
upgrade-to-newer-dependencies = false
```

```
Changed files:

('airflow-core/docs/core-concepts/executor/index.rst',)
FileGroupForCi.ENVIRONMENT_FILES did not match any file.
FileGroupForCi.API_FILES did not match any file.
FileGroupForCi.GIT_PROVIDER_FILES did not match any file.
FileGroupForCi.STANDARD_PROVIDER_FILES did not match any file.
FileGroupForCi.TESTS_UTILS_FILES did not match any file.
FileGroupForCi.ALL_SOURCE_FILES matched 1 files.
['airflow-core/docs/core-concepts/executor/index.rst']
FileGroupForCi.UI_FILES did not match any file.
FileGroupForCi.ALL_SOURCE_FILES enabled because it matched 1 changed files
SelectiveCoreTestType.API did not match any file.
SelectiveCoreTestType.CLI did not match any file.
SelectiveCoreTestType.SERIALIZATION did not match any file.
FileGroupForCi.KUBERNETES_FILES did not match any file.
FileGroupForCi.SYSTEM_TEST_FILES did not match any file.
FileGroupForCi.ALL_PROVIDERS_PYTHON_FILES did not match any file.
FileGroupForCi.ALL_PROVIDERS_DISTRIBUTION_CONFIG_FILES did not match any file.
FileGroupForCi.ALWAYS_TESTS_FILES did not match any file.
Remaining non test/always files: 1
We should run all core tests except providers.There are 1 changed files that seems to fall into Core/Other category
{'airflow-core/docs/core-concepts/executor/index.rst'}
Selected core test type candidates to run:
['API', 'Always', 'CLI', 'Core', 'Other', 'Serialization']
FileGroupForCi.DOC_FILES matched 1 files.
['airflow-core/docs/core-concepts/executor/index.rst']
FileGroupForCi.DOC_FILES enabled because it matched 1 changed files
FileGroupForCi.API_FILES disabled because it did not match any changed files
FileGroupForCi.ASSET_FILES did not match any file.
FileGroupForCi.ASSET_FILES disabled because it did not match any changed files
FileGroupForCi.ALL_PYPROJECT_TOML_FILES did not match any file.
FileGroupForCi.TASK_SDK_FILES did not match any file.
FileGroupForCi.TASK_SDK_FILES disabled because it did not match any changed files
FileGroupForCi.DEVEL_TOML_FILES did not match any file.
FileGroupForCi.ALL_AIRFLOW_PYTHON_FILES did not match any file.
FileGroupForCi.ALL_DEV_PYTHON_FILES did not match any file.
FileGroupForCi.ALL_DEVEL_COMMON_PYTHON_FILES did not match any file.
FileGroupForCi.ALL_AIRFLOW_CTL_PYTHON_FILES did not match any file.
FileGroupForCi.KUBERNETES_FILES disabled because it did not match any changed files
FileGroupForCi.HELM_FILES did not match any file.
FileGroupForCi.HELM_FILES disabled because it did not match any changed files
FileGroupForCi.TASK_SDK_FILES disabled because it did not match any changed files
FileGroupForCi.TASK_SDK_INTEGRATION_TEST_FILES did not match any file.
FileGroupForCi.TASK_SDK_INTEGRATION_TEST_FILES disabled because it did not match any changed files
FileGroupForCi.AIRFLOW_CTL_FILES did not match any file.
FileGroupForCi.AIRFLOW_CTL_FILES disabled because it did not match any changed files
FileGroupForCi.AIRFLOW_CTL_INTEGRATION_TEST_FILES did not match any file.
FileGroupForCi.AIRFLOW_CTL_INTEGRATION_TEST_FILES disabled because it did not match any changed files
FileGroupForCi.UI_FILES disabled because it did not match any changed files
FileGroupForCi.AIRFLOW_CTL_FILES disabled because it did not match any changed files
FileGroupForCi.API_CODEGEN_FILES did not match any file.
FileGroupForCi.API_CODEGEN_FILES disabled because it did not match any changed files
FileGroupForCi.GO_SDK_FILES did not match any file.
FileGroupForCi.GO_SDK_FILES disabled because it did not match any changed files
FileGroupForCi.JAVASCRIPT_PRODUCTION_FILES did not match any file.
FileGroupForCi.JAVASCRIPT_PRODUCTION_FILES disabled because it did not match any changed files
FileGroupForCi.PYTHON_PRODUCTION_FILES did not match any file.
FileGroupForCi.PYTHON_PRODUCTION_FILES disabled because it did not match any changed files
FileGroupForCi.ALL_PYTHON_FILES did not match any file.
FileGroupForCi.UI_ENGLISH_TRANSLATION_FILES did not match any file.
```

## 一些對於 Airflow CI 來說關鍵的 GitHub Actions 功能

這邊會以兩個問題來說明 Airflow CI 最關鍵的地方

### 要如何在 Jobs 之間傳遞資訊？ (GitHub Actions 要如何做到 Airflow XCom？)

上游的 job 可以定義 `jobs.<job_id>.outputs` 來定義要輸出變數  

**upstream job example**

```yaml
jobs:
  upstream-job:
    runs-on: ubuntu-latest
    outputs:
      output1: ${{ steps.step1.outputs.test }}
      output2: ${{ steps.step2.outputs.test }}
    steps:
      - id: step1
        run: echo "test=hello" >> "$GITHUB_OUTPUT"
      - id: step2
        run: echo "test=world" >> "$GITHUB_OUTPUT"
```

只要在 steps 中執行的任何 command 能夠 redirect 變數到 `$GITHUB_OUTPUT` ，就能夠被定義成 job 的輸出變數。  
如: 我們也可以執行一個 python script 並將結果寫入 `$GITHUB_OUTPUT`。

```python
# generate_upstream_outputs.py
import os

if __name__ == "__main__":
  with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
    for i in range(3):
      f.write(f"output{i}=value-{i}\n")
```

即使是用 script 動態產生的輸出變數，還是需要在 `jobs.<job_id>.outputs` 中定義要需要輸出給其他下游 job 的變數名稱。  
以這個範例來說，雖然 `generate_upstream_outputs.py` 會產生 `output0`, `output1`, `output2` 三個輸出變數，但只有 `output1` 和 `output2` 被定義在 `jobs.upstream-job.outputs` 中，所以下游 job 只能存取到這兩個變數。

```yaml
jobs:
  upstream-job:
    runs-on: ubuntu-latest
    outputs:
      # downstream job can only access outputs defined here
      # so the `generate-outputs.outputs.output0` is not accessible
      output1: ${{ steps.generate-outputs.outputs.output1 }}
      output2: ${{ steps.generate-outputs.outputs.output2 }}
    steps:
      - id: generate-outputs
        run: python generate_upstream_outputs.py
```

**downstream job example**

然後在下游的 job 使用 `needs.<job_id>.outputs.<output_name>` 來取得上游 job 的輸出變數。

```yaml
jobs:
# Assuming upstream-job is defined above
  downstream-job:
    runs-on: ubuntu-latest
    needs: [upstream-job] # We need to declare the dependency here !!!
    steps:
      - name: Use outputs from upstream job
        run: |
          echo "Output 1: ${{ needs.upstream-job.outputs.output1 }}"
          echo "Output 2: ${{ needs.upstream-job.outputs.output2 }}"
```

- https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/pass-job-outputs
- https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#jobsjob_idoutputs
- https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#jobsjob_idneeds

### 要如何只跑特定的 Job？ (GitHub Actions 要如何做到 Airflow 的 Condition？)

可以透過 `jobs.<job_id>.if` 來定義 job 執行的條件。

**example**

```yaml
jobs:
  conditional-job:
    runs-on: ubuntu-latest
    if: ${{ github.event_name == 'pull_request' && contains(github.event.pull_request.labels.*.name, 'run-conditional-job') }}
    steps:
      - name: Run only on PRs with specific label
        run: echo "This job runs only on PRs with 'run-conditional-job' label."
```

- https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#jobsjob_idif


## Architecture


### Selective Checks 機制

> https://github.com/apache/airflow/tree/main/dev/breeze/doc/ci


我一開始以為 Selective Checks 主要是根據 PR 上由 boring bot 自動標的 PR Label 來決定要跑哪些測試。但實際上 Selective Checks 主要是根據當前 PR 所更改到的檔案範圍來決定要跑哪些測試，PR Label 只是其中一個輔助的資訊來源之一。

- 檔案變更範圍 (Files Changed)
  - 屬於那些子系統 (Core, Providers, UI, Helm Chart, Kubernetes, Airflow CTL, Task SDK 等等)
  - 更改檔案數量
- 特殊檔案 (e.g. pyproject.toml, CI 框架本身等)
- GitHub Action Event (是 push, schedule 還是 pull_request 等)
- PR Labels (但目前並沒有特別整合 `area:xxx` labels)

- `build-info` job:
  - pre-define all the output of selective checks
  - by defining:
```yaml
jobs:
# ...
  build-info:
    # At build-info stage we do not yet have outputs so we need to hard-code the runs-on to public runners
    outputs:
      # ...
      run-api-codegen: ${{ steps.selective-checks.outputs.run-api-codegen }}
      run-api-tests: ${{ steps.selective-checks.outputs.run-api-tests }}
      run-coverage: ${{ steps.source-run-info.outputs.run-coverage }}
      run-go-sdk-tests: ${{ steps.selective-checks.outputs.run-go-sdk-tests }}
      run-helm-tests: ${{ steps.selective-checks.outputs.run-helm-tests }}
      run-kubernetes-tests: ${{ steps.selective-checks.outputs.run-kubernetes-tests }}
      run-mypy: ${{ steps.selective-checks.outputs.run-mypy }}
      run-system-tests: ${{ steps.selective-checks.outputs.run-system-tests }}
      run-task-sdk-tests: ${{ steps.selective-checks.outputs.run-task-sdk-tests }}
      run-task-sdk-integration-tests: ${{ steps.selective-checks.outputs.run-task-sdk-integration-tests }}
      runner-type: ${{ steps.selective-checks.outputs.runner-type }}
      run-ui-tests: ${{ steps.selective-checks.outputs.run-ui-tests }}
      run-ui-e2e-tests: ${{ steps.selective-checks.outputs.run-ui-e2e-tests }}
      run-unit-tests: ${{ steps.selective-checks.outputs.run-unit-tests }}
      run-www-tests: ${{ steps.selective-checks.outputs.run-www-tests }}
      # ...
    steps:
    # some setup steps ...
    - name: "Install Breeze"
      uses: ./.github/actions/breeze
      id: breeze
    - name: "Get information about the Workflow"
      id: source-run-info
      run: breeze ci get-workflow-info 2>> ${GITHUB_OUTPUT}
      env:
        SKIP_BREEZE_SELF_UPGRADE_CHECK: "true"
    - name: Selective checks
      id: selective-checks
      env:
        PR_LABELS: "${{ steps.source-run-info.outputs.pr-labels }}"
        COMMIT_REF: "${{ github.sha }}"
        VERBOSE: "false"
      run: breeze ci selective-check 2>> ${GITHUB_OUTPUT}
```

- [breeze ci selective-check 實作](https://github.com/apache/airflow/blob/26a9d3b81b1d514ac00476885ba29676cd8f27e6/dev/breeze/src/airflow_breeze/commands/ci_commands.py#L260-L271)
- [`SelectiveChecks` 的 `__str__` 屬性](https://github.com/apache/airflow/blob/26a9d3b81b1d514ac00476885ba29676cd8f27e6/dev/breeze/src/airflow_breeze/utils/selective_checks.py#L486-L495) 剩下就是根據各種條件來決定要跑哪些測試

### 各個子系統測試的 Job 定義

這邊以 Helm Tests 為例，說明如何根據 Selective Checks 的結果來決定要不要跑這個 Job。

各個子系統測試都是依賴 `build-info` job 的輸出變數再搭配 `if` 條件來決定要不要跑這個 Job，並且剩下的測試都只有 `needs: [build-info, build-ci-images]`，所以各個子系統測試都是平行執行的。

```yaml
jobs:
# ...
  tests-helm:
    name: "Helm tests"
    uses: ./.github/workflows/helm-tests.yml
    needs: [build-info, build-ci-images]
    permissions:
      contents: read
      packages: read
    with:
    # partial list of inputs passed from build-info job
      runners: ${{ needs.build-info.outputs.runner-type }}
      platform: ${{ needs.build-info.outputs.platform }}
      helm-test-packages: ${{ needs.build-info.outputs.helm-test-packages }}
      default-python-version: "${{ needs.build-info.outputs.default-python-version }}"
      use-uv: ${{ needs.build-info.outputs.use-uv }}
    # only if helm tests are required
    # based on the selective checks output
    if: >
      needs.build-info.outputs.run-helm-tests == 'true' &&
      needs.build-info.outputs.default-branch == 'main' &&
      needs.build-info.outputs.latest-versions-only != 'true'
```

- [jobs.tests-helm](https://github.com/apache/airflow/blob/26a9d3b81b1d514ac00476885ba29676cd8f27e6/.github/workflows/ci-amd-arm.yml#L381-L382)

## Example

- [Remove experimental note from EdgeExecutor #10714](https://github.com/apache/airflow/actions/runs/20952103684/job/60207742385?pr=60446)
