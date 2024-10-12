---
title: "2024 Appier 暑期實習心得"
summary: "在 Appier - Data Platform 部門的後端暑期實習心得"
description: "在 Appier - Data Platform 部門的後端暑期實習心得"
date: 2024-10-01T21:21:01+08:00
slug: "appier-summer-intern"
tags: ["blog","zh-tw","intern"]
# series: ["Documentation"]
# series_order: 9
cascade:
  showEdit: true
  showSummary: true
  hideFeatureImage: false
draft: false
---

## 面試

有關於 Appier 的面試過程 <br>
可以參考

{{< article link="/zh-tw/intern/summer-intern-interview-2024-appier/" >}}

總結來說，看完 Intern 的組成 <br>
只能說在大二升大三拿到 Appier 暑期實習的機會真的很幸運 ! <br>

## 關於暑期實習計劃

為什麼說是暑期實習「計畫」呢？ <br>

在我實習的第一天 <br>
剛好有舉辦一個聚集所有暑期實習的培訓 <br>
和後續與暑期實習有關的所有活動都是用「Summer Internship Program」來稱呼 <br>
今年是 Appier 的第 3 年暑期實習計畫 <br>

暑期實習計劃本身以活動來說主要分為 3 個部分 <br>
1. 培訓 (Orientation Training)
2. 專案本身
3. 專案分享

## 培訓 (Orientation Training)

雖然說是培訓 <br>
但其實算是一個很輕鬆的活動 <br>
也剛好辦在我實習的第一天 <br>

{{< figure
    src="orientation-snack.jpeg"
    alt="Orientation Snack"
    caption="當天還有[KOBE SWEETS 神戶果実](https://g.co/kgs/Sh6Yr8S)的蛋糕跟**再睡五分鐘**的飲料"
>}}

主要介紹暑期實習計劃的主要活動 <br>
歷年的申請狀況 ( 今年好像有 600 多位申請 ) <br>
公司的文化 <br>
各個 Intern 自我介紹 <br>
最後放時間讓大家自由交流 <br>

### Intern 的組成

當天大概有 15 位暑期 Intern <br>
聽完大家的自我介紹後 <br>
粗略統計有約 10 來個都是 NTU or 要出國讀 or 在國外讀回台灣的學生 <br>
也有準備要去念 MIT 的高中升大學生 [@jieruei](https://github.com/knosmos) Orz <br>

當天蠻好笑的是 <br>
幾乎每個人都有認識的朋友在這次的暑期實習 <br>
像我跟 [@m4xshen](https://github.com/m4xshen) 是高中同學 <br>
[@vax-r](https://github.com/vax-r) 算是在成大 GDSC 認識的 <br>
然後又有很多人說也跟另外一位 Intern 認識 <br>
聽到蠻多是之前在 AppWorks Camp 互相認識的 ~ <br>
讓 600 多取 15 的機率變得感覺好像不是那麼低了 XD <br>

## Onboarding

我其實是在 7 月第二個週才開始實習的 <br>
> 5 6 月左右 HR 有連絡我問可不可以延後一週開始 <br>
> 原本是在 7 月第一週開始 <br>
> 主要因為第一週有太多人要 Onboard <br>
> 所以希望能夠分散一下 <br>
> 因為我暑期實習的時間相對完整 ( 是到 9 月的第一個星期正式結束 ) <br>
> 有蠻多 Intern 都是要在 8 月中就結束了 <br>


第一個星期都在等相關的權限申請 <br>
所以都在看內部有關 Data Engineering 的文件 <br>
也正常參加 Team 上的 Meeting <br>
看一下現有的 Codebase <br>

## 專案本身

每個 Intern 都是在不同部門的專案上 <br>
所以大家做的專案都不太一樣 <br>
蠻看該部門當時的需求 <br>

而我是在 Data Platform 部門擔任 Backend Intern <br>
專案可以理解為「**Operation Dashboard**」<br>
這個 Dashboard 不是 Grafana 或是 Kibana 這種 Monitoring Dashboard <br>

而是一個 Data Platform 部門給上、下游相關部門使用的 Web Dashboard <br>
供與 Appier 的 OAuth Authentication 和內部的 Authorization 整合 <br>
提供相關部門在有權限的情況下能夠 <br>
- **改 Data Platform 相對應的 Config**: 如 XX Team 的 Dev Role 當前 Worker 數量
- **查看 Data Platform 的狀態**: 目前有哪些 Dataset，並提供相對應的 filter
- **自動化 Operation Task**: 原本需要對 Data Team 開 Ticket 的操作，現在可以在 Dashboard 上直接操作
- **也會對以上的操作保留相對應的 Audit Log 紀錄**

### 解決的問題

主要解決如下所提的情境

**XX Team 的 oncall 發現需要緊急增加 Worker 數量**
- 原本還是需要聯絡 Data Team 來改 Config 處理
  - 如果 Data Team 沒有人注意到，可能會造成 XX Team 的服務中斷
- 現在可以直接在 Dashboard 上操作，不用透過 Data Team 才能改 Config
  - XX Team 的 oncall 可以直接操作，並且有 Audit Log 紀錄


**XX Team 提出 Operation Task**
- 原本需要開 Ticket 給 Data Team 來處理
  - 一般來說這種 Task 都是下一段 script 就可以直接解決的
  - 但 Data Team 可能有更緊急的 Task 或是在會議中
- 現在可以直接在 Dashboard 上操作，不用透過 Data Team 才能處理 Task
  - 節省雙方的時間成本

## 技術層面

### 系統架構

Operation Dashboard 由 [Streamlit](https://streamlit.io/) 開發的前後端 <br>
使用 Postgres 紀錄 User Authorization <br>
並有另外一個 Cronjob 來定時同步 Appier 的 Authorization 關係到 Postgres <br>

還有像前面提到的情境 <br>
所以 Operation Dashboard 要能夠 call Kubernetes API 來改 Config <br>
或是 call Data Platform 內部的 API 來呈現狀態 <br>

### 框架選擇

之前也有其他 Team 有開發過類似需求的 Dashboard <br>
就是使用 [Streamlit](https://streamlit.io/) 來開發 <br>

Streamlit 是一個可以用 Python 寫 Web App 的框架 <br>
主要用於呈現 Data Visualization 或是 Machine Learning Model 的結果 <br>
( 內建提供很多對 Pandas, Matplotlib, Plotly 的支援 ) <br>

可以只透過 Python 來開發，不需要額外的前端知識 <br>
剛好 Data Platform 部門沒有前端的人力 <br>
所以選擇 Streamlit 來開發 <br>

### Streamlit Router Framework

因為這個 Dashboard 主要被當作前端使用而已 <br>
原生 streamlit 提供的 [multi-page: `st.navigation`](https://docs.streamlit.io/develop/api-reference/navigation/st.navigation) 功能 <br>
都需要直接把一個頁面寫在單一個 Python 檔案裡 <br>
以在 IDE 中來 trace code 來說是很不方便的 ( 沒辦法直接按 `shift` + `click` 來跳到 definition 的區塊 ) <br>

所以刻了基於[st.navigation](https://docs.streamlit.io/develop/api-reference/navigation/st.navigation) 的 **decorator-based** 的 framework <br>
可以讓不同的 Page 寫在同一個 Python 檔案裡 <br>
並提供 `Router` 來註冊不同的 Page <br>
能夠更方便的 trace code <br>
對於常寫 FastAPI 或 Flask 的人來說應該會比較習慣 <br>

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
> Framework 大概用起來會像這樣

### Authentication

Authentication 是指一個 User 是否已經登入 <br>

因為這個 Dashboard 是要給上、下游相關部門使用的 <br>
所以需要整合 Appier 的 OAuth Authentication 和內部的 Authorization <br>

Authentication 就透過 Google OAuth 來實現 <br>
不過因為 Streamlit 本身框架實作的限制，只能用內部的 session 來實現已經登入的狀態 <br>
不能透過 JWT + HTTP Only 的 Cookie 來實現 <br>

### Authorization

Authorization 是指一個 User 是否有權限執行某個 Action <br>

如果這邊還需要從 0 開始維護一個給所有 Data Platform 相關部門的 Authorization <br>
1. 會增加 Data Platform Team 的維護成本
2. 可能與原本 Appier 內部的 Groups-Users 關係有不一致的地方

至少簡化到只需要讓 Data Platform Team 維護 Groups-Users 與 Action 的對應關係就好 <br>
所以會有一個 **Cronjob** 來定時同步 Appier 的 Groups-Users 關係到 Postgres <br>
而在 Dashboard 上的 Authorization 都會透過這個 Postgres 來判斷是否有權限 <br>


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
> Authorization 在 Postgres 的 ER Diagram 大概會長這樣 <br>

## 專案分享

暑期實習計劃最重要的一環就是**約半小時的全英文專案分享** <br>
( 不過可以用 Google Slides 補一些講稿 ) <br>
最後會有 5 分鐘的 Q&A <br>
也都是全英文進行 <br> 

每個暑期 Intern 都會在實習的最後一週分享自己的專案 <br>
幾乎都是 2 位 Intern 一組來分享 <br>
所有 Appier 的同事都可以參加這個分享 <br>
會在實體的會議室裡進行 <br>
有興趣的人可以來會議室或實體參加 <br>
主要透過這個機會了解其他部門的維護的服務 <br>

## Team 與 Mentor

Data Platform Team 不到 10 人 <br>
因為不算 Product Team 所以也沒有前端，都是 Backend、Data Engineer <br>

算有 2 個 Mentor <br>
一個主要 mentor 我暑期實習的專案 <br>
還有另一位主要是 mentor 我 refactor API 的專案 <br>
( 在最後[#關於長期實習](#關於長期實習)提到的 refactor ) <br>

大家都很親切！ <br>
都很願意分享 Data Engineering 相關的知識、架構 <br>
跟自己的經驗 ～ <br>

## 辦公環境 & 食物

**辦公室** <br>
辦公室在信義區捷運象山站附近 <br>
可以蠻清楚的看到台北 101 <br>
有些樓層還有旋轉樓梯可以走上下樓 <br>

{{< gallery >}}
  <img src="/intern/appier-summer-intern/office-1.jpeg" class="grid-w100 md:grid-w100" />
  <img src="/intern/appier-summer-intern/office-2.jpeg" class="grid-w100 md:grid-w50" />
  <img src="/intern/appier-summer-intern/office-3.jpeg" class="grid-w100 md:grid-w50" />
{{< /gallery >}}

**午餐** <br>
因為在辦公室在信義區 <br>
午餐能吃到 200 內算超級便宜的 ~ <br>
跟 Team 去吃大部分都是去吃百貨公司 <br>
有時候也會往市政府的方向去吃小吃類的 <br>

{{< gallery >}}
  <img src="/intern/appier-summer-intern/team-meal-chun-shui-tang.jpeg" class="grid-w100 md:grid-w50" />
  <img src="/intern/appier-summer-intern/team-meal-dumpling.jpeg" class="grid-w100 md:grid-w50" />
  <img src="/intern/appier-summer-intern/team-meal-first-day.jpeg" class="grid-w100 md:grid-w50" />
  <img src="/intern/appier-summer-intern/team-meal-kafka.jpeg" class="grid-w100 md:grid-w50" />
{{< /gallery >}}
( 圖4: Team Building 吃火鍋，吃到開始畫出 Kafka 的架構也是合情合理的 ouo ) 


辦公室有一整櫃的飲料還有一些些零食 <br>
大部分都是小鋁箔包 <br>
幾乎每天都會拿一瓶豆漿來喝 XD <br>
偶爾會放一些水果 (有吃過香蕉、藍莓、桃子) <br>
自己吃的時候幾乎都買附近的健康餐盒配辦公室的飲料水果 ~ <br>


{{< gallery >}}
  <img src="/intern/appier-summer-intern/meal-box-1.jpeg" class="grid-w100 md:grid-w50" />
  <img src="/intern/appier-summer-intern/meal-box-2.jpeg" class="grid-w100 md:grid-w50" />
  <img src="/intern/appier-summer-intern/meal-box-3.jpeg" class="grid-w100 md:grid-w50" />
{{< /gallery >}}

**Happy Hour** <br>
每週五下午會有 Happy Hour <br>
可以點下午茶 ! <br>
有可能是飲料或是小點心，每次都不太一定 <br>
( 有一次是小木屋鬆餅 不過剛好當天是 Team Building 沒有吃到 超可惜的QQ )

{{< gallery >}}
  <img src="/intern/appier-summer-intern/happy-hour-3.jpeg" class="grid-w100 md:grid-w33" />
  <img src="/intern/appier-summer-intern/happy-hour-1.jpeg" class="grid-w100 md:grid-w33" />
  <img src="/intern/appier-summer-intern/happy-hour-2.jpeg" class="grid-w100 md:grid-w33" />
{{< /gallery >}}

**社團** <br>
還有一天遇到期中一個社團在中午分享如何調酒 <br>
當天就有訂一堆披薩跟韓式炸雞 ! <br>

{{< gallery >}}
  <img src="/intern/appier-summer-intern/club-fried-checken.jpeg" class="grid-w100 md:grid-w50" />
  <img src="/intern/appier-summer-intern/club-pizza.jpeg" class="grid-w100 md:grid-w50" />
{{< /gallery >}}

## 公司文化

每個公司都有自己的提倡的文化 <br>
Appier 的 core values 是 <br>
- open-mindedness
- direct communications
- ambition

在與 Mentor 聊天時也有討論到不同公司的文化 <br>
在 Design Review 或 Code Review 也有感覺到是蠻 open-minded 的 <br>
Mentor 或主管只會設定一個大方向 <br>
剩下所有的技術細節都是自己可以設計、與大家討論的 <br>
Team members 也會在 Review 中提供 feedback <br>

## 技術層面

### Data Engineering

這次最主要新接觸到的是都是 Data Engineering 相關的技術 <br>
有太多可以分享了 <br>
額外寫在這邊介紹 <br>

{{< article link="/backend/first-thought-of-data-engineering/" >}}

### Infra 與 Dev

在 Appier 這邊 <br>
自己部門 Application 的 Helm Chart 或是 Grafana Dashboard <br>
或是 Application 會用到的 Infra 如 Postgres、Redis、Kafka 等 <br>
都是屬於 Backend 的範圍 <br>
並不會有 Infra 來幫忙維護 <br>

Infra 是以 Saas 的方式提供如： <br>
有加上許多方便 plugin 的 ArgoCD <br>
還有多個 Kubernetes Cluster 的管理或升級等 <br>
或是與 k8s 整合好的 EFK 提供 Log tracing <br>
( 還有很多其他服務，不過目前有接觸到的只有這些 ) <br>

跟以前實習/ PT 的公司相比 <br>
主要是因為 Appier 的部門比較多 <br>
之前的公司也等於一個產品一個部門 <br>
部署或 Storage 相關的維護會有專職的 Infra <br>

在 Appier 這邊 Backend 的防守範圍就更大了 <br>
要對自己 Application 使用的 Infra 有更多的了解 <br>
才能處理 Production Issue 來找 root cause <br>

### Infra as Code 實踐

在 Appier 有非常多部門 <br>
有數十個 kubernetes cluster 或是 Cloud SQL Instance <br>
再加上 VPC、IAM、Secret 等等 <br>
這時候不太可能再用手動的方式來維護 <br>

在這邊又實際體會到 Infra as Code 的好處 <br>
可以 modularize 重複的 resource <br>
並且在 repo 的 Terraform 就應該與實際的 Instance 的狀態一致 <br>

當 Cloud Infra 到一定的規模時 <br>
IaC 就有存在的必要性 <br>


### Senior 的角色

- Review Code
- Cost Reduction
- Root Cause Analysis
- Sprint Planning
- Performance Tuning

這些都是發現平常蠻難接觸到 <br>
發現與 Senior 的差異 <br>

之前只有比較有機會接觸到一些針對 OLTP 的 performance improvement <br>
但這邊有很多針對 OLAP 、streaming 或 batch processing 的 tuning <br>
都是之前都沒有碰過的主題 <br>

## 開發流程

### Scrum 和 Sprint

應該所有部門都是跑 Scrum <br>
並用 Jira 來管理 Sprint <br>

以我目前待的 Data Platform 部門來說 <br>
是 2 週一個 Sprint <br>
每個 Sprint 的開頭會有一個 Sprint Planning + Retro <br>
隔週就是 Grooming <br>

每天都會有 Daily Standup <br>
就過一下目前 Ticket 的狀況 <br>
不過會有一天作為 No Meeting Day <br>
大家要約會議就盡量避開這天 <br>


### Design Review 和 Code Review

如果目前在做的 feature 或 refactor 需要設計新架構的話 <br>
就會有一張 Design 的 Ticket <br>
並且會拉所有人過 Design Review <br>
讓大家確認一下這個 System Design 有沒有什麼淺在的問題 <br>
對於未來的 Scalability 有沒有考慮到 <br>

我們部門的 Code Review 如果比較大的話 <br>
會拉一個 Code Review 的會來請大家幫忙看一下 <br>
如果只是小的修正就直接在 Slack @ 幫忙 approve <br>
> 覺得還蠻新鮮的，以為大家過 PR 都是非同步進行的 ~ <br>

### GitOps 與 Release 

每週三都會有 Release Meeting <br>
Service Owner 也會在 Release Note 加上自己的 Service 的更新 <br>

因為在 Kubernetes 上透過 ArgoCD 來部署 <br>
會在 Meeting 上跟各個 Service Owner 確認相對應的 PR 是否已經 Merge <br>
有沒有要在這週 Release <br>

如果 Release 當下有問題 <br>
就馬上 rollback <br>
如果有對外的服務更新 <br>
也會在 Slack 上通知 stakeholder <br>

## 關於長期實習

因為在 8 月第ㄧ週就把主要暑期實習的專案完成了 <br>
Mentor 也有問我對目前部門的哪一塊有興趣 <br>
我覺得要直接進入 Data Engineering 的專項
( 如: Hive, Spark, Airflow 等 ) <br>
還有蠻大的學習成本 <br>

想先從部門負責的 API 下手 <br>
( 剛好也是使用我算蠻熟習的 FastAPI ) <br>
當時因為要進行其他 Tech Stack 的 Migration <br>
就順便把原本是 Flask API 的 legacy codebase <br>
搬遷到 FastAPI 的 monorepo 上 <br>
同時也裡用新 Stack 的 feature 來改善原本的 API <br>

剛好我開始暑期實習時 <br>
Data Team 原本其中一個長期實習轉正職了 ! <br>
所以有 Headcount 可以轉長期實習 <br>
在 8 月底選課出來發現剛好星期一、二沒有課 ~ <br>
也想把正在 refactor 的 API 搬完 <br>
就決定繼續留下來做長期實習了 ! <br>