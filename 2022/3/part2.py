
def priority(letter: str):
    if "a" <= letter <= "z":
        return ord(letter) - 96
    
    return ord(letter) - 65 + 27

total = 0

with open("input.txt") as f:
    lines = f.read().split("\n")
    for i in range(0, len(lines), 3):
        cur_lines = lines[i : i + 3]
        intersection = set(cur_lines[0]) & set(cur_lines[1]) & set(cur_lines[2])
        item = intersection.pop()
        total += priority(item)

print("Total Priority:", total)