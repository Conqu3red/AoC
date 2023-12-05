from typing import *
from dataclasses import dataclass

@dataclass
class Range:
    dest: int
    src: int
    length: int

def load():
    with open("input.txt") as f:
        sections = f.read().split("\n\n")
        seeds = [int(n) for n in sections[0].split(":")[1].split()]

        maps: List[List[Range]] = []
        for section in sections[1:]:
            ranges: List[Range] = []
            for r in section.splitlines()[1:]:
                dest, src, length = r.split()
                ranges.append(Range(int(dest), int(src), int(length)))
            maps.append(ranges)
    
    return seeds, maps


def main():
    seeds, maps = load()

    for ranges in maps:
        new_seeds = [*seeds]
        for r in ranges:
            for i, seed in enumerate(seeds):
                if r.src <= seed < r.src + r.length:
                    new_seeds[i] = r.dest + (seed - r.src)
        seeds = new_seeds
    
    p1 = min(seeds)

    print(f"Part 1: {p1}")


main()