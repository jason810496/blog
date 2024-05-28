# Makefile for hugo site
dev:
	hugo server
.PHONY: dev

build:
	hugo
.PHONY: build

new-en:
	if [ -z "$(POST)" ];then echo "Usage: make new-en POST=my-post-name"; exit 1; fi
	hugo new --kind post-en content/${POST}.en.md
.PHONY: new-en

new-zh:
	if [ -z "$(POST)" ];then echo "Usage: make new-zh POST=my-post-name"; exit 1; fi
	hugo new --kind post-zh-tw content/${POST}.zh-tw.md
.PHONY: new-zh

new: new-en new-zh
.PHONY: new