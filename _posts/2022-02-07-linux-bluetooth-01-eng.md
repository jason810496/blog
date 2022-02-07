---
title: Connect bluetooth device on Linux
subtitle: connect airpods on Ubuntu OS 
date:   2022-02-07 19:45:00 +0800

tag: [linux,note,eng]

thumbnail-img: "https://i.imgur.com/VIQ7IAF.png" #1:1 (450:450)

cover-img: "https://i.imgur.com/rYVwo4W.png"

#For blog posts, if you want to add a thumbnail that will show up in the feed, use thumbnail-img: /path/to/image. If no thumbnail is provided, then cover-img will be used as the thumbnail. You can use thumbnail-img: "" to disable a thumbnail.
comments: true

# ======= Other parameters ========
layout: post
readtime: true

# test local : bundle exec kyll serve
---
# How to connect airpods on Ubuntu OS

{: .box-note}
**auther:** It's quite eazy , but I forget to push the setup button while connecting to PC  , which makes me confused for a afternoon LOL ... 

## UI interface 

{: .box-error}
**Hint:** Make sure push the setup button on the back of charging case until the status light flash white !

**1. open bluetooth setting on your laptop**

**2. make sure status light flash white while connecting airpods**

**3. connect your airpods!**

![ui-result](https://i.imgur.com/tBAtKyS.png){: .mx-auto.d-block :}

## Command line

As an Linux user , using UI interface 

to connect bluetooth devices is unacceptable (IJK 😂

Overall , connecting airpods in command line is coooool !!! 😎

### bluez

[**BlueZ**](http://www.bluez.org/) is the official Linux Bluetooth stack. It provides, in it's modular way, support for the core Bluetooth layers and protocols. 

#### install bluez on Ubuntu

```shell
sudo apt install bluez 
```
#### using **bluetoothctl** to manage bluetooth devices

run `bluetoothctl` in terminal
```shell
bluetoothctl
```

result :

![terminal-result](https://i.imgur.com/yHJRh2M.png){: .mx-auto.d-block :}

Ask what it can do ! 👉 Run `help` command

![terminal-help](https://i.imgur.com/aY4kIYW.png)


To connect our headset , we need to first **scan** all the devices nearby , **find** our device ,**pair** the headset and PC, and **connect** it.


{: .box-note}
**Note:** the `[dev]` below means the MAC address of device

MAC address :

MAC address of my headset is **4C:B9:10:47:C4:DD** , MAC address of your device might in form of **XX:XX:XX:XX:XX:XX** . Every device has a unique MAC (Hovever , you can change it through software )

#### command:
* **`exit`**
 It's essential to know how to quit (especially in Vim 😈 )

* **`deivices`**
 List available devices

* **`pair [dev]`**
 Pair with device

* **`paired-deivces`**
 List paired devices

* **`connect [dev]`**
 Connect device

* **`disconnect [dev]`**
 Disconnect device

connect airpods through command line :
![final-result](https://i.imgur.com/t9P8HAu.png)

enjoy your music 🎧 

recommended song : [1.5 hr study lofi ](https://music.youtube.com/watch?v=T7GvvbD6S2Y&list=RDAMVMT7GvvbD6S2Y)

##### reference
[https://www.makeuseof.com/manage-bluetooth-linux-with-bluetoothctl/](https://www.makeuseof.com/manage-bluetooth-linux-with-bluetoothctl/)
[https://ubuntu.com/core/docs/bluez/install-configure/install](https://ubuntu.com/core/docs/bluez/install-configure/install)
[https://unix.stackexchange.com/questions/96693/connect-to-a-bluetooth-device-via-terminal](https://unix.stackexchange.com/questions/96693/connect-to-a-bluetooth-device-via-terminal)





