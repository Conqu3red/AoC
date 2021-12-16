from typing import *

def load_data() -> Tuple[Set[Tuple[int, int]], List[Tuple[str, int]]]:
    with open("input.txt") as f:
        data = f.read()
    
    points, instructions = data.split("\n\n")
    points = set(tuple(int(n) for n in a.split(",")) for a in points.split("\n"))
    instructions = [line.replace("fold along ", "").split("=") for line in instructions.split("\n")]
    instructions = [(axis, int(val)) for axis, val in instructions]

    return points, instructions


def fold(data: Set[Tuple[int, int]], fold_pos: Tuple[str, int]):
    new_data = set()
    if fold_pos[0] == "y": # fold points up
        for p in data:
            if p[1] > fold_pos[1]:
                # y - (py - y)
                # y + -(py - y)
                # y + -py + y
                # 2y - py
                new_data.add((p[0], fold_pos[1] - (p[1] - fold_pos[1])))
            else:
                new_data.add(p)
    else:
        for p in data:
            if p[0] > fold_pos[1]:
                # y - (py - y)
                # y + -(py - y)
                # y + -py + y
                # 2y - py
                new_data.add((fold_pos[1] - (p[0] - fold_pos[1]), p[1]))
            else:
                new_data.add(p)
    
    return new_data


def main():
    points, instructions = load_data()

    points = fold(points, instructions[0])
    print(f"Part 1: {len(points)}")
    for instruction in instructions[1:]:
        points = fold(points, instruction)
    
    max_x = max(points, key=lambda x: x[0])[0]
    max_y = max(points, key=lambda x: x[1])[1]

    grid = [[False for x in range(max_x + 1)] for y in range(max_y + 1)]
    for point in points:
        grid[point[1]][point[0]] = True
    
    # display
    print("Part 2:")
    for line in grid:
        print("".join("#" if l else " " for l in line))

if __name__ == "__main__":
    main()