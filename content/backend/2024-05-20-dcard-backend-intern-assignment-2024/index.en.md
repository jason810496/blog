---
title: "2024 Dcard Backend Intern Assignment"
summary: "2024 Dcard Backend Intern Assignment"
description: "2024 Dcard Backend Intern Assignment"
date: 2024-09-21T21:52:52+08:00
slug: "dcard-backend-intern-assignment-2024"
tags: ["blog","en","backend","intern","system-design","dcard"]
# series: ["Documentation"]
# series_order: 9
cascade:
  showEdit: true
  showSummary: true
  hideFeatureImage: false
draft: false
---

> The gopher image is created by [gophers](https://github.com/egonelbre/gophers).

My Dcard interview notes can be found here:  <br>
{{< article link="/intern/summer-intern-interview-2024-dcard/" >}}

This post focuses on analyzing, designing, and implementing the backend internship assignment for Dcard 2024.  <br>
The final implementation can be found here:  
{{< github repo="jason810496/Dcard-Advertisement-API" >}}

## Assignment Description

The full assignment details are available at:  <br>
https://github.com/jason810496/Dcard-Advertisement-API/blob/main/2024%20Backend%20Intern%20Assignment.pdf  
Below is a simplified version: <br>

### Scenario

Using Golang, implement a simplified **advertisement serving service** that includes 2 RESTful APIs:  <br>
1. Admin API: Create advertisements with conditions.
2. Serving API: List all matching ads based on query conditions.

### Detailed Explanation

**Admin API**

> Only `Create` needs to be implemented (no need for List/Update/Delete).  
Field structure:
- `Title`: Advertisement title
- `StartAt`: Ad start time (active time)
- `EndAt`: Ad end time (active time)
- `Conditions`: Ad display conditions
  - All conditions are **optional**
  - Each condition can have **multiple selections**
  - Condition structure:
    - `Age`: `int:1~100`
    - `Gender`: `enum:M, F`
    - `Country`: `enum:TW, JP, ...` (ISO 3166-1 compliant)
    - `Platform`: `enum:android, ios, web`

**Serving API**

> Only `List` needs to be implemented (no need for Create/Update/Delete).  
- List active ads that match the conditions (`StartAt < Now < EndAt`).
- Support query parameters for filtering ads.
- Support pagination:
  - Use `limit` and `offset` to control results.
  - Sort by `endAt` in ascending order (ASC).

### Requirements, Assumptions, and Constraints

#### Implementation Requirements

- The serving API must handle over **10,000** RPS.
- **No need** to implement authentication.
- Validate parameters and handle errors appropriately.
- Write proper tests.
- Document the design choices and approach.

#### Assumptions and Constraints

- No more than **3000** ads will be created daily.
- Any third-party libraries are allowed.
- Any external storage solutions are allowed.

### API Example

Admin API: The following example represents an ad targeting users aged 20–30 in Taiwan or Japan, using Android or iOS, without gender restriction.
```bash
curl -X POST -H "Content-Type: application/json" \
  "http://<host>/api/v1/ad" \
  --data '{
     "title": "AD 55",
     "startAt": "2023-12-10T03:00:00.000Z",
     "endAt": "2023-12-31T16:00:00.000Z",
     "conditions": {
        {
           "ageStart": 20,
           "ageEnd": 30,
           "country": ["TW", "JP"],
           "platform": ["android", "ios"]
        }
     }  
  }'
```

Serving API: Request example
```bash
curl -X GET -H "Content-Type: application/json" \
  "http://<host>/api/v1/ad?offset=10&limit=3&age=24&gender=F&country=TW&platform=ios"
```
Serving API: Response example
```json
{
    "items": [
        {
            "title": "AD 1",
            "endAt": "2023-12-22T01:00:00.000Z"
        },
        {
            "title": "AD 31",
            "endAt": "2023-12-30T12:00:00.000Z"
        },
        {
            "title": "AD 10",
            "endAt": "2023-12-31T16:00:00.000Z"
        }
    ]
}
```

## Analysis

The task can be summarized as:  <br>
**Designing a read-heavy API capable of querying all records that match specific conditions over a certain time range.**

The basic approach starts with caching, primarily using Redis for server-side caching.  <br>
The challenge is designing an efficient and low-cost cache solution.

## Solution 1

When an ad is created, it is also stored in Redis.  <br>
A `Gender:Platform:Country:AgeRange:uuid` String key is created with a TTL based on the `EndAt` field. <br>
```
`F:android:TW:20-30:uuid1`: "title1,end1",
`M:ios:JP:30-40:uuid2`: "title2,end2",
```

**Creating an Ad:**  <br>
When an ad is created in the DB, a goroutine is also triggered to create a corresponding Redis key.

**Querying Ads:**  <br>
Use `SCAN` to search and store results in a `cache:Gender:Platform:Country:Age` ZSet key.  <br>
The TTL is relatively short (e.g., 5–10 minutes).  
> This allows subsequent searches with the same conditions but different offset/limit values to query efficiently.  
> It's like a secondary cache for searches, preventing repeated `SCAN` operations.

**Deleting Ads:**  <br>
- For String keys: TTL is set during creation, so no further action is needed.
- For ZSet keys: TTL is short (5–10 minutes), so no additional handling is required.

### Pros

- Each ad is stored as an independent key, making modifications easy.
- Ads have corresponding TTLs, avoiding the need for a separate mechanism to expire ads in Redis.

### Cons

- Inefficient use of Redis:
  - Storing all DB data in Redis isn't utilizing Redis purely as a cache.
- Excessive key usage:
  - Assuming 10 countries:
    - 3000 active ads as Strings.
    - 2 * 3 * 100 * 10 (Gender * Platform * Age * Country).
    - 6000 ZSets for ad combinations.
    - At least 9000 keys.
- Search efficiency is low:
  - Without a search cache, each `SCAN` has `O(N)` time complexity.
  - Additional processing is needed for age-based queries.

## Solution 2

Partition by Age, using 101 Hashes:
- Key: `ad:Age` (Age = `all` for all ages).
- Mapping:
  - Key: `Gender:Platform:Country`.
  - Value: Serialized ad list.
```
ad:0: {
        `F:android:TW`: [],
        `M:ios:JP`: [],
        ...
},
ad:1: {
        `Gender:Platform:Country`: [],
        ...
},
...
ad:99: {
        `Gender:Platform:Country`: [],
        ...
},
ad:all: {
        `Gender:Platform:Country`: [],
        ...
}
```

**Creating an Ad:**  
The ad is stored in the corresponding partitions for `ageStart` to `ageEnd`.  
This requires a `Lua Script` to ensure ACID properties.

**Querying Ads:**  
Use `HSCAN` with the `MATCH` option to filter ads in the corresponding partition.  
`HSCAN` returns a `cursor` for pagination.

**Deleting Ads:**  
A cron job periodically checks all partitions to clean up expired ads.  
Depending on consistency requirements, you might use `Lua Script` for ACID guarantees.  
Otherwise, `HSCAN` + `HDEL` is a sufficient alternative.

## System Architecture

### Initial Architecture

Originally, for Redis caching, I planned to use the **Redis Sentinel** architecture  
- To achieve **High Availability** and **Read Scalability**.


{{< mermaid >}}
flowchart TD
    Ingress[Ingress] 

    subgraph APCluster["`**Stateless AP**`"]
        subgraph AP1LocalCache[Local Cache]
        AP1[AP 1]
        end
        subgraph AP2LocalCache[Local Cache]
        AP2[AP 2]
        end
        subgraph AP3LocalCache[Local Cache]
        AP3[scale by k8s ...]
        end
    end
    %% Ingress --> AP1 & AP2 & AP3
    
    subgraph HAProxyCluster[HAProxy Deployment]
    HAProxy1[Proxy instance]
    HAProxy2[Standby]
    end

    subgraph RedisCluster["`Redis **sentinel**`"]
    RedisReplica1[(Replica 1)]
    RedisMaster[(Primary)]
    RedisReplica2[(Replica 2)]
    end

    Ingress --> APCluster -- Public API
    ( Query active AD )--> HAProxyCluster 
    HAProxyCluster -- load balance Read request --> RedisCluster
    %% HAProxyCluster --> RedisReplica1 & RedisReplica2

    subgraph PgCluster["`Postgres **Primary Replica**`"]
    PG[(Postgres\nPrimary)]
    PgReplica[(Postgres\nReplica)]
    PG -- WAL --> PgReplica
    end

    RedisMaster & RedisReplica1 & RedisReplica2 ---> PG & PgReplica
    APCluster == Admin API
    ( Create AD ) ==> PG


    %% subgraph CornWorkers[Cornjob Workers]
    %% ActiveWorker[Cornjob: Pre-heat AD]
    %% DeactiveWorkder[Cornjob: Deactive AD]
    Corn[CornJob]
    %% end
  
    %% PG <--> ActiveWorker --> RedisMaster
    %% PG <--> DeactiveWorkder --> RedisMaster

    RedisMaster <-- Pre-heat or aeactive AD
    ( use Lua script for atomic operation ) --> Corn <-- Query oncomming AD--> PG
{{< /mermaid >}}

### Final Architecture


{{< mermaid >}}
flowchart TD
    Ingress[Ingress] 

    
    Ingress --> APCluster

    subgraph APCluster["`**Stateless AP**`"]
        
        subgraph AP2LocalCache[Local Cache]
        AP2[AP 2]
        BG2[BG goroutine]
        AP2 -.- BG2
        end

        subgraph AP1LocalCache[Local Cache]
        AP1[AP 1]
        BG1["`Internal goroutine
        refresh local Cache`"]
        AP1 -.- BG1
        end

        
        
        
        subgraph AP3LocalCache[Local Cache]
        AP3[scale by k8s ...]
        BG3[BG goroutine]
        AP3 -.- BG3
        end
    end
    

    Redis[("Redis standalone")]


    AP1LocalCache -. "`Public API
    (if cached)`" .-> Redis

    AP1LocalCache -. "`Public API
    (if cached)`" .-> Redis


    subgraph PgCluster["`Postgres **Primary Replica**`"]
    PG[(Postgres\nPrimary)]
    PgReplica[(Postgres\nReplica)]
    PG -- WAL --> PgReplica
    end

    AP2LocalCache -. "`Public API
    (if not cache)`" .-> PG & PgReplica

    AP3LocalCache -. "`Public API
    (if not cache)`" .-> PG & PgReplica

    AP3LocalCache == Admin API
    ( Create AD ) ==> PG


    Corn[CornJob]

    Redis <-. "`Pre-heat or daeactive AD
    ( use **Lua** script for atomic operation )`" .-> Corn <-.-> PG
{{< /mermaid >}}

## Data Bottleneck: Postgres

Even with Redis serving as the server-side cache,  
the QPS still did not meet the initial target,  
and there was still a large amount of traffic hitting Postgres.  
> From the CPU and Memory usage:  
> Postgres CPU utilization reached 90%.

The solution at that time was to add an additional layer of **Local Cache** at the API level,  
with a background goroutine periodically updating the Local Cache.

After adding this Local Cache layer,  
the system managed to reach the goal of 10,000 RPS locally.

## Areas for Further Optimization

As I write this retrospective in September 2024,  
I’ve noticed some details that were overlooked in the original implementation:

1. Database Indexing
2. System Stability
3. Sharding

### Database Indexing

Back then, I used the [Gorm](https://gorm.io/) ORM to interact with Postgres.  
Gorm only creates an index on the Primary Key,  
but does not index other fields.

It would be useful to benchmark different combinations of indexes  
and determine which fields benefit from adding specific types of indexes for better performance.

### System Stability

At the time, when I realized that Redis caching still resulted in substantial traffic to Postgres,  
I didn't consider **system stability**.  
Instead, I hastily added a layer of Local Cache to hit the QPS target.

I should have used **[singleFlight](https://github.com/golang/sync/tree/master)**  
to prevent **high traffic from overwhelming Postgres**,  
(at least filtering out duplicate queries).  
This would have kept Postgres QPS within a reasonable range  
and ensured overall system stability.

### Sharding

During the interview follow-up on scalability,  
questions like: "What if there are 30 countries and 5 platforms?" arose.  
How do you maintain the same QPS target?

It’s easy to mention sharding,  
but in practice, implementing a stable, scalable system using sharding isn't that simple.  
If I had the opportunity, I would like to experiment with implementing it.
