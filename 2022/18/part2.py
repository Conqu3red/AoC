from typing import *
import math
import collections
import time

def load() -> Set[Tuple[int, int, int]]:
    with open("input.txt") as f:
        lines = f.read().split("\n")
    
    points = set()
    for line in lines:
        points.add(tuple(map(int, line.split(","))))
    
    return points


def surface_area(points: Set[Tuple[int, int, int]]):
    area = 0

    # calculate min and max_coordinates
    minimum = [math.inf, math.inf, math.inf]
    maximum = [-math.inf, -math.inf, -math.inf]

    for point in points:
        for i, v in enumerate(point):
            if v < minimum[i]:
                minimum[i] = v
            
            if v > maximum[i]:
                maximum[i] = v

    #print(minimum, maximum)
    
    start = points.pop()
    points.add(start)
    start = (start[0], start[1], minimum[2] - 2)

    # move up to edge of shape
    while start not in points:
        start = (start[0], start[1], start[2] + 1)
    
    start = (start[0], start[1], start[2] - 1)

    exclude: Set[Tuple[int, int, int]] = set([start])
    to_visit = collections.deque([start])

    while to_visit:
        (x, y, z) = to_visit.popleft()
        # find faces
        for dx, dy, dz in ((0, 0, -1), (0, 0, 1), (0, -1, 0), (0, 1, 0), (-1, 0, 0), (1, 0, 0)):
            new = (x + dx, y + dy, z + dz)
            if new in exclude:
                continue
            
            if new in points:
                area += 1
            elif minimum[0] - 1 <= new[0] <= maximum[0] + 1 and minimum[1] - 1 <= new[1] <= maximum[1] + 1 and minimum[2] - 1 <= new[2] <= maximum[2] + 1:
                to_visit.append(new)
                exclude.add(new)

    return area


points = load()
s = time.time()
print("Part 2:", surface_area(points))
e = time.time()
print(f"Completed in {e - s:.2f}s")