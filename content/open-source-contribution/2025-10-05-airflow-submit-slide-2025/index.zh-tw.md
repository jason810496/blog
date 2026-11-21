---
title: "2025 10 05 Airflow Submit Slide 2025"
summary: ""
description: ""
date: 2025-10-05T19:02:08+08:00
slug: "airflow-submit-slide-2025"
tags: ["blog","zh-tw"]
# series: ["Documentation"]
# series_order: 9
cascade:
  showEdit: true
  showSummary: true
  hideFeatureImage: false
draft: false
---

# Slide

- Title: Becoming an Apache Airflow Committer from 0
- Subtitle: Ship Code, Earn Trust, Lead Change

## About me

My information

## Table of Content

1. Why Contribute to Open Source
2. Areas to Contribute
3. How to get started
4. From the first PR to Committer
5. Summary and Takeaways

## 1. Why Contribute to Open Source

### Before Contributing

- Coding skills
- Design Patterns, Unit Test, Code Review
- System Level Design

### After Contributing

- Collaborate with top contributors over the world
- Communication Skills
- Design Documentation
- Career Opportunities (?)

## 2. Areas to Contribute

- Three typical contribution scenarios
- Background Knowledge before Contributing
- Scope-level Opportunities
- More Tips for Picking Issues

### Three typical contribution scenarios

- Non-code Contribution
  - Documentation
  - Translations
- Code Contribution
  - Bug Fix
  - New Feature
  - Improvement
- Code Review
  - I'm still learning on how to give better feedback for code reviews as well :)

### Background Knowledge before Contributing

#### Entities most known for Contributing to Core
- DagModel
- DagRun
- Task
- TaskInstance

#### User-facing Documentation

- The overall architecture of Airflow
- How to write Dag
- Classic features
  - TaskFlow API
  - Sensor
  - Trigger
  - Dynamic Task Mapping
  - XCom
  - Pools
  - Variables
  - Connections

#### We are good to go for contributing!

### Areas by difficulty

TODO: Update title

Scope

- Beginner Tasks
  - Unit test coverage
  - Type annotations
  - MyPy improvements
- Easy
  - Translations!
  - Documentation
  - Provider
  - CLI
- Mid
  - API Server
  - React UI
  - Breeze!
  - CI / CD Plan
    - CI Infrastructure
    - Integration tests, e2e tests, Kubernetes system tests
  - Helm Chart
  - Core Models
- Hard
  - Assets (Datasets)
  - Serialization
  - Scheduler
  - TaskSDK -> kind of system programming


### More Tips for Picking Issues

- Easy to start with
  - Good first issue
- Pick something you are interested in
  - [Based on GitHub Labels](https://github.com/apache/airflow/labels?page=4)
    - Directly find your interested area
      - Core API
      - TaskInstance Log
  - GitHub Projects
    - After having some context of the Proposal, feel free to pick up issue from there
- Dev Mailing List
- Join development of latest features by feature
  - Common interface for Versioning RemoteDagBundles
  - Providers Common Message Queue Package

## 3. How to get started

- Code Contribution
- Setting up Dev Env
- Some Tips for using Breeze
- Code Review

### Code Contribution (Fix, Feature)
- Make sure don't take issue of someone else ( avoid duplicate work )
- Start with small change
  - it will be easier to get review and merged
  - avoid burnout
- Backward compatibility
- Test coverage for your change

### Code Contribution (Improvements)
- Feel free to open issue to discuss before start working on it
  - Especially when change on the interface or not-compatible
    - Describe Trade-Off
- Or raise discussion on Dev Mailing List if it's a bigger change
- Avoid waste of time if we are not in right direction

### Setup Airflow Dev Env with 1 Step - Breeze
- [Contributor's Quick Start](https://github.com/apache/airflow/blob/d43b468c1852fb94f29748126242400cf22bb411/contributing-docs/03_contributors_quick_start.rst)
- [Airflow Breeze](https://github.com/apache/airflow/blob/main/dev/breeze/doc/README.rst)

Some Tips for using Breeze
```
breeze --backend postgres
# run pytest after entering the container
pytest airflow-core/...
```

```
breeze start-airflow --backend postgres
```

Advance Usage of Breeze
```
breeze start-airflow --backend postgres --integration localstack --integration elasticsearch --mount-sources providers-and-tests --use-airflow-version 3.0.6
```

Testing Latest Provider with Different version of Airflow Core
- reference: https://github.com/apache/airflow/pull/53821#issuecomment-3172693426


## Code Review

- Good communication skill
- Be kind to others!
- Provide constructive feedback
- Be open to discussion and different viewpoints



## 4. From the first PR to Committer

### 300 Hours in 5 months

- image
- avg 2 hours per day

### Dev Mailing List Invitation

image

### Apache Mail Address

image

### Keep Contributing

- Graph
- Merge PR, Review PR
- Link to gh-graph-generator
  - 40 to 60 reviews per month after becoming Committer

### No fast path, Just steady contribution

- Show the impact to the community!

## 5. Summary and Takeaways

- Background Knowledge before Contributing
- Note of using AI
- Some Mindsets
- Some Project to get started

### Background Knowledge before Contributing

- Dag And TaskInstance Entities
- User-phasing Docs
- Start with small change, learn along the way
  - No need to BFS / DFS on the whole codebase ?

### Note of using AI
- Simple answer, Yes
- Be responsible

### Some Mindsets
- Don’t burnout, enjoy the process
- Small steps, Big changes
- Be patient
- Be kind

### Some Project to get started
- [AIP-86: Deadline Alerts - Providers](https://github.com/apache/airflow/issues/55237)
- [CI/ CD Improvements](https://github.com/orgs/apache/projects/403)
- [UI Test Coverage](https://lists.apache.org/thread/hpbbmo2tokj6zzc9044vc66tdqcnbrjd)
- Improving Test Coverage
- Improving Type Annotations
- Improving MyPy Coverage


### Happy Contributing!

## Reference 

- https://www.reddit.com/r/dataengineering/comments/jhfg6p/long_time_opensource_users_start_contributing_to/
- https://blog.zhu424.dev/open-source-contribution/becoming-an-apache-airflow-committer-from-0/
- https://airflowsummit.org/slides/2021/y1-ContributingJourney.pdf