def horizontal(grid: list[list[str]], smudges: int = 0):
    for i in range(1, len(grid)):
        if sum(v != v2 for r, r2 in zip(grid[:i][::-1], grid[i:]) for v, v2 in zip(r, r2)) == smudges:
            return i
    return 0


def reflection(grid: list[list[str]], smudges: int = 0):
    return horizontal(grid, smudges) * 100 or horizontal([[row[i] for row in grid] for i in range(len(grid[0]))], smudges)


def main():
    with open("input.txt") as f:
        grids = [[list(line) for line in part.splitlines()] for part in f.read().split("\n\n")]
    
    p1 = 0
    p2 = 0
    for grid in grids:
        p1 += reflection(grid)
        p2 += reflection(grid, smudges=1)

    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")

main()