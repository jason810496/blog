---
title: "EDP Architecture"
summary: ""
description: ""
date: 2025-08-30T14:36:38+08:00
slug: "edp-architecture"
tags: ["blog","zh-tw"]
# series: ["Documentation"]
# series_order: 9
cascade:
  showEdit: true
  showSummary: true
  hideFeatureImage: false
draft: false
---

{{< mermaid >}}


flowchart LR
    %% Customer/SDK Layer
    CD[Customer Device, App SDK] --> SDKAPI[SDK Team API]
    
    %% Integration Team Components
    SDKAPI --> ETK[Enterprise Topic Kafka<br/>online_event, profile]
    ETK --> |sync periodically<br/>mins, hourly| GCS[GCS / S3 / Object Store<br/>for backfill purpose]
    SR[Schema Registry<br/>Store schema from customer] -.-> ETK
    
    %% EDP Team Components
    ETK --> DISP[Dispatcher<br/>Grouping, BinPacking]
    DISP --> GBTK[Group Based Kafka Topic]
    
    %% Bronze Layer
    GBTK --> |x~xx second latency| BT[Bronze Table<br/>Delta Lake format<br/>Structure Streaming<br/>online_event, profile]
    BT --> |if upsert/append fail| BQT[Bronze Quarantine Table]
    
    %% Silver Layer
    BT --> |CDF, trigger hourly,<br/>half-hourly, read from<br/>Schema Registry| ST[Silver Table<br/>Dropdown List, Lifetime Count<br/>ID Mapping, online_event_app_id_platform]
    SR -.-> ST
    
    %% Downstream Access
    ST --> TRINO[Trino]
    TRINO --> DPT[Downstream Product Team<br/>Aixon, Aris, BB, ...]
    
    %% Optimization Job
    DOJ[Daily Optimization Job] --> ST
    DOJ --> BQT
    
    %% Backfill Process
    GCS -.-> |Backfill| ST
    
    %% Styling
    classDef customerLayer fill:#e1f5fe
    classDef integrationLayer fill:#f3e5f5
    classDef edpLayer fill:#e8f5e8
    classDef downstreamLayer fill:#fff3e0
    
    class CD,SDKAPI customerLayer
    class ETK,GCS,SR integrationLayer
    class DISP,GBTK,BT,BQT,ST,DOJ edpLayer
    class TRINO,DPT downstreamLayer

{{< /mermaid >}}

![alt text](image-1.png)

{{< mermaid >}}

flowchart LR
    %% Customer/SDK Layer
    CD2[SDK Team / Product Team] --> MH[Mongo Hotstore<br/>For real-time data access, OLTP use]
    
    %% EUU Components
    MH --> |Mongo Change stream| EUUK[EUU Kafka]
    EUUK --> EUUBT[EUU Bronze Table<br/>profile, session, profile_detail<br/>event, event_detail, ...]
    
    %% Downstream Access
    EUUBT --> DPT2[Downstream Product Team<br/>Direct Databricks Query]
    
    %% Styling
    classDef customerLayer fill:#e1f5fe
    classDef euuLayer fill:#f0f4c3
    classDef downstreamLayer fill:#fff3e0
    
    class CD2 customerLayer
    class MH,EUUK,EUUBT euuLayer
    class DPT2 downstreamLayer

{{< /mermaid >}}


{{< mermaid >}}

flowchart LR
    %% Customer Layer
    CD[Customer Device, App SDK] --> SDKAPI[SDK Team API]
    
    %% Integration Team
    SDKAPI --> ETK[Enterprise Topic Kafka]
    ETK --> GCS[Object Store<br/>Backfill]
    SR[Schema Registry] -.-> ETK
    
    %% EDP Pipeline
    ETK --> DISP[Dispatcher] --> GBTK[Group Kafka] --> BT[Bronze Table]
    BT --> BQT[Bronze Quarantine]
    BT --> ST[Silver Table]
    ST --> TRINO[Trino] --> DPT[Product Teams]
    
    %% EUU Pipeline
    SDKAPI --> MH[Mongo Hotstore]
    MH --> |Change Stream| EUUK[EUU Kafka] --> EUUBT[EUU Bronze]
    EUUBT --> DPT2[Product Teams<br/>Direct Query]
    
    %% Optimization
    DOJ[Daily Optimization] --> ST
    DOJ --> BQT
    
    %% Styling
    classDef integration fill:#f3e5f5
    classDef edp fill:#e8f5e8
    classDef euu fill:#f0f4c3
    classDef downstream fill:#fff3e0
    
    class ETK,GCS,SR integration
    class DISP,GBTK,BT,BQT,ST,TRINO,DOJ edp
    class MH,EUUK,EUUBT euu
    class DPT,DPT2 downstream

{{< /mermaid >}}


## EDD(Enterprise Device Data)

### SDK Team / Product Team:

Customer Device, App SDK -> SDK Team API

### Integration Team:

SDK Team / Product Team -> Enterprise Topic Kafka (online_event, profile )

Enterprise Topic Kafka -> sync periodically (mins, hourly) to -> GCS / S3 / Object store (for backfill purpose )

Schema Registry ( Store schema from customer )

### EDP(Enterprise Data Platform) Team:

Enterprise Topic Kafka -- Dispatcher(For grouping, BinPacking) --> Group Based Kafka Topic

Group Based Kafka Topic -- x~xx second latency --> Bronze Table (Delta Lake format, Structure Streaming, online_event, profile)

Bronze Table -- if upsert/ append to Silver Table fail --> Bronze Quarantine Table

Bronze Table -- CDF, trigger hourly, half-hourly -- read from Schema Registry --> Silver Table( Dropdown List, Lifetime Count, ID Mapping, online_event_{app_id}_{platform} )

Silver Table -> Trino -> Downstream Product Team (Aixon, Aris, BB, ...)

Daily Optimization Job -> Silver Table, Bronze Quarantine Table

#### Note for Dispatcher
- The original intension of Grouping is to have a unified unit of processing
    - For example
        - 2 big customers and 5 small customers as a single group
        - 10 small customers as a single group
        - Use BinPacking to fit in the group
    - If there are N groups, then we will have N Kafka Topics and N Bronze Pipelines
- However, when switch to Databricks, the Bronze Pipeline is efficient enough
- Even for all customer, we just need 1 group to have seconds level latency
- So the grouping logic is used for distinguishing "testing: group 0" and "production: group 1" for now

#### Note For Bronze Quarantine Table:
- Unified Quarantine Table for all feature (onlline_event, profile, Dropdown List, Lifetime Count, ID Mapping)
- Have a "feature" column, if any Bronze -> Silver can't upsert/ append, will add the whole DF as variant

#### Note For Silver Table
- Set CutOffTimestamp to future time when onboarding for Bronze CDF
- Trigger Backfill after Bronze CDF streaming start
- Backfill will take GCS, S3 Raw Data from Integration Team for backfill
- We need Silver Table since Downstream Product Team already adapt Trino
    - However, Trino don't support read from variant (till now, 2025 Aug 30th)
    - So we need silver table to transform variant to normal column for Trino usage
    - When Trino support read from variant, we can remove the silver table
        - Then product teams can directly query the bronze table for their needs
        - EDP will update views of bronze table
        - Which means lower latency access to the most recent data
            - Since bronze table latency is in seconds, but silver table latency is in hours
- Unified Silver Table: (Dropdown List, Lifetime Count, ID Mapping)
- Source Id Based Table: (Online event, Profile)
    - We use PySpark ThreadPool for fan-out, since we will read from 1 bronze table but write to multiple Silver Table
    - By mapping source_id to the corresponding silver table for each thread

## EUU(Enterprise Unified Data)


SDK Team / Product Team -> Mongo Hotstore (For real-time data access, OLTP use)
Mongo Hotstore -- Mongo Change stream --> EUU Kafka
EUU Kafka --> EUU Bronze Table (profile, session, profile_detail, event, event_detail, ...)

### Note for EUU

Since this is a new architecture, all the downstream product team will leverage Databricks to query, so the Bronze Table will be sufficient for their needs.