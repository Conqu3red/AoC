from dataclasses import dataclass

@dataclass
class Beam:
    x: int
    y: int
    dx: int
    dy: int

def sim(grid: list[list[str]], start: Beam):
    beams: list[Beam] = [start]
    visited: set[tuple[int, int, int, int]] = set()
    energized: set[tuple[int, int]] = set()
    bounds = (len(grid[0]), len(grid))

    while beams:
        new_beams = []
        for b in beams:
            if (b.x, b.y, b.dx, b.dy) in visited or not (0 <= b.x < bounds[0] and 0 <= b.y < bounds[1]):
                continue
            
            visited.add((b.x, b.y, b.dx, b.dy))
            energized.add((b.x, b.y))
            
            cell = grid[b.y][b.x]
            if cell == "/":
                b.dx, b.dy = -b.dy, -b.dx
            elif cell == "\\":
                b.dx, b.dy = b.dy, b.dx
            elif cell == "|" and b.dy == 0:
                b.dx, b.dy = b.dy, b.dx
                new_beams.append(Beam(b.x, b.y, -b.dx, -b.dy))
            elif cell == "-" and b.dx == 0:
                b.dx, b.dy = b.dy, b.dx
                new_beams.append(Beam(b.x, b.y, -b.dx, -b.dy))
            
            b.x += b.dx
            b.y += b.dy
            new_beams.append(b)
        
        beams = new_beams
    
    return len(energized)


def part2(grid):
    best = 0
    for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
        # horizontal
        for y in (0, len(grid) - 1):
            for x in range(0, len(grid[0])):
                best = max(best, sim(grid, Beam(x, y, dx, dy)))
        
        # vertical
        for x in (0, len(grid[0]) - 1):
            for y in range(0, len(grid)):
                best = max(best, sim(grid, Beam(x, y, dx, dy)))
    
    return best


def main():
    with open("input.txt") as f:
        grid = [list(l) for l in f.read().splitlines()]
    
    p1 = sim(grid, Beam(x=0, y=0, dx=1, dy=0))
    p2 = part2(grid)

    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")

main()