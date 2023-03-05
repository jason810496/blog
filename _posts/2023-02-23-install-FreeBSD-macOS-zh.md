---
title: 計算機系統管理 安裝 FreeBSD
subtitle: 在 MacOS 安裝 FreeBSD
date:   2023-02-24 14:00:00 +0800

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


## FreeBSD 安裝 ( macOS )
### 在 MacOS 安裝 FreeBSD
**使用 `parallels desktop` 來操作**
- FreeBSD 的 IOS 檔案 ( 13.1 版) 列表 : https://download.freebsd.org/ftp/releases/arm64/aarch64/ISO-IMAGES/13.1/ 
-  [FreeBSD-13.1-RELEASE-arm64-aarch64-disc1.iso.xz (download link)](https://download.freebsd.org/ftp/releases/arm64/aarch64/ISO-IMAGES/13.1/FreeBSD-13.1-RELEASE-arm64-aarch64-disc1.iso.xz)

**`disc` 與 `did` 檔名結尾的比較**

https://forums.freebsd.org/threads/difference-between-disc-1-and-dvd-1.54329/

**在 `parallels desktop` 新增 VM**

1. 先選擇`控制中心`再選擇`創建一個虛擬機器`
![](https://i.imgur.com/psOYyxX.png)
2.  選擇繼續
![](https://i.imgur.com/unYkfC2.png)
3. 點選右邊的，使用鏡像檔來創建機器
![](https://i.imgur.com/5Uqrek1.png)
4. 繼續步驟
![](https://i.imgur.com/xIPiGQ5.png)
![](https://i.imgur.com/2J77zlM.png)
5. 忽略警告並選擇 **`其他作業系統`** (**不是選其他 linux 系統**)
![](https://i.imgur.com/BvEEWLJ.png)

**安裝 FreeBSD**

可以參考 : [NYCU NASA `安裝 FreeBSD` pdf ](https://nasa.cs.nycu.edu.tw/sa/2022//slides/01_Install_FreeBSD.pdf)

**ssh 進入 FreeBSD ( 從 macOS 的終端機進入 FreeBSD VM )**

1. 輸入 `ifconfig` 指令來確認當前裝置被分配到的 IP
![](https://i.imgur.com/Na3JHTB.png)
2. ssh 進入 FreeBSD ( 跟登入其他 VPS 的步驟一樣 )
![](https://i.imgur.com/BQYJWRs.png)
3. 成功登入
![](https://i.imgur.com/DtAVQsJ.png)

### 作業

**預先設定**
- `judge` 用戶 & `group` 設定
![](https://i.imgur.com/XwP2TO3.png)
- wireGuard VPN
![](https://i.imgur.com/49ca2bO.png)

**功課說明**
![](https://i.imgur.com/9O3WrjZ.png)

#### General task
- **SSH Public Key and judge User** : 
需要正確設定好 ssh 讓測試主機端有辦法連進來剛剛設定好的 VM 來測試主機的環境是否都達到作業需求。

`public key` (公鑰) 可以從 OJ(測試主機端) 下載，所以我們必須要將下載在本地端( macOS 這邊)的公鑰複製到 FreeBSD VM 中 (這個步驟可以看成是要將公鑰複製到任一台遠端的主機中一樣)

可以使用 `ssh-copy-id` 或 `scp` 指令來將 `public key` 複製到 VM 中。

另一個解法是使用 `curl` 指令，直接從 OJ 下載 `public key` ( 就可以省去從本地端複製到遠端主機的步驟 )

至於 `wiredGuard` 的設定檔可以利用 `scp` 來複製到 VM 中 ( 同樣也可以利用 `curl` 指令來省去這個複製的步驟 ) 

- **Install FreeBSD 13.1-RELEASE and apply the security patch** : 
在安裝 FreeBSD 後, 執行 `freebsd-version` 應該會得到 `13.1-RELEASE`  ( 並沒右 `p7` 標籤在後面 ) , 所以我們必須將系統更新到最新的修補版本 . 執行 `freebsd-update fetch install` 指令就可以將系統更新到最新修補版本了 .

- **Time Zone** : 
在執行 `bsdintall` 時，應該就已經把時區的部分設定完了
![](https://i.imgur.com/LmrMCfJ.png)
![](https://i.imgur.com/6ckwR95.png)

#### User & Group task
使用 `adduser` 指令( 在執行這個指令時，當前的用戶必須要有 `root` 的權限 ) 來新建立用戶並設定群組。

至於 `judge user could run sudo command without password` ( judge 用戶不需要輸入密碼就可以執行 `sudo` 指令 ) 的要求 , 我們必須要更改 `sudoer` 的設定檔 . (  同樣的，在執行這個指令時，當前的用戶必須要有 `root` 的權限 )

1. 透過 `visudo` 指令 : 
從指令名稱就大概推的出來要如何使用了，`visudo`會直接開啟 `vi` 編輯器讓我們修改 `sudoer` 設定檔案
![](https://i.imgur.com/1V51Gk2.png)
2. 透過 `vim` 編輯器來修改 `sudoer` 設定檔 : 
預設的 `sudoer` 設定檔位於 `/usr/local/etc/sudoers` , 所以我們可以透過 `vim` 來修改 `sudoer` 設定檔 ( `vim` 顯然比 `vi` 好用多了 ) .
![](https://i.imgur.com/HuXMivH.png)


#### WireGuard
用 `scp` 指令複製設定檔到 `/usr/local/etc/wireguard/` 目錄 . 再透過 `wg-quick` 指令來開啟 VPN .
![](https://i.imgur.com/lVqCi4t.png)

可以從這邊參考如何安裝 wireguard : 
https://www.wireguard.com/install/#freebsd-kmod-userspace-go-tools

### commands
- `freebsd-update fetch install` : 將系統更新至最新修補版本
- `shutdown -p now`
- `reboot`
- `su` : 
    - `su - USERNAME` : 切換至 USERNAME 用戶 ( 整個環境都會套用 )
    - `su USERNAME` : 切換至 USERNAME 用戶 ( 有些原本用戶的環境會被保留 ) 
- `groups USERNAME` : 檢查 `USERNAME` 的群組
- `adduser`
- `rmuser`
- `pw group mod GROUP_NAME -m USERNAME` : 將 `USERNAME` 用戶(已經建立的) 加到 `GROUP_NAME` 群組
- `visudo` : 編輯 sudoer 設定檔
    - sudoer 設定檔預設路徑 : `/usr/local/etc/sudoers`
- `wg-quick`
    - `wg-quick up /path/to/file.conf` : 啟動 VPN 
    - `/usr/local/etc/wiredguard/vpnName.conf` ( 預設的設檔路徑 )
- `scp`
    - `scp /path/to/local-server/file User@Host:/path/to/remove-server/dir`
- `ssh-copy-id`
    - `ssh-copy-id -i /path/to/keyGenFile.pub User@Host`
- `service sshd restart`

#### 遇到的奇怪 Bug ?

**Bug 說明:**
在設定完 `wiredGuard` 和 `authorized_keys` 後，測試主機端有辦法 `ping` 到 VM 但沒有辦法 ssh 進入 VM

I have tried remove `.ssh/authorized_keys` and download `public key` from judge server serverl times , however the judge server still not can ssh into MV.

**解決:**

我朋友歐文，直接把整個整個 `.ssh` 資料夾刪除再重新創建並複 `authorized_keys` 就解決了 . 

目前也還沒搞清楚是哪個步驟造成的？




#### 參考資料

- [install FreeBSD on Mac M1 chip using UTM](https://opensourcedoc.com/freebsd/freebsd-on-utm/)
- [install FreeBSD on Mac M1 chip using VMware](https://hackmd.io/@nckunasa/FreeBSD_on_M1_Machine)
- [NYCU SA [install FreeBSD] ](https://nasa.cs.nycu.edu.tw/sa/2022//slides/02_Installing_Applications.pdf)
- [NYCU SA [install Applications] ](https://nasa.cs.nycu.edu.tw/sa/2022//slides/02_Installing_Applications.pdf)