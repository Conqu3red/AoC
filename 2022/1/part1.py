highest = 0
current = 0

with open("input.txt") as f:
    lines = f.read().split("\n")
    for line in lines:
        if line == "":
            if current > highest:
                highest = current
            current = 0
        else:
            current += int(line)


print("Highest:", highest)