---
title: 76th LeetCode Bi-Weekly Contest
subtitle: Leetcode 76th 週賽
date:   2022-04-17 1:30:00 +0800

tag: [c++/c,notes,Leetcode]

thumbnail-img: "https://i.imgur.com/n6yKZDY.png" #1:1 (450:450)

cover-img: "https://i.imgur.com/wcIo3iO.png"

comments: true

# ======= Other parameters ========
layout: post
readtime: true

# test local : bundle exec jekyll serve
---
# 76th LeetCode Bi-Weekly Contest

[76th LeetCode Weekly Contest](https://leetcode.com/contest/biweekly-contest-76)

上週週賽解出一題，在學校也有開始刷刷題（不過效率不高就是了，都是解daily challange或是tag是`dp`,`kth-element`的）


這次雙週賽解出**兩題**

第三題是水題，但是~~寫爛吃兩個WA就沒有再送了~~

第四題沒想法

精神分數**三題**

**這次雙週賽的四個題目：**

- [Find Closest Number to Zero](https://leetcode.com/contest/biweekly-contest-76/problems/find-closest-number-to-zero/)

- [Number of Ways to Buy Pens and Pencils](https://leetcode.com/contest/biweekly-contest-76/problems/number-of-ways-to-buy-pens-and-pencils/)

- [Design an ATM Machine](https://leetcode.com/contest/biweekly-contest-76/problems/design-an-atm-machine/)

- [Maximum Score of a Node Sequence](https://leetcode.com/contest/biweekly-contest-76/problems/maximum-score-of-a-node-sequence/)

## Find Closest Number to Zero

[Find Closest Number to Zero](https://leetcode.com/contest/biweekly-contest-76/problems/find-closest-number-to-zero/)

### Description:

Given an integer array `nums` of size `n`, return the number with the value **closest** to `0` in `nums`. If there are multiple answers, return the number with the **largest** value.

### example:

```
Input: nums = [-4,-2,1,4,8]
Output: 1
Explanation:
The distance from -4 to 0 is |-4| = 4.
The distance from -2 to 0 is |-2| = 2.
The distance from 1 to 0 is |1| = 1.
The distance from 4 to 0 is |4| = 4.
The distance from 8 to 0 is |8| = 8.
Thus, the closest number to 0 in the array is 1.
```

要找出陣列中**與0的差**的元素，如果有兩個元素距離0都一樣近則選**較大**的

### Concept：

`O(n)`掃過去，開三個變數紀錄：

之前最小的差：`dif`

當前最佳解：`ans`

計算當前元素與0的差：`cur`

並更新最小差，如果當前差（`cur`）與之前最小差（`dif`）相同，則選較大的`ans`

## Solution：

**Solution**

```cpp
class Solution {
public:
    int findClosestNumber(vector<int>& nums) {
        int dif=INF, ans=-INF;

        for(int i:nums){
            int cur = abs(i);
            if( cur < dif){
                ans=i;
                dif = cur;
            }
            else if( dif == cur && i>ans){
                ans = i;
            }
        }

        return ans;
    }
};
```

## Number of Ways to Buy Pens and Pencils

[Number of Ways to Buy Pens and Pencils](https://leetcode.com/contest/biweekly-contest-76/problems/number-of-ways-to-buy-pens-and-pencils/)
### Description:

You are given an integer `total` indicating the amount of money you have. You are also given two integers `cost1` and `cost2` indicating the price of a pen and pencil respectively. You can spend **part or all** of your money to buy multiple quantities (or none) of each kind of writing utensil.

Return the **number of distinct ways** you can buy some number of pens and pencils.


### example:

**Example 1:**
```
Input: total = 20, cost1 = 10, cost2 = 5
Output: 9
Explanation: The price of a pen is 10 and the price of a pencil is 5.
- If you buy 0 pens, you can buy 0, 1, 2, 3, or 4 pencils.
- If you buy 1 pen, you can buy 0, 1, or 2 pencils.
- If you buy 2 pens, you cannot buy any pencils.
The total number of ways to buy pens and pencils is 5 + 3 + 1 = 9.
```
**Example 2:**
```
Input: total = 5, cost1 = 10, cost2 = 10
Output: 1
Explanation: The price of both pens and pencils are 10, which cost more than total, so you cannot buy any writing utensils. Therefore, there is only 1 way: buy 0 pens and 0 pencils.
```

給兩種筆的價格（`cost1` , `cost2`）和可以購買的金額(`total`)。

要求出**所有購買組合**的可能

### Concept：

一看到的時候被`dp`綁住了

一直從`knapsack problem`或是`coin change`的方向去想

不過這題只需要枚舉其中一個數量，並判斷金額有沒有超過限制

而可能的組數用乘法、除法記算就可以了

~~完全不用DP...~~

## Solution：

**Solution**

不過當時忘記把debug的`cout`拿掉，吃了一個TLE....

```cpp

class Solution {
public:
    long long waysToBuyPensPencils(int total, int cost1, int cost2) {
        int i = 0 ;
        long long ans=0;
        while(true){
            if( i*cost1 > total ) break;
            
            int cur = total - i*cost1;
            int j=cur/cost2;

            ans+=j+1;
            
            // cout<<j+1<<'\n';
            i++;
        }

        return (ans==0 ? 1:ans);
    }
};
```


## Maximum Product After K Increments

[Design an ATM Machine](https://leetcode.com/contest/biweekly-contest-76/problems/design-an-atm-machine/)

### Description :
There is an ATM machine that stores banknotes of `5` denominations: `20`, `50`, `100`, `200`, and 500 dollars. Initially the ATM is empty. The user can use the machine to deposit or withdraw any amount of money.

When withdrawing, the machine prioritizes using banknotes of **larger** values.

- For example, if you want to withdraw `$300` and there are `2` `$50` banknotes, `1` `$100` banknote, and `1` `$200` banknote, then the machine will use the `$100` and `$200` banknotes.

- However, if you try to withdraw `$600` and there are `3` `$200` banknotes and `1` `$500` banknote, then the withdraw request will be rejected because the machine will first try to use the `$500` banknote and then be unable to use banknotes to complete the remaining `$100`. Note that the machine is **not** allowed to use the `$200` banknotes instead of the `$500` banknote.


Implement the ATM class:

- `ATM()` Initializes the ATM object.

- `void deposit(int[] banknotesCount)` Deposits new banknotes in the order `$20`, `$50`, `$100`, `$200`, and `$500`.

- `int[] withdraw(int amount)` Returns an array of length `5` of the number of banknotes that will be handed to the user in the order `$20`, `$50`, `$100`, `$200`, and `$500`, and update the number of banknotes in the ATM after withdrawing. Returns `[-1]` if it is not possible (do not withdraw any banknotes in this case).
### Exmample:

**Example 1:**
```
Input
["ATM", "deposit", "withdraw", "deposit", "withdraw", "withdraw"]
[[], [[0,0,1,2,1]], [600], [[0,1,0,1,1]], [600], [550]]
Output
[null, null, [0,0,1,0,1], null, [-1], [0,1,0,0,1]]
```

設計一個提款機，可以**存款**、**提領**

提領方式是：由**大的**幣值開始取

### Concept：

沒想到紀錄幣值數量的陣列要開`long long`（因為至多有`5000`次 call ）

還有原本寫成:
```cpp
for(int i=0;i<5;i++){
    if( amount/coin[i] > last[i] ) continue;
}
```

應該是如果需要該幣值的數量大於剩餘的數量：還是先扣除剩餘的數量

### Solution:


```cpp
class ATM {
public:
    ATM() {
        
    }
    
    int coin[5] = {20,50,100,200,500} ;
    long long last[5]={};
    void deposit(vector<int> banknotesCount) {
        for(int i=0;i<5;i++){
            last[i]+=banknotesCount[i];
        }
    }
    
    vector<int> withdraw(int amount) {

        int cur= amount;
        vector<int> ans(5,0);

        for(int i=4;i>=0;i--){
            if( cur < coin[i] ) continue;
            
            ans[i] = min( (long long)(cur/coin[i]) , last[i] );
            cur-= ans[i]*coin[i];
        }



        if( cur > 0 ) return vector<int>(1,-1);

        for(int i=0;i<5;i++){
            last[i]-=ans[i];
        }
        
        return ans;
    }
};

```




## Maximum Score of a Node Sequence

[Maximum Score of a Node Sequence](https://leetcode.com/contest/biweekly-contest-76/problems/maximum-score-of-a-node-sequence/)

### Description :

There is an **undirected** graph with `n` nodes, numbered from `0` to `n - 1`.

You are given a `0-indexed` integer array `scores` of length `n` where `scores[i]` denotes the score of node `i`. You are also given a 2D integer array `edges` where `edges[i] = [ai, bi]` denotes that there exists an **undirected** edge connecting nodes `ai` and `bi`.

A node sequence is **valid** if it meets the following conditions:

- There is an edge connecting every pair of **adjacent** nodes in the sequence.

- No node appears more than once in the sequence.

The score of a node sequence is defined as the **sum** of the scores of the nodes in the sequence.

Return the **maximum score** of a valid node sequence with a length of `4`. If no such sequence exists, return `-1`.

### Example:

**Example 1:**

![ leetcode biwwely 76-4-1](https://i.imgur.com/sVsVN5g.png)

```

Input: scores = [5,2,9,8,4], edges = [[0,1],[1,2],[2,3],[0,2],[1,3],[2,4]]
Output: 24
Explanation: The figure above shows the graph and the chosen node sequence [0,1,2,3].
The score of the node sequence is 5 + 2 + 9 + 8 = 24.
It can be shown that no other node sequence has a score of more than 24.
Note that the sequences [3,1,2,0] and [1,0,2,3] are also valid and have a score of 24.
The sequence [0,3,2,4] is not valid since no edge connects nodes 0 and 3.

```

**Example 2:**

![ leetcode biwwely 76-4-2](https://i.imgur.com/N30G3V1.png)

```

Input: scores = [9,20,6,4,11,12], edges = [[0,3],[5,3],[2,4],[1,3]]
Output: -1
Explanation: The figure above shows the graph.
There are no valid node sequences of length 4, so we return -1.

```

給無相圖中的所有**邊**，要找出**節點和最大**且**長度 = 4**（有**4**個節點）的一條**鍊**

回傳符合條件的**節點最大和**

太久沒寫圖論（這應該是學測後寫的第一題...

都被之前`DFS`或`BFS`的框架綁住

當時是枚舉所有鍊的開頭，再DFS長度為4的鍊

但顯然超時

### Concept:

我看了這幾篇題解才看懂ㄉ 

[https://leetcode.com/problems/maximum-score-of-a-node-sequence/discuss/1953669/Python3-Explanation-with-pictures-top-3-neighbors](https://leetcode.com/problems/maximum-score-of-a-node-sequence/discuss/1953669/Python3-Explanation-with-pictures-top-3-neighbors)

[https://leetcode.com/problems/maximum-score-of-a-node-sequence/discuss/1953670/C%2B%2B-O(E)-edge-traverse](https://leetcode.com/problems/maximum-score-of-a-node-sequence/discuss/1953670/C%2B%2B-O(E)-edge-traverse)


[https://leetcode.com/problems/maximum-score-of-a-node-sequence/discuss/1953905/C%2B%2B-Simple-Edge-traversal-O(ElogE)](https://leetcode.com/problems/maximum-score-of-a-node-sequence/discuss/1953905/C%2B%2B-Simple-Edge-traversal-O(ElogE))

- **找出符合條件的鍊**
要找到**長度 = 4**的一條**鍊**

我們可以先抓一條**邊**(假設叫邊`a-b`)

我們只要再找出與`a`節點相連的`c`節點

再找出與`b`節點相連的`d`節點

看起來會像：`c-a-b-d`

(並且`c!=b` `a!=d` `c!=d`)

- **找出最大值**

建立圖後，可以將**有連結**的節點按照`score`**排序**

這樣枚舉該邊（一樣叫邊`a-b`）成功就會是以邊`a-b`當中心的**最大值**

像是這樣` ( ci ,cj ,ck ...) - a - b - ( di , dj ,dk ...) `

`( ci ,cj ,ck ...)`代表與`a`節點**相連**並按照`score`排序的節點

`( di ,dj ,dk ...)`代表與`b`節點**相連**並按照`score`排序的節點

一旦枚舉到符合條件的` ci - a - b - di `就會是以`a-b`為中心的**最大值**


### Solution:

```cpp

class Solution {
public:
    int maximumScore(vector<int>& scores, vector<vector<int>>& edges) {
        int n = scores.size();
        vector<vector<int> > G(n);

        for(auto e: edges){
            G[e[1]].PB(e[0]);
            G[e[0]].PB(e[1]);
        }

        for(auto &i:G){
            sort(range(i) , [&](const int &u,const int &v){
                return scores[u] > scores[v];
            });
        }

        int ans=-1;
        for(const auto &e:edges){
            // a-u-v-b 
            int u = e[0] ,v = e[1] , sum=scores[u]+scores[v];
            
            for(int a:G[u]){
                if( a==v) continue;

                bool flag = false;
                
                for(int b:G[v]){
                    
                    if( b==u || a==b) continue;

                    ans=max( ans, sum+scores[a]+scores[b]);
                    
                    flag = true;
                    break;
                }

                if( flag) break;
            }
        }

        return ans;

    }
};
```
