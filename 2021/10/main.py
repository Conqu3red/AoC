lookup1 = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137
}

lookup2 = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4
}

pairing = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">"
}

def process_line(line):
    stack = []
    for char in line:
        if char in "([{<":
            stack.append(char)
        else:
            # closing char
            if pairing[stack[-1]] != char:
                return lookup1[char], 0
            stack.pop()
    
    s = 0
    for char in reversed(stack):
        s = 5 * s + lookup2[pairing[char]]
    
    return 0, s


def main():
    with open("input.txt") as f:
        data = f.read().split("\n")
    
    p2_scores = []
    p1_total = 0
    for l in data:
        part1, part2 = process_line(l)
        p1_total += part1
        if part2 != 0:
            p2_scores.append(part2)

    p2_scores.sort()
    print(f"Part 1: {p1_total}")
    print(f"Part 2: {p2_scores[len(p2_scores) // 2]}")



if __name__ == "__main__":
    main()