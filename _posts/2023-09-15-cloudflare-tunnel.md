---
title: 設定 Cloudflare Tunnel 
subtitle: Ngrok 的替代方案
date:   2023-09-15 16:00:00 +0800

tag: [notes]

thumbnail-img: "https://raw.githubusercontent.com/jason810496/blog/main/_images/20230915_tunnel.png" #1:1 (450:450)

cover-img: "https://raw.githubusercontent.com/jason810496/blog/main/_images/20230915_start_tunnel.png"

comments: true

# ======= Other parameters ========
layout: post
readtime: true

# test local : bundle exec jekyll serve
---

## 前言

目前擔任程式設計（一）助教 <br>
因為實習課教室電腦的 IP 都是內網 IP <br>
然後系上  Online Judge 的 VM 只給學校 IP ( `140.116.xxx.xxx` ) 進來 <br>
沒有開放內網 IP 進來 <br>

原本用 [ngrok](https://ngrok.com/) 來做 NAT <br>
但是 ngrok 的免費版每個 tunnel 只給 40 人用 <br>
修課人數有 240 多個人 <br>
不太可能開 6 個 tunnel 再分配學生連線<br>
> 這樣非常麻煩... <br>
> 而且每次 ngrok 重啟都會換一個新的 domain <br>
> 這樣學生要重新設定連線的 domain <br>

## ngrok 的替代方案

[Cloudflare Tunnel](https://developers.cloudflare.com/cloudflare-one/connections/connect-apps) <br>

`Cloudflare Tunnel` Free Plan 的 : <br>
- dns setup 
- no connection limitation ( name server 要在 Cloudflare 上 )
- 其他與 ngrok 一樣

## cloudflare tunnel  文件

[https://developers.cloudflare.com/pages/how-to/preview-with-cloudflare-tunnel/](https://developers.cloudflare.com/pages/how-to/preview-with-cloudflare-tunnel/)

### Installtion

可以到[Cloudflare Tunnel Downloads](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/)找適合自己的 OS 的版本 <br>

Mac OS :
```bash
brew install cloudflare/cloudflare/cloudflared
```

Linux : 
```bash
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
sudo apt install ./cloudflared-linux-amd64.deb
```

## Normal Usage

如果是 ngrok : 
```bash
ngrok http 8888
```

如果是 cloudflare tunnel :
```bash
cloudflared tunnel --url http://localhost:8888
```

![start tunnel](https://raw.githubusercontent.com/jason810496/blog/main/_images/20230915_start_tunnel.png)

就可以從隨機生成 URL 連線到 `localhost:8888` 了 <br>
但是如果要自己設定 domain 的話，就要額外設定 `cloudflared` 的 config file <br>

## Advanced Usage

**在設定 domain 前，要確認 domain 的 Nameserver 是設定在 Cloudflare 上** <br>
> 設定完後：可以從自己的 DNS 連到 server 的 `localhost:<port>`

接著可以使用 command line 來設定 `cloudflared` 的 config file <br>

- Authentication
    ```bash
    cloudflared tunnel login
    ```
- Create a Tunnel
    ```bash
    cloudflared create <tunnel_name>
    ```
    ```bash
    cloudflared tunnel route dns <tunnel_name> <domain_name>
    ```
    會在 `~/.cloudflared/` 產生一個 `<tunnel_id>.json`


可以在 [cloudflare dashboard ](https://one.dash.cloudflare.com/) 中 `Access` 的 `tunnel` 看到 `<tunnel_id>` <br>
![access tunnel](https://raw.githubusercontent.com/jason810496/blog/main/_images/20230915_access_tunnel.png)

在 `DNS` 的 `records` 看到加上的 `<domain_name>` <br>
`content` 的部分是 `<tunnel_id>.cfargotunnel.com` <br>
![dns records](https://raw.githubusercontent.com/jason810496/blog/main/_images/20230915_dns_check.png)

### configuation

[cloudflare tunnel : setup configuration file](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/install-and-setup/tunnel-guide/local/local-management/configuration-file/)

接著在 `~/.cloudflared/` 中加上 `config.yaml` <br>
```yaml
tunnel: <tunnel-id>
credentials-file: /path/to/<tunnel-id>.json # 之前產生的 json file 在 ~/.cloudflared/ 中
ingress:
  - hostname: <domain-name>
    service: http://localhost:<port1>
  - service: http_status:404
```


在設定 `config.yaml` 的時候，可以設定多個 `ingress` <br>
這樣就可以把不同的 port 對應到不同的 domain <br>
> 例如 :
> - `localhost:8888` 對應到 `service1.domain.com`
> - `localhost:9999` 對應到 `service2.domain.com`

## Start Tunnel

啟動 tunnel :
```bash
cloudflared tunnel run <tunnel_name>
```

可以透過 `tmux` 讓 tunnel 在背景執行 <br>
可以參考 [tmux 常用指令](https://jason810496.github.io/blog/tmux/) !<br>

使用 `tmux` :

```bash
tmux new -s cloudflare-tunnel
```

然後在 `tmux` 中執行 `cloudflared tunnel run <tunnel_name>` <br>
按下 `ctrl + b` 再按 `d` 就可以離開 `tmux` <br>

如果要回到 `tmux` 中的話，可以用 `tmux attach -t cloudflare-tunnel` <br>

## Command list

- `cloudflared tunnel login`
- `cloudflared create <tunnel_name>`
- `cloudflared tunnel route dns <tunnel_name> <domain_name>` <br>
    > 會在 `~/.cloudflared/` 產生一個 `<tunnel_id>.json` 並在這邊加上 `config.yaml` <br>
    > 在 [cloudflare dashboard ](https://one.dash.cloudflare.com/) 中 `Access` 的 `tunnel` 可以看到 `<tunnel_id>`
- `cloudflared tunnel run <tunnel_name>`

## Reference

- [Cloudflare Tunnel : Overview](https://developers.cloudflare.com/cloudflare-one/connections/connect-apps)
- [Cloudflare Tunnel : Downloads](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/)
- [Cloudflare Tunnel : Setup configuration file](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/install-and-setup/tunnel-guide/local/local-management/configuration-file/)
- [Cloudflare Tunnel : Ingress](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/install-and-setup/tunnel-guide/local/local-management/ingress/)