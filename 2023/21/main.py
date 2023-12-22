from collections import deque

def visitable(grid, steps: int, x: int, y: int):
    visited = set()
    landable = set()
    queue = deque()
    queue.append((0, (x, y)))
    while queue:
        dist, (x, y) = queue.popleft()
        if dist > steps:
            continue
        if (x, y) in visited:
            continue
        if dist % 2 == steps % 2:
            landable.add((x, y))
        visited.add((x, y))
        for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            if grid[(x + dx) % len(grid[0])][(y + dy) % len(grid)] == ".":
                queue.append((dist + 1, (x + dx, y + dy)))
        
        #print(queue)
    
    return len(landable)

def main():
    with open("input.txt") as f:
        grid = [list(line) for line in f.read().splitlines()]
    
    x, y = next((x, y) for y, row in enumerate(grid) for x, cell in enumerate(row) if cell == "S")

    p1 = visitable(grid, 64, x, y)
    print(f"Part 1: {p1}")

    import matplotlib.pyplot as plt
    xs = range(0, 200)
    ys = []
    
    for steps in range(0, 200):
        ys.append(visitable(grid, steps, x, y))
        print(steps, ys[-1])
    

    
    plt.plot(xs, ys)
    #plt.plot(xs, [6*v**2 - 1371*v + 91956 for v in xs])
    plt.show()
    """ for steps in range(0, 65):
        print(steps, visitable(grid, steps, x, y)) """

main()

"""
133 -> 15747
134 -> 15978

"""