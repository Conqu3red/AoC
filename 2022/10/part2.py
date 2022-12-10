x = 1

sample_sum = 0

with open("input.txt") as f:
    instructions = f.read().split("\n")

pc = 0
cycle = 1
steps = 0
current = None

crt_x = 0

while pc < len(instructions):
    if not current:
        current = instructions[pc].split(" ")
    
    # crt code
    if x - 1 <= crt_x <= x + 1:
        print("#", end="")
    else:
        print(".", end="")

    crt_x += 1
    if crt_x >= 40:
        crt_x = 0
        print()
    
    steps += 1
    cycle += 1

    if current[0] == "noop" and steps == 1:
        steps = 0
        current = None
        pc += 1
    elif current[0] == "addx" and steps == 2:
        x += int(current[1])
        steps = 0
        current = None
        pc += 1