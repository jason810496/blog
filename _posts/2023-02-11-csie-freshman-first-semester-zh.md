---
title: 成大資工大一上紀錄
subtitle: 大一上到底做了什麼
date:   2023-06-23 12:00:00 +0800

tag: [csie]

thumbnail-img: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRJUt8wUbhe8qxSEK-0PTma9lypcE1AhPJrL58SICJPOQ&s" #1:1 (450:450)

cover-img: "https://oldsite.www.csie.ncku.edu.tw/ncku_csie/images/ncku/header5.png"

comments: true

# ======= Other parameters ========
layout: post
readtime: true

# test local : bundle exec jekyll serve
---

# 成大資工大一上紀錄

> 其實這篇文章是在大一升大二暑假寫的 <br>
> 主要是翻行事曆整理一下我到底大一上有做什麼 <br>

其實我大一上的重心並不是在學科 <br>
而是在接案、社團、偏實作的課程<br>
還有我真的有興趣的課程上 <br>

> 可能是因為高中後期對於學科疲乏 <br>
> 覺得學到的知識都無法運用在未來的場景 <br>
> 好像學這些沒什麼意義（？ <br>
> 比較多都是為了當下的分數而硬背起來的 <br>
> 這也是我比較不想管學科的原因 <br>

## 大一上到底做了什麼

主要會以這幾個方向來分類：

- **作業/接案**
- **社團**
- **比賽**
- **課程**
    - 實作類
    - 我有實際有興趣的
    - 學科類

## 作業/接案

因為不想花心力念一些只為了考試分數的學科 <br>
所以我就把時間花在作業和接案上 <br>
盡量多累積一些實作經驗 <br>

![blur calendar](https://github.com/jason810496/blog/blob/main/_images/20230211_blur_calendar.png?raw=true)
(模糊化的行事曆 <br>)

不過到期末發現好像接太多外務ㄌ <br>
有點忙不過來，大概一週就有好幾個 Deadline <br>

### 作業

其實在高三下我就有開始在接大學 DSA 相關的作業了 <br>
主要是當作練功，也順變賺點小外快 <br>

![repo screenshot]()

[專門放接案作業的 repository ](https://github.com/jason810496/freelance)

在上學期間接了不少個作業，主要也是寫 C++ <br>
偶爾有一些特別的作業：<br>
用 `Matlab` 來實作一些演算法 <br>
寫 `Scala` 這個完全沒聽過的 `functional programming language` <br>
或是超難的圖論題<br>

### 接案

剛好在成大二手版看到一個徵**網頁工讀生**的貼文 <br>
從高三上接觸前端，升大一暑假也有寫過一些後端 CRUD <br>
對基本的前後端應該都有一些概念 <br>
就去應徵看看 <br>

![fb post](https://github.com/jason810496/blog/blob/main/_images/20230211_fb_post.png?raw=true)


案主是也是成大的大學長 <br>
網站原本是由外包公司完成的 <br>
後來由另一位學長在幫忙修改、新增功能 <br>

整個網站的 tech stack 是：
- **Hosting** : 
    - [`Hostinger`](https://www.hostinger.com/) ( 我自己沒聽過，不過用起來延遲有時候有點嚴重 )
- **Frontend** :
    - `jQuery`
    - `raw HTML/CSS/JS`
- **Backend** :
    - `PHP`: [`Slim framework`](https://www.slimframework.com/) ( 那時候只知道 `Laravel`，沒聽過 `Slim` )
    - `MySQL`
- **Structure** :
    - `MVC`
- **Version Control** :
    - `Git`
    - `Self hosted Git server`: [`Gitea`](https://about.gitea.com/)
- **CI/CD** :
    - null (?)

> 這是算是我第一次接到的案子 <br>
> 也是我第一次接觸到 `MVC` 的架構 <br>
> 也是我認知到 `CI/CD` 的重要性的專案 <br>

網頁的瀏覽人數不高，不過整體的網頁架構也蠻複雜的（ 有些 Code 不太好看，蠻難改的 ） <br>
不過有蠻多 features 案主想要新增修改的 <br>
主要是跟保險有關的網站系統 <br>

**Features** ：
- 網頁前台
    - 保險計算
    - 保險推薦
    - 保險資訊
    - 文章系統
- 網頁後台
    - 會員系統管理
    - 保險 CRUS
    - 文章 CRUD

**負責的任務：**
- 一些小 bug fix：
    - 有些資料要先排序才再送到前端
        - 找到相對應的 SQL query，加上 `ORDER BY...`
    - 一些前端 RWD 跑版修正
        - 需要一直跟案主來回確認版型
- 新增後台文章 `wsywig` 編輯器：
    - `wsywig` 編輯器：類似 `Google doc` ，可以在網頁上直接編輯文章的段落、大小、顏色、加圖片...的工具
    - 原本的文章系統只有單純一個 `textarea`，沒有 `wsywig` 編輯器
    - 後來用 [`quill.js`](https://github.com/quilljs/quill) 這個開源的 js library 實作
    - 一開始找到付費的 [ `froala` ](https://froala.com/) ，當時沒有把文件看清楚，以為是可以免費試用的，後來才發現是付費的
- 很多前端的修正：
    - 一些 RWD 的跑版
    - 一些前端的 UI/UX 調整
    - 一些前端的功能新增
    - 遇到各種 `js` 的坑
    - 因為沒有用現在前端 `framework` ，整個的前端頁面架構蠻亂的，有時候要找到對應的 `css` 很花時間

![editor](https://github.com/jason810496/blog/blob/main/_images/20230211_editor.jpg?raw=true)
( 整合 `quill.js` 的 `wsywig` 編輯器到後台文章系統 )

**遇到奇怪的事：**
- `肉眼 + SMTP` 就是專案的 `CI/CD` ?_? :
    - 把當前 feature 弄好後，在 local 跑起來再開 `ngrok` 給案主測
    - 沒問題後把 code push 到 `Gitea` 上
    - 那要怎麼部署到 `Hostinger` 呢？
        - 真的是體會過才會知道好的 `CI/CD` 有多重要
        - 先把會更動到的檔案用 `SMTP` 備份下來 (方便之後有問題 rollback )
        - 再把有更新的檔案複製到 `Hostinger` 上
        - 所以就很容易會有 `Hostinger` 上的 code 跟 `Gitea` 上的 code 不一樣的問題...
- 在 backend 商業邏輯寫前端 :
    - 雖然整體是 `MVC` 架構
    - 不過會看到一個像後端的 `php` 檔案回傳一整個 component 的 html ，但沒有分離到 view (找了超久才知道要在哪裡改前端的某個 compoent )
- 對 Github 的抗拒 :
    - 不知道為什麼一開始學長和案主不想用 Github 
    - 反而大費周張自己架 git server 
    - 而且當時那個學長家裡的 WAN 並沒有申請固定 IP ，所以每次都要透過 `ngrok` 來連到 git server
    - 也就是我跟學長必須要同時在現在才有辦法 push code ( 而且每次都需要加新的 remote )
    - 如果用 Github 就不會有這個問題，而且還可以用 Github 跑一些 CI/CD 的流程


> 這個案子我接了大概 3-4 個月 <br>
> 也是我第一次接觸到 `CI/CD` 的重要性 <br>

**透過這個案子學到的：**
- 快速上手不熟悉的語言和框架
- 一些框架延伸的 design pattern
    - `MVC`、`DAO`
- 看懂別人的 code 的速度
- 上手別人專案的速度
    - 一開始真的看不蓋懂哪邊是在寫什麼邏輯
    - 後來慢慢熟悉後，就可以快速找到對應的 code
- 了解到 `CI/CD` 的重要性
- 對 `git` 更熟一些
    - 當時是對 feature 開 branch ，然後 `hostinger` 上的 code 就是 `master`
    - 偏向 `git flow` 的方式

## 社團


