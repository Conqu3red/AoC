import math

head = (0, 0)
tail = (0, 0)

vectors = {
    "R": (1, 0),
    "L": (-1, 0),
    "U": (0, 1),
    "D": (0, -1),
}

def sign(x: int):
    return 1 if x >=0 else -1

def compute_tail_change():
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
        tail_visited.add(tail)
        
        head = (head[0] + velocity[0], head[1] + velocity[1])
        tail = compute_tail_change()

        #print(head, tail)
    
print(len(tail_visited))
