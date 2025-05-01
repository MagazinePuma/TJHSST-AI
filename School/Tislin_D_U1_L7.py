# Dennis Tislin, Period 5, 2026 
# Data:
import random, math, time #, heapq
from math import pi, acos, sin, cos
from tkinter import *

class HeapPriorityQueue():
    def __init__(self):
        self.queue = ["dummy"]
        self.current = 1
   
    def next(self):
        if self.current >= len(self.queue):
            self.current = 1
            raise StopIteration
        out = self.queue[self.current]
        self.current += 1
        return out
   
    def __iter__(self):
        return self
   
    __next__ = next
   
    def isEmpty(self):
        return len(self.queue) == 1
   
    def swap(self, a, b):
        self.queue[a], self.queue[b] = self.queue[b], self.queue[a]
       
    def push(self, value):
        self.queue.append(value)
        self.heapUp(len(self.queue) - 1)
       
    def heapUp(self, k):
        while k // 2 > 0 and self.queue[k] < self.queue[k // 2]:
            self.swap(k, k // 2)
            k = k // 2
   
    def heapDown(self, k, size):
        left, right = k * 2, k * 2 + 1
        if left == size and self.queue[k] > self.queue[left]:
            self.swap(k, left)
        elif right <= size:
            maxC = (left if self.queue[left] < self.queue[right] else right)
            if self.queue[maxC] < self.queue[k]:
                self.swap(k, maxC)
                self.heapDown(maxC, size)
   
    def reheap(self):
        for i in range(len(self.queue) // 2, 0, -1):
            self.heapDown(i, len(self.queue) - 1)
   
    def pop(self):
        self.swap(1, len(self.queue) - 1)
        out = self.queue.pop()
        self.heapDown(1, len(self.queue) - 1)
        return out
   
    def remove(self, index):
        self.swap(index + 1, len(self.queue) - 1)
        out = self.queue.pop()
        self.reheap()
        return out

def calc_edge_cost(y1, x1, y2, x2):
    #
    # y1 = lat1, x1 = long1
    # y2 = lat2, x2 = long2
    # all assumed to be in decimal degrees
    # if (and only if) the input is strings
    # use the following conversions
    y1 = float(y1)
    x1 = float(x1)
    y2 = float(y2)
    x2 = float(x2)
    #
    R = 3958.76 # miles = 6371 km
    #
    y1 *= pi/180.0
    x1 *= pi/180.0
    y2 *= pi/180.0
    x2 *= pi/180.0
    #
    # approximate great circle distance with law of cosines
    #
    return acos( sin(y1)*sin(y2) + cos(y1)*cos(y2)*cos(x2-x1) ) * R
    #

# NodeLocations, NodeToCity, CityToNode, Neighbors, EdgeCost
# Node: (lat, long) or (y, x), node: city, city: node, node: neighbors, (n1,n2): cost
def make_graph(nodes = "rrNodes.txt", node_city = "rrNodeCity.txt", edges = "rrEdges.txt"):
    nodeLoc, nodeToCity, cityToNode, neighbors, edgeCost = {}, {}, {}, {}, {}
    map = {} # have screen coordinate for each node location
    # Your code goes here
    x = open(nodes, "r")
    for node in x.readlines():
        w, y, z = node.split()
        nodeLoc[w] = [float(y), float(z)]

    x = open(node_city, "r")
    for node in x.readlines():
        w = node.split()
        city = ' '.join(w[1:])
        nodeToCity[w[0]] = city
        cityToNode[city] = w[0]
        #city = nodeToCity[w[0]]

    x = open(edges, "r")
    for node in x.readlines():
        w, y = node.split()
        if w in neighbors:
            neighbors[w].add(y)
        else:
            neighbors[w] = {y}
        if y in neighbors:
            neighbors[y].add(w)
        else:
            neighbors[y] = {w}
        cost = calc_edge_cost(*nodeLoc[w], *nodeLoc[y]) #dist_heuristic(w, y)
        edgeCost[(w, y)] = cost
        edgeCost[(y, w)] = cost

    # Un-comment after you fill the nodeLoc dictionary.
    for node in nodeLoc: #checks each
        lat = float(nodeLoc[node][0]) #gets latitude
        long = float(nodeLoc[node][1]) #gets long
        modlat = (lat - 10)/60 #scales to 0-1
        modlong = (long+130)/70 #scales to 0-1
        map[node] = [modlat*800, modlong*1200] #scales to fit 800 1200

    ''' You may test your graph here:
    print ("34.90083 -90.218 ?", nodeLoc["2800002"])
    print ("Las Vegas ?", nodeToCity["3200014"])
    print ("3200014 ?", cityToNode["Las Vegas"])
    print ("{'3200044', '3200050', '3200013'} ?", neighbors["3200014"])
    print ("11.319736091806572 ?", edgeCost[("0600316", "0600427")])
    '''
    return [nodeLoc, nodeToCity, cityToNode, neighbors, edgeCost, map]

# Retuen the direct distance from node1 to node2
# Use calc_edge_cost function.
def dist_heuristic(n1, n2, graph):
# Your code goes here
    return calc_edge_cost(graph[0][n1][0], graph[0][n1][1], graph[0][n2][0], graph[0][n2][1])
    # return calc_edge_cost(*graph[0][n1], *graph[0][n2])

# Create a city path.
# Visit each node in the path. If the node has the city name, add the city name to the path.
# Example: ['Charlotte', 'Hermosillo', 'Mexicali', 'Los Angeles']
def display_path(path, graph):
    # Your code goes here
    print([graph[1][x] for x in path if x in graph[1]])

# Using the explored, make a path by climbing up to "s"
# This method may be used in your BFS and Bi-BFS algorithms.
def generate_path(state, explored, graph):
    path = [state]
    cost = 0
    # Your code goes here
    while explored[state] != "s":
        path.append(explored[state])
        cost += graph[4][(state, explored[state])]
        state = explored[state]

    return path[::-1], cost

def drawLine(canvas, y1, x1, y2, x2, col):
    x1, y1, x2, y2 = float(x1), float(y1), float(x2), float(y2)
    canvas.create_line(x1, 800-y1, x2, 800-y2, fill=col)

# Draw the final shortest path.
# Use drawLine function.
def draw_final_path(ROOT, canvas, path, graph, col='red'):
    # Your code goes here
    for i in range(len(path) - 1):
        drawLine(canvas, *graph[5][path[i]], *graph[5][path[i + 1]], col)

def draw_all_edges(ROOT, canvas, graph):
    ROOT.geometry("1200x800") #sets geometry
    canvas.pack(fill=BOTH, expand=1) #sets fill expand
    for n1, n2 in graph[4]: #graph[4] keys are edge set
        drawLine(canvas, *graph[5][n1], *graph[5][n2], 'white') #graph[5] is map dict

def bfs(start, goal, graph, col):
    ROOT = Tk() #creates new tkinter
    ROOT.title("BFS")
    canvas = Canvas(ROOT, background='black') #sets background
    draw_all_edges(ROOT, canvas, graph)
    
    counter = 0
    frontier, explored = [], {start: "s"}
    frontier.append(start)
    while frontier:
        s = frontier.pop(0)
        if s == goal:
            path, cost = generate_path(s, explored, graph)
            draw_final_path(ROOT, canvas, path, graph)
            return path, cost, counter
        for a in graph[3][s]: #graph[3] is neighbors
            if a not in explored:
                explored[a] = s
                frontier.append(a)
                drawLine(canvas, *graph[5][s], *graph[5][a], col)
        counter += 1
        if counter % 1000 == 0: ROOT.update()

    return None

def bi_bfs(start, goal, graph, col):
    # Your code goes here
    ROOT = Tk() #creates new tkinter
    ROOT.title("BI_BFS")
    canvas = Canvas(ROOT, background='black') #sets background
    draw_all_edges(ROOT, canvas, graph)
    
    # frontier = [[start], [goal]]
    # explored = [{start: "s"}, {goal: "s"}]
    # count, k = 0, 1
    
    # while frontier[0] and frontier[1]:
    #     k = 1 - k
    #     current = frontier[k].pop()
    #     f = frontier[k][:]
    #     f[k] -= {current}
        
    #     if current in f[1 - k]:
    #         path, cost2 = explored[k][current][1][:-1] + explored[1 - k][current][1][::-1], explored[k][current][0] + explored[1 - k][current][0]
    #         draw_final_path(ROOT, canvas, path, graph)
    #         return path, cost2
        
    #     for child in graph[3][current]:
    #         cost3 = explored[k][current][0]+ graph[4][(current, child)]
    #         if child not in explored[k] or explored[k][child][0] > cost3:
    #             frontier[k].push((cost3 + dist_heuristic(child, sg[1 - k], graph), child))
    #             f[k].add(child)
    #             explored[k][child] = (cost3, explored[k][current][1] + [child])
    #             drawLine(canvas, *graph[5][current], *graph[5][child], col)
                
    #     count += 1
    #     if count % 1000 == 0: ROOT.update()
        
    # return None
    
    frontier = [[start], [goal]]
    explored = [{start: "s"}, {goal: "s"}]
    count, k = 0, 1
    
    while frontier[0] and frontier[1]:
        k = 1 - k 
        temp = frontier[k][:]
        frontier[k] = []
        
        while temp:
            current = temp.pop(0)
            if current in frontier[1 - k]:
                path, cost = generate_path(current, explored[0], graph)
                path2, cost2 = generate_path(current, explored[1], graph)
                draw_final_path(ROOT, canvas, path[:-1] + path2[::-1], graph)
                return path[:-1] + path2[::-1], cost + cost2, count
            
            for node in graph[3][current]:
                if node not in explored[k]: # [list(x.keys()) for x in explored]
                    frontier[k].append(node)
                    explored[k][node] = current
                    drawLine(canvas, *graph[5][current], *graph[5][node], col)
                    
            count += 1
            if count % 1000 == 0: ROOT.update()
        
    return None

def a_star(start, goal, graph, col, heuristic = dist_heuristic):
    ROOT = Tk() #creates new tkinter
    ROOT.title("A_STAR")
    canvas = Canvas(ROOT, background='black')
    draw_all_edges(ROOT, canvas, graph)
    
    frontier = HeapPriorityQueue()
    frontier.push((0, start, [start]))
    explored = {start: (0, [start])}
    count = 0
    
    while frontier:
        cost, current, path = frontier.pop()
        
        if current == goal:
            #path2, cost2 = generate_path(current, explored, graph), cost
            draw_final_path(ROOT, canvas, path, graph)
            return path, cost, count 
        
        for child in graph[3][current]:
            if child not in explored or explored[child][0] > explored[current][0] + graph[4][(current, child)]:
                childList = path[:]
                childList.append(child)
                frontier.push((explored[current][0] + graph[4][(current, child)] + dist_heuristic(child, goal, graph), child, childList))
                explored[child] = (explored[current][0] + graph[4][(current, child)], childList)
                drawLine(canvas, *graph[5][current], *graph[5][child], col)
                
        count += 1
        if count % 1000 == 0: ROOT.update()
        
    return [], 0
                
    # frontier = HeapPriorityQueue()
    # frontier.push(((0, 0, start, "")))
    # explored = set()

    # print_log = False
    
    # while frontier:
    #     cost, level, current, compact = frontier.pop()
        
    #     if current == goal:
    #         explored.add(current)
    #         path2, cost2 = generate_path(current[2], explored, graph)
    #         draw_final_path(ROOT, canvas, path2, graph)
    #         return path2, cost2         # return "G"

    #     if current in explored:
    #         continue

    #     #if current in frontier:
    #     #    continue

    #     explored.add(current)

    #     for child, child_compact in graph[3][current[2]]:
    #         if child == goal:
    #             #explored.add(current)
    #             #explored.add(child)
    #             path2, cost2 = generate_path(current[2], explored, graph)
    #             draw_final_path(ROOT, canvas, path2, graph)
    #             return path2, cost2         # return compact + child_compact
            
    #         if child in explored:
    #             continue

    #         child_level = level + 1
    #         child_cost = child_level + dist_heuristic(child, goal, graph)
    #         new_child_compact = compact + child_compact
    #         frontier.push((child_cost, child_level, child, new_child_compact))
    #         drawLine(canvas, *graph[5][current[2]], *graph[5][child], col)

    # return None
    
    # if start == goal:
    #     path2, cost2 = generate_path(start, explored, graph) # path = [start] 
    #     draw_final_path(ROOT, canvas, path2, graph)
    #     return path2, cost2 #return [(start, start, 0, 0, "G")]
    
    # current = None
    # min = 0
    # #frontier = [{"current": start, "parent": start, "cost": 0, "level": 0, "compact": ""}]
    # frontier = []
    # heapq.heappush(frontier, (0, 0, start, [start], ""))
    # explored = {} # dist_heuristic(frontier, goal, graph)
    # #count = 0

    # print_log = False
    
    # while frontier:
    #     cost, level, current, path, compact = heapq.heappop(frontier)
        
    #     if current == goal:
    #         explored.add(current)
    #         path2, cost2 = generate_path(current[2], explored, graph)
    #         draw_final_path(ROOT, canvas, path2, graph)
    #         return path2, cost2

    #     if current in explored:
    #         continue

    #     # explored.add(current)

    #     for child, child_compact in graph[3][current[2]]: # generate_children(current)
    #         if child == goal:
    #             explored.add(current)
    #             explored.add(child)
    #             path2, cost2 = generate_path(current[2], explored, graph)
    #             draw_final_path(ROOT, canvas, path2, graph)
    #             return path2, cost2 # compact + child_compact, cost2
            
    #         child_level = level + 1
    #         child_cost = child_level + dist_heuristic(child, goal, graph)
            
    #         if child not in explored or child_cost < explored[child]:
    #             continue
            
    #         new_child_compact = compact + child_compact
    #         heapq.heappush(frontier, (child_cost, child_level, child, path+[child], new_child_compact))
    #         explored.add(child) # explored[child] = child_cost
    #         drawLine(canvas, *graph[5][current[2]], *graph[5][child], col)

    # return None

def bi_a_star(start, goal, graph, col, heuristic=dist_heuristic):
    # Your code goes here
    ROOT = Tk() #creates new tkinter
    ROOT.title("BI_A_STAR")
    canvas = Canvas(ROOT, background='black')
    draw_all_edges(ROOT, canvas, graph)
    
    frontier = [HeapPriorityQueue(), HeapPriorityQueue()]
    explored = [{start: (0, [start])}, {goal: (0, [goal])}]
    frontier[0].push((0, start))
    frontier[1].push((0, goal)) # dist_heuristic(start, goal, graph)
    f = [{start}, {goal}]
    sg = [start, goal]
    count, k = 0, 1
    
    while frontier[0] and frontier[1]:
        k = 1 - k
        cost, current = frontier[k].pop()
        f[k] -= {current}
        
        if current in f[1 - k]:
            path, cost2 = explored[k][current][1][:-1] + explored[1 - k][current][1][::-1], explored[k][current][0] + explored[1 - k][current][0]
            draw_final_path(ROOT, canvas, path, graph)
            return path, cost2, count
        
        for child in graph[3][current]:
            cost3 = explored[k][current][0]+ graph[4][(current, child)]
            if child not in explored[k] or explored[k][child][0] > cost3:
                frontier[k].push((cost3 + dist_heuristic(child, sg[1 - k], graph), child))
                f[k].add(child)
                explored[k][child] = (cost3, explored[k][current][1] + [child])  # + [child]
                drawLine(canvas, *graph[5][current], *graph[5][child], col)
                
        count += 1
        if count % 1000 == 0: ROOT.update()
        
    return None

def tri_directional(city1, city2, city3, graph, col, heuristic=dist_heuristic):
    # Your code goes here
    ROOT = Tk() #creates new tkinter
    ROOT.title("TRI_A_STAR")
    canvas = Canvas(ROOT, background='black')
    draw_all_edges(ROOT, canvas, graph)
    
    pathSM, costSM, countSM = tri_helper(city1, city3, graph, col, canvas, ROOT)
    pathME, costME, countME = tri_helper(city2, city3, graph, col, canvas, ROOT)
    pathSE, costSE, countSE = tri_helper(city1, city2, graph, col, canvas, ROOT)
    
    minCost, minPath1, minPath2, minCount = min([(costME + costSM, pathME[:-1], pathSM, countME + countSM), (costSM + costSE, pathSM[:-1], pathSE, countSM + countSE), (costSE + costME, pathSE[:-1], pathME, countSE + countME)]) # , (costSE + costME, pathSE[:-1] + pathME, countSE + countME)    pathME[:-1] + pathSM   
    draw_final_path(ROOT, canvas, minPath1, graph)
    draw_final_path(ROOT, canvas, minPath2, graph)
    
    return minCost, minPath1 + minPath2, minCount

def tri_helper(start, goal, graph, col, canvas, ROOT):
    frontier = [HeapPriorityQueue(), HeapPriorityQueue()]
    explored = [{start: (0, [start])}, {goal: (0, [goal])}]
    frontier[0].push((0, start))
    frontier[1].push((0, goal)) # dist_heuristic(start, goal, graph)
    f = [{start}, {goal}]
    sg = [start, goal]
    count, k = 0, 1
    
    while frontier[0] and frontier[1]:
        k = 1 - k
        cost, current = frontier[k].pop()
        f[k] -= {current}
        
        if current in f[1 - k]:
            path, cost2 = explored[k][current][1][:-1] + explored[1 - k][current][1][::-1], explored[k][current][0] + explored[1 - k][current][0]
            return path, cost2, count
        
        for child in graph[3][current]:
            cost3 = explored[k][current][0]+ graph[4][(current, child)]
            if child not in explored[k] or explored[k][child][0] > cost3:
                frontier[k].push((cost3 + dist_heuristic(child, sg[1 - k], graph), child))
                f[k].add(child)
                explored[k][child] = (cost3, explored[k][current][1] + [child])  # + [child]
                drawLine(canvas, *graph[5][current], *graph[5][child], col)
        
        count += 1
        if count % 1000 == 0: ROOT.update()
                
    return None

def main():
    start, goal = input("Start city: "), input("Goal city: ")
    third = input("Third city for tri-directional: ")
    print()
    graph = make_graph("rrNodes.txt", "rrNodeCity.txt", "rrEdges.txt") # Task 1
    cur_time = time.time()
    
    path, cost, count = bfs(graph[2][start], graph[2][goal], graph, 'yellow') #graph[2]is city to node
    p2, c2, count2 = a_star(graph[2][start], graph[2][goal], graph, 'blue')
    p3, c3, count3 = bi_bfs(graph[2][start], graph[2][goal], graph, 'green')
    p4, c4, count4 = bi_a_star(graph[2][start], graph[2][goal], graph, 'orange')
    c5, p5, count5 = tri_directional(graph[2][start], graph[2][goal], graph[2][third], graph, 'pink')
    
    if path != None: 
        display_path(path, graph)
        print("BFS Path: ", path)
        print("BFS Count: " + str(count))
        print("BFS Path Length: " + str(len(path)))
        print()
    else: print("No Path Found.")
    
    if p2 != None: 
        display_path(p2, graph)
        print("A_STAR Path: ", p2)
        print("A_STAR Count: " + str(count2))
        print("A_STAR Path Length: " + str(len(p2)))
        print()
    else: print ("No Path Found.")
    
    if p3 != None: 
        display_path(p3, graph)
        print("BI_BFS Path: ", p3)
        print("BI_BFS Count: " + str(count3))
        print("BI_BFS Path Length: " + str(len(p3)))
        print()
    else: print("No Path Found.")
    
    if p4 != None: 
        display_path(p4, graph)
        print("BI_A_STAR Path: ", p4)
        print("BI_A_STAR Count: " + str(count4))
        print("BI_A_STAR Path Length: " + str(len(p4)))
        print()
    else: print("No Path Found.")
    
    if p5 != None: 
        display_path(p5, graph)
        print("TRI_A_STAR Path: ", p5)
        print("TRI_A_STAR Count: " + str(count5))
        print("TRI_A_STAR Path Length: " + str(len(p5)))
        print()
    else: print("No Path Found.")
    
    print("Costs:")
    print ('BFS Path Cost:', cost)
    print ('BI_BFS Path Cost:', c3)
    print ('A_STAR Path Cost:', c2)
    print ('BI_A_STAR Path Cost:', c4)
    print ('TRI_A_STAR Path Cost:', c5)
    print ('BFS duration:', (time.time() - cur_time))
    print ()
"""
cur_time = time.time()
path, cost = bi_bfs(graph[2][start], graph[2][goal], graph, 'green')
if path != None: display_path(path, graph)
else: print ("No Path Found.")
print ('Bi-BFS Path Cost:', cost)
print ('Bi-BFS duration:', (time.time() - cur_time))
print ()
cur_time = time.time()
path, cost = a_star(graph[2][start], graph[2][goal], graph, 'blue')
if path != None: display_path(path, graph)
else: print ("No Path Found.")
print ('A star Path Cost:', cost)
print ('A star duration:', (time.time() - cur_time))
print ()
cur_time = time.time()
path, cost = bi_a_star(graph[2][start], graph[2][goal], graph, 'orange',
ROOT, canvas)
if path != None: display_path(path, graph)
else: print ("No Path Found.")
print ('Bi-A star Path Cost:', cost)
print ("Bi-A star duration: ", (time.time() - cur_time))
print ()
print ("Tri-Search of ({}, {}, {})".format(start, goal, third))
cur_time = time.time()
path, cost = tri_directional(graph[2][start], graph[2][goal], graph[2]
[third], graph, 'pink', ROOT, canvas)
if path != None: display_path(path, graph)
else: print ("No Path Found.")
print ('Tri-A star Path Cost:', cost)
print ("Tri-directional search duration:", (time.time() - cur_time))
"""
if __name__ == '__main__':
    main()

mainloop() # Let TK windows stay still

#if __name__ == '__main__':
#   main()
