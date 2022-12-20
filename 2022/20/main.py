from typing import *

def load() -> List[int]:
    with open("input.txt") as f:
        lines = f.read().split("\n")
    
    return list(map(int, lines))


numbers = load()

def mix(numbers: List[int], input: Optional[List[int]] = None):
    copy = input if input is not None else [(i, n) for i, n in enumerate(numbers)]
    #print(copy)

    for i, n in enumerate(numbers):
        copy_index = copy.index((i, n))
        steps = n % (len(numbers) - 1)
        
        copy.remove((i, n))
        copy.insert((copy_index + steps) % (len(numbers) - 1), (i, n))
    
    return copy

copy = mix(numbers)

zero = copy.index((numbers.index(0), 0))
print("Part 1:", copy[(zero + 1000) % len(copy)][1] + copy[(zero + 2000) % len(copy)][1] + copy[(zero + 3000) % len(copy)][1])



original = [n * 811589153 for n in numbers]
copy = [(i, n) for i, n in enumerate(original)]
for _ in range(10):
    copy = mix(original, copy)

zero = copy.index((original.index(0), 0))
print("Part 2:", copy[(zero + 1000) % len(copy)][1] + copy[(zero + 2000) % len(copy)][1] + copy[(zero + 3000) % len(copy)][1])
