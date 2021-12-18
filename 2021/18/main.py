import json
from typing import *
from dataclasses import dataclass
import math

@dataclass
class SnailNumber:
    depths: List[int]
    values: List[int]

    def __add__(self, other):
        if isinstance(other, SnailNumber):
            s_depths = [d + 1 for d in self.depths]
            o_depths = [d + 1 for d in other.depths]
            n = SnailNumber(s_depths + o_depths, self.values + other.values)
            reduce_snail_number(n)
            return n
    
    def magnitude(self):
        stack = [(d, v) for d, v in zip(self.depths, self.values)]
        
        while len(stack) > 1:
            for i in range(len(stack) - 1):
                if stack[i][0] == stack[i + 1][0]:
                    left = stack[i]
                    right = stack[i + 1]
                    new = 3 * left[1] + 2 * right[1]
                    del stack[i]
                    del stack[i]
                    stack.insert(i, (left[0] - 1, new))
                    break
            else:
                print(stack)
                return
            
        
        return stack[0][1]



def load_data() -> List[SnailNumber]:
    nums = []
    with open("input.txt") as f:
        lines = f.read().split("\n")
        for line in lines:
            n = flatten_snail_number(json.loads(line))
            reduce_snail_number(n)
            nums.append(n)
    
    return nums

def flatten_snail_number(number) -> SnailNumber:
    n = SnailNumber([], [])
    queue = [(number, 0)]
    while len(queue) > 0:
        cur, depth = queue.pop()
        if isinstance(cur, list):
            for element in reversed(cur):
                queue.append((element, depth + 1))
        else:
            n.depths.append(depth)
            n.values.append(cur)

    return n

def step_snail_number(number: SnailNumber, t: bool):
    prev = None

    for i in range(len(number.depths)):
        if t and number.depths[i] == prev and prev >= 5: # explode
            left = number.values[i - 1]
            right = number.values[i]

            if i - 2 >= 0:
                number.values[i - 2] += left
            
            if i + 1 < len(number.values):
                number.values[i + 1] += right
            
            # replace pair with zero

            number.values[i - 1] = 0
            number.depths[i - 1] -= 1
            del number.depths[i]
            del number.values[i]
            
            return True
        
        if not t and number.values[i] >= 10: # split
            number.depths.insert(i, number.depths[i] + 1)
            number.values.insert(i, number.values[i] // 2)
            number.depths[i + 1] += 1
            number.values[i + 1] = math.ceil(number.values[i + 1] / 2)

            return True
            
        prev = number.depths[i]
    
    return False

def reduce_snail_number(number: SnailNumber):
    do = True
    while do:
        for t in (True, False):
            do = step_snail_number(number, t)
            if do:
                break

def main():
    data = load_data()
    result = data[0]
    
    for i in range(1, len(data)):
        result += data[i]
        #print(result.values)
    
    print(f"Part 1: {result.magnitude()}")

    largest = 0
    for i in range(len(data)):
        first = data[i]
        for j in range(len(data)):
            if j != i:
                second = data[j]
                magnitude = (first + second).magnitude()
                if magnitude > largest:
                    largest = magnitude
    
    print(f"Part 2: {largest}")


if __name__ == "__main__":
    main()