from typing import *
from dataclasses import dataclass
from copy import deepcopy


@dataclass(eq=True)
class Vec3:
    x: float
    y: float
    z: float

    def __add__(self, o) -> 'Vec3':
        if isinstance(o, Vec3):
            return Vec3(self.x + o.x, self.y + o.y, self.z + o.z)
        return NotImplemented
    
    def __sub__(self, o) -> 'Vec3':
        if isinstance(o, Vec3):
            return Vec3(self.x - o.x, self.y - o.y, self.z - o.z)
        return NotImplemented
    
    def __hash__(self) -> int:
        return hash((self.x, self.y, self.z))

def load_data():
    with open("input.txt") as f:
        sections = f.read().split("\n\n")

    data = []

    for section in sections:
        coord_strings = section.split("\n")[1:]
        coords = set()
        for coord in coord_strings:
            x, y, z = coord.split(",")
            coords.add(Vec3(int(x), int(y), int(z)))

        data.append(coords)
    
    return data

def rotate(vec: Vec3, x: int, y: int, z: int) -> Vec3:
    new = Vec3(vec.x, vec.y, vec.z)

    for _ in range(x):
        new.y, new.z = new.z, -new.y
    for _ in range(y):
        new.x, new.z = new.z, -new.x
    for _ in range(z):
        new.x, new.y = new.y, -new.x
    
    return new
    

def change_points(points: Set[Vec3], x, y, z) -> Set[Vec3]:
    return {rotate(point, x, y, z) for point in points}


def convert_to_other(data1: Set[Vec3], data2: Set[Vec3]) -> Optional[Tuple[Vec3, Set[Vec3]]]:
    """Tries to Align `data2` to `data1`"""
    # testing to find if twelve points match between data1 and rotated data2 (can be offset)
    # checking all possible rotation permutations:    
    
    for x in range(4):
        for y in range(4):
            for z in range(4):
                applied_data2 = change_points(data2, x, y, z)

                offsets = [p1 - p2 for p2 in applied_data2 for p1 in data1]
                
                # count
                counts = {}
                for o in offsets:
                    counts[o] = counts.get(o, 0) + 1
                
                for offset, count in counts.items():
                    if count >= 12:
                        break
                else:
                    continue
                data2_offset = {p + offset for p in applied_data2}
                return offset, data2_offset
                
    return None





def main():
    data = load_data()
    solved = {0}
    solved_points = deepcopy(data[0])

    beacon_positions = [Vec3(0, 0, 0)]

    while len(data) > len(solved):
        for j in range(len(data)):
            if j not in solved:
                c = convert_to_other(solved_points, data[j])
                if c is not None:
                    offset, points = c
                    beacon_positions.append(offset)
                    solved_points |= points
                    solved.add(j)
                    print(f"Solved {j}")
    
    
    print(f"Part 1: {len(solved_points)}")

    furthest = 0
    for p in beacon_positions:
        for p2 in beacon_positions:
            dist = abs(p2.x - p.x) + abs(p2.y - p.y) + abs(p2.z - p.z)
            furthest = max(dist, furthest)
    
    print(f"Part 2: {furthest}")

if __name__ == "__main__":
    main()