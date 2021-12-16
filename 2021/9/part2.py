def is_lowest_point(heightmap, x, y):
    point = heightmap[y][x]
    max_y = len(heightmap) - 1
    max_x = len(heightmap[0]) - 1
    for cx, cy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        if (0 <= (x + cx) <= max_x) and (0 <= (y + cy) <= max_y) and (heightmap[y + cy][x + cx] <= point):
                return False
    
    return True

def recursive_get_basin_area_from_point(heightmap, x, y, done=None):
    # recursive solution
    if done is None:
        done = set()
    point = heightmap[y][x]
    max_y = len(heightmap) - 1
    max_x = len(heightmap[0]) - 1
    spaces_found = 0
    for cx, cy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        if (0 <= (x + cx) <= max_x) and (0 <= (y + cy) <= max_y) and (x + cx, y + cy) not in done: # bounds check
            done.add((x + cx, y + cy))
            new_point = heightmap[y + cy][x + cx]
            if new_point > point and new_point != 9:
                spaces_found += get_basin_area_from_point(heightmap, x + cx, y + cy, done)
    
    return 1 + spaces_found

def get_basin_area_from_point(heightmap, x, y):
    # iterative solution (neater)
    point = heightmap[y][x]
    max_y = len(heightmap) - 1
    max_x = len(heightmap[0]) - 1
    spaces_found = 0
    done = set()
    point_queue = [(x, y)]
    while len(point_queue):
        new_x, new_y = point_queue.pop()
        if (new_x, new_y) not in done:
            done.add((new_x, new_y))
            spaces_found += 1
            for cx, cy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                if (
                    (0 <= (new_x + cx) <= max_x)
                    and (0 <= (new_y + cy) <= max_y)
                    and (heightmap[new_y + cy][new_x + cx] > heightmap[new_y][new_x])
                    and (heightmap[new_y + cy][new_x + cx] != 9)
                ):
                    point_queue.append((new_x + cx, new_y + cy))
    
    
    return spaces_found

def main():
    with open("input.txt") as f:
        heightmap = [[int(i) for i in line] for line in f.read().split("\n")]
    
    total = 0
    basin_sizes = []
    for y in range(len(heightmap)):
        for x in range(len(heightmap[y])):
            if is_lowest_point(heightmap, x, y):
                total += 1 + heightmap[y][x]
                basin_sizes.append(get_basin_area_from_point(heightmap, x, y))
    
    basin_sizes.sort(reverse=True)
    
    
    print(f"Total: {total}")
    print(f"Largest Basin: {basin_sizes[0]}")
    print(f"Top 3 Basins multiplied: {basin_sizes[0] * basin_sizes[1] * basin_sizes[2]}")
    


if __name__ == "__main__":
    main()