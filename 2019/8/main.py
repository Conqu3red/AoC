import math

with open("input.txt") as f:
    data = f.read()

width = 25
height = 6

zeros = math.inf
value = 0

for i in range(0, len(data), width * height):
    region = data[i : i + (width * height)]
    z = region.count("0")
    if z < zeros:
        zeros = z
        value = region.count("1") * region.count("2")

print("Part 1:", value)

for y in range(height):
    for x in range(width):
        for offset in range(0, len(data), width * height):
            value = data[offset + y * width + x]
            if value != "2":
                print("#" if value == "1" else " ", end="")
                break
    print()
