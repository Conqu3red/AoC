import math
from typing import *

knots = [(0, 0) for _ in range(10)]

vectors = {
    "R": (1, 0),
    "L": (-1, 0),
    "U": (0, 1),
    "D": (0, -1),
}

def sign(x: int):
    return 1 if x >=0 else -1

def compute_knot_change(head: Tuple[int, int], tail: Tuple[int, int]):
    tx = 0
    ty = 0
    if abs(head[0] - tail[0]) == 2:
        tx = sign(head[0] - tail[0])
    
    if abs(head[1] - tail[1]) == 2:
        ty = sign(head[1] - tail[1])
    
    # diagonal and far
    if abs(head[0] - tail[0]) + abs(head[1] - tail[1]) == 3:
        tx = sign(head[0] - tail[0])
        ty = sign(head[1] - tail[1])
    
    return (tail[0] + tx, tail[1] + ty)

tail_visited = set()

with open("input.txt") as f:
    lines = f.read().split("\n")

for line in lines:
    direction, times = line.split(" ")
    times = int(times)
    velocity = vectors[direction]
    for _ in range(times):
        tail_visited.add(knots[-1])
        
        knots[0] = (knots[0][0] + velocity[0], knots[0][1] + velocity[1])
        for i in range(1, len(knots)):
            knots[i] = compute_knot_change(knots[i - 1], knots[i])


print(len(tail_visited))
