---
title: Dev Container
subtitle: 把 Docker container 當作自己的開發環境！
date:   2023-03-07 12:00:00 +0800

tag: [docker,notes]

thumbnail-img: "https://i.imgur.com/E9EPS9o.png" #1:1 (450:450)

cover-img: "https://i.imgur.com/RpOgfcD.jpg"

# cover-img : "https://i.imgur.com/Gmrglpd.jpg"

comments: true

# ======= Other parameters ========
layout: post
readtime: true

# test local : bundle exec jekyll serve
---

# Dev Container 

# 把 Docker Container 當作自己的開發環境！

## 起因

去年 Peter 跟我推薦 `Dev Container` 來開發，讓我發現 `Docker` 的強大！

## VsCode 的 Remote SSH 功能

在介紹 `Dev Container` 之前，先來介紹 VsCode 的其中一個強大的 extension : `Remote SSH `

![](https://i.imgur.com/gUR9epx.png)

這個插件可以讓你在 local 的 VsCode 打開一個**遠端主機的資料夾**來開發（ 可以讓你在遠端主機寫 code 跟平常在用 VsCode 一樣）

安裝好 Remote SSH 後，只需要在 VsCode 的左下角點選開新視窗（open a new window）

![](https://i.imgur.com/ovkKu9d.png)

再選 connect to Host (extension 會自動偵測 `.ssh` 裡面的 `config` 設定檔 )

![](https://i.imgur.com/nzo3YQl.png)

也可以選擇 Add new Host 直接來進行連線

![](https://i.imgur.com/ovkKu9d.png)

再開啟遠端主機的資料夾

![](https://i.imgur.com/gmLKj9x.png)

就可以像在 local 的 VsCode 進行開發了

![](https://i.imgur.com/x2CbjGp.png)


## Dev Container

[對 Docker 有一些理解後]()我們知道 Docker 可以透過 `-i` 這個 option (interative) 來進入 container ， 與 container 互動。

### 以正在運行的 container 來說

如果當前是 running 的 container：

例如：可能是一個在跑 web app 的 container

可以透過 `docker exec -it CONTAINER bash` 進入 container 的 `bash` shell 來修改一些設定檔，下指令。

### 以沒有在運行的 container 來說


###

基本上用起來就像一個完整的主機(不過 defult 的 image 並不會包括常見的 linux application，例如 `vi` 跟 `nano` 都不會預先安裝在裡面 )

以一個基本的 ubuntu image 為例：

### 以 Dev container 來說






