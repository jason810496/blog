# Makefile for hugo site
dev:
	hugo server
.PHONY: dev

build:
	hugo
.PHONY: build

new:
	if [ -z "$(POST)" ];then echo "Usage: make new POST=my-post-name"; exit 1; fi
	hugo new content content/${POST}.md
.PHONY: new