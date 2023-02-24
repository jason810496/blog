---
title: System Adminstration - Install FreeBSD&Application
subtitle: Install FreeBSD on MacOS
date:   2023-02-23 14:00:00 +0800

tag: [SA,linux,notes]

thumbnail-img: "https://i.imgur.com/E9EPS9o.png" #1:1 (450:450)

cover-img: "https://i.imgur.com/RpOgfcD.jpg"

# cover-img : "https://i.imgur.com/Gmrglpd.jpg"

comments: true

# ======= Other parameters ========
layout: post
readtime: true

# test local : bundle exec jekyll serve
---


## FreeBSD installation ( macOS )
### Install FreeBSD on macOS
**Install FreeBSD using `parallels desktop`**
- FreeBSD IOS 13.1 list : https://download.freebsd.org/ftp/releases/arm64/aarch64/ISO-IMAGES/13.1/ 
-  [FreeBSD-13.1-RELEASE-arm64-aarch64-disc1.iso.xz (download link)](https://download.freebsd.org/ftp/releases/arm64/aarch64/ISO-IMAGES/13.1/FreeBSD-13.1-RELEASE-arm64-aarch64-disc1.iso.xz)

**`disc` vs `did`**

https://forums.freebsd.org/threads/difference-between-disc-1-and-dvd-1.54329/

**Add new VM on `parallels desktop`**

1. navigate to controll panel and select `add new VM`
![](https://i.imgur.com/psOYyxX.png)
2. continue
![](https://i.imgur.com/unYkfC2.png)
3. create new VM from ISO file
![](https://i.imgur.com/5Uqrek1.png)
4. continue step
![](https://i.imgur.com/xIPiGQ5.png)
![](https://i.imgur.com/2J77zlM.png)
5. ignore alert and select **`other OS`** (**not other linux**)
![](https://i.imgur.com/BvEEWLJ.png)

**Install FreeBSD**

refernce to : [NYCU NASA `install FreeBSD` pdf ](https://nasa.cs.nycu.edu.tw/sa/2022//slides/01_Install_FreeBSD.pdf)

**ssh into FreeBSD ( login to FreeBSD via macOS terminal )**

1. type `ifconfig` command to check current device IP
![](https://i.imgur.com/Na3JHTB.png)
2. ssh into FreeBSD just like logging into other VPS
![](https://i.imgur.com/BQYJWRs.png)
3. successful login
![](https://i.imgur.com/DtAVQsJ.png)

### Homework

**prerequisites**
- judge user & group setting
![](https://i.imgur.com/XwP2TO3.png)
- wireGuard VPN
![](https://i.imgur.com/49ca2bO.png)

**homework**
![](https://i.imgur.com/9O3WrjZ.png)

#### General task
- **SSH Public Key and judge User** : 
The task is to setup correct ssh configuration so that judge server could ssh into our VM as `judge` user to test our evironment setting .
The `public key` could be download from OJ( online judge ) , then we have to copy `public key` from our local workspace ( macOS for me ) to FreeBSD VM ( which also can be seen as remote server )

By using `ssh-copy-id` or `scp` command , the `public key` can be sent to VM .
Another solutiuon is using `curl` command to dowdload `public key` directly from OJ .
As for configuration file of `wiredGuard` can be sent to VM via `scp` command . ( or using `curl` )

- **Install FreeBSD 13.1-RELEASE and apply the security patch** : 
After installing FreeBSD , run `freebsd-version` would get `13.1-RELEASE` as result ( without `p7` tag after ) , so we have to update the system to latest patch . By running `freebsd-update fetch install` command to get latest patch . 
- **Time Zone** : 
Time Zone have already setup during `bsdintall` 
![](https://i.imgur.com/LmrMCfJ.png)
![](https://i.imgur.com/6ckwR95.png)

#### User & Group task
Using `adduser` ( user must have `root` user's credential ) to create new user and also setting user's group meanwhile .

For the requirement of `judge user could run sudo command without password` , we have to config `sudoer` file . ( user must have `root` user's credential )

1. Using `visudo` command : 
config `sudoer` file directly via `vi` editor
![](https://i.imgur.com/1V51Gk2.png)
2. Edit `sudoer` file via `vim` : 
The default `sudoer` file is located at `/usr/local/etc/sudoers` , so we could edit `sudoer` file using `vim` instead of `vi` ( which is more easy to use ) .
![](https://i.imgur.com/HuXMivH.png)


#### WireGuard
Copy the configuration file into `/usr/local/etc/wireguard/` using `scp`.
And start VPN tunnel using `wg-quick` command.
![](https://i.imgur.com/lVqCi4t.png)



https://www.wireguard.com/install/#freebsd-kmod-userspace-go-tools

### commands
- `freebsd-update fetch install` : update system to latest patch version
- `shutdown -p now`
- `reboot`
- `su` : 
    - `su - USERNAME` : change to USERNAME ( the whole environment will change )
    - `su USERNAME` : change to USERNAME ( reserve some previous user information ) 
- `groups USERNAME` : check `USERNAME`'s groups
- `adduser`
- `rmuser`
- `pw group mod GROUP_NAME -m USERNAME` : add `USERNAME` user to `GROUP_NAME` group
- `visudo` : edit sudoer config file
    - sudoer file defult location : `/usr/local/etc/sudoers`
- `wg-quick`
    - `wg-quick up /path/to/file.conf`
    - `/usr/local/etc/wiredguard/vpnName.conf` ( defult config file location )
- `scp`
    - `scp /path/to/local-server/file User@Host:/path/to/remove-server/dir`
- `ssh-copy-id`
    - `ssh-copy-id -i /path/to/keyGenFile.pub User@Host`
- `service sshd restart`

#### Weird Bug ?

**Bug Situation:**
After setting up `wiredGuard` and `authorized_keys` , the judge server could `ping` VM but can't ssh into MV .

I have tried remove `.ssh/authorized_keys` and download `public key` from judge server serverl times , however the judge server still not can ssh into MV.

**Solution:**

My friend Owen remove the whole `.ssh` directory and create `.ssh` directory , copy `authorized_keys` then solve this condition . 




#### Reference

- [install FreeBSD on Mac M1 chip using UTM](https://opensourcedoc.com/freebsd/freebsd-on-utm/)
- [install FreeBSD on Mac M1 chip using VMware](https://hackmd.io/@nckunasa/FreeBSD_on_M1_Machine)
- [NYCU SA [install FreeBSD] ](https://nasa.cs.nycu.edu.tw/sa/2022//slides/02_Installing_Applications.pdf)
- [NYCU SA [install Applications] ](https://nasa.cs.nycu.edu.tw/sa/2022//slides/02_Installing_Applications.pdf)