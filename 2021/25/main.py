from typing import *

def load_data() -> List[List[Optional[str]]]:
    with open("input.txt") as f:
        lines = f.read().split("\n")
    
    return [
        [None if c == "." else c for c in line] for line in lines
    ]

def apply_step(data: List[List[Optional[str]]]) -> List[List[Optional[str]]]:
    new_data = [[None for _ in range(len(row))] for row in data]
    # left ones first, then down ones
    mx = len(data[0])
    my = len(data)

    for y, row in enumerate(data):
        for x, v in enumerate(row):
            nx = x
            if v == ">" and row[(x + 1) % mx] is None:
                nx = (x + 1) % mx

            if v is not None:
                new_data[y][nx] = v
    
    data = new_data
    new_data = [[None for _ in range(len(row))] for row in data]
    
    for y, row in enumerate(data):
        for x, v in enumerate(row):
            ny = y
            if v == "v" and data[(y + 1) % my][x] is None:
                ny = (y + 1) % my
            
            if v is not None:
                new_data[ny][x] = v
    
    return new_data

def print_state(s: List[List[Optional[str]]]):
    for line in s:
        for char in line:
            print("." if char is None else char, end="")  
        print()

def main():
    data = load_data()
    cur = data
    #print_state(cur)
    #print()
    n = 0
    while True:
        n += 1
        new = apply_step(cur)
        #print_state(new)
        #print(n)
        if new == cur:
            break
        cur = new
    
    print(f"Part 1: {n}")

if __name__ == "__main__":
    main()