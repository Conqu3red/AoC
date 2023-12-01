lower = 136818
upper = 685979

def next_digit(index: int, prev: int, has_double: bool):
    if index == 6 and not has_double: 
        yield prev, True
        return

    for i in range(prev, 10):
        yield i, has_double or i == prev

numbers = [(0, 0, False)]
valid = 0

while numbers:
    length, n, has_double = numbers.pop()
    for d, new_double in next_digit(length + 1, n % 10, has_double):
        new_n = n * 10 + d
        #print(length + 1, new_n)
        if length + 1 >= 6:
            if lower < new_n < upper and new_double:
                valid += 1
                #print(new_n)
        else:
            numbers.append((length + 1, new_n, new_double))



print("Part 1:", valid)