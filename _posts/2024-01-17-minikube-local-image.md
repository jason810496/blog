
如何在 minikube ( local k8s )上使用 local 機器的 image

透過 miniube image load 指令
1. minikube image load <name>:<tag>
要記得把 `imagePullPolicy` 設定為 `Never`


自建暫時的 image repository
對於所有 local k8s 都是用 不一定要 minikube
2. 


> 剛好遇到 ci build 出來的 image 怪怪的
> 享用 local image 來 debug


https://stackoverflow.com/questions/42564058/how-can-i-use-local-docker-images-with-minikube