---
title: 在 M1 Mac 上安裝 Ubuntu VM
subtitle: Install Ubuntu VM on Mac M1 Chip
date:   2022-09-14 12:00:00 +0800

tag: [notes]

thumbnail-img: "https://i.imgur.com/hATMpxZ.jpg" #1:1 (450:450)

cover-img: "https://i.imgur.com/CIZ4dC0.jpg"

comments: true

# ======= Other parameters ========
layout: post
readtime: true

# test local : bundle exec jekyll serve
---

# 在 M1 Mac 上安裝 Ubuntu VM

## 前言
之前是用 Parallels Desktop 來安裝各個 OS 的 VM <br>
但今天一鍵安裝 Ubuntu 卻跳出奇怪的 Error <br>

看網路說要升級 Parallels Desktop 到最新版才能解 QQ
也順便來看一下有沒有其他免費的 VM 軟體可以用 <br>
( 目前 Parallels Desktop 有提供 14 天的試用期，但之後要付費使用 ！ )

## VMWare Fusion
所以改用 [VMWare Fusion](https://www.vmware.com/tw/products/fusion.html) 來安裝。 <br>
目前提供個人免費使用，只需要先申請帳號就可以下載使用了 <br>


## 尋找 Arm based 的 Ubuntu Desktop iso
因為 ubuntu [官方下載頁面](https://ubuntu.com/download/server/arm) 只有 Arm 的 **Server** 版本 <br>
但我們一般在用的都是 **Desktop** 版本 <br>

所以花了一些時間爬文在


和從[這個 Youtube Tutorial](https://www.youtube.com/watch?v=zDgSwcAOSq8&ab_channel=MikeShah)看到他
使用的是同一個載點 [ubuntu ios release : Jammy Jellyfish](https://cdimage.ubuntu.com/jammy/daily-live/current/) <br>

## 需要注意的地方

[askubuntu : offical arm desktop images](https://askubuntu.com/questions/1042696/are-there-official-ubuntu-arm-aarch64-desktop-images) 的問題中提到的剛剛的載點 <br>

[https://cdimage.ubuntu.com/jammy/daily-live/current/](https://cdimage.ubuntu.com/jammy/daily-live/current/) 

是**非官方**的，不過有提供 Daily Build 的版本 <br>
不過就沒辦法找到 LTS 版本了 <br>
( 如 18.04 LTS, 20.04 LTS 就找不到了 ) 

## 安裝過程

直接新增一個 VM 再掛上剛剛下載的 iso 就可以了 


開機之後是以 `ubuntu` user 的身份登入 <br>
已經設好 sudo 的權限，並且不需要打密碼

## VMWare Fusion 相關

滑鼠要跳脫 VM 的方式是 `control + command` <br>

## Build From Arm server image

## Remove additional packages

```bash
sudo apt-get remove --auto-remove gnome-calendar 
sudo apt-get remove --auto-remove libreoffice*
sudo apt-get remove --auto-remove thunderbird
sudo apt-get remove --auto-remove rhythmbox
sudo apt-get remove --auto-remove shotwell
sudo apt-get remove --auto-remove totem
sudo apt-get remove --auto-remove cheese
sudo apt-get remove --auto-remove gnome-mahjongg
sudo apt-get remove --auto-remove aisleriot
sudo apt-get remove --auto-remove gnome-mines
sudo apt-get remove --auto-remove gnome-sudoku
sudo apt-get remove --auto-remove gnome-todo
sudo apt-get remove --auto-remove gnome-weather
sudo apt-get remove --auto-remove remmina
sudo apt-get remove --auto-remove simple-scan
```




