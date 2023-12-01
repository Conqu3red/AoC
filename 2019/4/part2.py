lower = 136818
upper = 685979


def validate_part1(n: int):
    prev = -1
    length = 0
    streak = False
    for d in str(n):
        if d == prev:
            length += 1
        elif int(d) < int(prev):
            return False
        else:
            if length >= 2:
                streak = True
            prev = d
            length = 1
    
    return streak or length >= 2


def validate_part2(n: int):
    prev = -1
    length = 0
    streak = False
    for d in str(n):
        if d == prev:
            length += 1
        elif int(d) < int(prev):
            return False
        else:
            if length == 2:
                streak = True
            prev = d
            length = 1
    
    return streak or length == 2

valid1 = 0
valid2 = 0

for i in range(lower, upper):
    valid1 += validate_part1(i)
    valid2 += validate_part2(i)

print("Part 1:", valid1)
print("Part 2:", valid2)