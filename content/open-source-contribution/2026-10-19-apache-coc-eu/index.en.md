---
title: "Apache CommunityOverCode Europe 2026 Recap: Airflow Contributor Day, Multi-Language SDKs, and Lakehouse Trends"
summary: "Notes from CommunityOverCode EU 2026 in Glasgow: the first-ever Airflow Contributor Day, our talk on Airflow's non-Python SDKs, and Lakehouse Day takeaways on agents, access control, semantic catalogs, and REST catalogs."
description: "A recap of Apache CommunityOverCode Europe 2026 (Glasgow): Community over Code in practice at Airflow Contributor Day, the Airflow Beyond Python talk, what I saw at Lakehouse Day, and real-world data infra talks from OpenAI, LinkedIn, Apple, and more."
date: 2026-10-24T18:52:39+08:00
slug: "apache-coc-eu"
tags: ["blog","en","open-source-contribution","data-engineering","airflow","lakehouse","apache-iceberg","conference"]
# series: ["Documentation"]
# series_order: 9
cascade:
  showEdit: true
  showSummary: true
  hideFeatureImage: false
draft: false
---

## Introduction

> ![featured](featured.jpg)
> The crew who set out together from Taiwan, left to right: [KuanHao](https://github.com/rich7420), me, [Peter](https://github.com/peterxcli), [GuanMing](https://github.com/guan404ming)  
> [Wei Lee](https://github.com/Lee-W) on the far right flew in from Japan 😆

The Lakehouse sessions this year spent a lot of time on the role agents play in data infrastructure, and how agents change the way we build it.
As always, scaling came up too.

This year also featured the very first Airflow Contributor Day.
Many Airflow PMC members, committers, contributors, and users got together to discuss the future of Airflow.


## Airflow Contributor Day: Community over Code, for Real

Unfortunately, one of Airflow's PMC members, [Jens](https://github.com/jscheffl), ran into some health issues a while ago,
so they couldn't join Airflow Summit or CommunityOverCode this year.
The good news is that Jens is doing much better now!

> ![airflow-contributor-day-group-photo](airflow-contributor-day-group-photo.jpeg)
> [One picture worth more than 1000 words: this is the summary of the Airflow Contributor Day](https://lists.apache.org/thread.html/5b0ok7fr6tc6lzslvcgx4nhbxkfcwq22)

[Jarek](https://github.com/potiuk), one of our senior members, brought a cardboard cutout of Jens to the venue, and it arrived even before most of us had left for the conference.
About a month before CoC, Jarek invited everyone to fly to Germany together after the conference to visit Jens.
Nobody else could adjust their schedule, so we sent along some small gifts and cards
for Jarek to hand over to Jens, and to bring Jens's latest news back to the rest of us!

This is what "Community over Code" really looks like.
We first came together for the sake of the project and its technology,
but over the long run, we've become friends.

On a lighter note: at last year's Airflow Summit, I went cycling in Seattle with Jens and the group.
It turned out to be all uphill, and I couldn't keep up with everyone.
I hope Jens recovers soon,
and that we get another chance to ride together (but let's skip the uphill roads next time!).


## Beyond Python: New Languages for Airflow

I gave this talk together with [Wei Lee](https://github.com/Lee-W).

![talk-airflow-beyond-python](talk-airflow-beyond-python.jpg)

Our angle was "language": Airflow is, in a sense, a language for describing workflows.
For more than ten years, though, that language could only be written in Python. This year, you can write it in Go, TypeScript, and Java as well.
And if we can use other programming languages, can we write it in natural language too?

For my part, I ran a live demo of a retail company where three engineering teams each use a different language.
In a single Airflow environment, they build one cross-team workflow, while each team keeps its own ownership and tech stack.
I then walked through how we run multi-language workflows while keeping Airflow's core control plane intact,
rather than reimplementing the core in every language.

![airflow-contributor-day-dag-level-queue-demo](airflow-contributor-day-dag-level-queue-demo.jpeg)

[Wei Lee](https://github.com/Lee-W) then covered interacting with Airflow in natural language and the [Common AI Provider](https://airflow.apache.org/blog/common-ai-provider-1.0/), which lets Airflow power AI-native workflows.

![wei-lee-common-ai](wei-lee-common-ai.jpg)

Slides: [Airflow-Beyond-Python-New-Languages-for-Tasks-and-Workflows](https://www.zhu424.dev/slides/2026-10-11-Airflow-Beyond-Python-New-Languages-for-Tasks-and-Workflows.pdf)

This session was only confirmed about a month before the conference. Someone in the Airflow track had cancelled at the last minute,
and the architecture for the non-Python SDKs had taken concrete shape by then.
Jarek helped us get onto the Airflow track's schedule.
Thanks again, [Jarek](https://github.com/potiuk), for giving us the chance to share this at CoC EU!


## What I Saw at Lakehouse Day: The Lakehouse in the Age of Agents

### Agents Demand Finer-Grained Access Control

The round table's central question was what the Lakehouse stack has to change once agents become users of the data. The speakers raised a few observations:
- **The impact of agent workloads**: it used to be only humans reading and writing tables. Now agents interact with tables freely, so the security bar is higher and access control needs to be more granular.
- **The return of on-prem**: on-prem is also viewed as a security measure. The Lakehouse stack can't consider only the cloud. It has to work on-premises too.
- **New file formats**: at the file-format and in-memory-format level, options beyond Parquet are emerging for different use cases (e.g., Lance). The community will need to converge on a standard to avoid fragmenting the ecosystem.

![lakehouse-day-round-table-wide](lakehouse-day-round-table-wide.jpeg)

### Influence Through Open Source: Tying a Project to Your Business

This was a Lakehouse Day talk by Sean and his Apple colleagues on Apple's Lakehouse adoption:
- A series of migrations and architectural trade-offs on the way from HDFS to a Lakehouse
- They rely mainly on [Apache DataFusion Comet](https://github.com/apache/datafusion-comet). When an organization has enough influence in a project, it can shape the project's features and release cadence, aligning the project's roadmap with internal goals.
- Comet's operator coverage needs to be as high as possible to avoid falling back to JVM-based execution or doing redundant data movement.

![lakehouse-day-apple-iceberg-at-scale-talk](lakehouse-day-apple-iceberg-at-scale-talk.jpeg)

### Lakehouse Stack Unification and Semantic Catalogs

- Table formats and compute engines have diverged, and integrating them is a shared challenge.
- When an agent accesses tables, it needs a unified standard: is my "revenue" the same thing as your "revenue"? Just as UTC gives everyone a common time reference, everyone needs to follow the same definition.
- [Apache Ossie](https://github.com/apache/ossie) targets exactly this problem by proposing an open standard for business semantics. Data infra vendors and catalog services are investing in it, and Apache Polaris has already integrated it.

### How REST Catalogs Affect Lakehouse Performance

Centralizing metadata lookups in a REST catalog such as Apache Polaris can significantly improve the Lakehouse's overall throughput.
Without one, the engine has to resolve metadata itself, which is very expensive.

## Talks That Stuck With Me

### Re-Architecting Airflow at OpenAI

![airflow-contributor-day-openai-rhino-talk](airflow-contributor-day-openai-rhino-talk.jpeg)

OpenAI's data infra team shared how they optimized Airflow 2 to handle the scaling demands of a new line of business.
Their cluster was already near its limit, and within six weeks they had to launch a much larger workload that it clearly couldn't handle.

They named their rewritten core the Rhino API, mainly to solve these two Airflow 2 problems:
- The scheduler isn't horizontally scalable.
- Every task runner pod connects directly to the DB; Rhino API removes that direct access.

Interestingly, to solve the scheduler bottleneck, their new architecture uses a single scheduler rather than replicas, and pre-fetches the task instances to run asynchronously without blocking.
Attendees did raise concerns about future scalability, but they said that after the new workload launched, their current capacity is enough for what's coming.

From the Airflow maintainers' perspective, though, Airflow 3 already addresses many of the problems they were solving.
If a user hits similar problems on Airflow 2 and has time to migrate,
we'd recommend upgrading straight to Airflow 3 rather than making these changes on Airflow 2,
so that the upgrade doesn't get harder later.

### Zero Downtime Kubernetes Cluster Migration for Airflow at LinkedIn

LinkedIn has long operated one of the largest Airflow clusters in the world.
[Stefan](https://github.com/1fanwang) from LinkedIn's data infra team shared how they do zero-downtime Kubernetes cluster migration on Airflow 2.
This was purely a Kubernetes cluster version upgrade, not an Airflow upgrade.

![airflow-contributor-day-linkedin-airflow-talk.jpeg](airflow-contributor-day-linkedin-airflow-talk.jpeg)

Their definition of zero downtime is strict: not even a single running task instance is interrupted, and nothing needs to be retried.
The core idea is to have the two Airflow clusters, one on the old Kubernetes cluster and one on the new, share the same metadata DB. When they switch over, the next task instance starts on the new cluster instead of the old one, and even in-progress DagRuns are unaffected.

Next, they plan to explore zero-downtime Airflow version upgrades, which will be a very interesting and challenging problem,
since it involves DB schema migrations and Airflow core code changes.

### Optimizing Lakehouse at OpenAI

I came into this one late and missed the opening context, but it covered how OpenAI optimizes its Lakehouse internally.
They've built in-house optimizations for both Delta and Iceberg tables, mainly targeting the small-files problem.

Under tight business deadlines, they can't wait for the community's next patch or minor release,
so they fork and build their own in-house solutions. To some extent this echoes what I wrote after [Apache CommunityOverCode Asia 2025](https://blog.zhu424.dev/open-source-contribution/apache-coc-asia/).
In the long run, though, it means the organization can't easily track upstream releases,
and may even accumulate technical debt.

### Apache Mahout

Last but not least, [GuanMing](https://github.com/guan404ming) and [KuanHao](https://github.com/rich7420), who traveled with us, presented Apache Mahout's QDP (Quantum Data Plane) feature and its roadmap.
It's probably unprecedented to present something as esoteric as quantum ML at a CoC venue.

> ![coc-qdp-gate-simulation-vs-fused-kernel-talk](coc-qdp-gate-simulation-vs-fused-kernel-talk.jpeg)
> [GuanMing](https://github.com/guan404ming)

> ![coc-qdp-architecture-engine-talk](coc-qdp-architecture-engine-talk.jpeg)
> [KuanHao](https://github.com/rich7420)

## New Friends, Food, and Sights Along the Way

### ASF Pokémon

On the first day of the conference, there happened to be a [Pokémon event](https://www.facebook.com/TheVideoGameMarket/posts/glasgow-gaming-market-starts-at-1100am-tomorrow-at-the-glasgow-club-bellahouston/1443770044600684/) nearby,
so the CoC organizers came up with an ASF edition of Pokémon called "Inframon".

{{< gallery >}}
  <img src="coc-inframon-cards-and-stickers.jpeg" alt="ASF-edition Pokémon (Inframon) cards and stickers" class="grid-w50" />
  <img src="coc-inframon-cards-and-stickers-face.jpeg" alt="ASF-edition Pokémon (Inframon) card faces" class="grid-w50" />
{{< /gallery >}}

Maybe [Apache Taipei](https://github.com/opensource4you/) can do something like this at our next event!

### Your ICLA Protects You

We happened to chat with Craig, the secretary who handles the ICLAs you sign when becoming a committer, and picked up some fun facts:
- About one-third of ICLAs get rejected, because people enter their GitHub ID where a legal name is expected, but a GitHub ID doesn't identify a real person.
- If a company wants to sue you over code you wrote for an Apache project, the ICLA protects you. The company can only sue the ASF.

### The Apache Taipei Crew

![team-dinner-steakhouse](team-dinner-steakhouse.jpeg)

Thanks to [Chia-Ping](https://github.com/chia7712), who, despite being busy with work in Taiwan, treated the Apache Taipei folks to a big group dinner.
Thanks also to Sean for introducing us to many of the data infra folks at Apple, giving us the chance to talk with more Lakehouse experts.

### Conference Food and Scottish Food

![conference-lunch-scottish-beef-pie](conference-lunch-scottish-beef-pie.jpeg)

The buffet lunches at the venue were pretty good.
What made this year special was that the gala dinner was held at a science museum.

{{< gallery >}}
  <img src="glasgow-science-centre-entrance.jpeg" alt="Glasgow Science Centre entrance" class="grid-w50" />
  <img src="glasgow-science-centre-interior.jpeg" alt="Inside the Glasgow Science Centre" class="grid-w50" />
{{< /gallery >}}

Everything we ate in Scotland was pretty tasty.

{{< gallery >}}
  <img src="pub-steak-and-fries.jpeg" alt="Steak and fries" class="grid-w100 md:grid-w33" />
  <img src="steakhouse-t-bone-steak.jpeg" alt="T-bone steak at a steakhouse" class="grid-w100 md:grid-w33" />
  <img src="hotel-breakfast.jpeg" alt="Hotel breakfast" class="grid-w100 md:grid-w33" />
{{< /gallery >}}

### Sights Along the Way

{{< gallery >}}
  <img src="airport-mirror-selfie.jpeg" alt="Group photo in the airport glass reflection" class="grid-w100 md:grid-w33 xl:grid-w25" />
  <img src="flight-seat-entertainment-system.jpeg" alt="In-flight entertainment system" class="grid-w100 md:grid-w33 xl:grid-w25" />
  <img src="glasgow-airport-wall-mural-group-photo.jpeg" alt="Group photo in front of the Glasgow Airport mural" class="grid-w100 md:grid-w33 xl:grid-w25" />
  <img src="supermarket-security-monitor.jpeg" alt="Supermarket security monitor" class="grid-w100 md:grid-w33 xl:grid-w25" />
  <img src="glasgow-church-tower.jpeg" alt="Church tower in Glasgow" class="grid-w100 md:grid-w33 xl:grid-w25" />
  <img src="glasgow-red-sandstone-building.jpeg" alt="Red sandstone building in Glasgow" class="grid-w100 md:grid-w33 xl:grid-w25" />
  <img src="edinburgh-scott-monument.jpeg" alt="Scott Monument in Edinburgh" class="grid-w100 md:grid-w33 xl:grid-w25" />
  <img src="lakehouse-day-conference-hall.jpeg" alt="Lakehouse Day venue" class="grid-w100 md:grid-w33 xl:grid-w25" />
  <img src="lakehouse-day-collaboration-is-the-architecture-slide.jpeg" alt="Collaboration is the architecture slide at Lakehouse Day" class="grid-w100 md:grid-w33 xl:grid-w25" />
  <img src="lakehouse-day-round-table-panelists.jpeg" alt="Lakehouse round table panelists" class="grid-w100 md:grid-w33 xl:grid-w25" />
  <img src="airflow-contributor-day-opening-and-cardboard-cutout.jpeg" alt="Airflow Contributor Day opening and the cardboard cutout" class="grid-w100 md:grid-w33 xl:grid-w25" />
  <img src="airflow-contributor-day-our-talk-airflow-beyond-python.jpeg" alt="Title slide of the Airflow Beyond Python talk" class="grid-w100 md:grid-w33 xl:grid-w25" />
  <img src="airflow-contributor-day-durable-execution-talk.jpeg" alt="The evolution of durable execution in Airflow talk" class="grid-w100 md:grid-w33 xl:grid-w25" />
{{< /gallery >}}


## Reflections

**The Value of Showing Up Consistently**

This year I ran into several people I'd met at CoC NA last year. Many big tech data infra teams attend year after year.
You can see how their focus areas change, where they're heading next, and how they solve their problems, which closes the information gap.
Showing up in person is how I learn which projects are worth watching and where they're actively heading.

As for the Airflow project itself, I'm very glad to have been part of CoC EU,
especially with a full day of Airflow's own track, and to have witnessed an important moment for the community.

**A Lot Gets Hashed Out at the Venue**

Beyond the heartwarming moments in the Airflow community, we also talked a lot about Airflow's future,
and about [some topics worth following up on](https://cwiki.apache.org/confluence/spaces/AIRFLOW/pages/311626658/Airflow+3+Workstreams), such as [Improve Airflow's debugging story](https://github.com/apache/airflow/issues/40975), Airflow Standalone Improvements, and Workflow-in-Workflow.

I also talked with [Peter](https://github.com/peterxcli), an Apache Ozone PMC member who came along, about how Ozone first runs the CI runner on the contributor's fork before running the actual tests on the main repo, which helps ensure code quality and security. We also discussed how each repo should have its own workflow for automated AI review, similar to GitHub Copilot or CodeRabbit, so we control the harness configuration ourselves and avoid vendor lock-in.


## Special Thanks

**Finally, special thanks to [Chia-Ping](https://github.com/chia7712). I'm still early in my career, and I didn't get a travel grant for Apache CommunityOverCode EU this year.**
**Without Chia-Ping's help, I wouldn't have been part of this Contributor Day, which meant so much to the Airflow community, and I wouldn't have had the chance to present Airflow's new-languages talk at CoC EU.**
