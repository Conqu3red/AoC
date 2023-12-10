import math

directions = {
    "|": [(0, 1), (0, -1)],
    "-": [(1, 0), (-1, 0)],
    "L": [(0,  -1), (1, 0)],
    "J": [(0, -1), (-1, 0)],
    "7": [(0, 1), (-1, 0)],
    "F": [(0, 1), (1, 0)],
    ".": [],
    "S": [(0, 1), (1, 0), (0, -1), (-1, 0)],
}


def visitable(grid: list[list[str]], x: int, y: int):
    for dx, dy in directions[grid[y][x]]:
        if 0 <= x + dx < len(grid[0]) and 0 <= y + dy < len(grid) and grid[y + dy][x + dx] != ".":
            yield x + dx, y + dy


def search(grid: list[list[str]], x: int, y: int):
    visited: set[tuple[int, int]] = set()
    to_visit = [(x, y)]

    while to_visit:
        x, y = to_visit.pop()
        
        if (x, y) in visited:
            continue
    
        visited.add((x, y))
        for nx, ny in visitable(grid, x, y):
            to_visit.append((nx, ny))
    
    return visited


def tile_to_subgrid(old, grid: list[list[str]], x: int, y: int):
    nx = x * 3 + 1
    ny = y * 3 + 1
    tile = old[y][x]

    placeholder = " " if tile == "." else "*"
    for i in range(-1, 2):
        for j in range(-1, 2):
            grid[ny + i][nx + j] = placeholder
    
    if tile != ".":
        grid[ny][nx] = "#"
    
    for dx, dy in directions[old[y][x]]:
        grid[ny + dy][nx + dx] = "#"
    

def area(old: list[list[tuple[int, int]]], loop: set[tuple[int, int]]):
    grid = [[" " for _ in range(len(old[0]) * 3)] for _ in range(len(old) * 3)]
    
    for x, y in loop:
        tile_to_subgrid(old, grid, x, y)
    
    #print("\n".join(["".join(row) for row in grid]))

    visited = set()
    to_visit = [(0, 0)]

    while to_visit:
        x, y = to_visit.pop()
        cell = grid[y][x]
        if cell == "#" or (x, y) in visited:
            continue
        visited.add((x, y))

        for dx, dy in directions["S"]:
            if 0 <= x + dx < len(grid[0]) and 0 <= y + dy < len(grid):
                to_visit.append((x + dx, y + dy))
    
    outer_cells = sum(1 for x, y in visited if grid[y][x] == " ") // 9
    return len(old) * len(old[0]) - len(loop) - outer_cells



def main():
    with open("input.txt") as f:
        lines = f.read().splitlines()
    
    grid = [list(l) for l in lines]

    found = False
    for y, row in enumerate(grid):
        for x, pipe in enumerate(row):
            if pipe == "S":
                found = True
                break
        if found:
            break
    
    loop = search(grid, x, y)

    p1 = math.ceil(len(loop) / 2)
    p2 = area(grid, loop)

    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")


main()
