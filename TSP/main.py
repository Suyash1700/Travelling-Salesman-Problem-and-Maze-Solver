import time
from heapq import heapify, heappush, heappop
# used as infinity for file input
INF=1000000000

# find fxn for union find
def find(parent, i):
    if parent[i] == i:
        return i
    return find(parent, parent[i])

# A function that does union of two sets of x and y
# (uses union by rank)
def union(parent, rank, x, y):
    xroot = find(parent, x)
    yroot = find(parent, y)

    # Attach smaller rank tree under root of
    # high rank tree (Union by Rank)
    if rank[xroot] < rank[yroot]:
        parent[xroot] = yroot
    elif rank[xroot] > rank[yroot]:
        parent[yroot] = xroot

    # If ranks are same, then make one as root
    # and increment its rank by one
    else:
        parent[yroot] = xroot
        rank[xroot] += 1

    # The main function to construct MST using Kruskal's
    # algorithm

def KruskalMST(inclusion_edges):
    result = []  # This will store the resultant MST

    #Assuming the Edges are sorted we take edges which have both vertices in inclusion edge
    alledges = []
    for i, j, k in graph.alledges:
        if i in inclusion_edges and j in inclusion_edges:
            alledges.append((i, j, k))

    parent = [i for i in range(graph.V + 1)]
    rank = [0] * (graph.V + 1)
    # An index variable, used for sorted edges
    i = 0
    # An index variable, used for result[]
    e = 0
    # Number of edges to be taken is equal to V-1
    while e < len(inclusion_edges) - 1 and i < len(alledges):
        # print("ff")
        #Pick the smallest edge and increment
        # the index for next iteration
        u, v, w = alledges[i]
        i = i + 1
        x = find(parent, u)
        y = find(parent, v)
        # If including this edge does't
        #  cause cycle, include it in result
        #  and increment the indexof result
        # for next edge
        if x != y:
            
            e = e + 1
            result.append([u, v, w])
            union(parent, rank, x, y)
        # Else discard the 
        
    # calculating cost of MST
    minimumCost = 0
    for u, v, weight in result:
        minimumCost += weight
    return minimumCost

# node of fringelist
class node:
    def __init__(self, a, cost) -> None:
        self.cost = cost
        self.path = a
        self.pathlength = len(a)
        self.remaining = graph.overall.difference(set(a))
    # shows all value of the object
    def showall(self):
        print(*self.path)
        print(self.remaining)
        print(self.cost)
        print("----------------------------------------------------")

    # all children of the objent in fringlist
    def childrens(self):
        retval = []
        # if path found then no children
        if self.pathlength == graph.V + 1:
            return retval
        #  special case to add 1st node at the end again
        if self.pathlength == graph.V:
            for i in range(1, graph.V + 1):
                if i == self.path[0]:
                    temp = self.path[::]
                    temp.append(self.path[0])
                    retval.append(node(temp, self.cost + graph.g[i][self.path[-1]]))
                    break
            return retval
            
        for i in self.remaining:
            value = graph.g[i][self.path[-1]]
            temp = self.path[::]
            temp.append(i)
            if value != INF:
                retval.append(node(temp, self.cost + value))
        return retval

    # to print the object
    def __str__(self) -> str:
        return "Cost : " + str(self.cost) + "\n" + " -> ".join(map(str, self.path))

    def __eq__(self, other):
        return (self.path == other.path) and (self.cost == other.cost)

    def __ne__(self, other):
        return not (self == other)

    def __lt__(self, other):
        return self.cost < other.cost

    def __gt__(self, other):
        return self.cost > other.cost

    def __le__(self, other):
        return self.cost <= other.cost

    def __ge__(self, other):
        return self.cost >= other.cost


    def __hash__(self):
        tbh = str(self.cost)
        tbh += " ".join(map(str, self.path))
        return hash(tbh)

class Graph:
    def __init__(self, n) -> None:
        self.V = n
        self.overall = set([i for i in range(1, n + 1)])
        self.g = [[INF] * (n + 1) for _ in range(n + 1)]
        self.alledges = []

    def addedge(self, x, y, value):
        self.alledges.append((x, y, value))
        self.g[x][y] = value
        self.g[y][x] = value

    # input as matrix
    def setmatrix(self, mat):
        for i in range(self.V):
            for j in range(self.V):
                self.g[i + 1][j + 1] = mat[i][j]
                if mat[i][j] != INF and i > j:
                    self.alledges.append((i + 1, j + 1, mat[i][j]))
        self.alledgesaded()

    # sorts edges so no need to sort every time in krusal
    def alledgesaded(self):
        self.alledges = sorted(self.alledges, key=lambda item: item[2])

    def show(self):
        for i in range(1, self.V + 1):
            print(*self.g[i][1:])
            print()

def astar():
    # heuristic function
    def fxn(node: node):
        hxn = KruskalMST(node.remaining)
        # print(node,node.remaining,hxn,hxn + node.cost)
        return hxn + node.cost

    count = 0
    # h is fringelist
    #    (heuristic cost , node(list,actual cost))
    h = [(0, node([1], 0))]
    heapify(h)

    while len(h) > 0:
        _, temp = heappop(h)
        count += 1
        # cheacking goal condition 
        if len(temp.path) == graph.V + 1:
            print(temp)
            break
        #  getting the children of the poped node
        for i in temp.childrens():
                val = fxn(i)
                heappush(h, (val, i))
        #  printing progress
        if count % 1000 == 0:
            print(count // 1000, len(temp.path))
    print(count)

# input from file
file = open("./TSPinput.txt", "r")
N = int(file.readline())
grid = []
for _ in range(N):
    grid.append(list(map(int, file.readline().split())))
graph = Graph(N)
graph.setmatrix(grid)
astar()