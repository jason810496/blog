---
title: "常用 tmux 指令"
summary: "常用 tmux 指令 Cheat Sheet"
description: "常用 tmux 指令 Cheat Sheet"
date: 2024-05-28T16:44:08+08:00
slug: "tmux"
tags: ["blog","zh-tw"]
# series: ["Documentation"]
# series_order: 9
cascade:
  showEdit: true
  showSummary: true
  hideFeatureImage: false
draft: false
---

{{< github repo="tmux/tmux" >}}

## 前言

因為系上開給程式設計一的 VM 需要設定 cloudflare tunnel 才能連線 <br>
( 有興趣可以看[我的 cloudflare-tunnel 設定過程]() ) <br>


所以想用 `tmux` 來讓 tunnel 一直在背景執行 <br>
也可以隨時查看 tunnel 的狀態 <br>

## tmux 概念

`tmux` 可以分成三個層級 <br>
1. Session
2. Window
3. Pane

### Session

Session 是 `tmux` 的最高層級 <br>
可以想像成一個 tmux 的工作區 <br>
一個 Session 可以有多個 Window <br>

![tmux ls : list session](tmux_ls.png)
( 列出所有可用的 session )

### Window

Window 是 `tmux` 的第二層 <br>
可以想像成一個 Session 中的不同視窗 <br>
一個 Window 可以有多個 Pane <br>

### Pane

Pane 是 `tmux` 的第三層 <br>
可以想像成一個 Window 中的不同分割畫面 <br>
一個 Pane 只能有一個 Shell <br>
同一個 Window 中的 Pane 可以被水平或垂直分割 <br>
![tmux +s](tmux_preview.png)

( 所以可以被切成這樣 )

## tmux 常用指令

如果是在 tmux 中，可以直接按 `Ctrl + b` 來進入 tmux 的指令模式 <br>
( 像是在 vim 中按 `:` 一樣 ) <br>

### Session

從 command line : <br>
- `tmux new -s <session-name>` : 新增一個名為 `<session-name>` 的 session
- `tmux ls` : 列出所有可用的 session
- `tmux attach -t <session-name>` : 連接到名為 `<session-name>` 的 session

在 tmux 中 : <br>
- `Ctrl + b + d` : 離開 tmux session <br>
    並不會把 session 關掉，只是離開而已 <br>
    所以在 session 中的程式還是會繼續執行 !!!
- `Ctrl + b + s` : 列出所有可用的 session
    ![tmux +s](tmux_session.png)

### Window

- `Ctrl + b + c` : 新增一個 window
- `Ctrl + b + n` : 切換到下一個 window
- `Ctrl + b + p` : 切換到上一個 window
- `Ctrl + b + w` : 列出所有可用的 window

### Pane

pane 分割:
- `Ctrl + b + %` : 垂直分割畫面 ( 左右分割 )
- `Ctrl + b + "` : 水平分割畫面 ( 上下分割 )
- `Ctrl + b + x` : 關閉目前的 pane

調整 pane 的大小:
可以先按 `Ctrl + b ` 再按 `:` 進入 tmux 的指令模式 <br>
然後輸入 `resize-pane` ( 可以按 `Tab` 來自動補全 ) <br>
再加上 `-U` ( 上 ) `-D` ( 下 ) `-L` ( 左 ) `-R` ( 右 ) <br>
再加上數字來調整 pane 的大小 <br>
![resize-pane](resize_pane.png)

在 pane 之間切換:
- `Ctrl + b + <arrow-key>` : 切換到指定的 pane
- `Ctrl + b + q` : 會在 pane 上顯示一個數字
    - `Ctrl + b + q + <number>` : 切換到指定的 pane

![pane ls](pane_ls.png)