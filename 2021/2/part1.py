with open("input.txt") as f:
    instructions = [l.split(" ") for l in f.read().split("\n")]

x = 0
depth = 0

for instruction_name, value in instructions:
    value = int(value)
    if instruction_name == "forward":
        x += value
    elif instruction_name == "down":
        depth += value
    elif instruction_name == "up":
        depth -= value

print(f"{x = }, {depth = }")
print(x * depth)