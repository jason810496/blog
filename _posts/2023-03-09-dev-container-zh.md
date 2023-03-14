---
title: Dev Container
subtitle: 把 Docker container 當作自己的開發環境！
date:   2023-03-14 12:00:00 +0800

tag: [docker,notes]

thumbnail-img: "https://i.imgur.com/5JvtUhQ.png" #1:1 (450:450)

cover-img: "https://i.imgur.com/Dwr5Hmf.png"

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

去年 [Peter](https://github.com/peterxcli) 跟我推薦 `Dev Container` 來開發，讓我發現 `Docker` 的強大！

## Dev Container

[對 Docker 有一些理解後](#)我們知道 Docker 可以透過 `-i` 這個 option ( 也就是 interative mode ) 來進入 container ， 與 container 互動。

### 以正在運行的 container 來說

如果當前是 running 的 container：

例如：可能是一個在跑 web app 的 container

可以透過 `docker exec -it CONTAINER bash` 進入 container 的 `bash` shell 來修改一些設定檔，下指令。

先用 `docker ps` 看一下當前有哪些運行的 container
![](https://i.imgur.com/gVqXs8m.png)

接著就可以透過 `docker exec -it 05777cc91423 bash` 進入 container 了
![](https://i.imgur.com/4w3sdRn.png)

### 以沒有在運行的 container 來說

先用 `docker ps -a` 看所有的 container ( 要加上 `-a` tag )
![](https://i.imgur.com/2NTV8w6.png)

接著就可以透過 `docker start -i CONTAINER` 重啟並進入 container 
![](https://i.imgur.com/TAuTY1Q.png)


### 整題而言

基本上用起來就像一個完整的主機(不過 defult 的 image 並不會包括常見的 linux application，例如 `vi` 跟 `nano` 等終端機編輯器都不會預先安裝在裡面 )

不過還沒有方便到可以當作開發環境(畢竟要將檔案複製到 container 中還需要透過 `docker cp` 或是預先開好 `volumn` 等，必較蠻煩的動作 )

## 以 Dev container 來說

Dev container (VSCode 的 extension) 幫我們整合好與 docker 連動的開發環境
![](https://i.imgur.com/4Bw5GUE.png)

只需要開啟 VSCode 的 `command palette` (快捷鍵：`command + Shift + p`) 並打 `Dev container` ，就可以將當前的資料夾在 container 中打開，並開好 volumn (local 的檔案更新時，container 中的檔案也會更新)

## 心得

Dev container 與 [VSCode Remote SSH](https://jason810496.codes/blog/2023/03/07/vscode-remote-ssh-zh/) 這個 extension 相似 (可以看成透過 `Remote SSH` 進入 Docker container 中 )

Dev container 可以幫我們維護本機環境的整潔（同時可以確保專案可以在所有開發者的環境中運行）

這邊推薦一個透過 Dev Container (`Docker`) 讓我們更容易使用 `Latex` 的專案：

[https://github.com/hegerdes/VSCode-LaTeX-Container](https://github.com/hegerdes/VSCode-LaTeX-Container)

在把專案 `git clone` 到 local 後，只要以 Dev Container 開啟

![](https://i.imgur.com/LcjFqnq.png)

就可以不用額外安裝任何 `Latex` 相關的套件，就可以在 VSCode 寫 `Latex` 了 ( 並且該專案還能讓我們即時預覽 `pdf` ， 非常方便！)

![](https://i.imgur.com/3nnA0PK.png)








