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