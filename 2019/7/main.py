import itertools

with open("input.txt") as f:
    parts = [int(op) for op in f.read().split(",")]

def execute(parts, setting, power):
    i = 0
    output = 0

    inputs = [setting, power]

    def par(opcode, i, param):
        
        mode = opcode % (10 ** (param + 2)) // (10 ** (param + 1))
        if mode == 0:
            return parts[i + param]
        elif mode == 1:
            return i + param

    while i < len(parts):
        op = parts[i]
        code = parts[i] % 100
        if code == 1:
            parts[par(op, i, 3)] = parts[par(op, i, 1)] + parts[par(op, i, 2)]
            i += 4
        elif code == 2:
            parts[par(op, i, 3)] = parts[par(op, i, 1)] * parts[par(op, i, 2)]
            i += 4
        elif code == 3:
            parts[par(op, i, 1)] = inputs.pop(0)
            i += 2
        elif code == 4:
            output = parts[par(op, i, 1)]
            i += 2
        elif code == 5: # jump if true
            if parts[par(op, i, 1)] != 0:
                i = parts[par(op, i, 2)]
            else:
                i += 3
        elif code == 6: # jump if false
            if parts[par(op, i, 1)] == 0:
                i = parts[par(op, i, 2)]
            else:
                i += 3
        elif code == 7:
            parts[par(op, i, 3)] = int(parts[par(op, i, 1)] < parts[par(op, i, 2)])
            i += 4
        elif code == 8:
            parts[par(op, i, 3)] = int(parts[par(op, i, 1)] == parts[par(op, i, 2)])
            i += 4
        elif code == 99:
            break
    
    return output

best = 0

for perm in itertools.permutations(range(0, 5)):
    power = 0
    for n in perm:
        power = execute([*parts], n, power)
    
    if power > best:
        best = power

print("Part 1:", best)