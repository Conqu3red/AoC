stacks = []

with open("input.txt") as f:
    s_lines, instructions = f.read().split("\n\n")

    for l in s_lines.split("\n"):
        if l[0] == "[":
            for n, box in enumerate(l[1::4]):
                if len(stacks) <= n:
                    stacks.append([])
                if box != " ":
                    stacks[n].insert(0, box)

    for ins in instructions.split("\n"):
        amount, start, dest = map(int, ins.split(" ")[1::2])
        for _ in range(amount):
            stacks[dest - 1].append(stacks[start - 1].pop())
        


print("Tops:", "".join(s[-1] for s in stacks))