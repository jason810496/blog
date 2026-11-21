### The Evolution of Large-Scale Software:

### Insights from Apache Airflow

---

## Table of Content


<div style="display: flex;">
  <div style="flex: 2; padding-right: 1em;">
    <ul>
      <li>What is Apache Airflow</li>
      <li>How Software Grows</li>
      <li>Codebase Management</li>
      <li>Continuous Integration</li>
      <li>Release</li>
      <li>Backward Compatibility</li>
    </ul>
  </div>
  <div style="flex: 1;">
    <p>#2630762</p>
    <img src="https://hackmd.io/_uploads/Hy8kGyFZge.png" alt="QR Code for NetDB: The Evolution of Large-Scale Software" style="width: 50%;" />
  </div>
</div>


---


### @Zhe-You(Jason) Liu

- **NCKU CSIE Junior**
- **Apache Airflow Committer**
- **LinkedIn:** [zhe-you-liu](https://linkedin.com/in/zhe-you-liu)
- **GitHub:** [jason810496](https://github.com/jason810496)

---

## What is Apache Airflow


----

![Airflow-Logo](https://www.apache.org/logos/res/airflow/airflow-1.png =70%x)

- **Top 5** project in **The ASF**
- **40k** stars on GitHub
- Used by over **80000+** companies
    - including Apple, Uber, LinkedIn ...
- Most Common Data orchestration Tool


----


```python 

import json

import pendulum

from airflow.sdk import dag, task

@dag(
    schedule=None,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    tags=["example"],
)
def tutorial_taskflow_api():
    
    @task()
    def extract():
        data_string = '{"1001": 301.27, "1002": 433.21, "1003": 502.22}'

        order_data_dict = json.loads(data_string)
        return order_data_dict

    @task(multiple_outputs=True)
    def transform(order_data_dict: dict):
        total_order_value = 0

        for value in order_data_dict.values():
            total_order_value += value

        return {"total_order_value": total_order_value}

    @task()
    def load(total_order_value: float):

        print(f"Total order value is: {total_order_value:.2f}")
        
    # dependencies
    order_data = extract()
    order_summary = transform(order_data)
    load(order_summary["total_order_value"])

tutorial_taskflow_api()

```

----

## Complex Workflow

![graph](https://hackmd.io/_uploads/rkmCUkt-lx.png)


----

## UI - Dag

![dag](https://blog.zhu424.dev/data-engineering/apache-airflow-101/dag-view_hu0ce8b986d186baead6e079512a6bc6fd_98303_1320x0_resize_lanczos_3.png =80%x)


----

## UI - Grid

![grid](https://hackmd.io/_uploads/BJ_iLkYZxl.png =80%x)

----

### What Problems Does Airflow Solve?

- **Workflow Observability**
- **Retryability of Workflows**
- **Significantly reduce** operational workload


----

## More about Apache Airflow

- My Blog - [Apache Airflow 101](https://blog.zhu424.dev/zh-tw/data-engineering/apache-airflow-101/)
- What problems does it solve?
- Understand its
    - common use cases
    - architecture
    - limitations

---

## How Software Grows

----

### For Big Features

- **The ASF style**
    - **Improvement Proposal**
    - Design Document
        - Example: [AIP-72](https://cwiki.apache.org/confluence/display/AIRFLOW/AIP-72+Task+Execution+Interface+aka+Task+SDK)

----

### Proposal lifecycle


![Proposal Lifecycle](https://hackmd.io/_uploads/BJQGR1tbxg.jpg =50%x)



----

### Voting Process


- at least 72 hours
    - (extend if weekend)
- **binding votes**
    - **only committers or PMC**
- non-binding votes
    - community

----

### Voting Process

- give **+1 and -1 votes**.
    - at least **3 +1 binding votes** 
- **any -1 binding vote**
    - back to `Discuss`

----

### More about Voting Process

- [Apache Voting Process](https://www.apache.org/foundation/voting.html#votes-on-code-modification)
- [Dev Mail](https://lists.apache.org/list.html?dev@airflow.apache.org)

----


### After Accepted

- **break down** the proposal into
    - smaller tasks
    - manageable tasks
- **GitHub Projects**
    - Track Issues with Kanban
    - AIP-XX
    - [Airflow GitHub Projects](https://github.com/apache/airflow/projects)

---

## Codebase Management

----

### Monorepo vs Polyrepo

![image](https://hackmd.io/_uploads/B1-7TPKbxe.png =70%x)
> Image from [Decoding Microfrontends: Monorepo x Polyrepo Dilemma](https://blog.stackademic.com/monorepo-vs-polyrepo-the-differences-68f6f995ae2f)

----

### Monorepo (Single Repository)

- **Unified version control**
- **Unified CI/CD** pipelines
- **Simplified dependency management**
- **Atomic changes** across projects
- **Code sharing** between projects

----

### Polyrepo (Multiple Repositories)

- **Project isolation**
- **Independent deployment**
- **Granular permissions**
- **Technology diversity**
- **Smaller repos** (faster cloning)

----

### Airflow - Monorepo


* ``apache-airflow-core``
    * core of Apache Airflow (there are few more s separated)
* ``apache-airflow-task-sdk``
    * task-sdk distribution that are imported by the providers
* ``apache-airflow-providers-*``
    * More than 90 providers to communicate with external services


----

### Airflow Provider Structure

Each provider is a separate python project, with its own ``pyproject.toml`` file and similar structure:

```

  PROVIDER
         |- pyproject.toml   # project configuration
         |- provider.yaml    # additional metadata for provider
         |- src
         |.   \- airflow.providers.PROVIDER
         |                                \ # here are hooks, operators, sensors, transfers
         |- docs   # docs for provider are stored here
         \- tests
                | -unit
                |      | PROVIDER
                |               \ # here unit test code is present
                | - integration
                |             | PROVIDER
                |                      \ # here integration test code is present
                \- system
                         | PROVIDER
                                  \ # here system test code is present
                                  
```

----

### Airflow Providers System

- **Independent versioning**
  - Each provider has its own version
- **Independent release cycles**
  - Release when needed
- **Reduced dependencies**
  - Install only what you need
- **Technical decoupling**

```bash
pip install apache-airflow-providers-amazon==7.3.0
```

----

### When to Split Into Modules (Code level)?

![image](https://hackmd.io/_uploads/ByoC1dt-lx.png =70%x)
> Image from [The Clean Code Blog](https://blog.cleancoder.com/)

----

### Key Principle: Single Source of Truth

> "Don't copy any code"

- **Extract common code** into shared libraries
- **Make reusable components, interfaces**
- **Avoid duplicated logic** across teams

---

## Continuous Integration

----

### Local CI Before each Commit

- **Code Quality and Linting**
  - Code must pass **black, ruff, mypy**
  - **pre-commit** checks (Git Hook)
- **Static analysis**
  - Catch bugs early
  - Ensures consistent style


----

### Pre-commit

![pre-commit](https://blog.zhu424.dev/open-source-contribution/becoming-an-apache-airflow-committer-from-0/pre-commit-hooks_hu813f725f8cb2da841674ddaa0f134996_210985_1320x0_resize_lanczos_3.png =50%x)

----

### Why Testing in CI?

- **100+ PRs weekly** need verification
- Testing ensures each PR:
  - Won't break existing features
  - Doesn't degrade performance
  - Maintains overall stability

----

### Testing Across Versions

- **Matrix testing**
  - Provider tests against multiple Core versions
- **Compatibility assertions**
  - Verify behavior consistency
- **Integration tests**
  - Ensure components work together

----

### Testing Pyramid

![Testing Pyramid](https://ctf-cci-com.imgix.net/5yK8Y4Xyw9UrFKrwofhpRY/93abeed26295d8be191b53da9bf62ca5/article-image-2.png?ixlib=rb-3.2.1&w=2000&auto=format&fit=max&q=60 =70%x)
> From [circleci/testing-pyramid](https://circleci.com/blog/testing-pyramid/)

----

### Testing Levels

- **Unit Testing**
  - Testing individual functions/modules
  - Uses Mock objects for isolation
- **Integration Testing**
  - Testing interactions between modules
  - Requires actual databases/services
- **System Testing**
  - Testing complete Airflow workflows
  - Similar to End-to-End testing

----

### Good PR = More Test Code

- **Test Coverage** matters:
  - Each `if` means 2 test cases
  - PR should cover all possible paths
- **Quality over quantity**
  - Test code often > product code

----

### Example: My First PR

- [PR #42902](https://github.com/apache/airflow/pull/42902/files)
- Product code change: **1 line**
- Test code:
  - Multiple test cases
  - Mock objects
  - 20+ discussion comments

----

> "A good PR example has test code 
> several times longer than product code"
>
> "Code without tests that explodes in 
> production is really annoying"
>
> - [JC Tech](https://www.facebook.com/share/p/15pSudbSPq/)

---

## Release

----

### Semantic Versioning

- Format: **MAJOR.MINOR.PATCH** (X.Y.Z)
- **MAJOR**: Incompatible API changes
- **MINOR**: New features (backward-compatible)
- **PATCH**: Bug fixes (backward-compatible)

----

### Examples in Airflow

- `1.10.15` → `2.0.0`: Breaking API changes
- `2.0.0` → `2.1.0`: New features, backward compatible
- `2.1.0` → `2.1.1`: Bug fixes only

----

### Branch Management Strategy

![a-normal-week-in-airflow](https://hackmd.io/_uploads/H1PLWeYWee.png)


- **100+ Active PRs** weekly!
    - Just a normal week in Airflow

----

### Branch Types

- **main**:
  - Current development branch
  - Next Major or Minor version features
- **vX-Y-stable**:
  - Release branch
  - Used for official releases
- **vX-Y-test**:
  - Patch branch
  - Bug fixes after release

----

![git-diagram](https://hackmd.io/_uploads/r1J6egKZlg.svg)


----

### Real-world Example

- Airflow just released `3.0.1`
- `main` branch contains features for `3.1.0`
- Using Airflow `2.8.3` and hit a bug?
  - Check `v2-8-test` branch, not `main`!

----

### Backporting

- Fixing bugs across versions
- Two approaches:
  - **Automated Cherry-pick**
    - With label `backport-to-vX-Y-test`
    - Works for minimal branch differences
  - **Manual Backport PR**
    - For branches with thousands of commits difference

----

### Providers Release

- Unique to Airflow
- Released from `main` branch
- Independent versioning
- Allows focused updates

---


## Backward Compatibility

----

### What is Backward Compatibility?

- Ability of **newer software versions** to:
  - Work with **older data formats**
  - Support **older APIs**
  - Not break **existing functionality**

----

### Why It Matters

- **User trust**
  - Users won't update if upgrades break workflows
- **Support costs**
  - Breaking changes increase support burden
- **Ecosystem health**
  - Extensions and plugins need stability
- **Adoption rates**
  - Smoother updates = faster adoption

----

### Airflow's Complexity

- **Independent release cycles**
  - Core: `3.0.1` → `3.1.0`
  - Providers: Their own schedule
- **Dependencies between components**
  - Core API changes affect Providers
  - Provider updates must work with multiple Core versions

----

### Core Compatibility Strategies

- **Deprecation cycles**
  - Mark features as deprecated before removal
  - Warnings for at least one minor release
- **Interface stability**
  - Stable public APIs vs internal APIs
- **Compatible parameter changes**
  - Default parameters preserved
  - New parameters are optional

----

### Provider Compatibility Strategies

- **Support matrix**
  - Each Provider declares compatible Core versions
  - Example: `apache-airflow-providers-google>=8.0.0` 
    - `"apache-airflow": ">=2.4.0"`
- **Feature detection**
  - Check Core features before using them

----

### Example: Breaking Changes in `3.0.0`

- **Removed previously deprecated features**
  - But were warned about in `2.x` releases
- **Changed parameter defaults**
  - With migration path documented
- **Providers adapted** for both:
  - New Core API in `3.0.0`
  - Backward compatibility with `2.x`


----

### Documentation Best Practices

- **Version-specific notes**
- **Migration guides**
- **Compatibility tables**
- **Code examples** for different versions

----

### Example: Compatible Interfaces

```python
if AIRFLOW_V_3_0_PLUS:
    from airflow.utils.log.file_task_handler import StructuredLogMessage

    header = [
        StructuredLogMessage(
            event="::group::Log message source details",
            sources=[host for host in logs_by_host.keys()],
        ),  # type: ignore[call-arg]
        StructuredLogMessage(event="::endgroup::"),
    ]  # type: ignore[misc]

    message = header + [
        StructuredLogMessage(event=concat_logs(hits)) for hits in logs_by_host.values()
    ]

    # greater than 3.0
    if not AIRFLOW_V_3_0:
        from airflow.providers.elasticsearch.version_compat import (
            get_compatible_output_log_stream,
        )

        message = get_compatible_output_log_stream(message)  # type: ignore[assignment]
else:
    message = [
        (host, concat_logs(hits))  # type: ignore[misc]
        for host, hits in logs_by_host.items()
    ]
```