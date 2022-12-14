from typing import *

def load_cells() -> Set[Tuple[int, int]]:
    cells: Set[Tuple[int, int]] = set()
    with open("input.txt") as f:
        lines = f.read().split("\n")
    
    for line in lines:
        points = line.split(" -> ")
        x, y = map(int, points[0].split(","))
        for point in points[1:]:
            dx, dy = map(int, point.split(","))
            for local_x in range(min(x, dx), max(x, dx) + 1):
                for local_y in range(min(y, dy), max(y, dy) + 1):
                    cells.add((local_x, local_y))
            
            x, y = dx, dy
        
    return cells


def simulate_sand(cells: Set[Tuple[int, int]]) -> int:
    n_sand = 0

    max_y = 0
    for (_, y) in cells:
        if y > max_y:
            max_y = y
    
    void_y = max_y + 1

    while True:
        sand_x, sand_y = 500, 0

        while True:
            sand_y += 1
            if (sand_x, sand_y) in cells:
                sand_x -= 1
                if (sand_x, sand_y) in cells:
                    sand_x += 2
                    if (sand_x, sand_y) in cells:
                        sand_x -= 1
                        sand_y -= 1
                        break

            if sand_y >= void_y:
                return n_sand
        
        cells.add((sand_x, sand_y))
        n_sand += 1


cells = load_cells()
print("Part 1:", simulate_sand(cells))