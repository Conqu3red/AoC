with open("input.txt") as f:
    lines = f.read().split("\n")

traverse = {}
reverse = {}
for line in lines:
    prev, next = line.split(")")
    reverse[next] = prev
    if prev in traverse:
        traverse[prev].append(next)
    else:
        traverse[prev] = [next]

direct = len(traverse)

# compute indirect
orbits = {"COM": 0}
to_visit = ["COM"]
while to_visit:
    v = to_visit.pop()
    if v in traverse:
        for next in traverse[v]:
            orbits[next] = orbits[v] + 1
            to_visit.append(next)

print("Part 1:", sum(orbits.values()))


# Part 2
def path_back(position):
    positions = []
    while position != "COM":
        position = reverse[position]
        positions.append(position)
    
    return positions

san = path_back("SAN")
you = path_back("YOU")

for index, (s, y) in enumerate(zip(reversed(san), reversed(you))):
    if s != y:
        cross = index - 1
        break

dist = len(san) - cross + len(you) - cross - 2

print("Part 2:", dist)