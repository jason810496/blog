---
title: "Tmux Cheat Sheet"
summary: "Common tmux commands Cheat Sheet"
description: "Common tmux commands Cheat Sheet"
date: 2024-05-28T16:44:08+08:00
slug: "tmux"
tags: ["blog","en"]
# series: ["Documentation"]
# series_order: 9
cascade:
  showEdit: true
  showSummary: true
  hideFeatureImage: false
draft: false
---

{{< github repo="tmux/tmux" >}}


## Introduction

Since the VM provided for the Programming 1 course requires a Cloudflare tunnel setup for connection <br>
(If interested, you can see [my Cloudflare-tunnel setup process]()) <br>

I wanted to use `tmux` to keep the tunnel running in the background <br>
and to check the tunnel's status at any time <br>

## tmux Concepts

`tmux` can be divided into three levels <br>
1. Session
2. Window
3. Pane

### Session

Session is the highest level in `tmux` <br>
You can think of it as a workspace in tmux <br>
A session can have multiple windows <br>

![tmux ls : list session](tmux_ls.png)
(List all available sessions)

### Window

Window is the second level in `tmux` <br>
You can think of it as different windows within a session <br>
A window can have multiple panes <br>

### Pane

Pane is the third level in `tmux` <br>
You can think of it as different split screens within a window <br>
A pane can only have one shell <br>
Panes in the same window can be split horizontally or vertically <br>
![tmux +s](tmux_preview.png)

(This is how it can be split)

## Common tmux Commands

If you are in tmux, you can press `Ctrl + b` to enter tmux command mode <br>
(Just like pressing `:` in vim) <br>

### Session

From the command line: <br>
- `tmux new -s <session-name>` : Create a new session named `<session-name>`
- `tmux ls` : List all available sessions
- `tmux attach -t <session-name>` : Attach to a session named `<session-name>`

In tmux: <br>
- `Ctrl + b + d` : Detach from the tmux session <br>
    This does not close the session; it just detaches <br>
    The programs in the session will continue to run!!!
- `Ctrl + b + s` : List all available sessions
    ![tmux +s](tmux_session.png)

### Window

- `Ctrl + b + c` : Create a new window
- `Ctrl + b + n` : Switch to the next window
- `Ctrl + b + p` : Switch to the previous window
- `Ctrl + b + w` : List all available windows

### Pane

Splitting panes:
- `Ctrl + b + %` : Split the screen vertically (left/right split)
- `Ctrl + b + "` : Split the screen horizontally (top/bottom split)
- `Ctrl + b + x` : Close the current pane

Resizing panes:
You can first press `Ctrl + b` then `:` to enter tmux command mode <br>
Then type `resize-pane` (you can use `Tab` for auto-completion) <br>
Then add `-U` (up) `-D` (down) `-L` (left) `-R` (right) <br>
Followed by a number to adjust the size of the pane <br>
![resize-pane](resize_pane.png)

Switching between panes:
- `Ctrl + b + <arrow-key>` : Switch to the specified pane
- `Ctrl + b + q` : Display a number on each pane
    - `Ctrl + b + q + <number>` : Switch to the specified pane

![pane ls](pane_ls.png)
