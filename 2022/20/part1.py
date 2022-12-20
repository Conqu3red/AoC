from typing import *

def load() -> List[int]:
    with open("input.txt") as f:
        lines = f.read().split("\n")
    
    return list(map(int, lines))


numbers = load()

def run(numbers: List[int]):
    copy = [(i, n) for i, n in enumerate(numbers)]
    #print(copy)

    for i, n in enumerate(numbers):
        copy_index = copy.index((i, n))
        #copy.pop(copy_index)
        copy.pop(copy_index)
        steps = n % (len(numbers) - 1)
        if n > 0:
            """ copy_index += 1
            if copy_index == len(numbers):
                copy_index = 0
            for _ in range(n):
                copy_index += 1
                if copy_index == len(numbers):
                    copy_index = 0 """
            copy.insert(((copy_index + n) % (len(numbers) - 1)), n)
        elif n == 0:
            copy.insert(copy_index, n)
        else:
            """ if copy_index == 0:
                copy_index == len(numbers)
            for _ in range(abs(n)):
                copy_index -= 1
                #print(copy_index)
                if copy_index == 0:
                    copy_index = len(numbers) """
            #copy.insert(copy_index, n)
            copy.insert(((copy_index + n) % (len(numbers) - 1)), n)

        #print(n, copy)
    
    return copy

copy = run(numbers)

zero = copy.index(0)
print(1000, copy[(zero + 1000) % len(copy)])
print(2000, copy[(zero + 2000) % len(copy)])
print(3000, copy[(zero + 3000) % len(copy)])
print(copy[(zero + 1000) % len(copy)] + copy[(zero + 2000) % len(copy)] + copy[(zero + 3000) % len(copy)])