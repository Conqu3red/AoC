
def priority(letter: str):
    if "a" <= letter <= "z":
        return ord(letter) - 96
    
    return ord(letter) - 65 + 27

total = 0

with open("input.txt") as f:
    lines = f.read().split("\n")
    for line in lines:
        half = len(line) // 2
        first = set(line[:half])
        second = set(line[half:])
        intersection = first & second
        item = intersection.pop()
        total += priority(item)

print("Total Priority:", total)