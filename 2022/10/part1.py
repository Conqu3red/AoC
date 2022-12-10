x = 1

sample_sum = 0

with open("input.txt") as f:
    instructions = f.read().split("\n")

pc = 0
cycle = 1
steps = 0
current = None
while pc < len(instructions):
    if not current:
        current = instructions[pc].split(" ")
    
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
    
    if (cycle - 20) % 40 == 0:
        print(cycle, current)
        sample_sum += cycle * x


print(sample_sum)