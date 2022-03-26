---
title: C系列 void pointer之噩夢
subtitle: 搞了一整天的insertion sort QQ
date:   2022-03-11 15:50:00 +0800

tag: [c++/c,notes]

thumbnail-img: "https://i.imgur.com/Kxil1A3.png" #1:1 (450:450)

cover-img: "https://i.imgur.com/k0ouwUg.png"

comments: true

# ======= Other parameters ========
layout: post
readtime: true

# test local : bundle exec jekyll server
---

# 區區一個Insertion sort ...
接到一個單純實作出**Insertion sort**的case，原本預計10-20min解決掉，沒想到花了一整天QQ

題目： 作出一個通用類別的insertion sort function
```c

// InsertionSort algorithm for arrays of a generic type
// the function gets an array of length n of objects of given size
// it also get a compare function
// and sorts the array using the compare function

int Insertion_sort(void *arr , int n ,size_t s , int(*compare)(void *a,void *b)){

	/* implementation !*/
};
```

順帶一提，程式的作業評測方法也很酷，主要是寫在C的標頭檔(`algo.h` ,`algo.c`)，而確認程式正確性是直接寫在`main.c`( 也可能是大學大學作業都是這種形式 )
```shell
├── algo.c
├── algo.h
└── test.c

```

## generic sort function

通用性排序函式的必要參數：
- void pointer
- sizeof data type
- compare function

1. void pointer
`void pointer`可以裝入各種資料形態從 `int` ,`char` , `long long` 到`*int` , `*char` ,`*your_struct_type` 都可以，所以可以傳入各種資料形態的陣列。

2. sizeof data type
先備知識：

要知道`arr[i]`跟`arr[i+1`的memory address差`sizeof(data)` 

以`int arr_int[N]` 為例： `sizeof(int)` = `4 byte` ( `sizeof()`的return type是`size_t` )


```c++
for(int i=0;i<5;i++){
	cout<<&arr[i]<<'\n';
}
```
可以看到memory address都差4
```shell
0x7ffcfd869c30
0x7ffcfd869c34
0x7ffcfd869c38
0x7ffcfd869c3c
0x7ffcfd869c40
```

3. compare function

搭配data type 的compare function在主要的`Sort`函式判斷`arr[i]`,`arr[j]`的優先順序

## 實作 inertion sort

完整的sort function
```c
int Sort(void* arr, int n, size_t s, int (*compare)(const void*, const void*)) {
  
  int cnt=0 ;

  for(int i=1;i<n;i++){
    int j=i-1;
    char t[s];
    memcpy(t,arr+i*s,s);

    while(compare( t, (arr+j*s) )<0 && j>=0) {
      memcpy( (arr + s*(j+1)), (arr + s*j), s);
      memcpy(arr + s *s*j,temp, s);
      cnt++;
      j--;
    }
    memcpy((arr+(j+1)*s),t,s);
  }

  return cnt;
} 
```

call sort function :
```c
Sort(ar, len, sizeof(int), cmpr);
```

**實作細節**

- `char t[s]` : 

是暫存`arr[i]`的的變數,因為`char`是`1 byte` 所以 `char t[s]`剛好可以存一個`arr[i]`

- `arr+s*i` :

 要索引資料時，利用`arr[i]`與`arr[i+1]`差一個資料形態的大小的概念,所以原本`arr[i]`要寫成`arr+i*s`來索引
 
- `memcpy` : 

`memcpy`的用法 ：

把`pointer_2`的資料搬到`pointer_1`
```c
memcpy(pointer_1 , pointer_2 , sizeof(data) );
```


## Conclusion

因為實在是太不熟`pointer`了, 這個作業搞了超久

不過終於搞懂`void pointer`的用法ㄌ
