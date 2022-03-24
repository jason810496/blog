---
title:  打造好看的Github Profile
subtitle: 如何把Github首頁改得很潮！
date:   2022-02-08 19:16:00 +0800

tag: [github,note]

thumbnail-img: "https://i.imgur.com/fj8HzX8.png" #1:1 (450:450)

cover-img: "https://i.imgur.com/D5S7ElO.png"

#For blog posts, if you want to add a thumbnail that will show up in the feed, use thumbnail-img: /path/to/image. If no thumbnail is provided, then cover-img will be used as the thumbnail. You can use thumbnail-img: "" to disable a thumbnail.
comments: true

# ======= Other parameters ========
layout: post
readtime: true

# test local : bundle exec jekyll serve
---


## Github Profile

當我點開大神的Github首頁都會先看到有一堆炫炮徽章、activity統計紀錄的


## 預處理：

首先，要知道在Github個人首頁顯示的頁面是在`username`的repository

例如：

我的用戶名稱是`jason810496`

那我的github首頁的ur;會是`https://github.com/jason810496`

而這個特別的repository的url會在`https://github.com/jason810496/jason810496`

所以需要先建一個跟你`username`一樣名字的repository

像這樣：

![screen shot of my repo ](https://i.imgur.com/29rPdRA.png)

(他有在右邊提示說這是一個特別的repository，其中的`README.md`會在個人首頁被看到)

## 好用的工具

### Hackmd

我們已經知道其實個人首頁是一個`README.md`

就是以`Markdown`寫的

如果不會`Markdown`？

語法教學： [Markdown語法教學(Hackmd)](https://hackmd.io/c/tutorials-tw/%2Fs%2Ffeatures-tw) （個人覺得不同種的Markdown都大同小異，常用的標題大小、url連結、圖片連結、列點式標題都是相通的

那就可以開始把重要的個人資訊寫成MD，並放在`username`的respository了！

編寫MD我推薦[`Hackmd`](https://hackmd.io)

原因如下：

1. 線上編輯


