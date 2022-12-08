from typing import *

with open("input.txt") as f:
    lines = f.read().split("\n")

    trees = [[int(c) for c in l] for l in lines]
    visible = [[False for _ in l] for l in lines]

    def scan_coords(start: Tuple[int, int], direction: Tuple[int, int]):
        me = trees[start[1]][start[0]]
        x = start[0] + direction[0]
        y = start[1] + direction[1]
        i = 0
        while 0 <= x < len(trees[0]) and 0 <= y < len(trees):
            i += 1

            if trees[y][x] >= me:
                break
            
            x += direction[0]
            y += direction[1]
        
        return i
        
    
    def scenic_score(x: int, y: int):
        max_x = len(trees[0])
        max_y = len(trees)

        r = 1
        for d in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            r *= scan_coords((x, y), d)
        
        return r

    best = 0
    for y in range(len(trees)):
        for x in range(len(trees[y])):
            best = max(best, scenic_score(x, y))
    

    print(best)