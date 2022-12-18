from typing import *

def load() -> Set[Tuple[int, int, int]]:
    with open("input.txt") as f:
        lines = f.read().split("\n")
    
    points = set()
    for line in lines:
        points.add(tuple(map(int, line.split(","))))
    
    return points


def surface_area(points: Set[Tuple[int, int, int]]):
    area = 0

    for x, y, z in points:
        for dx, dy, dz in ((0, 0, -1), (0, 0, 1), (0, -1, 0), (0, 1, 0), (-1, 0, 0), (1, 0, 0)):
            new = (x + dx, y + dy, z + dz)
            if new not in points:
                area += 1
    
    return area


points = load()
print(surface_area(points))