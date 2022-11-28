import math


def f(a):
    return a[2]


def find(li, x, y):
    for i in range(len(li)):
        if (li[i][0] == x and li[i][1] == y):
            return i
    return -1


n, m = map(int, input().split())
maze = []
for _ in range(n):
    maze.append(input())
startx, starty = map(int, input().split())
endx, endy = map(int, input().split())
# node=[posx,posy,value,fromx,fromy]
li = []
removed = []
for i in range(n):
    for j in range(m):
        if(maze[i][j]!='#'):
            li.append([i, j, math.inf, -1, -1])
ans = True
li[find(li, startx, starty)][2] = 0
# print(li)
x = startx
y = starty
while(x != endx or y != endy):
    temp2 = find(li, x, y)
    temp = find(li, x+1, y)
    if(x+1 < n and maze[x+1][y] != "#" and temp != -1):
        if(li[temp][2] > li[temp2][2]+int(maze[x+1][y])):
            li[temp][2] = li[temp2][2]+int(maze[x+1][y])
            li[temp][3] = x
            li[temp][4] = y
    temp = find(li, x - 1, y)
    if(x-1 > -1 and maze[x-1][y] != "#" and temp != -1):
        if(li[temp][2] > li[temp2][2]+int(maze[x-1][y])):
            li[temp][2] = li[temp2][2]+int(maze[x-1][y])
            li[temp][3] = x
            li[temp][4] = y
    temp = find(li, x, y+1)
    if(y+1 < m and maze[x][y+1] != "#" and temp != -1):
        if(li[temp][2] > li[temp2][2]+int(maze[x][y+1])):
            li[temp][2] = li[temp2][2]+int(maze[x][y+1])
            li[temp][3] = x
            li[temp][4] = y
    temp = find(li, x, y-1)
    if(y-1 > -1 and maze[x][y-1] != "#" and temp != -1):
        if(li[temp][2] > li[temp2][2]+int(maze[x][y-1])):
            li[temp][2] = li[temp2][2]+int(maze[x][y-1])
            li[temp][3] = x
            li[temp][4] = y
    removed.append(li[temp2])
    del li[temp2]
    li.sort(key=f)
    x = li[0][0]
    y = li[0][1]
    if math.isinf(li[0][2]):
        ans = False
        break
removed.append(li[find(li, x, y)])
del li[find(li, x, y)]
print()
# print(removed)
if(ans):
    while(x != startx or y != starty):
        print(x, y)


        temp = find(removed, x, y)
        x = removed[temp][3]
        y = removed[temp][4]
    print(x, y)
    print("value is ",removed[find(removed, endx, endy)][2])
    print("time relatively : ",len(removed) )
else:
    print("path not possible")
