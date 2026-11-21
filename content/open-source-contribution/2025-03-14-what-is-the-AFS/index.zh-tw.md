---
title: "2025 03 14 What Is the AFS"
summary: ""
description: ""
date: 2025-03-15T18:22:49+08:00
slug: "what-is-the-AFS"
tags: ["blog","zh-tw"]
# series: ["Documentation"]
# series_order: 9
cascade:
  showEdit: true
  showSummary: true
  hideFeatureImage: false
draft: false
---


### Apache Software Foundation

Apache Software Foundation (ASF) 是一個非營利組織，致力於支持 Apache 軟體基金會的開源軟體專案 <br>
ASF 旗下有許多知名的開源專案，如 Hadoop、Kafka、Airflow 等 <br>

### Committer

Committer 是 ASF 專案的核心貢獻者，負責對專案進行維護、開發、審查等工作 <br>
Committer 有權限對專案進行寫入操作，如合併 PR、發布版本等 <br>
Committer 由 PMC (Project Management Committee) 選出 <br>

{{< mermaid >}}

graph TD;
    
    subgraph ASF[Apache Software Foundation]
        style ASF fill:#ffcccc,stroke:#333,stroke-width:2px, color:#ffffff, font-size: 20px, font-weight: bold;
        
        %% Kafka Project
        subgraph KafkaProject["Kafka Project"]
            style KafkaProject fill:#ff9999,stroke:#333,stroke-width:1px;
            
            subgraph KafkaCommitter["Committer"]
                style KafkaCommitter fill:#ff6666,stroke:#333,stroke-width:1px;
                
                subgraph KafkaProjectManagementCommittee["PMC"]
                    style KafkaProjectManagementCommittee fill:#ff3333,stroke:#333,stroke-width:1px;
                    
                end
            end
        end

        %% Airflow Project
        subgraph AirflowProject["Airflow Project"]
            style AirflowProject fill:#ff9999,stroke:#333,stroke-width:1px;
            
            subgraph AirflowCommitter["Committer"]
                style AirflowCommitter fill:#ff6666,stroke:#333,stroke-width:1px;
                
                subgraph AirflowProjectManagementCommittee["PMC"]
                    style AirflowProjectManagementCommittee fill:#ff3333,stroke:#333,stroke-width:1px;
                    
                end
            end
        end


        %% Hadoop Project
        subgraph HadoopProject["Hadoop Project"]
            style HadoopProject fill:#ff9999,stroke:#333,stroke-width:1px;
            
            subgraph HadoopCommitter["Committer"]
                style HadoopCommitter fill:#ff6666,stroke:#333,stroke-width:1px;
                
                subgraph HadoopProjectManagementCommittee["PMC"]
                    style HadoopProjectManagementCommittee fill:#ff3333,stroke:#333,stroke-width:1px;
                    
                end
            end
        end
    end



{{< /mermaid >}}

>

{{< alert "circle-info" >}}

關於 ASF 與 Committer 的更多資訊，也可以參考 [Byron Hsu](https://github.com/ByronHsu)大大的[Open Source 開源社群的第一門課 | 如何成為 Apache Committer](https://byronhsu1230.medium.com/open-source-%E9%96%8B%E6%BA%90%E7%A4%BE%E7%BE%A4%E7%9A%84%E7%AC%AC%E4%B8%80%E9%96%80%E8%AA%B2-%E5%A6%82%E4%BD%95%E6%88%90%E7%82%BA-apache-committer-451d42e853d6) 的文章

{{< /alert >}}