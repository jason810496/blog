---
title:  Build a eye-catching Github Profile !
subtitle: How to make Github profile fancy !
date:   2022-02-08 19:16:00 +0800

tag: [github,notes,eng]

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

When I browse over expert's Github profile page , I see numerous elaborate
當我點開大神的Github首頁都會先看到有一堆炫炮徽章、activity統計紀錄的card...

看起來就很專業，也可以提供一些簡單的個人資訊（最常使用哪個語言、commit次數、連續活躍天數...

一方面是讓別人對自己有初步的了解，另一方面是~~自己看了很開心~~
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

只要登入hackmd的帳號，無論在電腦還是手機都可以**即時**編輯檔案

2. 同時預覽

如下圖所示，可以同時編輯、預覽該MD的結果
![](https://i.imgur.com/cbSRefz.png)


### Github profile readme generator

[Github首頁產生器](https://rahuldkjain.github.io/gh-profile-readme-generator/)

真的沒什麼想法、不知道如何下手或~~單純有點懶~~

這是一個非常簡便的工具，只要將欄位都填好再勾選技能樹

如圖：
![](https://i.imgur.com/uiQR2Hz.png)

![](https://i.imgur.com/e6g9Dc0.png)

不到5分鐘就完成你的Github Profile了

結果：
![](https://i.imgur.com/UpHSaev.png)

## 那card呢？

回歸今天的主題：

在首頁顯示有炫炮統計資料的卡片

而剛剛`README`中下方三個卡片的markdown如下：

```html

![LJO's GitHub stats](https://github-readme-stats.vercel.app/api?username=jason810496&show_icons=true&theme=tokyonight&hide_border=true)

![Top Langs](https://github-readme-stats.vercel.app/api/top-langs/?username=jason810496&layout=compact&theme=tokyonight&hide_border=true)

[![GitHub Streak](https://github-readme-streak-stats.herokuapp.com?user=jason810496&theme=tokyonight&hide_border=true&date_format=M%20j%5B%2C%20Y%5D)](https://git.io/streak-stats)
```

可以看到都是一個個**圖片**所夠成的卡片（依我的理解應該是需要一個server來處理這些get request 並透過github api生成這些卡片的圖片，這可以突破在靜態網頁要顯示即時資訊的限制！）

## 其他相關的card

### Wakatime


[Wakatime](https://wakatime.com/)是一個可以在不同IDE統計使用時間的Plugin（可以紀錄在這個檔案、專案的時間，使用不同語言的時間，本週的使用總時間、從註冊至今的coding time...

要使用以下的card都要先註冊Wakatime並且在常用的IDE裝好Plugin才能有資料

如這個[project](https://github.com/anuraghazra/github-readme-stats/)可以看到Wakatime紀錄不同語言的使用時間

![LJO's wakatime stats](https://github-readme-stats.vercel.app/api/wakatime?username=jason810496&theme=tokyonight&hide_border=true)

而這是註冊至今的總coding時間（登入後會在左邊navbar中的[`share`](https://wakatime.com/share)

[![wakatime](https://wakatime.com/badge/user/5c4d6a5b-0b6e-45b9-b81f-78e13584375d.svg)](https://wakatime.com/@5c4d6a5b-0b6e-45b9-b81f-78e13584375d)

### 各大解題系統的card

如果身為一個專門打程式競賽的肯定在各大online judge刷過很多題

#### TIOJ
也只有找到一個，但是頗有質感ㄉ

[TIOJ stats card](https://github.com/JacobLinCool/TIOJ-Stats-Card)
#### Leetcode
跟上面TIOJ是同一個作者

[Leetcode stats card](https://github.com/JacobLinCool/LeetCode-Stats-Card)
#### Codeforce
查了Github但是很多為完成品，只有這個是完成而且還可以運作的(不過我覺得還可以加強，到時候應該會發個PR

[Codeforce stats card](https://cf-stats.siriuskoan.workers.dev/)
#### Atcoder
只有找到這個：

[Atcoder Trophies](https://github.com/KATO-Hiro/AtCoderTrophies)

#### Zerojudge
**NULL**

目前還沒有人做過

（3/26更，所以**我自己做了一個**[Zerojudge stats](https://github.com/jason810496/Zerojudge-stats)不過目前是Beta版本，還有很多東西要加強

## 總結

Github Profile是一個可以放入很多小巧思的地方

可以提供些有用的簡述讓瀏覽者多認識你

但是不要忘了美化首頁

讓它看起來更上心悅目！






##### reference
https://github.com/anuraghazra/github-readme-stats/discussions/1329
https://github.com/denvercoder1/github-readme-streak-stats
https://github-readme-streak-stats.herokuapp.com/demo/
https://github.com/anuraghazra/github-readme-stats#repo-card-exclusive-options

