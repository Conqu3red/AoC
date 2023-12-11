import math


directions = {
    "|": {(0, 1), (0, -1)},
    "-": {(1, 0), (-1, 0)},
    "L": {(0,  -1), (1, 0)},
    "J": {(0, -1), (-1, 0)},
    "7": {(0, 1), (-1, 0)},
    "F": {(0, 1), (1, 0)},
    ".": set(),
    "S": {(0, 1), (1, 0), (0, -1), (-1, 0)},
}


def in_bounds(grid: list[list[str]], x: int, y: int):
    return 0 <= x < len(grid[0]) and 0 <= y < len(grid)


def visitable(grid: list[list[str]], x: int, y: int):
    for dx, dy in directions[grid[y][x]]:
        if in_bounds(grid, x + dx, y + dy) and grid[y + dy][x + dx] != ".":
            yield x + dx, y + dy


def determine_start_pipe(grid: list[list[str]], x: int, y: int) -> str:
    facing = []
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if (dx != 0 or dy != 0) and in_bounds(grid, x + dx, y + dy):
                facing.extend([(dx, dy) for dir in directions[grid[y + dy][x + dx]] if dx == -dir[0] and dy == -dir[1]])
    
    assert len(facing) == 2
    facing = set(facing)
    for k, dirs in directions.items():
        if dirs == facing:
            return k


def get_cycle(grid: list[list[str]], x: int, y: int):
    cycle: list[tuple[int, int]] = []

    while len(cycle) == 0 or (x, y) != cycle[0]:
        for nx, ny in visitable(grid, x, y):
            if len(cycle) == 0 or (nx, ny) != cycle[-1]:
                cycle.append((x, y))
                x, y = nx, ny
                break
    
    return cycle


def tile_to_subgrid(old, grid: list[list[str]], x: int, y: int):
    nx, ny = x * 3 + 1, y * 3 + 1
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
        if grid[y][x] == "#" or (x, y) in visited:
            continue
        visited.add((x, y))
        to_visit.extend([(x + dx, y + dy) for dx, dy in directions["S"] if in_bounds(grid, x + dx, y + dy)])
    
    outer_cells = sum(1 for x, y in visited if grid[y][x] == " ") // 9
    return len(old) * len(old[0]) - len(loop) - outer_cells


def main():
    with open("input.txt") as f:
        grid = [list(l) for l in f.read().splitlines()]
    
    x, y = next((x, y) for y, row in enumerate(grid) for x, pipe in enumerate(row) if pipe == "S")
    start_pipe = determine_start_pipe(grid, x, y)
    grid[y][x] = start_pipe
    print(f"Determined start tile to be {start_pipe}")
    loop = get_cycle(grid, x, y)

    p1 = math.ceil(len(loop) / 2)
    p2 = area(grid, loop)

    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")


main()
