from typing import *
from dataclasses import dataclass
import math
from copy import deepcopy
import json

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
    
    def __getitem__(self, index):
        return (self.x, self.y, self.z)[index]
    
    def __list__(self):
        return [self.x, self.y, self.z]
    
    def __hash__(self) -> int:
        return hash((self.x, self.y, self.z))
    
    zero = None

Vec3.zero = Vec3(0, 0, 0)

def encode_Vec3(obj):
    if isinstance(obj, Vec3):
        return {"Vec3": True, "x": obj.x, "y": obj.y, "z": obj.z}
    
    raise TypeError(
        f'Object of type {obj.__class__.__name__} '
        f'is not JSON serializable'
    )

def as_vec3(obj):
    if "Vec3" in obj:
        return Vec3(obj["x"], obj["y"], obj["z"])
    return obj

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

                for p2 in applied_data2:
                    for p1 in data1:
                        # p2 + ? = p1 => p1 - p2 = ?
                        offset = p1 - p2

                        data2_offset = {p + offset for p in applied_data2}

                        intersect = data1 & data2_offset
                        if len(intersect) >= 12:
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

    print(beacon_positions)
    with open("beacon_positions.json", "w") as f:
        json.dump(beacon_positions, f, default=encode_Vec3)

if __name__ == "__main__":
    main()