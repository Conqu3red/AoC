def process(grid: list[list[str]]):
    for row in range(len(grid[0])):
        for col in range(len(grid)):
            if grid[col][row] == "O":
                for col2 in range(col - 1, -1, -1):
                    if grid[col2][row] == ".":
                        grid[col2][row] = "O"
                        grid[col2 + 1][row] = "."
                    else:
                        break

    return grid

def cycle(grid):
    for i in range(4):
        process(grid)
        grid = [[row[i] for row in reversed(grid)] for i in range(len(grid[0]))]
    return grid

def part2(grid: list[list[str]]):
    cache = {}
    cycles = 0
    while cycles < 1_000_000_000:
        grid = cycle(grid)
        compressed = "\n".join("".join(line) for line in grid)
        cycles += 1
        if compressed in cache:
            print("Cycle at", cycles)
            length = cycles - cache[compressed]
            cycles += ((1_000_000_000 - cycles) // length) * length
            break
        
        cache[compressed] = cycles
    
    while cycles < 1_000_000_000:
        grid = cycle(grid)
        cycles += 1

    return count(grid)

def count(grid):
    return sum(len(grid) - r for r, row in enumerate(grid) for cell in row if cell == "O")

def main():
    with open("input.txt") as f:
        data = f.read()
        grid = [list(l) for l in data.split("\n")]
        grid2 = [list(l) for l in grid]

    p1 = count(process(grid))
    p2 = part2(grid2)

    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")

main()