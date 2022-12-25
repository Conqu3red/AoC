from typing import *
import math

def load():
    with open("input.txt") as f:
        data = f.read()
    
    return data.split("\n")


def SNAFU_to_int(num: str):
    digits = {
        "=": -2,
        "-": -1,
        "0": 0,
        "1": 1,
        "2": 2,
    }
    int_num = 0

    for i, char in enumerate(reversed(num)):
        int_num += (5 ** i) * digits[char]
    
    return int_num

def int_to_SNAFU(num: int):
    sanfu_num = ""
    digits = {
        -2: "=",
        -1: "-",
        0: "0",
        1: "1",
        2: "2",
    }
    top_pow = math.ceil(math.log(num, 5))
    leading = True
    for i in range(top_pow, -1, -1):
        # closest
        closest_j = 0
        closest_dist = math.inf
        for j in range(-2, 3):
            if abs(num - j * (5 ** i)) < closest_dist:
                closest_j = j
                closest_dist = abs(num - j * (5 ** i))
        
        if closest_j != 0:
            leading = False
        
        if not leading:
            sanfu_num += digits[closest_j]
        num -= closest_j * (5 ** i)
    
    return sanfu_num



numbers = load()

total = sum(SNAFU_to_int(num) for num in numbers)
print(total)
print("Solution:", int_to_SNAFU(total))