directions = {
    "R": (1, 0),
    "D": (0, 1),
    "L": (-1, 0),
    "U": (0, -1)
}

def area(commands: list[tuple[str, int]]):
    vert: list[tuple[int, int]] = [(0, 0)]
    x, y = 0, 0
    b = 0

    for dir, length in commands:
        dx, dy = directions[dir]
        x += dx * length
        y += dy * length
        vert.append((x, y))
        b += length
    
    area = sum((y + y1) * (x - x1) / 2 for (x, y), (x1, y1) in zip(vert, vert[1:]))
    i = area - b / 2 + 1
    return int(i + b)


def main():
    with open("input.txt") as f:
        lines = f.read().splitlines()
    
    commands = [line.split() for line in lines]
    dirs = ["R", "D", "L", "U"]
    c1 = [(dir, int(length)) for (dir, length, _) in commands]
    c2 = [(dirs[int(color[-2])], int(color[2:-2], base=16)) for (*_, color) in commands]
    
    p1 = area(c1)
    p2 = area(c2)

    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")

main()