totals = []
current = 0

with open("input.txt") as f:
    lines = f.read().split("\n")
    for line in lines:
        if line == "":
            totals.append(current)
            current = 0
        else:
            current += int(line)


totals = list(sorted(totals, reverse=True))

print("Top 3 sum:", sum(totals[:3]))