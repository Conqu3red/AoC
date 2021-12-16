
def compute_positions(lines):
    positions = {}
    for line in lines:
        if line[0] == line[2]:
            for y in range(min(line[1], line[3]), max(line[1], line[3]) + 1):
                positions[line[0], y] = positions.get((line[0], y), 0) + 1
        if line[1] == line[3]:
            for x in range(min(line[0], line[2]), max(line[0], line[2]) + 1):
                positions[x, line[1]] = positions.get((x, line[1]), 0) + 1
    
    return positions

def main():
    with open("input.txt") as f:
        lines = [[int(n) for n in line.replace(" -> ", ",").split(",")] for line in f.read().split("\n")]
    
    positions = compute_positions(lines)
    print("Squares >= 2 =", len(list(filter(lambda x: x >= 2, positions.values()))))

if __name__ == "__main__":
    main()