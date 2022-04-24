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

- [Longest Path With Different Adjacent Characters](https://leetcode.com/contest/weekly-contest-289/problems/longest-path-with-different-adjacent-characters/)

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

**cornered path**：是在 grid 上最多轉一次彎的路徑

題目要求合法的路經中的乘積**尾數最多有幾個 0**

例如：

路徑上有`10 20 3 7 5 19`

這些的乘積是`399000`

所以要回傳 `3` （尾數有 3 個零）

~~比賽時完全沒有想法~~

### Concept：

1. 位數要有 0 的條件

尾數要有 0 ，勢必乘積中要有`2`和`5`，並且`2`和`5`以外的數字相乘並不會影響答案

所以對於每一個的數字，只需要紀錄`2`和`5`的因數數量

如：這格數字是`1500`可以紀錄成`{2,3}`（我用`pair`來表示：`first`是`2`的數量，`second`是`5`的數量）

2. 要如何知道一條路徑的尾數有幾個 0 ?

看了高手的解法，關鍵是：

**前綴合**

開 2 個 `mxn` 的陣列紀錄從**上方**累加的和從**左方**累加的前綴合

紀錄從上個位置累加過來的`2`和`5`的數量

3. 枚舉合法路徑

合法路徑可以是 ：

(以下`(i,j)`都代表座標)
- Up-Left :

`(0,j)`到`(i,j)`在從`(i,j)`到`(i,0)` 
- Up-right :

`(0,j)`到`(i,j)`在從`(i,j)`到`(i,n-1)` 
- Down-Left :

`(m-1,j)`到`(i,j)`在從`(i,j)`到`(i,0)`
- Down-Right :

`(m-1,j)`到`(i,j)`在從`(i,j)`到`(i,n-1)`

然後雙層迴圈枚舉所有中間座標`( i , j )`

(並且要注意標界限制，對於`i==0`或是`j==0`需要特判)

3. 尾數最多 0 的合法路徑

藉由`2.`和`3.`的技巧：

尾數最多`0`的合法 path 是枚舉到的`( i , j )`中

- `Up-Left`
- `Up-Right`
- `Down-Left`
- `Down-Right`

這 4 個路經的`max( min( factor 5 of ith path , factor 2 of ith path ) )`

### Solution:

就算了解概念後，實做還是挺麻煩...（ 尤其是邊界的限制 ）

也可以`overload operator`來降低實做的複雜度（在做`pair`的前綴合的時候）

```cpp
#define pii pair<int,int>
#define F first
#define S second

class Solution {
public:
    pii Get(int x){
        int factor2=0 ,factor5=0;
        while( x%5==0 ){
            factor5++;
            x/=5;
        }
        while( x%2==0 ){
            factor2++;
            x/=2;
        }
        return { factor2 , factor5 } ;// factor: 2,5 
    }
    int maxTrailingZeros(vector<vector<int>>& grid) {
        int  m = grid.size() , n = grid[0].size() ; 
        vector< vector< pii > > Hor(m, vector<pii>(n) ) , Ver(m,vector<pii>(n) ) ;
        
        for(int j=0;j<n;j++){
            Hor[0][j] = Get( grid[0][j] );
        }
        // prefix sum
        for(int i=1;i<m;i++){
            for(int j=0;j<n;j++){
                pii cur = Get(grid[i][j]);
                Hor[i][j].F = Hor[i-1][j].F + cur.F;
                Hor[i][j].S = Hor[i-1][j].S + cur.S;
            }
        }
        
        for(int i=0;i<m;i++){
            Ver[i][0] = Get( grid[i][0] );
        }
        
        for(int i=0;i<m;i++){
            for(int j=1;j<n;j++){
                pii cur = Get(grid[i][j]);
                Ver[i][j].F = Ver[i][j-1].F + cur.F;
                Ver[i][j].S = Ver[i][j-1].S + cur.S;
            }
        }
        
        
        int ans=0;
        for(int i=0;i<m;i++){
            for(int j=0;j<n;j++){
                int Up_2 = Hor[i][j].F;
                int Down_2 = (i==0 ? Hor[m-1][j].F :Hor[m-1][j].F - Hor[i-1][j].F);
                int Left_2 = (j==0 ? 0:Ver[i][j-1].F);
                int Right_2 = Ver[i][n-1].F - Ver[i][j].F;
                
                int Up_5 = Hor[i][j].S;
                int Down_5 = (i==0 ? Hor[m-1][j].S :Hor[m-1][j].S - Hor[i-1][j].S);
                int Left_5 = (j==0 ? 0:Ver[i][j-1].S);
                int Right_5 = Ver[i][n-1].S - Ver[i][j].S;
                
                int UL=min(Up_2+Left_2,Up_5+Left_5);
                int UR=min(Up_2+Right_2,Up_5+Right_5);
                int DL=min(Down_2+Left_2,Down_5+Left_5);
                int DR=min(Down_2+Right_2,Down_5+Right_5);
                
                ans=max(ans, max(max(UL,UR),max(DL,DR) ));
                
            }
        }
        
        return ans;
    }
};

```

## Longest Path With Different Adjacent Characters

[Longest Path With Different Adjacent Characters](https://leetcode.com/contest/weekly-contest-289/problems/longest-path-with-different-adjacent-characters/)

### Description :

You are given a **tree** (i.e. a connected, undirected graph that has no cycles) **rooted** at node `0` consisting of `n` nodes numbered from `0` to `n - 1`. The tree is represented by a **0-indexed** array `parent` of size `n`, where `parent[i]` is the parent of node `i`. Since node `0` is the root, `parent[0] == -1`.

You are also given a string `s` of length `n`, where `s[i]` is the character assigned to node `i`.

Return the length of the **longest path** in the tree such that no pair of **adjacent** nodes on the path have the same character assigned to them.



### Example:

**Example 1:**

![Ex 1 ](https://assets.leetcode.com/uploads/2022/03/25/testingdrawio.png)

```
Input: parent = [-1,0,0,1,1,2], s = "abacbe"
Output: 3
Explanation: The longest path where each two adjacent nodes have different characters in the tree is the path: 0 -> 1 -> 3. The length of this path is 3, so 3 is returned.
It can be proven that there is no longer path that satisfies the conditions. 
```

**Example 2:**

![ Ex 2](https://assets.leetcode.com/uploads/2022/03/25/graph2drawio.png)

```
Input: parent = [-1,0,0,0], s = "aabc"
Output: 3
Explanation: The longest path where each two adjacent nodes have different characters is the path: 2 -> 0 -> 3. The length of this path is 3, so 3 is returned.
```

**Constraints:**

- `n == parent.length == s.length`
- `1 <= n <= 105`
- `0 <= parent[i] <= n - 1` for all `i >= 1`
- `parent[0] == -1`
- `parent` represents a valid tree.
- `s` consists of only lowercase English letters.

給一棵**Tree**，並且每個node都是char，又求由**沒有相同char相鄰**的**最長路徑**

### Concept:

有想到`DFS`但是沒有想到完整的架構

反而想到`樹壓平`＋`Sliding Window`的奇怪操作（但這是錯ㄉ ）

看了別人的解法，其中的關鍵是：

一棵**樹**中**最長的合法路徑**是：

**「由該節點最長的兩個合法路徑所組成」**

(好像很理所當然，但是知道這個關鍵就不需要將 `DFS` 的所有子path都枚舉過一遍)


1. 建立 Tree

原本只有給`parent`的關係，先還原成`Tree`（`Parent`指向`child`）

2. DFS 

`First`和`Second`分別紀錄的是對於該節點的**最長路徑**和**次長路徑**

並且要更新答案時要順變考慮**子節點與當前節點是否為相同字元**（題目要求要不同字元）

`ans`是開在 `class`的變數，紀錄DFS到當前`Max Path Length`

而`DFS`回傳的是**包含當前節點的最長路徑**

### Solution:

```cpp
class Solution {
public:
    
    int ans=0 , n ;
    vector< vector<int> > G;
    int DFS(int cur,string &s){
        int First=0 , Second=0;
        
        for(int nxt:G[cur] ){
            int res = DFS(nxt , s);
            if( s[cur]==s[nxt] ) continue;
            if( res > Second) Second = res;
            if( Second > First ) swap(First,Second);
        }
        
        ans = max( ans , First+Second+1);
        return First+1;
    }
    int longestPath(vector<int>& parent, string s) {
        n = parent.size();
        G.resize(n);
        
        for(int i=1;i<n;i++){
            G[ parent[i] ].push_back(i);
        }
        DFS(0,s);
        
        return ans;
    }
};
```