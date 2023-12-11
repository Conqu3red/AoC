import time

def expand(grid, expanded_rows, expanded_cols, expansion):
    galaxies = []
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == "#":
                galaxies.append((x + sum(expanded_cols[:x]) * (expansion - 1), y + sum(expanded_rows[:y]) * (expansion - 1)))
    return galaxies

def distance(galaxies):
    return sum(abs(g1[0] - g2[0]) + abs(g1[1] - g2[1]) for i, g1 in enumerate(galaxies) for g2 in galaxies[i:])

def main():
    with open("input.txt") as f:
        grid = f.read().splitlines()

    s = time.time()
    expanded_rows = [all(r == "." for r in row) for row in grid]
    expanded_cols = [all(row[i] == "." for row in grid) for i in range(len(grid[0]))]
    p1 = distance(expand(grid, expanded_rows, expanded_cols, 2))
    p2 = distance(expand(grid, expanded_rows, expanded_cols, 1000000))
    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")

    e = time.time()
    print(f"{e-s:.2f}s")

main()