from typing import *

class Instruction(NamedTuple):
    enable: bool
    xrange: Tuple[int, int]
    yrange: Tuple[int, int]
    zrange: Tuple[int, int]

def load_data() -> List[Instruction]:
    with open("input.txt") as f:
        lines = f.read().split("\n")
    
    instructions = []
    for line in lines:
        state, ranges = line.split(" ")
        int_ranges = []
        for range in ranges.split(","):
            low, high = range.split("..")
            int_ranges.append((int(low[2:]), int(high)))
    
        instructions.append(Instruction(state == "on", *int_ranges))
    
    return instructions

def compute_enabled(instructions: List[Instruction]):
    enabled = set()
    for i in instructions:
        for x in range(max(i.xrange[0], -50), min(i.xrange[1], 50) + 1):
            for y in range(max(i.yrange[0], -50), min(i.yrange[1], 50) + 1):
                for z in range(max(i.zrange[0], -50), min(i.zrange[1], 50) + 1):
                    if i.enable:
                        enabled.add((x, y, z))
                    else:
                        if (x, y, z) in enabled:
                            enabled.remove((x, y, z))
    
    return enabled


def main():
    instructions = load_data()
    print(len(compute_enabled(instructions)))

if __name__ == "__main__":
    main()