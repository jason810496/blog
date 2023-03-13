---
title: VSCode Remote SSH
subtitle: 用 VsCode 在遠端主機開發
date:   2023-03-07 12:00:00 +0800

tag: [ssh,notes]

thumbnail-img: "https://i.imgur.com/bTWmT5X.png" #1:1 (450:450)

cover-img: "https://i.imgur.com/ovkKu9d.png"

# cover-img : "https://i.imgur.com/Gmrglpd.jpg"

comments: true

# ======= Other parameters ========
layout: post
readtime: true

# test local : bundle exec jekyll serve
---

# VsCode Remote SSH

# 用 VsCode 在遠端主機開發

## VsCode 的 Remote SSH 功能

來介紹 VsCode 的其中一個強大的 extension : `Remote SSH `

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

![](https://i.imgur.com/HnxzWSA.png)

## 使用情境

### 在遠端環境開發

- 需要到  VPS（GCP / AWS / Azure / linode 等）或其他主機上開發時：

對於不太熟悉 command-line editor ( `vim` / `Emacs` 等) 的開發者來說，可以在遠端環境用 VsCode 是很大的幫助。

之前[拿 GCP 來當作開發環境時](https://jason810496.github.io/blog/2022/09/08/gcp-ssh/)，也是使用 VsCode Remote SSH 來進行開發


### 連線至 local VM

- 所使用的 VM 沒有 shared folder 的功能：

當然可以用 `scp` 或是 `sftp` 來傳輸，但是也可以以 Remote SSH Extension 來 sync 兩邊的檔案





