import math

with open("input.txt") as f:
    wires = [[(s[0], int(s[1:])) for s in line.split(",")] for line in f.read().split("\n")]

directions = {
    "R": (1, 0),
    "L": (-1, 0),
    "U": (0, 1),
    "D": (0, -1),
}

def traverse(wire):
    pos = (0, 0)
    points = {}
    total_steps = 0
    for dir, steps in wire:
        for s in range(steps):
            pos = (pos[0] + directions[dir][0], pos[1] + directions[dir][1])
            total_steps += 1
            points[pos] = total_steps
    return points

def main():
    p1 = traverse(wires[0])

    min_st = math.inf
    min_manhattan = math.inf
    pos = (0, 0)
    total_steps = 0
    for dir, steps in wires[1]:
        for _ in range(steps):
            pos = (pos[0] + directions[dir][0], pos[1] + directions[dir][1])
            total_steps += 1
            if pos in p1:
                man = abs(pos[0]) + abs(pos[1])
                min_manhattan = min(min_manhattan, man)
                st = total_steps + p1[pos]
                min_st = min(min_st, st)

    print("Part 1:", min_manhattan)
    print("Part 2:", min_st)

main()