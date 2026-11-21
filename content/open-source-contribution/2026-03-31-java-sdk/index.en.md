---
title: "2026 03 31 Java Sdk"
summary: ""
description: ""
date: 2026-03-31T11:43:38+08:00
slug: "java-sdk"
tags: ["blog","en"]
# series: ["Documentation"]
# series_order: 9
cascade:
  showEdit: true
  showSummary: true
  hideFeatureImage: false
draft: false
---


**Based on patched-airflow.py and example/src/java/org/apache/airflow/example/JavaExample.java, the JavaExample.java can work for both return the dag-structure (dag-processing, JavaDagFileProcessorProcess) and the execution runtime (JavaActivitySubprocess), is it because of the the Java Comm Server will return different response based on the in-comming request?**

Yes, but the important detail is that it is not JavaExample.java deciding the mode by itself. The Python side starts the same JAR in two different Airflow contexts, then sends a different first message over the comm socket.

In DAG processing, JavaDagFileProcessorProcess immediately sends DagFileParseRequest after the comm connection is accepted at patched-airflow.py:150. On the Java side, CoordinatorComm.handleIncoming matches that request type and returns a DagParsingResult built from bundle.dags at sdk/src/main/kotlin/org/apache/
airflow/sdk/execution/Comms.kt:194. That is why the same JavaExample bundle can produce DAG structure.

In task execution, JavaActivitySubprocess does not send a parse request. It calls _on_child_started(...) at patched-airflow.py:331, and the runtime path sends StartupDetails from the supervisor at sdk/src/main/kotlin/org/apache/airflow/sdk/execution/Supervisor.kt:129. Java then matches StartupDetails, looks up
bundle.dags[dagId].tasks[taskId], instantiates the task, runs it, and returns SucceedTask or TaskState("failed") at sdk/src/main/kotlin/org/apache/airflow/sdk/execution/Comms.kt:199.

So the answer is: yes, the Java comm layer returns different responses based on the incoming request type, but more precisely:

1. Python explicitly chooses which request to send first.
2. The Java Server only wires sockets; CoordinatorComm does the dispatch at sdk/src/main/kotlin/org/apache/airflow/sdk/Server.kt:62.
3. JavaExample.java works for both because its Bundle contains both the DAG definitions and the task classes at example/src/java/org/apache/airflow/example/JavaExample.java:47.

During runtime, the Java task can also send follow-up RPCs like GetConnection, GetVariable, GetXCom, and SetXCom through CoordinatorClient at sdk/src/main/kotlin/org/apache/airflow/sdk/execution/Client.kt:37, which is why task execution is a two-way protocol rather than a single response.
