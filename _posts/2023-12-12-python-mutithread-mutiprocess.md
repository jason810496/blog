
### 為什麼會這樣？

這是因為 **FastAPI** 有一個 **worker** 的概念 <br>
> 這邊的 worker 不是指 **message queue** 的 worker <br>

<br>



當我們發出 request 時，FastAPI 會將這個 request 丟給一個 worker 去處理 <br>
而這個 worker 會一直處理這個 request 直到處理完畢 <br>

<br>

所以當我們發出多個 request 時，會有多個 worker 同時在處理這些 request <br>

<br>

但是這些 worker 都是在同一個 process 裡面 <br>
所以當我們的 CPU 資源不足時，這些 worker 會開始競爭 CPU 資源 <br>

<br>

而這個競爭 CPU 資源的過程，就是我們看到的 response time 變長的原因 <br>



由於 Python 的 Ｍuti-threading 並不是真的 multi-threading <br>
是由 GIL (Global Interpreter Lock) 來控制 <br>

<br>

這會導我們在處理 CPU bound (需要大量 CPU 資源) 的工作時 <br>
執行效率會變得很差 <br>

<br>

所以 muti-threading 比較適合處理 I/O bound (需要大量 I/O 資源) 的工作 <br>

在 Python 中，比較推薦使用 **multiprocessing** 來處理 CPU bound 的工作 <br>
可以充分利用多核心的 CPU 資源 <br>202