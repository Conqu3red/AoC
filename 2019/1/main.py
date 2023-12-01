
with open("input.txt") as f:
    values = [int(v) for v in f.read().split("\n")]

fuel = sum((mass // 3) - 2 for mass in values)
print("Part 1:", fuel)

total = 0
for module in values:
    fuel = module
    while fuel >= 0:
        fuel = (fuel // 3) - 2
        if fuel > 0:
            total += fuel

print("Part 2:", total)