
def load():
    with open("input.txt") as f:
        data = f.read().split("\n")
    return data

def main():
    data = load()
    total = 0
    for line in data:
        digits = [int(c) for c in line if c.isnumeric()]
        total += digits[0] * 10 + digits[-1]
    
    print("Part 1:", total)


main()