def is_lowest_point(heightmap, x, y):
    point = heightmap[y][x]
    max_y = len(heightmap) - 1
    max_x = len(heightmap[0]) - 1
    for cx, cy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        if (0 <= (x + cx) <= max_x) and (0 <= (y + cy) <= max_y) and (heightmap[y + cy][x + cx] <= point):
                return False
    
    return True
    

def main():
    with open("input.txt") as f:
        heightmap = [[int(i) for i in line] for line in f.read().split("\n")]
    
    total = 0
    for y in range(len(heightmap)):
        for x in range(len(heightmap[y])):
            if is_lowest_point(heightmap, x, y):
                total += 1 + heightmap[y][x]
            
    
    print(f"Total: {total}")
    


if __name__ == "__main__":
    main()