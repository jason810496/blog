---
title: 289th LeetCode Weekly Contest
subtitle: Leetcode 289th 週賽
date:   2022-04-18 22:30:00 +0800

tag: [c++/c,notes,Leetcode]

thumbnail-img: "https://i.imgur.com/n6yKZDY.png" #1:1 (450:450)

cover-img: "https://i.imgur.com/MBxEay3.png"

comments: true

# ======= Other parameters ========
layout: post
readtime: true

# test local : bundle exec jekyll serve
---
# 289th LeetCode Weekly Contest

[289th LeetCode Weekly Contest](https://leetcode.com/contest/weekly-contest-289)

一樣解出前兩題

第三、四題真的很有深度（對我而言啦...

**這次週賽的四個題目：**

- [Calculate Digit Sum of a String](https://leetcode.com/contest/weekly-contest-289/problems/calculate-digit-sum-of-a-string/)

- [Minimum Rounds to Complete All Tasks](https://leetcode.com/contest/weekly-contest-289/problems/minimum-rounds-to-complete-all-tasks/)

- [Maximum Trailing Zeros in a Cornered Path](https://leetcode.com/contest/weekly-contest-289/problems/maximum-trailing-zeros-in-a-cornered-path/)

- [Maximum Total Beauty of the Gardens](https://leetcode.com/contest/weekly-contest-288/problems/maximum-total-beauty-of-the-gardens/)

## Calculate Digit Sum of a String

[Calculate Digit Sum of a String](https://leetcode.com/contest/weekly-contest-289/problems/calculate-digit-sum-of-a-string/)


### Description:

You are given a string `s` consisting of digits and an integer `k`.

A **round** can be completed if the length of `s` is greater than `k`. In one round, do the following:

1. **Divide** `s` into **consecutive groups** of size `k` such that the first `k` characters are in the first group, the next `k` characters are in the second group, and so on. **Note** that the size of the last group can be smaller than `k`.
2. **Replace** each group of `s` with a string representing the sum of all its digits. For Example, `"346"` is replaced with `"13"` because `3 + 4 + 6 = 13`.
3. **Merge** consecutive groups together to form a new string. If the length of the string is greater than k, repeat from step `1`.
Return `s` after all rounds have been completed.



### Example:

```
Input: s = "11111222223", k = 3
Output: "135"
Explanation: 
- For the first round, we divide s into groups of size 3: "111", "112", "222", and "23".
  ​​​​​Then we calculate the digit sum of each group: 1 + 1 + 1 = 3, 1 + 1 + 2 = 4, 2 + 2 + 2 = 6, and 2 + 3 = 5. 
  So, s becomes "3" + "4" + "6" + "5" = "3465" after the first round.
- For the second round, we divide s into "346" and "5".
  Then we calculate the digit sum of each group: 3 + 4 + 6 = 13, 5 = 5. 
  So, s becomes "13" + "5" = "135" after second round. 
Now, s.length <= k, so we return "135" as the answer.
```

將原本的數字字串不斷分切成`k`等分，並將每等分都**依照各位數加總**，再將加總後的結果**組成新字串**，直到最後的字串長度**小於等於k**

### Concept：

就照著題意暴力硬做

## Solution：

**Solution**

```cpp
#define range(x) x.begin(),x.end()

class Solution {
public:
    int to_int(string s){
        int ret=0;
        for(int i=0;i<s.size();i++){
            ret+=s[i]-'0';
        }
        return ret;
    }
    string to_str(int n){
        string ret= "";
        
        while(n){
            ret+=char('0'+n%10);
            n/=10;
        }
        
        if(ret=="") return "0";
        reverse(range(ret));
        return ret;
    }

    string digitSum(string s, int k) {
        
        while( s.size() > k ){
            int last=0,next=k, n = s.size();

            vector<string> Sub;
            while(last+k <= n){
                Sub.push_back(s.substr(last,k) );
                last+=k;
            }
            if(last<n){
                Sub.push_back(s.substr(last,s.size()-last));
            }
            

            for(string &i:Sub){
                i = to_str( to_int(i) );
            }
            
            s.clear();
            
            for(string &i:Sub){
                s+=i;
            }
            
        }

        return s;
    }
};
```

## Minimum Rounds to Complete All Tasks

[Minimum Rounds to Complete All Tasks](https://leetcode.com/contest/weekly-contest-289/problems/minimum-rounds-to-complete-all-tasks/)

### Description:

You are given a **0-indexed** integer array `tasks`, where `tasks[i]` represents the difficulty level of a task. In each round, you can complete either 2 or 3 tasks of the **same difficulty level**.

Return the **minimum** rounds required to complete all the tasks, or `-1` if it is not possible to complete all the tasks.

### Example:

**Example 1:**
```
Input: tasks = [2,2,3,3,2,4,4,4,4,4]
Output: 4
Explanation: To complete all the tasks, a possible plan is:
- In the first round, you complete 3 tasks of difficulty level 2. 
- In the second round, you complete 2 tasks of difficulty level 3. 
- In the third round, you complete 3 tasks of difficulty level 4. 
- In the fourth round, you complete 2 tasks of difficulty level 4.  
It can be shown that all the tasks cannot be completed in fewer than 4 rounds, so the answer is 4.
```
**Example 2:**
```
Input: tasks = [2,3,3]
Output: -1
Explanation: There is only 1 task of difficulty level 2, but in each round, you can only complete either 2 or 3 tasks of the same difficulty level. Hence, you cannot complete all the tasks, and the answer is -1.
```

轉換題意就是：在一次操作中，可以**刪除 2 或 3 個**陣列中**相同的數字**，並求出清空陣列的最少操作次數（如果不能將陣列中所有數字刪除回傳`-1`）

### Concept：

1. 討論無法達成的情況
經過簡單的觀察可以發現，如果某個數字**出現次數小於 2**就**無法被消除**

而 2 跟 3 可以組合出所有的質數（`5=3+2` , `7=3+2+2` ... ）所以**出現次數大於等於 2 的**數字都可以被刪除

2. 求畜最小操作次數
要求出清空該數字的最小操作數量，也就是盡可能的用**3**來表示該數字**出現的次數**

又一個數字`mod 3`可以分成以下 3 個情況：

這邊設某個數字的出現次數為`Count`
- `Count%3 == 0 `

每次都刪去 3 個就是最小操作次數

也就是刪除該數字需要 `Count/3` 次
- `Count%3 == 2 `

我覺得`%3==2`的情況比較顯見

最小操作次數是`Count/3 + 1`

因為最後餘`2`，而每次操作只能刪掉 2 或 3 個數字

所以最後`+1` (代表刪除最後剩餘的 2 個數字)

- `Count%3 == 1 `

這種情況代表`Count`可以被看成：

`Count = (3+3+3...3) + (3+1)`

而最後的`(3+1)`可以拆成`2+2`

數量剛好是`Count/3 +1 `

**綜合以上：**

- `Count%3 == 1` or `Count%3 == 2` 
最小操作次數：都是`Count/3 + 1`次

- `Count% == 0 `
最小操作次數：`Count/3`次

## Solution：

一開始用`unordered_map`(Hash table)紀錄每個數字出現幾次

```cpp

class Solution {
public:
    int minimumRounds(vector<int>& tasks) {
        unordered_map<int,int> M;
        for(int i:tasks){
            M[i]++;
        }

        int ans=0;
        for(auto i:M){
            int cur = i.second;
            if( cur <2) return -1;

            int last = cur%3;

            if(last==1 || last==2 ){
                ans+=cur/3+1;
            }
            else {
                ans+=cur/3;
            }
        }

        return ans;
    }
};

```

## Maximum Trailing Zeros in a Cornered Path

[Maximum Trailing Zeros in a Cornered Path](https://leetcode.com/contest/weekly-contest-289/problems/maximum-trailing-zeros-in-a-cornered-path/)

### Description :
You are given a 2D integer array `grid` of size `m x n`, where each cell contains a positive integer.

A **cornered path** is defined as a set of adjacent cells with **at most** one turn. More specifically, the path should exclusively move either **horizontally** or **vertically** up to the turn (if there is one), without returning to a previously visited cell. After the turn, the path will then move exclusively in the **alternate** direction: move vertically if it moved horizontally, and vice versa, also without returning to a previously visited cell.

The **product** of a path is defined as the product of all the values in the path.

Return the **maximum** number of **trailing zeros** in the product of a cornered path found in `grid`.

Note:

- **orizontal** movement means moving in either the left or right direction.
- **Vertical** movement means moving in either the up or down direction.
### Exmample:

**Example 1:**
![Ex 1](https://assets.leetcode.com/uploads/2022/03/23/ex1new2.jpg)
```
Input: grid = [[23,17,15,3,20],[8,1,20,27,11],[9,4,6,2,21],[40,9,1,10,6],[22,7,4,5,3]]
Output: 3
Explanation: The grid on the left shows a valid cornered path.
It has a product of 15 * 20 * 6 * 1 * 10 = 18000 which has 3 trailing zeros.
It can be shown that this is the maximum trailing zeros in the product of a cornered path.

The grid in the middle is not a cornered path as it has more than one turn.
The grid on the right is not a cornered path as it requires a return to a previously visited cell.
```

**Example 2:**
![Ex 2](https://assets.leetcode.com/uploads/2022/03/25/ex2.jpg)
```
Input: grid = [[4,3,2],[7,6,1],[8,8,8]]
Output: 0
Explanation: The grid is shown in the figure above.
There are no cornered paths in the grid that result in a product with a trailing zero.
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