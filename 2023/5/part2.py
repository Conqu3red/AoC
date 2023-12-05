from typing import *
from dataclasses import dataclass

@dataclass
class Seed:
    src: int
    length: int

@dataclass
class Range:
    dest: int
    src: int
    length: int

def load():
    with open("input.txt") as f:
        sections = f.read().split("\n\n")
        parts = [int(n) for n in sections[0].split(":")[1].split()]
        seeds: List[Seed] = []
        for i in range(0, len(parts), 2):
            seeds.append(Seed(parts[i], parts[i + 1]))

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
        moved = []
        to_process = [*seeds]
        while to_process:
            seed = to_process.pop()
            intersected = False
            for r in ranges:
                if seed.src < r.src + r.length and seed.src + seed.length > r.src:
                    intersected = True
                    intersect = Seed(max(seed.src, r.src), 0)
                    intersect.length = min(seed.src + seed.length, r.src + r.length) - intersect.src
                    intersect.src += r.dest - r.src # move
                    moved.append(intersect)
                    if seed.src < r.src: # left part that didn't move
                        to_process.append(Seed(seed.src, r.src - seed.src))
                    
                    if seed.src + seed.length > r.src + r.length: # right part that didn't move
                        to_process.append(Seed(r.src + r.length, seed.src + seed.length - r.src - r.length))
            
            if not intersected:
                moved.append(seed)
            
        seeds = moved
    
    p1 = min(seed.src for seed in seeds)
    print(f"Part 2: {p1}")


main()