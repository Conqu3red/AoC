from typing import *
from copy import copy, deepcopy
from part1 import load_data

class PathVisitor2:
    def __init__(self, mapping: Dict[str, List[str]]) -> None:
        self.paths = []
        self.mapping = mapping

    def find_path(self, path: List[str], visited: Set[str] = None, used_twice_visit = False):
        if visited is None:
            visited = set()
        to_visit = self.mapping.get(path[-1], [])
        
        for v in to_visit:
            if v == "end":
                path.append(v)
                self.paths.append(path)
            elif v == "start" or v.islower() and v in visited and used_twice_visit:
                pass
            else:
                new_path = deepcopy(path)
                new_path.append(v)
                new_visited = deepcopy(visited)
                new_visited.add(v)
                new_used_twice_visit = (v.islower() and v in visited) or used_twice_visit

                self.find_path(new_path, new_visited, new_used_twice_visit)

def main():
    mapping = load_data()
    p = PathVisitor2(mapping)
    p.find_path(["start"], {"start"})

    #for path in p.paths:
    #    print(",".join(path))

    print(f"Part 2: {len(p.paths)}")

if __name__ == "__main__":
    main()