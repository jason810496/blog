---
title: "2025 06 29 Vm Setup"
summary: ""
description: ""
date: 2025-06-29T15:51:17+08:00
slug: "vm-setup"
tags: ["blog","zh-tw"]
# series: ["Documentation"]
# series_order: 9
cascade:
  showEdit: true
  showSummary: true
  hideFeatureImage: false
draft: false
---

## Linux

New User
```bash
# create a new user
sudo adduser jason
# add user to sudo group
sudo usermod -aG sudo jason
# switch to the new user
su - jason
```

Common tools
```bash
sudo apt update
# common tools
sudo apt install -y \
  curl \
  wget \
  git \
  vim 
```

zsh & oh-my-zsh
```bash
sudo apt install -y zsh
# install oh-my-zsh
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
# p10k theme & autosuggestions
git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/themes/powerlevel10k
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
```

`~/.zshrc` Setup
```bash
# ...
ZSH_THEME="powerlevel10k/powerlevel10k"
# ...
plugins=( git zsh-autosuggestions docker docker-compose kubectl zsh-pre-commit-autocomplete)
```

Python tools
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

kubernetes tools