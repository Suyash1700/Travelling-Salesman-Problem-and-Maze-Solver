import math
import time
from collections import defaultdict,deque,Counter
from sys import stdin,stdout
from bisect import bisect_left,bisect_right
import sys
from heapq import heapify, heappush, heappop 
import random
n=50
arr=[i for i in range(n)]
random.shuffle(arr)
file=open("./TSPinput.txt","w")
file.write(str(n)+"\n")
ans=[[1000000000]*n for _ in range(n)]
edges=set()
for i in range(n):
    temp=[arr[i],arr[i-1]]
    temp.sort()
    edges.add(tuple(temp))
    val=random.randint(1,10)
    ans[arr[i]][arr[i-1]]=val
    ans[arr[i-1]][arr[i]]=val

count=0
while count<500:
    i=random.randint(0,n-2)
    j=random.randint(i,n-1  )
    if((i,j) not in edges):
        count+=1
        val=random.randint(5,100)
        ans[i][j]=val
        ans[j][i]=val

# print(arr)
# for i in ans:
#     print(*i)
print(*list(map(lambda x:x+1,arr)))
for i in range(n):
    # print(*ans[i])
    file.write(" ".join(map(str,ans[i])))
    file.write("\n")