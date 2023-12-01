with open("input.txt") as f:
    parts = [int(op) for op in f.read().split(",")]

def execute(parts):
    for i in range(0, len(parts), 4):
        opcode = parts[i]
        if opcode == 1:
            parts[parts[i + 3]] = parts[parts[i + 1]] + parts[parts[i + 2]]
        elif opcode == 2:
            parts[parts[i + 3]] = parts[parts[i + 1]] * parts[parts[i + 2]]
        elif opcode == 99:
            break
    
    return parts
        

def part_one(parts):
    parts[1] = 12
    parts[2] = 2

    parts = execute([*parts])
    return parts[0]

def part_two(parts):
    for x in range(100):
        for y in range(100):
            parts[1] = x
            parts[2] = y

            p = execute([*parts])
            if p[0] == 19690720:
                return 100 * x + y

print("Part 1:", part_one(parts))

print("Part 2:", part_two(parts))