---
title: 288th LeetCode Weekly Contest
subtitle: Leetcode 288th 週賽
date:   2022-04-10 15:50:00 +0800

tag: [c++/c,notes,Leetcode]

thumbnail-img: "https://i.imgur.com/n6yKZDY.png" #1:1 (450:450)

cover-img: "https://i.imgur.com/Zp6EhUO.png"

comments: true

# ======= Other parameters ========
layout: post
readtime: true

# test local : bundle exec jekyll server
---
# 288th LeetCode Weekly Contest

[288th LeetCode Weekly Contest](https://leetcode.com/contest/weekly-contest-288)

真的太久沒有解題打程競，今天只有解出一題...

在補題目發現其實精神分數有**三題**

第二題實做到一半就不寫了（因為忘記有`substr`這種好東西，被字串操作搞瘋）

第三題只是忘記開`long long`...


**這次週賽的四個題目：**

- [Largest Number After Digit Swaps by Parity](https://leetcode.com/contest/weekly-contest-288/problems/largest-number-after-digit-swaps-by-parity/)

- [Minimize Result by Adding Parentheses to Expression](https://leetcode.com/contest/weekly-contest-288/problems/minimize-result-by-adding-parentheses-to-expression/)

- [Maximum Product After K Increments](https://leetcode.com/contest/weekly-contest-288/problems/maximum-product-after-k-increments/)

- [Maximum Total Beauty of the Gardens](https://leetcode.com/contest/weekly-contest-288/problems/maximum-total-beauty-of-the-gardens/)

## Largest Number After Digit Swaps by Parity3

[Largest Number After Digit Swaps by Parity](https://leetcode.com/contest/weekly-contest-288/problems/largest-number-after-digit-swaps-by-parity/)

### Description:

```
You are given a positive integer num. You may swap any two digits of num that have the same parity (i.e. both odd digits or both even digits).

Return the largest possible value of num after any number of swaps.
```

### example:

```
Input: num = 1234
Output: 3412
Explanation: Swap the digit 3 with the digit 1, this results in the number 3214.
Swap the digit 2 with the digit 4, this results in the number 3412.
Note that there may be other sequences of swaps but it can be shown that 3412 is the largest possible number.
Also note that we may not swap the digit 4 with the digit 1 since they are of different parities.
```

簡單來說，你可以對input中**相同性質**(這邊指的是都是**奇數**或都是**偶數**)的數字進行交換，要求經過交換後(也有可能不需要交換)可以達到的**最大值**

### Concept：

所以，我們可以將input中的數字分為：`Odd`跟`Even`

又因為`Odd`只能跟`Odd`換，`Even`只能跟`Even`換

為了達到最大值，勢必要將**大的數字擺在小的數字前面**

## Solution：

將input拆成`Odd`跟`Even`，各自**sort**之後再組合成Answer

**Solution**

```cpp
class Solution {
public:
    int largestInteger(int num) {
        vector<int> orig(0) ;
        vector<int> Odd(0) , Even(0);
        int n;
        while(num){
            int v = num%10;
            int Type =num%2;
            if(Type){
                Odd.push_back(-v);
            }
            else{
                Even.push_back(-v);
            }
            orig.push_back(Type);
            num/=10;
        }
        sort(Odd.begin() , Odd.end());
        sort(Even.begin() , Even.end());
        
        n= orig.size();
        reverse(orig.begin() , orig.end());

        int Ans=0;
        int I=0,J=0;

        for(int t : orig){
            Ans*=10;
            if( t ){
                Ans-=Odd[I++];
            }
            else{
                Ans-=Even[J++];
            }
            
        }
        return Ans;
    }
};
```

其中將每一位數字`push_back`到`vector`中的時候，我將數字乘一個**負號**，因為`algorithm`預設是小大到排序，而**負號**可以取代`compare function`的作用（但sort完記得再取一次負號將數字轉正）

當然sort的部份可以寫成`counting sort`，但是範圍不大用一般的sort也不會差太多。

## Minimize Result by Adding Parentheses to Expression 

[Minimize Result by Adding Parentheses to Expression](https://leetcode.com/contest/weekly-contest-288/problems/minimize-result-by-adding-parentheses-to-expression/)

### Description:

```
You are given a 0-indexed string expression of the form "<num1>+<num2>" where <num1> and <num2> represent positive integers.

Add a pair of parentheses to expression such that after the addition of parentheses, expression is a valid mathematical expression and evaluates to the smallest possible value. The left parenthesis must be added to the left of '+' and the right parenthesis must be added to the right of '+'.

Return expression after adding a pair of parentheses such that expression evaluates to the smallest possible value. If there are multiple answers that yield the same result, return any of them.

The input has been generated such that the original value of expression, and the value of expression after adding any pair of parentheses that meets the requirements fits within a signed 32-bit integer
```

### example:

**Example 1:**
```
Input: expression = "247+38"
Output: "2(47+38)"
Explanation: The expression evaluates to 2 * (47 + 38) = 2 * 85 = 170.
Note that "2(4)7+38" is invalid because the right parenthesis must be to the right of the '+'.
It can be shown that 170 is the smallest possible value.
```
**Example 3:**
```
Input: expression = "12+34"
Output: "1(2+3)4"
Explanation: The expression evaluates to 1 * (2 + 3) * 4 = 1 * 5 * 4 = 20.
```

**Example 3:**
```
Input: expression = "999+999"
Output: "(999+999)"
Explanation: The expression evaluates to 999 + 999 = 1998.
```

將括號插入運算式中，並求出插入後運算結果最小值的運算式

### Concept：

雖然當時沒有寫出來，不過那時候的解題思路算是對的（字串操作的部份一直寫爛）

可以將第一個數字（叫第一個數字`A`）和第二個數字（叫第二個數字`B`）都各拆成兩半如：

題目：`"247+38"`

247:
```
247 0
24 7
2 47
0 247
```
38:
```
38 0
3 8
0 38
```

而題目要求的就是：
```
A第一部份*( A第二部份 + B第一部份 ) * B第二部份
```

所以將兩個數字都拆成兩個部份後，再經過兩層for迴圈枚舉就好了

還有記得`A第一部份`或`B第二部份`為`0`時要改成`1`下去乘
## Solution：

當時因為實做一直爛掉，而且沒有用**`substr`**這種好用的工具，一開始就將`string`轉成`vector<int>`，最後才看到答案是要`string`就~~崩潰不寫了~~

在賽後還是有實做出來，不過真的寫的又臭又長...
**Solution**

沒用`substr`或`atoi`寫出來的版本：

```cpp
class Solution {
public:

    string to_str(int n){
        string res;
        while(n){
            res+=char(n%10+'0');
            n/=10;
        }
        reverse(res.begin(),res.end());
        return res;
    }
    string minimizeResult(string expression) {
        vector<int> numA,numB;
        bool f= false;

        for(char i:expression){
            if(i=='+'){
                f=true;
                continue;
            }
            if(f){
                numB.push_back(i-'0');
            }
            else{
                numA.push_back(i-'0');
            }
        }
        vector< pair<int,int> > vecA , vecB;
        int nA = numA.size()  ,nB = numB.size();

        for(int i=nA; i>=0 ;i--){
            int j=0,Front=0,Back=0;
            for(;j<i;j++){
                Front*=10;
                Front+=numA[j];
            }

            for(;j<nA;j++){
                Back*=10;
                Back+=numA[j];
            }
            vecA.push_back( {Front,Back} );
        }

        for(int i=nB; i>=0 ;i--){
            int j=0,Front=0,Back=0;
            for(;j<i;j++){
                Front*=10;
                Front+=numB[j];
            }

            for(;j<nB;j++){
                Back*=10;
                Back+=numB[j];
            }
            vecB.push_back( {Front,Back} );
        }
        

        int Ans = INT_MAX;
        string Result;
        for(int i=0;i<vecA.size();i++){
            for(int j=0;j<vecB.size();j++){
                auto A = vecA[i];
                auto B = vecB[j];
                int A_Front =  (A.first==0 ? 1:A.first);
                int A_Back = A.second;
                int B_Front = B.first;
                int B_Back = (B.second==0 ? 1:B.second);

                if( A_Back==0 || B_Front==0) continue;
                int res = A_Front*( A_Back + B_Front )*B_Back;
                
                if( res<Ans){
                    Ans=res;
                    Result=(A.first==0 ? "":to_str(A_Front))+"("+to_str(A_Back)+"+"+to_str(B_Front)+")"+(B.second==0 ? "":to_str(B_Back));
                }
            }
        }


        cout<<Ans<<'\n';
        return Result;
    }
};

```

簡潔很多的版本：
```cpp
class Solution {
public:
    int to_int(string str){
        int ret=0;
        for(char i:str){
            ret*=10;
            ret+=int(i-'0');
        }
        return ret;
    }
    string minimizeResult(string exp) {
        int exp_len = exp.size();
        int add_idx = 0;
        for(char i:exp){
            if(i=='+'){
                break ;
            }
            add_idx++;
        }
        
        string numA = exp.substr(0,add_idx);
        string numB = exp.substr(add_idx+1 , exp_len-add_idx);

        cout<<numA<<' '<<numB;
        int nA = numA.size()  ,nB = numB.size();

        vector<pair<string,string> > vecA , vecB;

        for(int i=0;i<=nA;i++){
            vecA.push_back( {numA.substr(0,i) , numA.substr(i,nA-i)} );
        }

        for(int i=0;i<=nB;i++){
            vecB.push_back( {numB.substr(0,i) , numB.substr(i,nB-i)} );
        }

        int n = vecA.size() , m = vecB.size();

        int Min = INT_MAX;
        string Ans;
        for(auto i:vecA){
            for(auto j:vecB){
                if( i.second=="" || j.first=="") continue;

                int A_Front = (i.first=="" ? 1:to_int(i.first));
                int A_Back = to_int(i.second);
                int B_Front = to_int(j.first);
                int B_Back = (j.second=="" ? 1:to_int(j.second));
                int cur = A_Front*(A_Back+B_Front)*B_Back;

                if( cur < Min){
                    Min=cur;
                    Ans=i.first+"("+i.second+"+"+j.first+")"+j.second;
                }
            }
        }
        return Ans;
    }
};

```

## Maximum Product After K Increments

- [Maximum Product After K Increments](https://leetcode.com/contest/weekly-contest-288/problems/maximum-product-after-k-increments/)

### Description :
```
You are given an array of non-negative integers nums and an integer k. In one operation, you may choose any element from nums and increment it by 1.

Return the maximum product of nums after at most k operations. Since the answer may be very large, return it modulo 109 + 7.
```

### Exmample:

**Example 1:**
```
Input: nums = [0,4], k = 5
Output: 20
Explanation: Increment the first number 5 times.
Now nums = [5, 4], with a product of 5 * 4 = 20.
It can be shown that 20 is maximum product possible, so we return 20.
Note that there may be other ways to increment nums to have the maximum product.
```

**Example 2:**
```
Input: nums = [6,3,3,2], k = 2
Output: 216
Explanation: Increment the second number 1 time and increment the fourth number 1 time.
Now nums = [6, 4, 3, 3], with a product of 6 * 4 * 3 * 3 = 216.
It can be shown that 216 is maximum product possible, so we return 216.
Note that there may be other ways to increment nums to have the maximum product.
```

可以進行`K`次操作，每次操作都可以將任意的元素`+1`。

要求進行完K次操作後，所有元素的**乘積**（並`mod 1e9+7`）

### Concept：

一看到題目的時候就很**Greedy**的想：「總共可以加K次，那就每次都抓出最小的來加！」

要可以動態的插入資料，而且取出的資料都是最小值的資料結構...

也只有`priority_queue`了！( 這邊指的是Min Heap )

但是為什麼這樣會是乘積最大值？（~~我也不會證明~~）
### Solution:

結果打比賽時忘記開`long long`...

```cpp
class Solution {
public:
    int maximumProduct(vector<int>& nums, int k) {
        priority_queue<int,vector<int> ,greater<int> > pq;
        long long Mod = 1e9+7;
        for(const int i : nums){
            pq.push(i);
        }

        while(k--){
            int v = pq.top();
            pq.pop();
            pq.push( v+1);
        }

        long long ans=1;
        while(pq.size()){
            ans=( ans*pq.top() )%Mod;
            pq.pop();
        }

        return int(ans);
    
    }
};
```

而將所有`nums`的元素丟入`priority_queue`的部份可以這樣初始化（看別人的code看到的）

```cpp

priority_queue<int,vector<int> ,greater<int> > pq( nums.begin() , nums.end() );
```



## Maximum Total Beauty of the Gardens 

[Maximum Total Beauty of the Gardens](https://leetcode.com/contest/weekly-contest-288/problems/maximum-total-beauty-of-the-gardens/)

### Description :
Alice is a caretaker of n gardens and she wants to plant flowers to maximize the total beauty of all her gardens.

You are given a 0-indexed integer array flowers of size n, where flowers[i] is the number of flowers already planted in the ith garden. Flowers that are already planted cannot be removed. You are then given another integer newFlowers, which is the maximum number of flowers that Alice can additionally plant. You are also given the integers target, full, and partial.

A garden is considered complete if it has at least target flowers. The total beauty of the gardens is then determined as the sum of the following:

- The number of complete gardens multiplied by full.
- The minimum number of flowers in any of the incomplete gardens multiplied by partial. If there are no incomplete gardens, then this value will be 0.

Return the maximum total beauty that Alice can obtain after planting at most newFlowers flowers.

### Example:

```
Input: flowers = [1,3,1,1], newFlowers = 7, target = 6, full = 12, partial = 1
Output: 14
Explanation: Alice can plant
- 2 flowers in the 0th garden
- 3 flowers in the 1st garden
- 1 flower in the 2nd garden
- 1 flower in the 3rd garden
The gardens will then be [3,6,2,2]. She planted a total of 2 + 3 + 1 + 1 = 7 flowers.
There is 1 garden that is complete.
The minimum number of flowers in the incomplete gardens is 2.
Thus, the total beauty is 1 * 12 + 2 * 1 = 12 + 2 = 14.
No other way of planting flowers can obtain a total beauty higher than 14.
```

### Concept:

比賽時感覺有點DP，但是完全沒有頭緒

也還沒看懂

解法待補...