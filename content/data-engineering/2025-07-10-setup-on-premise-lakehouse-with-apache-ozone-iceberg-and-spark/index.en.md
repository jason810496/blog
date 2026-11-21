---
title: "2025 07 10 Setup on Premise Lakehouse With Apache Ozone Iceberg and Spark"
summary: ""
description: ""
date: 2025-07-08T11:43:48+08:00
slug: "setup-on-premise-lakehouse-with-apache-ozone-iceberg-and-spark"
tags: ["blog","en"]
# series: ["Documentation"]
# series_order: 9
cascade:
  showEdit: true
  showSummary: true
  hideFeatureImage: false
draft: false
---

## Lakehouse Architecture

ACID transactions, schema evolution, and time travel

## Apache Ozone

https://ozone.apache.org/docs/edge/start/kubernetes.html

## Apache Iceberg

https://hub.docker.com/r/tabulario/iceberg-rest
https://github.com/databricks/iceberg-rest-image
https://www.tabular.io/blog/rest-catalog-docker/

https://www.tabular.io/apache-iceberg-cookbook/getting-started-connect-rest-catalog/

https://www.dremio.com/blog/apache-iceberg-101-your-guide-to-learning-apache-iceberg-concepts-and-practices/#h-hands-on-apache-iceberg-exercises

CATALOG_IO__IMPL

https://iceberg.apache.org/spark-quickstart/?h=catalog_io__impl#docker-compose

### Kafka Connect

https://iceberg.apache.org/docs/1.8.1/kafka-connect/#configuration
https://github.com/databricks/iceberg-kafka-connect

## Spark on Kubernetes

https://cloud.google.com/bigquery/docs/blms-rest-catalog

## Trino on Kubernetes

https://trino.io/docs/current/installation/kubernetes.html
https://documentation.alluxio.io/ee-da-en/compute/trino-on-kubernetes


trino + iceberg
https://trino.io/docs/current/object-storage/metastores.html#rest-catalog


## References

- Architecture of a Lakehouse
  - https://medium.com/engineering-cloudera/open-data-lakehouse-powered-by-apache-iceberg-on-apache-ozone-a225d5dcfe98
- Apache Ozone
  - https://ozone.apache.org/docs/edge/start/kubernetes.html
- Apache Polaris with Apache Iceberg
  - https://www.confessionsofadataguy.com/how-i-barely-survived-setting-up-polaris-as-an-iceberg-rest-catalog/
  - https://www.dremio.com/blog/getting-hands-on-with-polaris-oss-apache-iceberg-and-apache-spark/
- Apache Iceberg with Apache Spark
  - https://www.chenshaowen.com/blog/use-iceberg-and-spark-on-kubernetes.html
  - https://medium.com/@kurangdoa/apache-iceberg-with-spark-in-kubernetes-minikube-b178cb5daacf

[![Star History Chart](https://app.repohistory.com/api/svg?repo=apache/airflow&type=Date&theme=dark&transparent=false&color=f86262)](https://app.repohistory.com/star-history)


## TODO

- fix polaris ./polaris setup guide