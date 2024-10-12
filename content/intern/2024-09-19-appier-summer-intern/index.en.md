---
title: "2024 Appier Summer Internship Reflection"
summary: "Reflection on my backend summer internship in the Data Platform department at Appier"
description: "Reflection on my backend summer internship in the Data Platform department at Appier"
date: 2024-10-01T21:21:01+08:00
slug: "appier-summer-intern"
tags: ["blog","en","intern"]
# series: ["Documentation"]
# series_order: 9
cascade:
  showEdit: true
  showSummary: true
  hideFeatureImage: false
draft: false
---

## Interview

For details about the Appier interview process, please refer to:

{{< article link="/en/intern/summer-intern-interview-2024-appier/" >}}

In summary, after learning about the intern team, I can only say that getting the opportunity for a summer internship at Appier as a rising junior was really fortunate!

## About the Summer Internship Program

Why do I call it a "program"? 

On my first day of the internship, there happened to be a training session gathering all summer interns. All subsequent activities related to the summer internship were referred to as the "Summer Internship Program." This year marked the 3rd year of Appier's summer internship program.

The summer internship program mainly consisted of three parts:
1. Training (Orientation Training)
2. The project itself
3. Project sharing

## Orientation Training

Though it's called training, it was actually a very relaxed event and happened to take place on my first day.

{{< figure
    src="orientation-snack.jpeg"
    alt="Orientation Snack"
    caption="There were also cakes from [KOBE SWEETS 神戸果実](https://g.co/kgs/Sh6Yr8S) and drinks from **再睡五分钟** on that day."
>}}

The session mainly introduced the key activities of the summer internship program, the application status over the years (apparently, there were over 600 applications this year), company culture, self-introductions from the interns, and time for open networking.

### Composition of the Intern Team

There were about 15 summer interns that day. After hearing everyone's self-introductions, a rough estimate showed that around 10 of them were either NTU students, planning to study abroad, or studying overseas and had returned to Taiwan. There was even a high school graduate heading to MIT [@jieruei](https://github.com/knosmos) Orz.

A funny thing that day was that almost everyone knew someone else in the internship program. For example, I was high school classmates with [@m4xshen](https://github.com/m4xshen), and I knew [@vax-r](https://github.com/vax-r) from NCKU's GDSC. Many others mentioned that they also knew another intern from before, often from previous AppWorks Camp interactions. It made the odds of getting picked (15 out of over 600) seem a bit less daunting XD.

## Onboarding

I actually started my internship in the second week of July.
> Around May or June, HR contacted me to see if I could start a week later than planned. The original start date was in the first week of July. This was mainly because too many people were onboarding that first week, and they wanted to spread it out. Since I had a relatively flexible summer internship timeline (ending in the first week of September), they suggested I start later. Many other interns had to wrap up by mid-August.

During my first week, I spent most of the time waiting for access to the relevant permissions. I spent time reading internal documents related to Data Engineering, attending team meetings, and reviewing the existing codebase.

## The Project

Each intern worked on different projects in various departments, depending on the needs of their department at the time.

I was a Backend Intern in the Data Platform department. My project could be understood as an "**Operation Dashboard**." This dashboard wasn't like Grafana or Kibana monitoring dashboards.

It was a Web Dashboard provided by the Data Platform department for use by upstream and downstream departments, integrating with Appier's OAuth Authentication and internal Authorization. The dashboard allowed authorized departments to:
- **Modify Configurations related to the Data Platform**: e.g., adjust the number of workers for a particular dev role in the XX Team.
- **View the Status of the Data Platform**: Check current datasets and provide relevant filters.
- **Automate Operation Tasks**: Actions that previously required opening a ticket with the Data Team could now be done directly through the dashboard.
- **Keep Records of the Above Operations with Audit Logs**: For accountability and tracking purposes.

### Solved Problems

The main scenarios addressed are as follows:

**XX Team's on-call needs to urgently increase the number of Workers**
- Previously, this required contacting the Data Team to change the configuration.
  - If no one in the Data Team noticed, it could result in a service interruption for XX Team.
- Now, changes can be made directly on the Dashboard without needing the Data Team to adjust the configuration.
  - XX Team's on-call can operate directly, with Audit Log records.

**XX Team submits an Operation Task**
- Previously, a ticket had to be submitted to the Data Team for handling.
  - Generally, such tasks could be resolved by running a short script.
  - However, the Data Team might be occupied with more urgent tasks or in meetings.
- Now, tasks can be managed directly on the Dashboard without needing the Data Team.
  - This saves time for both parties.

## Technical Aspects

### System Architecture

The Operation Dashboard is developed using [Streamlit](https://streamlit.io/) as both front-end and back-end. <br>
It uses Postgres to record User Authorization. <br>
There is an additional Cronjob to regularly sync Appier's Authorization relations into Postgres. <br>

Additionally, as mentioned earlier, the Dashboard needs to call the Kubernetes API to adjust configurations or call internal Data Platform APIs to display status. <br>

### Framework Selection

There were other teams that previously developed similar dashboards using [Streamlit](https://streamlit.io/). <br>

Streamlit is a framework for developing web apps in Python, primarily used for presenting data visualizations or results of machine learning models (it provides extensive support for Pandas, Matplotlib, Plotly). <br>

It allows development using only Python without the need for additional front-end expertise, which was suitable since the Data Platform department lacks front-end resources. <br> Therefore, Streamlit was chosen for development. <br>

### Streamlit Router Framework

Since the Dashboard is primarily used as a front-end, the native [multi-page: `st.navigation`](https://docs.streamlit.io/develop/api-reference/navigation/st.navigation) provided by Streamlit requires each page to be written in a single Python file. <br> This makes code tracing in an IDE inconvenient (you can't directly jump to a definition block using `shift` + `click`). <br>

So, I developed a **decorator-based** framework based on [st.navigation](https://docs.streamlit.io/develop/api-reference/navigation/st.navigation). <br> This allows different pages to be written in the same Python file and provides a `Router` for registering different pages, making code tracing easier. <br> Those familiar with FastAPI or Flask might find this approach more intuitive. <br>

```python
import streamlit as st
from framework import Router

router = Router(prefix="/dashboard")

@router.page("/config")
def config_page():
    st.write("Config Page")

@router.page("/status")
def status_page():
    st.write("Status Page")
```
> This is a sample usage of the framework.

### Authentication

Authentication determines whether a user is logged in. <br>

Since the Dashboard is intended for use by upstream and downstream departments, it needs to integrate Appier's OAuth Authentication and internal Authorization. <br>

Authentication is implemented using Google OAuth. <br> However, due to limitations in Streamlit's framework, only internal sessions can be used to track login status, rather than using JWT + HTTP Only cookies. <br>

### Authorization

Authorization determines whether a user has the right to perform a certain action. <br>

Starting from scratch to maintain an authorization system for all Data Platform-related departments would:
1. Increase maintenance overhead for the Data Platform Team.
2. Potentially cause discrepancies with Appier's existing Groups-Users relations.

To simplify the process, the Data Platform Team only needs to maintain the mapping between Groups-Users and Actions. <br> Therefore, a **Cronjob** periodically syncs Appier's Groups-Users relations into Postgres. <br> The Dashboard checks this Postgres database to determine authorization. <br>

{{< mermaid >}}
erDiagram
  Group {
    int group_id PK
    string group_name
  }

  User {
    int user_id PK
    string user_name
  }

  Action {
    string action_name PK
  }

  Group }o--|| Action : "can do"
  User }o--|| Action : "can do"
  Group }o--|| User : "has"
{{< /mermaid >}}
> The ER Diagram of the Authorization in Postgres would look like this. <br>

## Project Presentation

The most important part of the Summer Internship Program is a **30-minute English project presentation**. <br>
(However, you can use Google Slides to supplement your speech) <br>
This is followed by a 5-minute Q&A session, also conducted entirely in English. <br>

Each summer intern shares their project in the last week of their internship, with almost all presentations being conducted in pairs. <br> All Appier employees are welcome to attend these presentations. <br> They take place in a physical conference room, allowing interested parties to join either in person or virtually. <br> This is a great opportunity to learn about the services maintained by other departments. <br>

## Team and Mentorship

The Data Platform Team consists of fewer than 10 people. <br>
Since it isn't a Product Team, there are no frontend specialists, only Backend and Data Engineers. <br>

I had two mentors: <br>
One primarily mentored me on the summer internship project. <br>
The other mainly mentored me on the API refactoring project. <br>
(This is mentioned later in the [#About Long-term Internship](#about-long-term-internship)) <br>

Everyone was very friendly! <br>
They were always willing to share knowledge about Data Engineering, system architecture, and their experiences. <br>

## Work Environment & Food

**Office** <br>
The office is located near Xiangshan Station in the Xinyi District, Taipei. <br>
You can clearly see Taipei 101. <br>
Some floors even have spiral staircases for moving between floors. <br>

{{< gallery >}}
  <img src="/intern/appier-summer-intern/office-1.jpeg" class="grid-w100 md:grid-w100" />
  <img src="/intern/appier-summer-intern/office-2.jpeg" class="grid-w100 md:grid-w50" />
  <img src="/intern/appier-summer-intern/office-3.jpeg" class="grid-w100 md:grid-w50" />
{{< /gallery >}}

**Lunch** <br>
Since the office is in Xinyi District, a lunch costing under 200 TWD is considered a steal. ~ <br>
Most of the time, when dining with the team, we would go to department stores. <br>
Sometimes, we’d head towards City Hall for some local street food. <br>

{{< gallery >}}
  <img src="/intern/appier-summer-intern/team-meal-chun-shui-tang.jpeg" class="grid-w100 md:grid-w50" />
  <img src="/intern/appier-summer-intern/team-meal-dumpling.jpeg" class="grid-w100 md:grid-w50" />
  <img src="/intern/appier-summer-intern/team-meal-first-day.jpeg" class="grid-w100 md:grid-w50" />
  <img src="/intern/appier-summer-intern/team-meal-kafka.jpeg" class="grid-w100 md:grid-w50" />
{{< /gallery >}}
(Figure 4: Team building hotpot session—drawing Kafka's architecture while eating makes sense too ouo) 

The office has a shelf full of drinks and some snacks, mostly small pouches. <br>
I would grab a soy milk almost every day XD <br>
Occasionally, there were fruits available (I’ve had bananas, blueberries, and peaches). <br>
I often paired my healthy lunch boxes bought nearby with the office drinks and fruits. ~ <br>

{{< gallery >}}
  <img src="/intern/appier-summer-intern/meal-box-1.jpeg" class="grid-w100 md:grid-w50" />
  <img src="/intern/appier-summer-intern/meal-box-2.jpeg" class="grid-w100 md:grid-w50" />
  <img src="/intern/appier-summer-intern/meal-box-3.jpeg" class="grid-w100 md:grid-w50" />
{{< /gallery >}}

**Happy Hour** <br>
Every Friday afternoon, there’s a Happy Hour where you can order afternoon tea! <br>
It could be drinks or snacks; it varies each time. <br>
(One time it was waffles from Xiaomu, but I missed out since it was during a Team Building session. So unfortunate QQ)

{{< gallery >}}
  <img src="/intern/appier-summer-intern/happy-hour-3.jpeg" class="grid-w100 md:grid-w33" />
  <img src="/intern/appier-summer-intern/happy-hour-1.jpeg" class="grid-w100 md:grid-w33" />
  <img src="/intern/appier-summer-intern/happy-hour-2.jpeg" class="grid-w100 md:grid-w33" />
{{< /gallery >}}

**Clubs** <br>
One day, a club shared how to make cocktails during lunch. <br>
That day, we ordered a bunch of pizzas and Korean fried chicken! <br>

{{< gallery >}}
  <img src="/intern/appier-summer-intern/club-fried-checken.jpeg" class="grid-w100 md:grid-w50" />
  <img src="/intern/appier-summer-intern/club-pizza.jpeg" class="grid-w100 md:grid-w50" />
{{< /gallery >}}

## Company Culture

Every company has its own values. <br>
Appier's core values are: <br>
- open-mindedness
- direct communications
- ambition

I also discussed different company cultures with my mentors during conversations. <br>
This open-mindedness was evident during Design Review or Code Review sessions. <br>
Mentors or supervisors would set a broad direction, leaving the technical details up to me to design and discuss with the team. <br>
Team members would also provide feedback during reviews. <br>

## Technical Aspects

### Data Engineering

This time, I mainly encountered new technologies related to Data Engineering. <br>
There's so much to share. <br>
I’ve written an additional post to introduce it. <br>

{{< article link="/backend/first-thought-of-data-engineering/" >}}

### Infra and Dev

At Appier, <br>
managing the Helm Chart or Grafana Dashboard for the department's own applications, <br>
or the Infra used by applications like Postgres, Redis, Kafka, etc., <br>
falls within the scope of Backend. <br>
There is no dedicated Infra team to help maintain these. <br>

Infra is provided as a SaaS, such as: <br>
ArgoCD with many convenient plugins, <br>
managing or upgrading multiple Kubernetes clusters, <br>
or EFK integrated with k8s for log tracing. <br>
(There are many other services, but these are the ones I've interacted with so far.) <br>

Compared to previous internships or part-time jobs, <br>
this difference is mainly because Appier has more departments. <br>
In previous companies, each product was essentially its own department, <br>
and deployment or storage-related maintenance had dedicated Infra teams. <br>

At Appier, the responsibilities of Backend are broader. <br>
It requires a deeper understanding of the Infra used by our own applications <br>
to handle production issues and find root causes. <br>

### Implementing Infra as Code

Appier has many departments, <br>
with dozens of Kubernetes clusters or Cloud SQL instances, <br>
along with VPCs, IAM, Secrets, and so on. <br>
At this scale, manual maintenance is no longer feasible. <br>

Here, I truly experienced the benefits of Infra as Code. <br>
It allows the modularization of repetitive resources, <br>
and the Terraform in the repo should be consistent with the actual state of the instances. <br>

When Cloud Infra reaches a certain scale, <br>
IaC becomes a necessity. <br>

### Role of Senior Engineers

- Review Code
- Cost Reduction
- Root Cause Analysis
- Sprint Planning
- Performance Tuning

These are areas that I found are not easy to engage with regularly, <br>
and where the difference between myself and a Senior becomes apparent. <br>

Previously, I mostly had the opportunity to work on performance improvements for OLTP. <br>
However, here there are many opportunities to work on tuning for OLAP, streaming, or batch processing, <br>
which are topics I had not encountered before. <br>

## Development Process

### Scrum and Sprint

It seems that all departments follow Scrum, <br>
and use Jira to manage Sprints. <br>

For the Data Platform department where I'm currently working, <br>
each Sprint lasts for 2 weeks. <br>
At the beginning of each Sprint, there’s a Sprint Planning + Retro meeting, <br>
and a Grooming session the following week. <br>

There’s a Daily Standup every day <br>
to go over the current status of the tickets. <br>
However, there’s one designated No Meeting Day each week <br>
to avoid scheduling meetings on that day as much as possible. <br>

### Design Review and Code Review

If the current feature or refactor involves designing a new architecture, <br>
a Design ticket will be created. <br>
All team members are invited for a Design Review <br>
to ensure there are no potential issues with the system design <br>
and to consider the future scalability. <br>

In our department, if a Code Review is relatively large, <br>
a Code Review meeting is scheduled for everyone to review it together. <br>
For minor fixes, it's done directly through Slack with a request for approval. <br>
> It feels quite new to me, as I thought PR reviews were always done asynchronously. ~ <br>

### GitOps and Release

Every Wednesday, there's a Release Meeting. <br>
Service Owners also add their service updates to the Release Note. <br>

Since deployment is done on Kubernetes using ArgoCD, <br>
the meeting involves confirming with each Service Owner whether the corresponding PRs have been merged <br>
and whether they want to release that week. <br>

If there are issues during the release, <br>
a rollback is done immediately. <br>
For updates to external services, <br>
stakeholders are notified via Slack. <br>

## About the Long-term Internship

Since I completed the main summer internship project in the first week of August, <br>
my mentor asked me which areas of the department I was interested in. <br>
I felt that diving directly into the specifics of Data Engineering <br>
(such as Hive, Spark, Airflow, etc.) would involve a significant learning curve. <br>

I decided to start with the APIs managed by the department <br>
(which, coincidentally, use FastAPI, a framework I am quite familiar with). <br>
At that time, we were migrating to a new tech stack, <br>
so I took the opportunity to migrate the legacy Flask API codebase <br>
to a FastAPI monorepo. <br>
I also used features from the new stack to improve the original API. <br>

Just as I started the summer internship, <br>
one of the long-term interns on the Data Team transitioned to a full-time role! <br>
This opened up a headcount for a long-term internship. <br>
At the end of August, when I saw that my class schedule was free on Mondays and Tuesdays, <br>
and I wanted to finish migrating the refactored API, <br>
I decided to stay on and continue as a long-term intern! <br>