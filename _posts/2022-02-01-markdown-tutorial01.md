---
title: Markdown 語法測試
subtitle: check markdown syntax on site
date:   2022-02-01 22:52:00 +0800

tag: [markdown,note]

thumbnail-img: "/assets/img/markdown-img02.png" #1:1 (450:450)

cover-img: "/assets/img/markdown-turtorial-bg01.png"

#For blog posts, if you want to add a thumbnail that will show up in the feed, use thumbnail-img: /path/to/image. If no thumbnail is provided, then cover-img will be used as the thumbnail. You can use thumbnail-img: "" to disable a thumbnail.
comments: true

# ======= Other parameters ========
layout: post
readtime: true

# test local : bundle exec jekyll serve
---

# h1 heading

**粗體字**

- 條列式
- one
- another
- the other

*Italics font*

~~Strikethrough~~

這是^上標^

這是~下標~

==Marked text==

Table example :

| Number | Next number | Previous number |
| :------ |:--- | :--- |
| Five | Six | Four |
| Ten | Eleven | Nine |
| Seven | Eight | Six |
| Two | Three | One |


Code with syntax highlighting:

```cpp
#define int long long 
#define INF 1e9

singed main(){

    priority_queue<int> pq;
    cout<<"112 to 112 ?!";
    return 0;
}
```

- [ ] Todo List
- [ ] a Blog a day
- [ ] solving a problem a day
- [ ] participate a contest a week



### Notification

{: .box-note}
**Note:** This is a notification box.

### Warning

{: .box-warning}
**Warning:** This is a warning box.

### Error

{: .box-error}
**Error:** This is an error box.