---
title:  在linux連接藍芽裝置
subtitle: 如何在Ubuntu系統連接airopds? 
date:   2022-02-07 20:16:00 +0800

tag: [linux,note]

thumbnail-img: "https://i.imgur.com/VIQ7IAF.png" #1:1 (450:450)

cover-img: "https://i.imgur.com/rYVwo4W.png"

#For blog posts, if you want to add a thumbnail that will show up in the feed, use thumbnail-img: /path/to/image. If no thumbnail is provided, then cover-img will be used as the thumbnail. You can use thumbnail-img: "" to disable a thumbnail.
comments: true

# ======= Other parameters ========
layout: post
readtime: true

# test local : bundle exec kyll serve
---
# 如何在Ubuntu系統連接airpods


{: .box-note}
**我 :** 後來才發現超簡單ㄉ，其實是在連線的時候我沒有按著airpods充電盒子後面的按鈕才連不上 = = 害我搞了一個下午（怒 

## UI界面


{: .box-error}
**提示:** 記得先按著盒子後面的設定按鈕等它閃白燈時再連線！

**1. 打開電腦的藍芽設定** ( Ubuntu的界面很user friendly應該不會找不到ㄅ)

**2. 確認airpods充電盒的燈有閃白光**

**3. 從設定選取自己的裝置!**

![ui-result](https://i.imgur.com/tBAtKyS.png){: .mx-auto.d-block :}

## 終端機

身為linux使用者，用UI界面來連藍芽裝置~~太弱了~~（誤

無論如何，從終端機連上藍芽裝置超帥ㄉ😎(肯定是要在朋友面前秀一波操作！！

### bluez

[**BlueZ**](http://www.bluez.org/) 是官方 Linux Bluetooth 棧，由多層協定、服務以及配置工具組成。 ( from [https://www.easyatm.com.tw/wiki/BlueZ](https://www.easyatm.com.tw/wiki/BlueZ) )

#### 在Ubuntu安裝bluez

```shell
sudo apt install bluez 
```
#### 用 **bluetoothctl** 管理藍芽裝置

在終端機執行`bluetoothctl`
```shell
bluetoothctl
```

結果 :

![terminal-result](https://i.imgur.com/yHJRh2M.png){: .mx-auto.d-block :}

問它可以做什麼 ! 👉 執行 `help` 來詢問

![terminal-help](https://i.imgur.com/aY4kIYW.png)


要連接我們的耳機，我們要先 **scan**附近的所有裝置，**find**自己的裝置,**pair**耳機跟電腦,最後 **connect**它.


{: .box-note}
**Note:** 下方的 `[dev]` 都是指裝置的 MAC address

MAC地址：

我耳機的**MAC地址**是 **4C:B9:10:47:C4:DD** ，MAC第都指是以 **XX:XX:XX:XX:XX:XX** 的形式呈現. 每個裝置都有自己獨一無二的MAC (當然可以透過軟體修改)

#### 指令：
* **`exit`**
 知道如何退出是很重要的 ( 尤其是在Vim 😈 )

* **`deivices`**
 列出所有附近的裝置

* **`pair [dev]`**
 配對裝置

* **`paired-deivces`**
 列出配對過的裝置

* **`connect [dev]`**
 連接裝置

* **`disconnect [dev]`**
 與裝置取消連線

透過終端機連接airpods :
![final-result](https://i.imgur.com/t9P8HAu.png)

可以帥氣的聽音樂ㄌ 🎧 

推streetvoice上的歌 : [好暈好暈](https://streetvoice.com/konwang3/songs/666091/)

##### reference
[https://www.makeuseof.com/manage-bluetooth-linux-with-bluetoothctl/](https://www.makeuseof.com/manage-bluetooth-linux-with-bluetoothctl/)
[https://ubuntu.com/core/docs/bluez/install-configure/install](https://ubuntu.com/core/docs/bluez/install-configure/install)
[https://unix.stackexchange.com/questions/96693/connect-to-a-bluetooth-device-via-terminal](https://unix.stackexchange.com/questions/96693/connect-to-a-bluetooth-device-via-terminal)





