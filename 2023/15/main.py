def gen_hash(s: str):
    v = 0
    for c in s:
        v = ((v + ord(c)) * 17) % 256
    return v

def process(parts: list[str]):
    boxes: list[list[tuple[str]]] = [[] for _ in range(256)]

    for p in parts:
        if p.endswith("-"):
            label = p[:-1]
            box = gen_hash(label)
            boxes[box] = [lens for lens in boxes[box] if lens[0] != label]
        else:
            # =
            label, strength = p.split("=")
            box = gen_hash(label)
            strength = int(strength)
            found = False
            for i, lens in enumerate(boxes[box]):
                if lens[0] == label:
                    boxes[box][i] = (label, strength)
                    found = True
                    break
            if not found:
                boxes[box].append((label, strength))
    
    total = 0
    for i, box in enumerate(boxes, start=1):
        for j, (label, strength) in enumerate(box, start=1):
            total += i * j * strength
    
    return total


def main():
    with open("input.txt") as f:
        parts = f.read().split(",")
    
    p1 = sum(gen_hash(p) for p in parts)
    p2 = process(parts)
    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")


main()