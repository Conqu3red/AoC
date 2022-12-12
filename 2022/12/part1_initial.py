from typing import *
from dataclasses import dataclass
import math
import heapq

data = []
start = None
end = None

with open("input.txt") as f:
    lines = f.read().split("\n")
    for y, line in enumerate(lines):
        data.append([])
        for x, char in enumerate(line):
            if "a" <= char <= "z":
                data[-1].append(ord(char) - ord("a"))
            elif char == "S":
                data[-1].append(0)
                start = (x, y)
            elif char == "E":
                data[-1].append(26)
                end = (x, y)
                

@dataclass
class Node:
    value: int
    x: int
    y: int
    tdist: float
    done: bool

def dijkstra(_grid: List[List[int]], start: Tuple[int, int]):
    grid = [[Node(n, x, y, math.inf, False) for x, n in enumerate(line)] for y, line in enumerate(_grid)]

    current = grid[start[1]][start[0]]
    current.tdist = 0

    unvisited = []
    heapq.heappush(unvisited, (current.tdist, current.x, current.y))
    
    def neighbours(node: Node):
        for cx, cy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            if (0 <= node.x + cx < len(grid[0])) and (0 <= node.y + cy < len(grid)):
                if grid[node.y + cy][node.x + cx].value - 1 <= node.value:
                    yield grid[node.y + cy][node.x + cx]


    while unvisited:
        t = heapq.heappop(unvisited)
        current = grid[t[2]][t[1]]
        if current.done:
            continue
        
        for node in neighbours(current):
            if not node.done:
                new_dist = current.tdist + 1
                node.tdist = min(node.tdist, new_dist)
                heapq.heappush(unvisited, (node.tdist, node.x, node.y))
        
        current.done = True
    
    return grid

r = dijkstra(data, start)
print(r[end[1]][end[0]].tdist)