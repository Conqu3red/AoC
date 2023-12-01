import math
nums = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9
}

to_search = list(nums.keys()) + [str(n) for n in nums.values()] + ["0"]

def load():
    with open("input.txt") as f:
        data = f.read().split("\n")
    return data

def main():
    data = load()
    total = 0
    for line in data:
        l = min(
            ((line.find(s), s) for s in to_search),
            key=lambda x: x[0] if x[0] != -1 else math.inf
        )[1]
        
        r = max(((line.rfind(s), s) for s in to_search), key=lambda x: x[0])[1]
        
        l = int(l) if l.isnumeric() else nums[l]
        r = int(r) if r.isnumeric() else nums[r]

        total += l * 10 + r
    
    print(f"Part 2: {total}")


main()