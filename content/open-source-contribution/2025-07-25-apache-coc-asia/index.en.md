---
title: "What Apache CommunityOverCode Asia 2025 Reveals About Asian Open Source and Data Infrastructure"
summary: "A localized data stack in China, streaming-first data infrastructure, enterprise open source investment, Open Governance, and lessons Taiwan's technical communities can take away."
description: "A localized data stack in China, streaming-first data infrastructure, enterprise open source investment, Open Governance, and lessons Taiwan's technical communities can take away."
date: 2026-05-28T11:51:30+08:00
slug: "apache-coc-asia"
tags: ["blog","en","open-source-contribution","data-engineering"]
# series: ["Documentation"]
# series_order: 9
cascade:
  showEdit: true
  showSummary: true
  hideFeatureImage: false
draft: false
---

{{< gallery >}}
  <img src="/open-source-contribution/apache-coc-asia/coc-asia-attendee-badge.jpeg" alt="Badge" class="grid-w100 md:grid-w50" />
{{< /gallery >}}

## Introduction

After attending [Apache CommunityOverCode Asia](https://asia.communityovercode.org/), my strongest impression was not simply that I had listened to several more technical talks about Apache projects. It was that Asia, especially large enterprises in China, has clearly grown an open source technical path that is different from the cloud data architectures commonly seen in North America.

If Apache CommunityOverCode North America felt to me like an intersection between Apache projects, cloud vendors, commercial products, and international users, then **Apache CommunityOverCode Asia felt more like bringing the large-scale data scenarios accumulated inside Chinese enterprises onto the Apache stage**. The sessions there naturally talked about traffic and business pressure from real production environments: live streaming, short videos, real-time recommendations, holiday promotions, flash sales, risk control, and similar scenarios.


## Regional Tech Stack Differences

The most direct observation from this trip was that **China's data infrastructure has a very strong regional tech stack**.

When people in North America or Taiwan discuss data platforms, it is easy to think of [Snowflake](https://docs.snowflake.com/), [Databricks](https://docs.databricks.com/), [BigQuery](https://cloud.google.com/bigquery/docs), [dbt](https://docs.getdbt.com/docs/introduction), [Apache Airflow](https://airflow.apache.org/docs/), [Apache Kafka](https://kafka.apache.org/documentation/), [Apache Spark](https://spark.apache.org/docs/latest/), [Kubernetes](https://kubernetes.io/docs/home/), plus a collection of managed cloud services. In China, many companies are not simply bringing in that same combination. Instead, they have spent years building their own open source stacks, which are then adopted, contributed to, and commercialized by other companies inside China.

Real-time computing is heavily centered around [Apache Flink](https://flink.apache.org/), rather than treating [Apache Spark](https://spark.apache.org/) as the default answer for data processing. In discussions about OLAP and Lakehouse architectures, I also repeatedly saw projects such as [Apache Doris](https://doris.apache.org/) and [Apache Paimon](https://paimon.apache.org/) mentioned.

**What impressed me was that [Apache Airflow](https://airflow.apache.org/) was almost invisible in orchestration contexts. In North America or Taiwan, any discussion about data pipelines almost certainly brings up [Airflow](https://airflow.apache.org/docs/). But after going through the Asia agenda and talking with people at almost every booth, the only engineer I met who knew [Airflow](https://airflow.apache.org/docs/) existed was at the [Cloudera](https://docs.cloudera.com/) booth**.

This is not simply a matter of different technical preferences. Many of these projects grew out of Chinese enterprises' own scenarios and were then adopted by other Chinese enterprises. Based on conversations on site, case studies, and booth materials, the user distribution of some projects was also clearly concentrated inside China. Their visibility among users outside China was much lower.

{{< gallery >}}
  <img src="/open-source-contribution/apache-coc-asia/open-source-developer-trends-slide.jpeg" alt="Open source developer trends presentation" class="grid-w100 md:grid-w50" />
  <img src="/open-source-contribution/apache-coc-asia/apache-openrank-project-ranking-slide.jpeg" alt="Apache OpenRank project ranking presentation" class="grid-w100 md:grid-w50" />
  <img src="/open-source-contribution/apache-coc-asia/apache-openrank-project-table-closeup.jpeg" alt="Close-up of the Apache OpenRank project table" class="grid-w100 md:grid-w50" />
{{< /gallery >}}

An open source project can live under Apache and operate through English documentation, GitHub issues, and mailing lists, but its actual users, contributors, commercial companies, and best practices can still be highly concentrated in a specific language, industry, or region. The Apache brand is global, but technical adoption is not always evenly globalized. Although these projects still follow "The Apache Way", most user discussions and development contributions **happen in Chinese on WeChat groups**.


## Ant Group's High-SLA Streaming Pipeline

The session that impressed me most on the afternoon of Day 1 was:

[Ant Group's Next Generation High SLA Stream Computing System Built on Apache Technology Stack](https://asia.communityovercode.org/sessions/streaming-880299.html)

![ant-group-stream-computing-talk](ant-group-stream-computing-talk.jpeg)
![real-time-asset-platform-slide](real-time-asset-platform-slide.jpeg)

The speaker began with several very practical questions:

1. How can the implementation difficulty of BI logic be reduced?
2. How should the SLA of a data pipeline be defined?
3. How can the SLA of a data pipeline be guaranteed?

This system was not a point optimization. It handled the pipeline lifecycle end to end. It distinguished between release process, maintaining mode, managed process, and not managed process. It also addressed how to observe and protect the entire pipeline when metrics are unavailable from upstream systems. Underneath, there was a SQL layer, a compute interface, and a design for compiling the same semantics into different compute engines such as [Flink](https://flink.apache.org/) and [Spark](https://spark.apache.org/docs/latest/).

What impressed me was not any single technical term, but the fact that "SLA" here was not just a simple alerting rule. It was the center of the system design. From bare metal classification, fault tolerance, master backup, hot backup, cold backup, and switch backup to observation and auto recovery for metrics across the whole pipeline, everything revolved around one idea: a data pipeline should not merely be able to run. It should be something the system can guarantee.

The speaker mentioned that this high-SLA stream computing system was no longer a proof of concept as of March 2025. It had become an engineering practice that needed to face real production environments.

**This made me think of where [Airflow](https://airflow.apache.org/docs/) is heading in 2026: it is moving toward more data workflow capabilities for the AI era**, such as the [Common AI Provider](https://airflow.apache.org/blog/common-ai-provider/), [AIP-105 Pluggable Retry Policies](https://cwiki.apache.org/confluence/display/AIRFLOW/AIP-105%3A%2BPluggable%2BRetry%2BPolicies), and the [LLM Retry Policy](https://airflow.apache.org/docs/apache-airflow-providers-common-ai/stable/retry_policies.html) in the [common-ai provider](https://airflow.apache.org/docs/apache-airflow-providers-common-ai/stable/index.html). If a retry policy can understand errors, outputs, context, and repair strategies more intelligently, then it is no longer just "rerun the task after failure". It can evolve toward a **self-healing data pipeline**.

In addition, [Astronomer](https://www.astronomer.io/) is already working on [Astro disaster recovery](https://www.astronomer.io/docs/astro/disaster-recovery) and [Astro Private Cloud data plane failover](https://www.astronomer.io/docs/astro-private-cloud/data-plane-failover). I do not think high-SLA pipelines should remain something only giant companies like Ant Group can build. By 2026, even a company with only dozens or hundreds of people should be able to use the Apache stack, managed platforms, AI retry policies, and standardized observability to build self-service, observable, self-healing data pipelines, as long as data pipelines are core infrastructure for that company.

This is also what I find interesting about where [Airflow](https://airflow.apache.org/docs/) can go next. It can become the control plane in a data platform responsible for coordination, observation, retries, governance, and self-healing. Hopefully, it can also let data engineers stop waking up at 3 a.m. to fix pipelines.

## A Shared Runtime for AI / ML Workloads: Ray

{{< gallery >}}
  <img src="ray-usage-1.jpeg" alt="Ray Usage 1" class="grid-w100 md:grid-w50" />
  <img src="ray-usage-2.jpeg" alt="Ray Usage 2" class="grid-w100 md:grid-w50" />
{{< /gallery >}}

Beyond streaming and data infrastructure, this conference also made me more clearly feel where [Ray](https://docs.ray.io/en/master/ray-overview/index.html) sits in AI / ML workloads. Although this was Apache's annual conference, Ray, which currently belongs to the [PyTorch Foundation](https://pytorch.org/foundation/), was still repeatedly mentioned in multiple sessions.

This was very different from the China data stack I mentioned earlier. Many Chinese enterprises build their own data infrastructure or deeply customize it, sometimes even growing new Apache projects out of it. But at the AI / ML runtime layer, the trend I saw was more like **"build on top of [Ray](https://docs.ray.io/en/master/ray-overview/index.html)"**, rather than every company reinventing its own distributed runtime.

My guess is that the distributed AI runtime problem is simply too deep: resource scheduling, mixed GPU / CPU workloads, distributed training, batch inference, model serving, fault tolerance, autoscaling, and observability are all hard problems. If [Ray](https://docs.ray.io/en/master/ray-overview/index.html) has already become a sufficiently general execution layer, the more practical approach for companies is usually to build their platform capabilities, permissions, data integration, task templates, cost governance, and internal workflows on top of it, instead of rewriting a distributed runtime from scratch.

## Streaming-First Data Infrastructure

Another very obvious difference was that data infrastructure in the Asia agenda naturally centered on streaming.

In my memory of Apache CommunityOverCode North America, streaming compute engines were not such a central theme. But in Asia, topics such as [Apache Flink](https://flink.apache.org/), [Apache Pulsar](https://pulsar.apache.org/docs/), message queues, streaming joins, and streaming warehouses naturally appeared on the main stage. This was not just a matter of technical preference. It reflected differences in the business scenarios themselves.

Large internet companies in China have many high-frequency scenarios: short-video recommendations, live-streaming interaction, live commerce, flash-sale events, ad delivery, and real-time risk control. These scenarios naturally push engineering teams toward streaming-first architectures because of their requirements for latency, throughput, stability, and data freshness. A message queue is not only a buffer layer between systems. It is the entry point for the entire real-time data flow. Stream processing is not merely a supplement to batch pipelines. It is the core of whether many business capabilities can exist at all.

{{< gallery >}}
  <img src="/open-source-contribution/apache-coc-asia/mq.jpeg" alt="Message Queue" class="grid-w100 md:grid-w50" />
  <img src="/open-source-contribution/apache-coc-asia/flink-sql-ai-talk.jpeg" alt="Flink SQL AI Talk" class="grid-w100 md:grid-w50" />
{{< /gallery >}}

This also explains why graph computing appeared more often than I had expected. The core problems of many large internet services are not single-table analytics, but networks of relationships: users, products, livestreamers, content, transactions, devices, IP addresses, risk-control events, recommendation paths, all connected to one another. When the data relationships themselves are complex and must also be processed in real time, graph and streaming naturally get discussed together.

![stream-graph-computing-talk](stream-graph-computing-talk.jpeg)
![stream-join-operator-slide](stream-join-operator-slide.jpeg)

One interesting session this time was [Accelerating Multi-stream Join by Stream Graph Computing](https://asia.communityovercode.org/sessions/streaming-907134.html). It discussed using Stream Graph Computing to accelerate multi-stream joins, which means reframing the streaming join problem as an incremental computation problem on a graph. When the business problem is fundamentally about relationships and paths, a graph compute engine is not just an academic topic. It has a chance to become part of real-time features, risk-control rules, and recommendation systems.

[Apache Fluss](https://fluss.apache.org/) was another example in this streaming-first trend that left a deep impression on me.

This project [entered the Apache Incubator in June 2025](https://incubator.apache.org/clutch/fluss.html), and Apache CommunityOverCode Asia 2025 was held from July 25 to 27, 2025. In other words, when I heard about it at the venue, it had almost just entered the Apache ecosystem and was still a very new project.

> ![Fluss](fluss.jpeg)
> As a side note, at the end of the session I also saw [Kafka](https://kafka.apache.org/documentation/) PMC [ChiaPing Tsai](https://github.com/chia7712) ask how the advantages [Fluss](https://fluss.apache.org/) claims over [Kafka](https://kafka.apache.org/documentation/) could be addressed from Kafka's perspective.

The session I remember most clearly was [When Flink Meets Fluss: The Future of Streaming Warehouse](https://asia.communityovercode.org/sessions/streaming-889266.html). It did not package [Fluss](https://fluss.apache.org/) as "yet another storage system". Instead, it placed Fluss very clearly inside the [Flink](https://flink.apache.org/) ecosystem: [Kafka](https://kafka.apache.org/documentation/) + [Flink](https://flink.apache.org/) is already a common combination for streaming warehouses and real-time analytics, but when data moves back and forth between message queues, stream processing, online serving, and lakehouse storage, system boundaries become increasingly complex. The emergence of Fluss is, to some extent, a response to that complexity.

July 2025 was the first time I saw this project. But by May 2026, when I was writing this article, I had already seen more and more posts and videos about [Fluss](https://fluss.apache.org/) on LinkedIn and YouTube. It is also one of the China-originated enterprise open source Apache projects that I have seen more often internationally so far, at least if we set open source models aside and look only at projects related to data infrastructure.

![kafka-4-highlights-talk](kafka-4-highlights-talk.jpeg)

Of course, I also had to attend the session from the OpenSource4You [#apache-kafka channel](https://opensource4you.slack.com/archives/C06MSQ9V4F3). I usually just lurk in the channel, so it was great to see [JiunnYang Huang](https://github.com/m1a2st), [PoAn Yang](https://github.com/FrankYang0529), [TengYao Chi](https://github.com/frankvicky), and [KuanPo Tseng](https://github.com/brandboat) share the new features in [Kafka 4.0](https://kafka.apache.org/40/documentation.html) in person. It was also especially exciting to see [ChiaPing Tsai](https://github.com/chia7712) discuss with the Fluss speaker on site about how to solve the core pain points in streaming scenarios.


## Enterprise Investment in Open Source

This conference also made it very clear how much Chinese enterprises value open source. It is not only about individual engineers contributing. Companies treat open source as part of technical influence, recruiting, commercialization, and standard setting.

At the venue, I saw many companies building their own data platforms with Apache projects, and also abstracting internal capabilities into open source projects. The scale and level of investment even reached the point where "open source software" could become part of performance evaluation. This is very different from the way Taiwanese companies often treat open source as "free software we can use".

I also saw many very young engineers on site, perhaps 24 or 26 years old, who were already responsible for maintaining important modules in certain Apache or open source projects at large companies, with titles such as Senior Engineer. This left a strong impression on me. Hiring in Chinese enterprises does not seem as tightly tied to master's degrees as it often is in Taiwanese companies.

## Open Source Is Not the Same as Open Governance

However, there is one issue that I think needs to be separated clearly: **Open Source and Open Governance are not the same thing**.

Many open source projects from China probably start when a company open sources its internal tech stack. This model usually has clear business needs, complete production scenarios, and a company willing to invest engineers in long-term maintenance, so the project can grow very quickly. But from a governance perspective, it often starts as a single-stakeholder project: the main roadmap, main maintainers, and main production requirements all come from the same company.

Even after some projects are donated to the ASF, governance does not become truly multi-party maintenance overnight. The ASF emphasizes [Community over Code](https://www.apache.org/foundation/) and consensus-based, community-driven governance. The [Apache Incubator](https://incubator.apache.org/) also helps podlings learn the Apache style of governance. But based on what I observed on site, **the main maintenance volume of many projects is still highly concentrated in the original company**. This does not mean those projects are bad. It means we need to recognize the distance between "the code is open source" and "the project is governed by multiple independent stakeholders".

This is also the interesting tension I see in open source in China: the volume of open source is large, and enterprise investment is real, but some projects feel more like company-level infrastructure being open sourced externally than open governance communities shaped from the beginning by multiple companies, individuals, and users.

![apache-developer-contribution-ranking-slide](apache-developer-contribution-ranking-slide.jpeg)

This also explains why Chinese enterprises have a better chance of growing their own data infrastructure through OSS, while this is less common in Taiwan. The business needs, user numbers, traffic scale, and data volume of large internet services in China are enough to support an entire team maintaining internal data infrastructure for the long term, and even open sourcing it, commercializing it, and donating it to a foundation. The scale and data volume of many Taiwanese companies are different. Directly using cloud services, managed databases, managed [Kafka](https://kafka.apache.org/documentation/), managed [Airflow](https://airflow.apache.org/docs/), and managed warehouses is often much cheaper than supporting an entire data infrastructure team.

So it is not that Taiwan lacks engineering ability. The economic model is different. When service scale has not yet grown large enough to require building the underlying systems in-house, it is hard for a company to justify assigning a group of engineers full time to maintain an open source data stack. This also makes open source in Taiwan more likely to appear in communities and individual contributions, rather than in large data infrastructure projects incubated by companies themselves.

## How Open Source Projects Become Companies

Several sessions in this year's agenda discussed OSS, commercialization, and startups together. On the morning of Day 2, I attended two of them:

- From Commits to Capital: Turning Open Source Passion into a Startup Journey by William Guo
- The Three Things That Make or Break a Software Startup by Rui Su

{{< gallery >}}
  <img src="/open-source-contribution/apache-coc-asia/open-source-startup-journey-talk.jpeg" alt="From Commits to Capital session" class="grid-w100 md:grid-w50" />
  <img src="/open-source-contribution/apache-coc-asia/software-startup-success-factors-talk.jpeg" alt="The Three Things That Make or Break a Software Startup session" class="grid-w100 md:grid-w50" />
{{< /gallery >}}

I found this type of topic very interesting because it was not simply about project governance or a technical roadmap. It directly asked: how can an OSS project driven by engineers and contributors become a startup that can survive?

These OSS-to-startup talks are something I saw less often at Apache CommunityOverCode North America. The North America event more often focused on technical evolution, use cases, foundation governance, release processes, and maintainer collaboration. The Asia event more directly put open source projects, enterprise scenarios, productization, and commercialization on the same table.

The most practical point from the first session was that an Apache project cannot become a commercial company on GitHub stars alone. Stars represent attention, but they do not represent revenue. What really matters is product value, business value, market value, and total addressable market.

It also did not describe open source startups in overly romantic terms. Commercializing an open source project brings many difficulties: Professional Services can easily become a labor-based service business; Managed Service will face competition from cloud vendors; Open Core requires maintaining both the open source edition and the commercial edition; if too many Enterprise Features are open, competitors may modify them and win bids at lower prices; but if too many are closed, community trust can be damaged.

So the essence of commercialization is not merely "packaging an open source project into a product". It requires clear decisions about:

- Which capabilities belong in the open source core?
- Which capabilities are enterprise-grade features, such as RBAC, environment separation, audit, and governance?
- How can contributors, users, and early adopters be converted into paying customers?

The second session was more about startup fundamentals: early marketing, blogs, tutorial videos, SEO, use cases, building in public, and Crossing the Chasm. Technical enthusiasts can bring you GitHub stars, but early adopters are the ones who are truly willing to test a product inside a company. In the early stage, the founder must also be the primary salesperson, because only the founder understands the real problem the product is trying to solve.

Looking at these two sessions together, they are actually part of the same story as the regional tech stack discussed earlier. If a place has enough real scenarios, enough enterprises willing to invest, and enough engineers willing to contribute, it will naturally grow open source projects, commercial companies, and a talent cycle.

## Taiwan's Technical Events Are Actually Not Small

After attending Apache CommunityOverCode Asia, and also CoC NA, **I actually feel even more strongly that Taiwan's technical community is not small**.

**If we look only at on-site attendance and community mobilization, COSCUP, SITCON, and PyCon Taiwan are all very large. In many cases, they even felt denser to me than the crowds at Apache CommunityOverCode Asia or North America**. Taiwan does not lack technical events, nor does it lack engineers willing to share. The real differences may be in industrial structure, how companies invest, and whether we turn community energy into long-term open source contributions.

Looking at the timeline, Taiwan actually started very early. [COSCUP 2006](https://coscup.org/2006/) was already held in 2006, while China's [Kaiyuanshe](https://kaiyuanshe.cn/article/How-to-join-KAIYUANSHE) was founded in 2014. In other words, **if we look only at the history of open source community activities, Taiwan did not start later. COSCUP began many years before Kaiyuanshe**.

But if we look at the current volume of open source contributions, China is clearly much larger than Taiwan. The [2024 China Open Source Annual Report](https://kaiyuanshe.github.io/2024-China-Open-Source-Report/data.html) also shows the rapid growth of China's open source ecosystem in contributors, projects, and adoption. Even if many contributions are concentrated in projects incubated by Chinese enterprises themselves, and are not necessarily contributions to globally adopted upstream projects, the total volume is still very substantial.

The difference here is not just whether the community is active. It is whether companies treat open source as a formal engineering strategy. Taiwan has a strong community culture, but large Chinese enterprises have bigger business scenarios, larger service scale, and more people formally assigned by companies to open source maintenance. When these conditions stack together, open source moves from an event culture into industry-level engineering investment.

Taiwanese communities are very good at organizing events and helping students and engineers encounter technology for the first time. But if we want more people to enter large open source projects such as [Apache](https://github.com/apache/), [CNCF](https://www.cncf.io/), and the [Linux Foundation](https://www.linuxfoundation.org/), the things I think about are:

- Connect "listening to talks" to "actually sending PRs".
- Connect "individual learning" to "companies being willing to invest engineering time".
- Connect "one-off events" to "weekly review, mentoring, and issue triage".
- Connect "Taiwanese engineers are strong" to "being visible in international projects".

What I saw at Apache CommunityOverCode Asia was not that Taiwan lacks something. It was that when enterprises, communities, students, and open source foundations are truly connected, they can create a tremendous amount of momentum. This is also what [OpenSource4You](https://github.com/opensource4you/readme) is currently pushing forward. Thanks again, ChiaPing.

## TAC Friends

Although I did not receive a TAC (Travel Assistance Committee) grant for Apache CoC Asia this time, I still stayed around the Apache booth and helped hand out stickers.

I was also very happy to meet and talk with TAC friends such as Owen, Peter, Ryan, Simon, and Nick at the venue. In many cases, the most valuable part of attending an international conference is not listening to talks in one direction. It is exchanging views with engineers from different places between sessions, over meals, and at gatherings after the event about open source, careers, project maintenance, and company culture.

Congratulations as well to Simon and Nick, whose careers have both been going very smoothly recently.

{{< gallery >}}
  <img src="/open-source-contribution/apache-coc-asia/coc-asia-tac.jpeg" alt="Apache CommunityOverCode Asia TAC friends group photo" class="grid-w100 md:grid-w50" />
  <img src="/open-source-contribution/apache-coc-asia/coc-asia-group-photo.jpeg" alt="Apache CommunityOverCode Asia group photo" class="grid-w100 md:grid-w50" />
{{< /gallery >}}

## OpenSource4You Apache Kafka and Apache Gravitino Gathering

ChiaPing also invited people who were in Beijing and active in the OpenSource4You [#apache-kafka](https://opensource4you.slack.com/archives/C06MSQ9V4F3) and [#apache-gravitino](https://opensource4you.slack.com/archives/C07473LAC15) channels to have dinner together. We talked a lot about Apache projects, communities, and companies. It was also an interesting experience to see an online meetup become a real in-person gathering, especially when these were people whose technical insights and project updates I usually only saw online.

![OpenSource4You and Apache Gravitino friends gathering](/open-source-contribution/apache-coc-asia/apache-gravitino-gathering.jpeg)

## The Conference Buffet

The buffet provided at the venue was much richer than I expected. The food was good, with flavors I rarely get to try, but it was still not too unfamiliar to enjoy.

{{< gallery >}}
  <img src="/open-source-contribution/apache-coc-asia/conference-buffet-cold-dishes.jpeg" alt="Conference buffet cold dishes" class="grid-w100 md:grid-w33" />
  <img src="/open-source-contribution/apache-coc-asia/braised-yellow-croaker-buffet.jpeg" alt="Conference buffet yellow croaker dish" class="grid-w100 md:grid-w33" />
  <img src="/open-source-contribution/apache-coc-asia/conference-buffet-plate.jpeg" alt="Conference buffet plate" class="grid-w100 md:grid-w33" />
{{< /gallery >}}

## Walking Around Beijing and Food

Outside the conference, I also took the chance to walk around Beijing. I went to the Old Summer Palace, Peking University, and the Qianmen area. As a reminder to friends who might go next time: apply for each attraction visit one month in advance, or you may end up like us, only able to stare at Peking University from outside the gate.

{{< gallery >}}
  <img src="/open-source-contribution/apache-coc-asia/old-summer-palace.jpeg" alt="Old Summer Palace" class="grid-w100 md:grid-w33" />
  <img src="/open-source-contribution/apache-coc-asia/peking-university.jpeg" alt="Peking University" class="grid-w100 md:grid-w33" />
  <img src="/open-source-contribution/apache-coc-asia/xibei-restaurant-group-selfie.jpeg" alt="Group selfie at Xibei restaurant" class="grid-w100 md:grid-w33" />
  <img src="/open-source-contribution/apache-coc-asia/qianmen-history-map.jpeg" alt="Qianmen historical map" class="grid-w100 md:grid-w33" />
  <img src="/open-source-contribution/apache-coc-asia/qianmen-starbucks-reserve.jpeg" alt="Qianmen Starbucks Reserve" class="grid-w100 md:grid-w33" />
  <img src="/open-source-contribution/apache-coc-asia/zhengyangmen-gate.jpeg" alt="Zhengyangmen Gate" class="grid-w100 md:grid-w33" />
{{< /gallery >}}

We also ate quite a lot on our own during this trip, including spicy fish, lamb skewers, yogurt, and finally roast duck at Quanjude. But I forgot to try douzhi.

{{< gallery >}}
  <img src="/open-source-contribution/apache-coc-asia/spicy-fish.jpeg" alt="Spicy fish" class="grid-w100 md:grid-w33 xl:grid-w25" />
  <img src="/open-source-contribution/apache-coc-asia/spicy-fish-hotpot.jpeg" alt="Spicy fish hotpot" class="grid-w100 md:grid-w33 xl:grid-w25" />
  <img src="/open-source-contribution/apache-coc-asia/spicy-intestine-hotpot.jpeg" alt="Spicy intestine hotpot" class="grid-w100 md:grid-w33 xl:grid-w25" />
  <img src="/open-source-contribution/apache-coc-asia/lamb-skewers-and-noodle-soup.jpeg" alt="Lamb skewers and noodle soup" class="grid-w100 md:grid-w33 xl:grid-w25" />
  <img src="/open-source-contribution/apache-coc-asia/bubble-milk-tea.jpeg" alt="Bubble milk tea" class="grid-w100 md:grid-w33 xl:grid-w25" />
  <img src="/open-source-contribution/apache-coc-asia/beijing-pastry-gift-box.jpeg" alt="Beijing pastry gift box" class="grid-w100 md:grid-w33 xl:grid-w25" />
  <img src="/open-source-contribution/apache-coc-asia/beijing-yogurt-cups.jpeg" alt="Beijing yogurt" class="grid-w100 md:grid-w33 xl:grid-w25" />
  <img src="/open-source-contribution/apache-coc-asia/souvenir-cake.jpeg" alt="Souvenir pastry" class="grid-w100 md:grid-w33 xl:grid-w25" />
  <img src="/open-source-contribution/apache-coc-asia/beijing-meat-pie.jpeg" alt="Beijing meat pie" class="grid-w100 md:grid-w33 xl:grid-w25" />
  <img src="/open-source-contribution/apache-coc-asia/quanjude-roast-duck-platter.jpeg" alt="Quanjude roast duck platter" class="grid-w100 md:grid-w33 xl:grid-w25" />
  <img src="/open-source-contribution/apache-coc-asia/quanjude-roast-duck-restaurant.jpeg" alt="Quanjude roast duck restaurant" class="grid-w100 md:grid-w33 xl:grid-w25" />
  <img src="/open-source-contribution/apache-coc-asia/peking-duck-pancake-bites.jpeg" alt="Peking duck pancake bites" class="grid-w100 md:grid-w33 xl:grid-w25" />
{{< /gallery >}}

## Special Thanks

**Finally, I especially want to thank [ChiaPing](https://github.com/chia7712). Last year, when I was still a student, I did not receive travel support for Apache CommunityOverCode Asia. Without ChiaPing's help, I probably would not have had the chance to go to the venue with my friends from NCKU, Owen and Peter, and broaden my perspective.**

For me at the time, actually walking into the Apache annual conference in Asia and talking with local companies at their booths was an extremely rare experience.
Almost no one there knew about [Airflow](https://airflow.apache.org/docs/), so I leaned into being the extrovert going from booth to booth introducing what Airflow is, while also using the chance to understand what problems each project solved and where each one sat in the overall data infrastructure hierarchy.

## Questions I Took Away

After this conference, I think the questions most worth continuing to think about are:

1. When we talk about open source, do we also care about open governance?
2. Can Taiwan grow a more regionally distinctive open source data stack, instead of always only being a user of foreign tools?
3. Are Taiwanese companies willing to treat open source contributions as part of engineering capability and technical branding, instead of only treating them as employees' after-work interests?
4. Can we build a long-term mentoring mechanism more like [GSoC](https://summerofcode.withgoogle.com/) or Open Source Promotion Plan, so students can truly enter large projects?

Originally, I only wanted to attend Apache-related technical talks. But what I saw from CoC Asia was that open source is not only code, and it is not only foundation governance. It is also company strategy, talent training, business models, regional industrial structure, and engineering culture.

For me, this is also a major motivation to keep contributing to [Apache Airflow](https://airflow.apache.org/docs/). As data pipelines become increasingly real-time, increasingly complex, and increasingly dependent on AI collaboration and self-healing, an open governance workflow orchestration system like Airflow still has a lot of room to move forward.
