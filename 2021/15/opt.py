from typing import *
from dataclasses import dataclass
import math
import heapq
import mheap as heapq
from timeit import default_timer as timer

def load_data():
    with open("input.txt") as f:
        data = f.read()
    
    return [[int(l) for l in line] for line in data.split("\n")]

@dataclass
class Node:
    value: int
    x: int
    y: int
    tdist: float
    done: bool

def get_distance(_grid: List[List[int]]):
    grid = [[Node(n, x, y, math.inf, False) for x, n in enumerate(line)] for y, line in enumerate(_grid)]

    current = grid[0][0]
    current.tdist = 0
    dest = grid[-1][-1]

    unvisited = []
    heapq.heappush(unvisited, (current.tdist, current.x, current.y))
    
    def neighbours(node: Node):
        for cx, cy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            if (0 <= node.x + cx < len(grid[0])) and (0 <= node.y + cy < len(grid)):
                yield grid[node.y + cy][node.x + cx]


    while not dest.done:
        t = heapq.heappop(unvisited)
        current = grid[t[2]][t[1]]
        if current.done:
            continue
        
        for node in neighbours(current):
            if not node.done:
                new_dist = current.tdist + node.value
                node.tdist = min(node.tdist, new_dist)
                heapq.heappush(unvisited, (node.tdist, node.x, node.y))
        
        current.done = True
    
    return grid

def expand_grid(grid: List[List[int]]):
    dy = len(grid)
    dx = len(grid[0])
    for y in range(0, dy * 5):
        if y >= len(grid):
            grid.append([])
        
        for x in range(0, dx * 5):
            if x < dx and y < dy:
                continue
        
            if y < dy:
                new_value = grid[y][x - dx] + 1
            else:
                new_value = grid[y - dy][x] + 1
            
            if new_value > 9:
                new_value = 1
            
            if x >= len(grid[y]):
                grid[y].append(new_value)
            else:
                grid[y][x] = new_value
    
    return grid
            
            

def main():
    grid = load_data()
    s = get_distance(grid)
    print(f"Part 1: {s[-1][-1].tdist}")

    large_grid = expand_grid(grid)
    s = timer()
    large_s = get_distance(grid)
    e = timer()
    print(f"Time: {e:.2f}s")
    print(f"Part 2: {large_s[-1][-1].tdist}")


if __name__ == "__main__":
    main()