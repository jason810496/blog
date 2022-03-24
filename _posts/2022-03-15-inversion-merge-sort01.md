---
title: 逆序數對(Array Inversion)
subtitle: Merge sort 順便計算逆序數對
date:   2022-03-024 19:08:00 +0800

tag: [algorithm,note]

thumbnail-img: "https://i.imgur.com/Kxil1A3.png"

cover-img: "/assets/img/markdown-turtorial-bg01.png"


comments: true

# ======= Other parameters ========
layout: post
readtime: true

# test local : bundle exec jekyll server
---

# 逆序數對

在Merge sort的時候計算逆序數對

先來觀察Merge sort 的過程：

1. 分治 
一直重複從中點把陣列切成兩半直到子陣列剩單個元素
2. 合併

我覺得Merge sort 的關鍵就在**Merge**的過程

用圖演示Merge sort都無法把Merge 的精髓畫出來

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
