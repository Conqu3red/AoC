def process_step(data) -> int:
    flashes = 0

    # increment all by one
    for row in data:
        for i in range(len(row)):
            row[i] += 1

    flash_done_lookup_table = [[False for _ in range(len(data[0]))] for _ in range(len(data))]

    # apply flashes
    new_flash = True
    while new_flash:
        new_flash = False
        for y in range(len(data)):
            for x in range(len(data[y])):
                if not flash_done_lookup_table[y][x] and data[y][x] > 9:
                    flash_done_lookup_table[y][x] = True
                    flashes += 1
                    new_flash = True
                    # increment adjacent
                    for cy in (-1, 0, 1):
                        for cx in (-1, 0, 1):
                            if (0 <= (y + cy) < len(data)) and (0 <= (x + cx) < len(data[y + cy])): # bounds
                                data[y + cy][x + cx] += 1
    
    # set all flashed octupus to zero
    for y in range(len(data)):
        for x in range(len(data[y])):
            if flash_done_lookup_table[y][x]:
                data[y][x] = 0
    
    return flashes

def load_data():
    with open("input.txt") as f:
        data = [[int(i) for i in line] for line in f.read().split("\n")]
    return data

def print_data(data):
    print("\n".join(["".join("█" if n == 0 else str(n) for n in l) for l in data]))
    print()

def main():
    data = load_data()

    num_flashes = 0
    for i in range(100):
        num_flashes += process_step(data)
        print_data(data)
    
    print(f"Flashes: {num_flashes}")

if __name__ == "__main__":
    main()