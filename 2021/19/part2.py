from part1 import Vec3, as_vec3
import json

def main():
    furthest = 0
    with open("beacon_positions.json") as f:
        data = json.load(f, object_hook=as_vec3)
    
    for p in data:
        for p2 in data:
            dist = abs(p2.x - p.x) + abs(p2.y - p.y) + abs(p2.z - p.z)
            furthest = max(dist, furthest)
    
    print(f"Part 2: {furthest}")

if __name__ == "__main__":
    main()