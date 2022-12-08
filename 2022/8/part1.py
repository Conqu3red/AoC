from typing import *

with open("input.txt") as f:
    lines = f.read().split("\n")

    trees = [[int(c) for c in l] for l in lines]
    visible = [[False for _ in l] for l in lines]

    def scan_coords(coords: Iterable[Tuple[int, int]]):
        highest = -1
        for coord in coords:
            tree = trees[coord[1]][coord[0]]
            if tree > highest:
                highest = tree
                visible[coord[1]][coord[0]] = True

    for y in range(len(trees)):
        scan_coords((x, y) for x in range(len(trees[y])))
        scan_coords((x, y) for x in range(len(trees[y]) - 1, -1, -1))
    
    for x in range(len(trees[0])):
        scan_coords((x, y) for y in range(len(trees)))
        scan_coords((x, y) for y in range(len(trees) - 1, -1, -1))
    

    print(sum(sum(l) for l in visible))