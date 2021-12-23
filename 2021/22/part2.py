from typing import *
from dataclasses import dataclass
import math
from math import inf

@dataclass
class Cuboid:
    xrange: Tuple[int, int]
    yrange: Tuple[int, int]
    zrange: Tuple[int, int]

    def intersection(self, other: 'Cuboid') -> Optional['Cuboid']:
        xrange = (max(self.xrange[0], other.xrange[0]), min(self.xrange[1], other.xrange[1]))
        yrange = (max(self.yrange[0], other.yrange[0]), min(self.yrange[1], other.yrange[1]))
        zrange = (max(self.zrange[0], other.zrange[0]), min(self.zrange[1], other.zrange[1]))

        if xrange[0] >= xrange[1] or yrange[0] >= yrange[1] or zrange[0] >= zrange[1]:
            return None

        return Cuboid(xrange, yrange, zrange)
    
    def volume(self):
        return abs(self.xrange[1] - self.xrange[0]) * abs(self.yrange[1] - self.yrange[0]) * abs(self.zrange[1] - self.zrange[0])
    
    def get_extending_cuboids(self) -> List['Cuboid']:
        return [
            Cuboid((-inf, self.xrange[0]), (-inf, +inf),           (-inf, +inf)),            # left
            Cuboid((self.xrange[1], +inf), (-inf, +inf),           (-inf, +inf)),            # right
            Cuboid(self.xrange,            (-inf, +inf),           (-inf, self.zrange[0])),  # front
            Cuboid(self.xrange,            (-inf, +inf),           (self.zrange[1], +inf)),  # back
            Cuboid(self.xrange,            (-inf, self.yrange[0]), self.zrange),             # bottom
            Cuboid(self.xrange,            (self.yrange[1], +inf), self.zrange),             # top
        ]

    def cutout(self, other: 'Cuboid') -> List['Cuboid']:
        intersection = self.intersection(other)
        if intersection is None:
            return [Cuboid(self.xrange, self.yrange, self.zrange)]
        
        # create cuboids extending out to inf, around self
        #        xrange     yrange     zrange
        # left   -inf -x    -inf +inf  -inf +inf
        # right  +x   +inf  -inf +inf  -inf +inf
        
        # front  -x   +x    -inf +inf  -inf -z
        # back   -x   +x    -inf +inf  +z   +inf
        
        # bottom -x   +x    -inf -y    -z   +z
        # top    -x   +x    +y   +inf  -z   +z

        parts = []
        
        for box in other.get_extending_cuboids():
            i = self.intersection(box)
            #print(box, intersection)
            if i is not None:
                parts.append(i)

        return parts


class Instruction(NamedTuple):
    enable: bool
    box: Cuboid


def load_data() -> List[Instruction]:
    with open("input.txt") as f:
        lines = f.read().split("\n")
    
    instructions = []
    for line in lines:
        state, ranges = line.split(" ")
        int_ranges = []
        for range in ranges.split(","):
            low, high = range.split("..")
            int_ranges.append((int(low[2:]) - .5, int(high) + .5))
            # shift by .5 because we are technically including the edge values inside us!
    
        instructions.append(Instruction(state == "on", Cuboid(*int_ranges)))
    
    return instructions
    

def remove_overlapping(box: Cuboid, boxes: List[Cuboid]) -> List[Cuboid]:
    done_parts = []
    parts_queue: List[Tuple[int, Cuboid]] = [(0, box)]
    while len(parts_queue) > 0:
        #print(len(parts_queue))
        i, part = parts_queue.pop()
        if i >= len(boxes):
            done_parts.append(part)
        else:
            new_parts = part.cutout(boxes[i])
            for p in new_parts:
                parts_queue.append((i + 1, p))
    
    return done_parts


def compute_enabled(instructions: List[Instruction]) -> List[Cuboid]:
    enabled_area: List[Cuboid] = []
    for i in instructions:
        if i.enable:
            enabled_area += remove_overlapping(i.box, enabled_area)
        
        else:
            new_enabled_area = []
            for b in enabled_area:
                new_enabled_area += b.cutout(i.box)
            
            enabled_area = new_enabled_area
    
    return enabled_area


def main():
    instructions = load_data()

    boxes = compute_enabled(instructions)
    total = int(sum(box.volume() for box in boxes))
    print(f"Part 2: {total}")

if __name__ == "__main__":
    main()