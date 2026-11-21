---
title: "2025 06 29 on Prem Kubernetes Setup"
summary: ""
description: ""
date: 2025-06-29T14:57:37+08:00
slug: "on-prem-kubernetes-setup"
tags: ["blog","zh-tw"]
# series: ["Documentation"]
# series_order: 9
cascade:
  showEdit: true
  showSummary: true
  hideFeatureImage: false
draft: false
---

# Add User to sudo Group

```bash
# create a new user
sudo adduser jason
# add user to sudo group
sudo usermod -aG sudo jason
# switch to the new user
su - jason
```

## Tools

```bash
# common tools
sudo apt update
sudo apt install -y git \
  curl \
  vim

# docker (copy from https://docs.docker.com/engine/install/ubuntu/)
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl.sha256"
echo "$(cat kubectl.sha256)  kubectl" | sha256sum --check
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# uv python package manager
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Clone kubespray

```bash
# clone kubespray
git clone https://github.com/kubernetes-sigs/kubespray.git --depth=1 --branch release-2.28
cd kubespray
# install dependencies
uv venv --python 3.11 
source .venv/bin/activate
uv pip install -U -r requirements.txt
```

## Get Root without Password

```bash
sudo su -
# edit sudoers file
vim /etc/sudoers
# add the following line at the end
jason ALL=(ALL) NOPASSWD: ALL
```

`ctrl+o` then `enter` to save and `ctrl+x` to exit.

## Edit Inventory

```bash
# copy sample local inventory
cp -rfp inventory/local inventory/mycluster
# for multiple nodes, should copy `inventory/sample` instead

# edit inventory
vim inventory/mycluster/inventory.ini
# edit addons:
vim inventory/mycluster/group_vars/k8s_cluster/addons.yml
```


```bash
# run kubespray
ansible-playbook -i inventory/mycluster/inventory.ini cluster.yml -b -v --private-key ~/.ssh/id_rsa
```


https://medium.com/@leonardo.bueno/setting-up-a-kubernetes-cluster-with-kubespray-1bf4ce8ccd73