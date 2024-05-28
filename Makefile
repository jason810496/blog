# Makefile for hugo site
dev:
	hugo server
.PHONY: dev

build:
	hugo
.PHONY: build

new-en:
	if [ -z "$(POST)" ];then echo "Usage: make new-en POST=my-post-name"; exit 1; fi
	# create directory if not exists
	if [ ! -d "content/${POST}" ];then mkdir content/${POST}; fi
	# check if the post exists
	if [ -f "content/${POST}.en.md" ];then echo "The post ${POST}.en.md already exists"; exit 1; fi
	hugo new --kind post-en content/${POST}/index.en.md
.PHONY: new-en

new-zh:
	if [ -z "$(POST)" ];then echo "Usage: make new-zh POST=my-post-name"; exit 1; fi
	# create directory if not exists
	if [ ! -d "content/${POST}" ];then mkdir content/${POST}; fi
	# check if the post exists
	if [ -f "content/${POST}.zh-tw.md" ];then echo "The post ${POST}.zh-tw.md already exists"; exit 1; fi
	hugo new --kind post-zh-tw content/${POST}/index.zh-tw.md
.PHONY: new-zh

new: new-en new-zh
.PHONY: new

rm:
	if [ -z "$(POST)" ];then echo "Usage: make rm POST=my-post-name"; exit 1; fi
	rm -r content/${POST}
.PHONY: rm